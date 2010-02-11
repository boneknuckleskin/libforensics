# Copyright 2010 Michael Murr
#
# This fi_le is part of LibForensics.
#
# LibForensics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibForensics is distributed in the hope that it will _be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with LibForensics.  If not, see <http://www.gnu.org/licenses/>.

"""Convenience module for using native ctypes."""

# stdlib imports
from ctypes import (
    c_uint8, c_int8, c_uint16, c_int16, c_uint32, c_int32, c_uint64, c_int64,
    c_float, c_double
)

__docformat__ = "restructuredtext en"
__all__ = [
    "int8", "uint8",
    "int16_le", "int16_be", "uint16_le", "uint16_be",
    "int32_le", "int32_be", "uint32_le", "uint32_be",
    "int64_le", "int64_be", "uint64_le", "uint64_be",
    "float32_le", "float32_be", "float64_le", "float64_be"
]

int8 = c_int8
uint8 = c_uint8

int16_le = c_int16.__ctype_le__
int16_be = c_int16.__ctype_be__
uint16_le = c_uint16.__ctype_le__
uint16_be = c_uint16.__ctype_be__

int32_le = c_int32.__ctype_le__
int32_be = c_int32.__ctype_be__
uint32_le = c_uint32.__ctype_le__
uint32_be = c_uint32.__ctype_be__

int64_le = c_int64.__ctype_le__
int64_be = c_int64.__ctype_be__
uint64_le = c_uint64.__ctype_le__
uint64_be = c_uint64.__ctype_be__

float32_le = c_float.__ctype_le__
float32_be = c_float.__ctype_be__
float64_le = c_double.__ctype_le__
float64_be = c_double.__ctype_be__
