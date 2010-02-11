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

"""Data types that have native support in the :mod:`ctypes` module."""

# stdlib imports
from math import ceil
from ctypes import (
    c_int8, c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_int64, c_uint64,
    c_float, c_double
)

# local imports
from lf.dtypes.basic import Basic

__docformat__ = "restructuredtext en"
__all__ = [
    "int8", "uint8", "int16", "uint16", "int32", "uint32", "int64", "uint64",
    "float32", "float64"
]

class Native(Basic):
    """Base class for :class:`Native` data types."""

    pass
# end class Native

class int8(Native):
    """Signed 8-bit integer."""

    _size_ = 1
    _ctype_ = c_int8
# end class int8

class uint8(Native):
    """Unsigned 8-bit integer."""

    _size_ = 1
    _ctype_ = c_uint8
# end class uint8

class int16(Native):
    """Signed 16-bit integer."""

    _size_ = 2
    _ctype_ = c_int16
# end class int16

class uint16(Native):
    """Unsigned 16-bit integer."""

    _size_ = 2
    _ctype_ = c_uint16
# end class uint16

class int32(Native):
    """Signed 32-bit integer."""

    _size_ = 4
    _ctype_ = c_int32
# end class int32

class uint32(Native):
    """Unsigned 32-bit integer."""

    _size_ = 4
    _ctype_ = c_uint32
# end class uint32

class int64(Native):
    """Signed 64-bit integer."""

    _size_ = 8
    _ctype_ = c_int64
# end class int64

class uint64(Native):
    """Unsigned 64-bit integer."""

    _size_ = 8
    _ctype_ = c_uint64
# end class uint64

class float32(Native):
    """32-bit floating point number."""

    _size_ = 4
    _ctype_ = c_float
# end class float32

class float64(Native):
    """64-bit floating point number."""

    _size_ = 8
    _ctype_ = c_double
# end class float64
