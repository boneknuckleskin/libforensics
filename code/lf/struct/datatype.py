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
Classes to describe data types.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.struct.datastruct import Primitive

__docformat__ = "restructuredtext en"
__all__ = [
    "Bool", "Int8", "UInt8", "Int16", "UInt16", "Int32", "UInt32", "Int64",
    "UInt64", "Float32", "Float64", "Bytes", "Char"
]

class Bool(Primitive):
    """Boolean"""

    format_str = "?"
    size = 1
# end class Bool

class Int8(Primitive):
    """Signed 8 bit integer"""

    format_str = "b"
    size = 1
# end class Int8

class UInt8(Primitive):
    """Unsigned 8 bit integer"""

    format_str = "B"
    size = 1
# end class UInt8

class Int16(Primitive):
    """Signed 16 bit integer"""

    format_str = "h"
    size = 2
# end class Int16

class UInt16(Primitive):
    """Unsigned 16 bit integer"""

    format_str = "H"
    size = 2
# end class UInt16

class Int32(Primitive):
    """Signed 32 bit integer"""

    format_str = "i"
    size = 4
# end class Int32

class UInt32(Primitive):
    """Unsigned 32 bit integer"""

    format_str = "I"
    size = 4
# end class UInt32

class Int64(Primitive):
    """Signed 64 bit integer"""

    format_str = "q"
    size = 8
# end class Int64

class UInt64(Primitive):
    """Unsigned 64 bit integer"""

    format_str = "Q"
    size = 8
# end class UInt64

class Float32(Primitive):
    """32 bit floating point number"""

    format_str = "f"
    size = 4
# end class Float32

class Float64(Primitive):
    """64 bit floating point number"""

    format_str = "d"
    size = 8
# end class Float64

class Bytes(Primitive):
    """Byte string"""

    def __init__(self, length, field_name=None):
        """
        Initializes a Bytes object.

        :parameters:
            length
                The length of the string, in bytes.

            field_name
                The name of the data structure, if used as a field.
        """

        super(Bytes, self).__init__()
        self.size = length
        self.field_name = field_name
    # end def __init__

    @property
    def format_str(self):
        return "{0}s".format(self.size)
    # end def format_str
# end class Bytes

# NOTE: need to add this to unit tests....
class Char(Primitive):
    """Byte string of length 1"""

    format_str = "c"
    size = 1
# end class Char
