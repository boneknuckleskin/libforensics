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
Describe and read data structures.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from math import ceil

from lf.datastruct.consts import BIG_ENDIAN, LITTLE_ENDIAN, DEFAULT_ENDIAN
from lf.datastruct.decode import Decoder
from lf.datastruct import structuple

__docformat__ = "restructuredtext en"
__all__ = [
    "bit", "int8", "uint8", "int16", "uint16", "int32", "uint32", "int64",
    "uint64", "float32", "float64", "raw", "char", "array", "DataStruct",
    "DataStruct_LE", "DataStruct_BE", "Bits", "Bits8", "UBits8", "Bits16",
    "UBits16", "Bits32", "UBits32", "Bits64", "UBits64", "ListStruct"
]

class Field():
    """
    Base class for all data structure fields recognized by the framework.

    .. attribute:: name

        The name of the field.

    .. attribute:: size

        The size of the field.  The units for this depends on the subclass.
    """

    size = 0

    def __init__(self, name):
        """
        Initializes a Field object.

        :parameters:
            name
                The name of the field.
        """

        self.name = name
    # end def __init__
# end class Field

class bit(Field):
    """
    Represents one or more bits

    .. attribute:: size

        The number of bits in the field.
    """

    def __init__(self, name, size=1):
        """
        Initializes a bit object.

        :parameters:
            name
                The name of the field.

            size
                The number of bits in the field. (def: 1)
        """

        super(bit, self).__init__(name)
        self.size = size
    # end def __init__
# end class bit

class IntegralSize(Field):
    """
    Base class for fields with an integral size.

    .. attribute:: size

        The number of bytes required to represent the field.
    """

    size = 0
# end class IntegralSize

class Primitive(IntegralSize):
    """
    Fields of integral size, that can be used to create other fields.

    .. attribute:: format_str

        A format string that the struct module can use to extract the field.
    """

    format_str = None
# end class Primitive

class BuiltIn(Primitive):
    """Fields that have built-in support from the struct module"""

    pass
# end class BuiltIn

class int8(BuiltIn):
    """Signed 8-bit integer"""

    size = 1
    format_str = "b"
# end class int8

class uint8(BuiltIn):
    """Unsigned 8-bit integer"""

    size = 1
    format_str = "B"
# end class uint8

class int16(BuiltIn):
    """Signed 16-bit integer"""

    size = 2
    format_str = "h"
# end class int16

class uint16(BuiltIn):
    """Unsigned 16-bit integer"""

    size = 2
    format_str = "H"
# end class uint16

class int32(BuiltIn):
    """Signed 32-bit integer"""

    size = 4
    format_str = "i"
# end class int32

class uint32(BuiltIn):
    """Unsigned 32-bit integer"""

    size = 4
    format_str = "I"
# end class uint32

class int64(BuiltIn):
    """Signed 64-bit integer"""

    size = 8
    format_str = "q"
# end class int64

class uint64(BuiltIn):
    """Unsigned 64-bit integer"""

    size = 8
    format_str = "Q"
# end class uint64

class float32(BuiltIn):
    """32-bit floating point number"""

    size = 4
    format_str = "f"
# end class float32

class float64(BuiltIn):
    """64-bit floating point number"""

    size = 8
    format_str = "d"
# end class float64

class char(BuiltIn):
    """bytes of length 1 (single character)"""

    size = 1
    format_str = "c"
# end class char

class raw(BuiltIn):
    """A series of raw bytes"""

    def __init__(self, name, size):
        """
        Initializes a raw object.

        :parameters:
            name
                The name of the field.

            size
                The number of bytes in the field.
        """

        super(raw, self).__init__(name)
        self.size = size
    # end def __init__

    @property
    def format_str(self):
        """
        A struct format string.

        :rtype: str
        :returns: A format string that the struct module can use.
        """

        return "{0}s".format(self.size)
    # end def format_str
# end class raw

