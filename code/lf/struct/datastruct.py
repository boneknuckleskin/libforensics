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
Classes to describe data structures.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.struct.consts import DEFAULT_ENDIAN, LITTLE_ENDIAN, BIG_ENDIAN

__docformat__ = "restructuredtext en"
__all__ = [
    "Array", "DataStruct", "DataStruct_LE", "DataStruct_BE", "Primitive"
]

class DataStructBase():
    """
    Base class for data structures.  Don't inherit directly from this class,
    instead use Primitive (or more often) DataStruct

    .. attribute:: field_name (optional)

        The name of the data structure, if used as a field.

    .. attribute:: size

        The size of the data structure, in bytes.
    """

    def __init__(self, field_name=None):
        """
        Initializes a DataStructBase object.

        :parameters:
            field_name
                An optional name of the data structure, if used as a field.
        """

        self.field_name = field_name

        if not hasattr(self, "size"):
            self.size = 0
        # end if
    # end def __init__
# end class DataStructBase

class Primitive(DataStructBase):
    """
    Base class for primitive data structures.  Primitive data structures are
    for native data types, understood by the standard library's struct module.

    .. attribute:: format_str

        A format string suitable for the standard library's struct module.
    """

    format_str = None

    def flatten(self, my_id=1):
        """
        Flattens the data structure.

        :parameters:
            my_id
                The identifier for the data structure.

        :rtype: tuple
        :returns: A list of identifers and classes, suitable for creating a
                  dictionary.
        """

        return [(my_id, self)]
    # end def flatten
# end class Primitive

class DataStruct(DataStructBase):
    """
    Base class for composite data structures.  Composite data structures are
    composed of other (both primitive and composite) data structures.

    .. attribute:: fields

        A list of the fields that belong to the data structure.

    .. attribute:: byte_order

        The byte ordering of the data structure.
    """

    # These should be overridden in a subclass
    fields = list()
    byte_order = DEFAULT_ENDIAN

    def __init__(self, field_name=None):
        """
        Initializes a DataStruct class.

        :parameters:
            field_name
                An optional name of th data structure, if used as a field.
        """

        super(DataStruct, self).__init__(field_name)
    # end def __init__

    @property
    def size(self):
        return sum([field.size for field in self.fields])
    # end def size

    def flatten(self, my_id=1):
        """
        Flattens the data structure.

        :parameters:
            my_id
                The identifier for the data structure.

        :rtype: tuple
        :returns: A list of identifers and classes, suitable for creating a
                  dictionary.
        """

        ids_and_classes = [(my_id, self)]
        next_id = my_id * 2

        for field in self.fields:
            ids_and_classes.extend(field.flatten(next_id))
            next_id = (next_id * 2) + 1
        # end for

        return ids_and_classes
    # end def flatten
# end class DataStruct

class DataStruct_LE(DataStruct):
    """Convenience class for creating little endian data structures"""

    byte_order = LITTLE_ENDIAN
# end class DataStruct_LE

class DataStruct_BE(DataStruct):
    """Convenience class for creating big endian data structures"""

    byte_order = BIG_ENDIAN
# end class DataStruct_BE

class Array(DataStruct):
    """
    A composite data structure, composed of an array of homogenous data
    structures.

    Unlike the DataStruct class, this class usually is *not* subclassed.
    Instead instantiate this class directly (similar to a Primitive).

    NOTE: byte_order is ignored.
    """

    def __init__(self, count, data_struct, field_name=None):
        """
        Initializes an Array object.

        :parameters:
            count
                The number of elements in the array.

            data_struct
                The data structure in the array.

            field_name
                An optional name of the data structure, if used as a field.
        """

        super(Array, self).__init__(field_name)
        self.fields = [data_struct] * count
    # end def __init__
# end class Array
