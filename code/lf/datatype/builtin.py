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
Data types that have "built-in" support from the struct module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from math import ceil

from lf.datatype.base import Basic

__docformat__ = "restructuredtext en"
__all__ = [
    "int8", "uint8", "int16", "uint16", "int32", "uint32", "int64", "uint64",
    "float32", "float64", "raw", "char"
]

class BuiltIn(Basic):
    """Fields that have built-in support from the struct module"""

    pass
# end class BuiltIn

class int8(BuiltIn):
    """Signed 8-bit integer"""

    _size_ = 1
    _format_ = "b"
# end class int8

class uint8(BuiltIn):
    """Unsigned 8-bit integer"""

    _size_ = 1
    _format_ = "B"
# end class uint8

class int16(BuiltIn):
    """Signed 16-bit integer"""

    _size_ = 2
    _format_ = "h"
# end class int16

class uint16(BuiltIn):
    """Unsigned 16-bit integer"""

    _size_ = 2
    _format_ = "H"
# end class uint16

class int32(BuiltIn):
    """Signed 32-bit integer"""

    _size_ = 4
    _format_ = "i"
# end class int32

class uint32(BuiltIn):
    """Unsigned 32-bit integer"""

    _size_ = 4
    _format_ = "I"
# end class uint32

class int64(BuiltIn):
    """Signed 64-bit integer"""

    _size_ = 8
    _format_ = "q"
# end class int64

class uint64(BuiltIn):
    """Unsigned 64-bit integer"""

    _size_ = 8
    _format_ = "Q"
# end class uint64

class float32(BuiltIn):
    """32-bit floating point number"""

    _size_ = 4
    _format_ = "f"
# end class float32

class float64(BuiltIn):
    """64-bit floating point number"""

    _size_ = 8
    _format_ = "d"
# end class float64

class char(BuiltIn):
    """bytes of length 1 (single character)"""

    _size_ = 1
    _format_ = "c"
# end class char

class raw(BuiltIn):
    """A series of raw bytes"""

    def __init__(self, size):
        """
        Initializes a raw object.

        :parameters:
            size
                The number of bytes in the field.
        """

        super(raw, self).__init__()
        self._size_ = size
    # end def __init__

    @property
    def _format_(self):
        """
        A struct format string.

        :rtype: str
        :returns: A format string that the struct module can use.
        """

        return "{0}s".format(self._size_)
    # end def _format_
# end class raw
