# Copyright 2010 Michael Murr
#
# This file is part of LibForensics.
#
# LibForensics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibForensics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with LibForensics.  If not, see <http://www.gnu.org/licenses/>.

"""Support for a Data Access Layer (DAL)"""

# stdlib imports
from string import Template
from ctypes import sizeof
from operator import itemgetter
from itertools import count
from keyword import iskeyword

# local imports
from lf.dec import ByteIStream
from lf.dec.consts import SEEK_SET

__docformat__ = "restructuredtext en"
__all__ = [
    "structuple", "Structuple", "ActiveStructuple", "CtypesWrapper",
    "Converter", "StdLibConverter"
]

_valid_name_characters = \
    "abcdefhigjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

class MetaStructuple(type):
    """Meta class for Structuples."""

    def __new__(cls, name, bases, clsdict):
        # Create a temporary class, so we can have Python automatically find
        # inheritable properties.
        tmp_cls = super(MetaStructuple, cls).__new__(cls, name, bases, clsdict)

        # The _fields_, _aliases_, and _auto_slots_ properties are inheritable.
        fields = getattr(tmp_cls, "_fields_", [])
        aliases = getattr(tmp_cls, "_aliases_", {})
        auto_slots = getattr(tmp_cls, "_auto_slots_", None)


        # Find the parent _fields_ attribute (for inheritance purposes)
        for parent_class in tmp_cls.__mro__[1:]:
            if hasattr(parent_class, "_fields_"):
                parent_fields = parent_class._fields_
                break
            # end if
        else:
            parent_fields = list()
        # end for

        # Merge the two lists, with fields and aliases taking precedence over
        # parent_fields
        ignore_fields = set(fields)
        ignore_fields.update(aliases.keys())
        parent_fields = [x for x in parent_fields if x not in ignore_fields]
        new_fields = list(parent_fields)
        new_fields.extend(fields)
        fields = tuple(new_fields)

        # Create the properties
        for (index, field) in enumerate(fields):
            clsdict[field] = property(itemgetter(index))
        # end for

        # Create any aliases
        if aliases:
            for (source, target) in aliases.items():
                if target in clsdict:
                    clsdict[source] = clsdict[target]
                # end if
            # end for
        # end if

        # Update the class dictionary with the (possibly) new _fields_
        clsdict["_fields_"] = fields

        # Add __slots__ only if auto_slots is True, and clsdict doesn't already
        # have a __slots__ property.
        if auto_slots and ("__slots__" not in clsdict):
            clsdict["__slots__"] = tuple()
        # end if

        # Return the new class
        return super(MetaStructuple, cls).__new__(cls, name, bases, clsdict)
    # end def __new__
# end class MetaStructuple