class MetaBits(type):
    """Metaclass to setup up bits and decoder in Bits classes"""

    def __init__(cls, name, bases, clsdict):
        """Initializes a Bits.__class__ object"""

        bits = clsdict.get("bits")
        size = clsdict.get("size")
        decoder = clsdict.get("decoder")
        mro = cls.__mro__

        if bits is None:
            for klass in mro:
                try:
                    bits = klass.bits
                    break
                except AttributeError:
                    pass
                # end try
            else:
                raise AttributeError("Bits classes must have a bits attribute")
            # end for
        # end if

        if size is None:
            for klass in mro:
                try:
                    size = klass.size
                    break
                except AttributeError:
                    pass
                # end try
            else:
                raise AttributeError("Bits classes must have a size attribute")
            # end for
        # end if

        max_bit_size = size * 8

        bit_size = sum([bit_obj.size for bit_obj in bits])
        if bit_size < max_bit_size:
            bits.append(bit("bits_pad_", (max_bit_size - bit_size)))
        # end if
        setattr(cls, "bits", bits)

        if not decoder:
            setattr(cls, "decoder", Decoder(bits))
        # end if

        super(MetaBits, cls).__init__(name, bases, clsdict)
    # end def __init__
# end class MetaBits

class Bits(Primitive, metaclass=MetaBits):
    """
    A wrapper around bits, used to ensure an intergral size

    .. attribute:: bits

        A list of bit objects, describing the individual bits.  At class build
        time, one extra element may be added (to account for unused bits) by
        the metaclass.  It will be called "bits_pad_".

    .. attribute:: decoder

        A Decoder that can extract the individual bits. (built by a Metaclass)
    """

    bits = list()
    decoder = None
    size = 0

    def __init__(self):
        """
        Initializes a Bits object.

        :raises:
            TypeError
                If self.bits contains something other than bit objects.

            OverflowError
                If the cumulative size of self.bits is too big for the
                container.
        """

        super(Bits, self).__init__("")
        bit_size = 0

        for bfield in self.bits:
            if not isinstance(bfield, bit):
                raise TypeError("Bits classes can only contain bit objects")
            # end if

            bit_size += bfield.size
        # end for

        if bit_size > (self.size * 8):
            raise OverflowError("Too many bits")
        # end if
    # end def __init__
# end class Bits

class Bits8(Bits):
    """A bit structure represented by a signed 8-bit integer"""

    size = 1
    format_str = "b"
# end class bits8

class UBits8(Bits):
    """A bit structure represented by an unsigned 8-bit integer"""

    size = 1
    format_str = "B"
# end class ubits8

class Bits16(Bits):
    """A bit structure represented by a signed 16-bit integer"""

    size = 2
    format_str = "h"
# end class bits16

class UBits16(Bits):
    """A bit structure represented by an unsigned 16-bit integer"""

    size = 2
    format_str = "H"
# end class UBits16

class Bits32(Bits):
    """A bit structure represented by a signed 32-bit integer"""

    size = 4
    format_str = "i"
# end class Bits32

class UBits32(Bits):
    """A bit structure represented by an unsigned 32-bit integer"""

    size = 4
    format_str = "I"
# end class UBits32

class Bits64(Bits):
    """A bit structure represented by a signed 64-bit integer"""

    size = 8
    format_str = "q"
# end class Bits64

class UBits64(Bits):
    """A bit structure represented by an unsigned 64-bit integer"""

    size = 8
    format_str = "Q"
# end class UBits64

class MetaComposite(type):
    """Metaclass to build tuple_factory and size attributes of Composites"""

    def __init__(cls, name, bases, clsdict):
        """Initializes a newly created Composite class"""

        tuple_factory = clsdict.get("tuple_factory")
        fields = clsdict.get("fields")

        if not fields:
            for klass in cls.__mro__:
                try:
                    fields = klass.fields
                    break
                except AttributeError:
                    pass
                # end try
            else:
                raise AttributeError(
                    "Composite classes must have a fields attribute"
                )
            # end for
        # end if

        if not tuple_factory:
            field_names = list()

            for field in fields:
                if isinstance(field, Bits):
                    field_names.extend([bfield.name for bfield in field.bits])
                else:
                    field_names.append(field.name)
                # end if
            # end for
            field_names = " ".join(field_names)
            tuple_name = "".join(["__st_", name])

            setattr(
                cls,
                "tuple_factory",
                structuple.make(tuple_name, field_names, rename=True)
            )
        # end if

        size = clsdict.get("size")
        if size is None:
            size = sum([field.size for field in fields])
            setattr(cls, "size", size)
        # end if

        super(MetaComposite, cls).__init__(name, bases, clsdict)
    # end def __init__
# end class MetaComposite

