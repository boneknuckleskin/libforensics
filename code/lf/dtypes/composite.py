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

"""Data types composed of primitive data types."""

# stdlib imports
from operator import itemgetter
from collections import OrderedDict
from ctypes import (
    LittleEndianStructure, BigEndianStructure, c_uint8
)

# local imports
from lf.dtypes.base import Primitive
from lf.dtypes.consts import BIG_ENDIAN, LITTLE_ENDIAN
from lf.dtypes.bits import BitType

__docformat__ = "restructuredtext en"
__all__ = [
    "Composite", "Record", "LERecord", "BERecord"
]

class MetaRecord(type):
    """Metaclass to build _fields_ attribute of Record data types"""

    @classmethod
    def __prepare__(metacls, name, bases):
        """Makes a Composite's dict an OrderedDict"""

        return OrderedDict()
    # end class __prepare__

    def __new__(cls, name, bases, clsdict):
        """Builds the _fields_ attribute"""

        new_cls = type.__new__(cls, name, bases, clsdict)
        new_clsdict = new_cls.__dict__

        fields = new_clsdict.get("_fields_")
        mro = new_cls.__mro__

        if fields is None:
            fields = list()

            klsdicts = [klass.__dict__ for klass in mro]

            # Find the most recent _fields_, since it should contain every
            # _fields_ before it.
            for klsdict in klsdicts:
                _fields_ = klsdict.get("_fields_")
                if _fields_:
                    break
                # end if
            else:
                _fields_ = list()
            # end for

            fields.extend(_fields_)
            for (key, value) in clsdict.items():
                if not key.startswith("_"):
                    fields.append((key, value))
                # end if
            # end for

            new_cls._fields_ = fields
        # end if

        return new_cls
    # end def __new__

    def __init__(cls, name, bases, clsdict):
        """Makes the _ctype_ and _size_ attributes"""

        # This we *have* to have
        fields = cls._fields_
        byte_order = cls._byte_order_

        ctype = clsdict.get("_ctype_")
        size = clsdict.get("_size_")

        if ctype is None:
            my_field_names = map(itemgetter(0), fields)
            ctypes_fields = list()

            for (field_name, field) in fields:
                if isinstance(field, list):
                    ctype = field[0]._ctype_ * len(field)
                    ctypes_fields.append((field_name, ctype))
                elif hasattr(field, "_int_type_"):
                    for(bname, bfield) in field._fields_:
                        if bname in my_field_names:
                            raise ValueError(
                                "Duplicate field name {0}".format(bname)
                            )
                        # end if

                        ctypes_fields.append(
                            (bname, field._int_type_, bfield._size_)
                        )
                    # end for
                else:
                    ctypes_fields.append((field_name, field._ctype_))
                # end if

            # end for

            anonymous = clsdict.get("_anonymous_")
            if anonymous is None:
                anonymous = []
            # end if

            pack = clsdict.get("_pack_")
            if pack is None:
                pack = 1
            # end if

            ctype_name = clsdict.get("_ctype_name_")
            if ctype_name is None:
                ctype_name = "".join(["__ctype_", name])
            # end if

            ctypes_dict = {
                "_fields_": ctypes_fields,
                "_pack_": pack,
                "_anonymous_": anonymous
            }

            if byte_order == LITTLE_ENDIAN:
                ctypes_bases = (LittleEndianStructure,)
            else:
                ctypes_bases = (BigEndianStructure,)
            # end if

            cls._ctype_ = type(ctype_name, ctypes_bases, ctypes_dict)
        # end if

        if size is None:
            size = 0

            for (field_name, field) in fields:
                if isinstance(field, list):
                    size += field[0]._size_ * len(field)
                else:
                    size += field._size_
                # end if
            # end for

            cls._size_ = size
        # end if
    # end def __init__
# end class MetaRecord

class Composite(Primitive):
    """Base class for data types that can be composed of data types.
    Since this is a :class:`Primitive` class, subclasses can be used to both
    compose data types, as well as be composed of other data types.

    Fields are implemented as class attributes.  For instance:

        >>> from lf.dtypes import LERecord, int8, uint8
        >>> class SomeStruct(LERecord):
        ...     field1 = int8
        ...     field2 = uint8
        ...
        >>>

    Will create a class called SomeStruct, with two fields called field1 and
    field2.

    Composite objects can also inherit from each other, adding the new fields
    to the old ones.  Continuing the previous example:

        >>> class AnotherStruct(SomeStruct):
        ...     field3 = uint8
        ...
        >>>

    Will create a class called AnotherStruct, with three fields called field1,
    field2, and field 3.


    .. attribute:: _fields_

        A list of (field name, ctype object) tuples.  If this is None, it is
        created automatically by the metaclass.

    .. attribute:: _byte_order_

        The byte ordering to use (:const:`LITTLE_ENDIAN` or
        :const:`BIG_ENDIAN`)

    .. attribute:: _pack_

        The _pack_ attribute used when creating the :attr:`_ctype_` attribute.
        The default is 1.

    .. attribute:: _anonymous_

        The value of the _anonymous_ attribute used when creating the
        :attr:`_ctype_` attribute.

    .. attribute:: _ctype_name_

        The name to use for the :attr:`_ctype_` attribute.  If this is not
        specified, a name is autogenerated by a metaclass, based on the class
        name.

    """

    _fields_ = None
    _pack_ = 1
    _byte_order_ = LITTLE_ENDIAN
# end class Composite

class Record(Composite, metaclass=MetaRecord):
    """Base class for creating record data types."""

    pass
# end class Record

class LERecord(Record):
    """Class for creating little endian record data types."""

    _byte_order_ = LITTLE_ENDIAN
# end class LERecord

class BERecord(Record):
    """Class for creating big endian record data types."""

    _byte_order_ = BIG_ENDIAN
# end class BERecord