def structuple(name, fields, aliases=None, auto_slots=False, rename=False):
    """Factory function to create new :class:`Structuple` classes.

    :type name: str
    :param name: The name for the new :class:`Structuple` class.

    :type fields: iterable
    :param fields: A string, dictionary, or iterable of the names of the
                   attributes and their positions.  If this is a string or
                   iterable, the positions are determined by the order in which
                   the names occur, starting with position 0 (first element).
                   If this is a dictionary, the keys are the names of the
                   attributes, and the positions are the values.

    :type aliases: :class:`dict`
    :param aliases: A dictionary of aliases for attributes.  The keys are the
                    names of the aliases, and the values are the names of the
                    attributes the aliases should point to.

    :type auto_slots: ``bool``
    :param auto_slots: If true, the :attr:`__slots__` attribute is
                       automatically defined for the created class and all
                       subclasses, until a subclass sets the
                       :attr:`_auto_slots_` attribute to ``False``.

    :type rename: ``bool``
    :param rename: If ``True``, duplicate attribute names are automatically
                   renamed to field_name__XXX, where XXX is the position of the
                   name.

    :rtype: :class:`Structuple`
    :returns: The newly created class.

    """
    if isinstance(fields, dict):
        field_names = tuple(fields.keys())
    else:
        if isinstance(fields, str):
            fields = fields.replace(",", " ")
            field_names = fields.split()
        else:
            try:
                field_iter = iter(fields)
            except TypeError:
                raise TypeError("fields must be a str, dict, or iter")
            # end try

            field_names = list(field_iter)
        # end if

        already_seen = list()
        for (index, field_name) in enumerate(field_names):
            if field_name in already_seen:
                if rename:
                    field_name = "{0}__{1}".format(field_name, index)
                    already_seen.append(field_name)
                else:
                    raise ValueError(
                        "Duplicate field name {0}".format(field_name)
                    )
                # end if
            else:
                already_seen.append(field_name)
            # end if
        # end for

        field_names = tuple(already_seen)
        fields = dict(zip(field_names, count()))
    # end if

    field_positions = tuple([fields[field_name] for field_name in field_names])

    for field_name in field_names:
        if field_name[0].lower() not in "abcdefghijklmnopqrstuvwxyz":
            raise ValueError("Field names can only start with a letter: {0}".
                format(field_name)
            )
        elif iskeyword(field_name):
            err_msg = "Field names can not be keywords: {0}".format(field_name)
            raise ValueError("Field names can not be keywords: {0}".format(
                field_name
            ))
        # end if

        for char in field_name[1:]:
            if char not in _valid_name_characters:
                raise ValueError("Field names can only contain underscores and"
                    "alphanumeric characters: {0}".format(field_name)
                )
            # end if
        # end for
    # end for

    clsdict = { "_fields_": field_names, "__slots__": tuple() }

    if aliases:
        clsdict["_aliases_"] = aliases
    # end if

    if auto_slots:
        clsdict["_auto_slots_"] = auto_slots
    # end if

    return MetaStructuple(name, (tuple,), clsdict)
# end def structuple

class Structuple(tuple, metaclass=MetaStructuple):
    """Base class for creating tuples with named attribute access.

    .. attribute:: _fields_

        A list of names of the attributes, in the same order as the
        corresponding elements of the tuple.

    .. attribute:: _aliases_

        A dictionary to describe attributes that are aliases for other
        attributes.  The keys are the alias names, and the values are the names
        of the attributes they should point to.

    .. attribute:: _auto_slots_

        If ``True``, then the :attr:`__slots__` attribute is created
        automatically for all subclasses, until a subclass sets _auto_slots_ to
        ``False``.

    .. note::

        When inheriting from this class (or a subclass) the _fields_ attribute
        in subclasses *appends* to the _fields_ attribute of the parent(s).
        This means that subclasses will have all of the fields of the
        parent(s).

        The caveat is that if a subclass defines a field or alias that is
        already defined in the parent class, then the field is kept in the
        position specified by the subclass.

        For example:

            >>> from lf.dtypes import Structuple
            >>> class ParentClass(Structuple):
            ...     _fields_ = ("field0", "field1", "field2")
            ...
            >>> class SubClass1(ParentClass):
            ...     _fields_ = ("field3", "field4", "field5")
            ...
            >>> class SubClass2(ParentClass):
            ...     _fields_ = ("field6", "field1", "field7")
            ...
            >>> ParentClass._fields_
            ('field0', 'field1', 'field2')
            >>> SubClass1._fields_
            ('field0', 'field1', 'field2', 'field3', 'field4', 'field5')
            >>> SubClass2._fields_
            ('field0', 'field2', 'field6', 'field1', 'field7')

    """
    # Lists the fields that get created as attributes (in order)
    _fields_ = tuple()

    # Lists the attributes that are aliases for fields
    _aliases_ = dict()

    # If this is true, _fields_ overrides inherited _fields_.  If not, _fields_
    # extends inherited _fields_.
    _override_fields_ = False

    # If true, __slots__ is created automatically for all subclasses (until one
    # of them sets _autoslots_ to False.
    _auto_slots_ = False

    __slots__ = tuple()
# end class Structuple