class Composite(IntegralSize, metaclass=MetaComposite):
    """
    Fields composed of other fields.

    .. attribute:: fields

        A list of the nested fields.

    .. attribute:: tuple_factory

        A factory that can create tuples that describe the field. (created by
        the Metaclass)
    """

    fields = list()
    tuple_factory = None

    def __init__(self, name):
        """
        Initializes a Composite object.

        :parameters:
            name
                The name of the field.

        :raises:
            TypeError
                If any of the nested fields are not a descendent of
                IntegralSize.
        """

        super(Composite, self).__init__(name)

        for field in self.fields:
            if not isinstance(field, IntegralSize):
                raise TypeError(
                    "Composites can only contain integral sized fields"
                )
            # end if
        # end for
    # end def __init__

    def flatten(self, root_id=1, expand_bits=True):
        """
        Flattens the composite structure into a form usable with an NAryTree.

        :parameters:
            root_id
                The identifer to use as the root identifier.

            expand_bits
                If true, will include the bits as individual fields.  Otherwise
                the entire Bits object will be considered a single field.

        :rtype: list
        :returns: A list of (id, object) tuples, used to create an NAryTree.
        """

        flattened = [(root_id, self)]
        field_id = (root_id * 2)

        for field in self.fields:
            if isinstance(field, Composite):
                flattened.extend(field.flatten(field_id, expand_bits))
            elif isinstance(field, Bits) and expand_bits:
                for bfield in field.bits:
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
    # end def flatten
# end class Composite

class array(Composite):
    """A field composed of a homogeneous list of fields"""

    tuple_factory = tuple

    def __init__(self, name, field, count):
        """
        Initializes an array object.

        :parameters:
            name
                The name of the array.

            field
                A field object to use.

            count
                The number of items in the array.

        :raises:
            TypeError
                If field is not an IntegralSize'd field.
        """

        # Set this up first so the parent class does the type checking
        self.fields = (field,) * count
        super(array, self).__init__(name)

        self.size = field.size * count
    # end def __init__
# end class array

class DataStruct(Composite):
    """
    A data structure.

    .. attribute:: byte_order

        The byte ordering of the data structure.
    """

    byte_order = DEFAULT_ENDIAN

    def __init__(self, name=""):
        """
        Initializes a DataStruct object.

        :parameters:
            name
                The name of the field.  This is optional if the DataStruct is
                not contained inside of another DataStruct.
        """

        super(DataStruct, self).__init__(name)
    # end def __init__
# end class DataStruct

class DataStruct_LE(DataStruct):
    """Convenience class for creating little endian data structures"""

    byte_order = LITTLE_ENDIAN
# end class DataStruct_LE

class DataStruct_BE(DataStruct):
    """Convenience class for creating big endian data structures"""

    byte_order = BIG_ENDIAN
# end class DataStruct_BE


class ListStruct():
    """
    Struct-like class for creating a list of existing data structures.

    This class is a convenience class, for extracting a homogenous list of
    data structures.  It is basically an array wrapper around a user-supplied
    data structure.
    """

    tuple_factory = tuple

    def __init__(self, data_struct, count):
        """
        Initializes a ListStruct object.

        :parameters:
            data_struct
                A DataStruct to extract.

            count
                The number of instances of data_struct to extract.

        :raises:
            TypeError
                If data_struct is not an instance of DataStruct
        """

        if not isinstance(data_struct, DataStruct):
            raise TypeError("ListStructs can only be composed of DataStructs")
        # end if

        self.fields = [data_struct] * count
        self.size = data_struct.size * count
    # end def __init__

    def flatten(self, root_id=1, expand_bits=True):
        """
        Flattens the composite structure into a form usable with an NAryTree.

        :parameters:
            root_id
                The identifer to use as the root identifier.

            expand_bits
                If true, will include the bits as individual fields.  Otherwise
                the entire Bits object will be considered a single field.

        :rtype: list
        :returns: A list of (id, object) tuples, used to create an NAryTree.
        """

        flattened = [(root_id, self)]
        field_id = (root_id * 2)

        for field in self.fields:
            if isinstance(field, Composite):
                flattened.extend(field.flatten(field_id, expand_bits))
            elif isinstance(field, Bits) and expand_bits:
                for bfield in field.bits:
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
    # end def flatten
# end class ListStruct
