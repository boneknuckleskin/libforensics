# Copyright 2009 Michael Murr
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

"""
Data types composed of primitive data types.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from inspect import isclass
from collections import OrderedDict
from lf.datatype.base import Primitive
from lf.datatype.consts import BIG_ENDIAN, LITTLE_ENDIAN, DEFAULT_ENDIAN
from lf.datatype.bits import BitType
from lf.datatype import structuple

__docformat__ = "restructuredtext en"
__all__ = [
    "ExtractableArray", "LEExtractableArray", "BEExtractableArray", "array",
    "Record", "LERecord", "BERecord"
]

class MetaComposite(type):
    """Metaclass to build tuple_factory and size attributes of Composites"""

    @classmethod
    def __prepare__(metacls, name, bases):
        """Makes a Composite's dict an OrderedDict"""

        return OrderedDict()
    # end class __prepare__

    def __new__(cls, name, bases, clsdict):
        """Builds the _fields_ and _factory_ attributes"""

        new_cls = type.__new__(cls, name, bases, clsdict)
        new_clsdict = new_cls.__dict__

        fields = new_clsdict.get("_fields_")
        size = new_clsdict.get("_size_")
        mro = new_cls.__mro__

        if fields is None:
            fields = list()

            klsdicts = [klass.__dict__ for klass in mro]
            klsdicts[0] = clsdict

            for klsdict in klsdicts:
                try:
                    _fields_ = iter(klsdict.get("_fields_"))
                except TypeError:
                    _fields_ = iter(klsdict.items())
                # end try

                klass_fields = list()
                for (fname, datatype) in _fields_:
                    if not fname.startswith("_"):
                        klass_fields.append((fname, datatype))
                    # end if
                # end for

                klass_fields.extend(fields)
                fields = klass_fields
            # end for

            new_cls._fields_ = fields
        # end if

        return new_cls
    # end def __new__

    def __init__(cls, name, bases, clsdict):
        """Sets up the _factory_ and _size_ values"""

        factory = clsdict.get("_factory_")
        size = clsdict.get("_size_")
        fields = cls._fields_

        if factory is None:
            field_names = list()

            for (fname, dtype) in fields:
                if isclass(dtype):
                    check_if_is = issubclass
                else:
                    check_if_is = isinstance
                # end if

                if check_if_is(dtype, BitType):
                    field_names.extend(
                        [bfield[0] for bfield in dtype._fields_]
                    )
                else:
                    field_names.append(fname)
            # end for

            field_names = " ".join(field_names)
            tuple_name = "".join(["__st_", name])
            cls._factory_ = structuple.make(tuple_name, field_names, True)
        # end if

        if size is None:
            size = sum([field[1]._size_ for field in fields])
            cls._size_ = size
        # end if
    # end def __init__
# end class MetaComposite

class Composite(Primitive, metaclass=MetaComposite):
    """
    Data types composed of other data types.

    .. attribute:: _fields_

        A list of the fields in the data type.  If this is None, then it is set
        by the metaclass.
    """

    _fields_ = None

    @classmethod
    def _flatten(cls, root_id=1, expand_bits=True):
        """
        Flattens the composite structure into a form usable with an NAryTree.

        :parameters:
            root_id
                The identifer to use as the root identifier.

            expand_bits
                If true, will include the bits as individual fields.  Otherwise
                the entire BitType object will be considered a single field.

        :rtype: list
        :returns: A list of (id, object) tuples, used to create an NAryTree.
        """

        flattened = [(root_id, cls)]
        field_id = root_id * 2

        for (name, field) in cls._fields_:
            if isclass(field):
                check_is = issubclass
            else:
                check_is = isinstance
            # end if

            if check_is(field, Composite):
                flattened.extend(field._flatten(field_id, expand_bits))
            elif expand_bits and check_is(field, BitType):
                for (bfname, bfield) in field._fields_:
                    flattened.append((field_id, bfield))
                    field_id = (field_id * 2) + 1
                # end for

                continue
            else:
                flattened.append((field_id, field))
            # end if

            field_id = (field_id * 2) + 1
        # end for

        return flattened
    # end def _flatten
# end class Composite

class Extractable():
    """
    Interface for data types that can be used with Extractors.

    .. attribute:: _byte_order_

        The byte ordering for the structure.

    .. attribute:: _factory_

        A function that is used to create the collection objects during
        extraction.
    """

    _byte_order_ = None
    _factory_ = None
# end class Extractable

class Record(Extractable, Composite):
    """A data type composed of other data types."""

    _factory_ = None
# end class Record

class LERecord(Record):
    """Convenience class for creating little endian records"""

    _byte_order_ = LITTLE_ENDIAN
# end class LERecord

class BERecord(Record):
    """Convenience class for creating big endian records"""

    _byte_order_ = BIG_ENDIAN
# end class BERecord

class array(Composite):
    """A data type composed of a homogenous list of other data types."""

    _factory_ = list

    def __init__(self, data_type, count):
        """
        Initializes an array object.

        :parameters:
            data_type
                A Primitive data type.

            count
                The number of items in the array.

        :raises:
            TypeError
                If field is not a Primitive type.
        """

        if isclass(data_type):
            check_is = issubclass
        else:
            check_is = isinstance
        # end if

        if not check_is(data_type, Primitive):
            if hasattr(data_type, "__name__"):
                name = data_type.__name__
            elif hasattr(data_type.__class__, "__name__"):
                name = data_type.__class__.__name__
            else:
                name = str(data_type)
            # end if

            raise TypeError("{0} is not a Primitive type".format(name))
        # end if

        super(array, self).__init__()

        self._fields_ = [("", data_type)] * count
        self._size_ = data_type._size_ * count
    # end def __init__

    def _flatten(self, root_id=1, expand_bits=True):
        """
        Flattens the composite structure into a form usable with an NAryTree.

        :parameters:
            root_id
                The identifer to use as the root identifier.

            expand_bits
                If true, will include the bits as individual fields.  Otherwise
                the entire BitType object will be considered a single field.

        :rtype: list
        :returns: A list of (id, object) tuples, used to create an NAryTree.
        """

        flattened = [(root_id, self)]
        field_id = root_id * 2

        for (name, field) in self._fields_:
            if isclass(field):
                check_is = issubclass
            else:
                check_is = isinstance
            # end if

            if check_is(field, Composite):
                flattened.extend(field._flatten(field_id, expand_bits))
            elif expand_bits and check_is(field, BitType):
                for (bfname, bfield) in field._fields_:
                    flattened.append((field_id, bfield))
                    field_id = (field_id * 2) + 1
                # end for

                continue
            else:
                flattened.append((field_id, field))
            # end if

            field_id = (field_id * 2) + 1
        # end for

        return flattened
    # end def _flatten
# end class array

class ExtractableArray(Extractable, array):
    """An array that is extractable"""

    _factory_ = list
# end class ExtractableArray

class LEExtractableArray(ExtractableArray):
    """Convenience class to create little endian ExtractableArrays."""

    _byte_order_ = LITTLE_ENDIAN
# end class LEExtractableArray

class BEExtractableArray(ExtractableArray):
    """Convenience class to create big endian ExtractableArrays."""

    _byte_order_ = BIG_ENDIAN
# end class BEExtractableArray