class ActiveStructuple(Structuple):
    """Base class for value objects.

    .. attribute:: _takes_stream

        True if the :meth:`from_stream` method is implemented.

    .. attribute:: _takes_ctype

        True if the :meth:`from_ctype` method is implemented.

    """

    _auto_slots_ = True
    _takes_stream = False
    _takes_ctype = False

    @classmethod
    def from_bytes(cls, bytes_):
        """Creates an ActiveStructuple from a :class:`bytes` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type bytes_: :class:`bytes`
        :param bytes_: A :class:`bytes` object to read from.

        :rtype: :class:`ActiveStructuple`
        :returns: The corresponding :class:`ActiveStructuple`

        """
        return cls.from_stream(byte.open(bytes_))
    # end def from_bytes

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates an ActiveStructuple from an :class:`lf.dec.IStream` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the :class:`ActiveStructuple`

        :type offset: int or ``None``
        :param offset: The start of the :class:`ActiveStructuple`

        :rtype: :class:`ActiveStructuple`
        :returns: The corresponding :class:`ActiveStructuple`

        """
        raise NotImplementedError
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates an ActiveStructuple from a :mod:`ctypes` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type ctype: :class:`ctypes._CData`
        :param ctype: A :mod:`ctypes` object that describes the values of the
                      attributes.

        :rtype: :class:`ActiveStructuple`
        :reeturns: The corresponding :class:`ActiveStructuple`.

        """
        raise NotImplementedError
    # end def from_ctype
# end class ActiveStructuple

class CtypesWrapper(ActiveStructuple):
    """An ActiveStructuple that is a wrapper around a ctypes instance.

    .. attribute:: _ctype_

        The ctypes instances to wrap.
    """

    _ctype_ = None
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_bytes(cls, bytes_):
        """Creates a :class:`CtypesWrapper` object from a ``bytes`` object.

        :type bytes_: ``bytes``
        :param bytes_: A ``bytes`` object to read from.

        :rtype: :class:`CtypesWrapper`
        :returns: The corresponding :class:`CtypesWrapper` class.

        """
        inst = cls._ctype_.from_buffer_copy(bytes_)

        return cls.from_ctype(inst)
    # end def from_bytes

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a CtypesWrapper from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the :class:`CtypesWrapper`

        :type offset: ``int`` or ``None``
        :param offset: The start of the :class:`CtypesWrapper`

        :rtype: :class:`CtypesWrapper`
        :returns: The corresponding :class:`CtypesWrapper` object.

        """
        ctype = cls._ctype_

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        inst = ctype.from_buffer_copy(stream.read(sizeof(ctype)))

        return cls.from_ctype(inst)
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a CtypesWrapper from a ctype.

        :type ctype: :class:`ctypes._CData`
        :param ctype: A :mod:`ctypes` object that describes the values of the
                      attributes.

        :rtype: :class:`CtypesWrapper`
        :returns: The corresponding :class:`CtypesWrapper`.
        """

        return cls([getattr(ctype, field) for field in cls._fields_])
    # end from_ctype
# end class CtypesWrapper

class Converter():
    """Base class to convert data into a native Python object.

    .. attribute:: _takes_stream

        True if the :meth:`from_stream` method is implemented.

    .. attribute:: _takes_ctype

        True if the :meth:`from_ctype` method is implemented.

    """

    _takes_stream = False
    _takes_ctype = False

    @classmethod
    def from_bytes(cls, bytes_):
        """Creates a Python object from a :class:`bytes` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type bytes_: :class:`bytes`
        :param bytes_: A :class:`bytes` object to read from.

        :rtype: object
        :returns: The corresponding Python object.

        """
        return cls.from_stream(byte.open(bytes_))
    # end def from_bytes

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a Python object from an :class:`lf.dec.IStream` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the Python object.

        :type offset: int or ``None``
        :param offset: The start of the Python object.

        :rtype: object
        :returns: The corresponding Python object.

        """
        raise NotImplementedError
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a Python object from a :mod:`ctypes` object.

        .. note::

            This method is available if :attr:`_takes_ctype` is ``True``.

        :type ctype: :class:`ctypes._CData`
        :param ctype: A :mod:`ctypes` object that describes the values of the
                      attributes.

        :rtype: object
        :returns: The corresponding Python object.

        """

        raise NotImplementedError
    # end def from_ctype
# end class Converter

class StdLibConverter(Converter):
    """Base class for :class:`Converters` to Python standard library objects"""

    pass
# end class StdLibConverter

