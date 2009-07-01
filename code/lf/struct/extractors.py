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
Convenience module that contains extractors for primitive data types.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.struct import datatype
from lf.struct.datastruct import DataStruct
from lf.struct.extract import extractor_factory as factory
from lf.struct.consts import LITTLE_ENDIAN, BIG_ENDIAN

__docformat__ = "restructuredtext en"
__all__ = [
    "int8", "uint8", "int16_le", "uint16_le", "int32_le", "uint32_le",
    "int64_le", "uint64_le", "float32_le", "float64_le",
    "int16_be", "uint16_be", "int32_be", "uint32_be", "int64_be", "uint64_be",
    "float32_be", "float64_be", "char", "bool"
]

class _Int8(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Int8("value") ]
# end class _Int8

class _UInt8(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.UInt8("value") ]
# end class _UInt8

class _Int16_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Int16("value") ]
# end class _Int16_LE

class _Int16_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.Int16("value") ]
# end class _Int16_BE

class _UInt16_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.UInt16("value") ]
# end class _UInt16_LE

class _UInt16_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.UInt16("value") ]
# end class _UInt16_BE

class _Int32_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Int32("value") ]
# end class _Int32_LE

class _Int32_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.Int32("value") ]
# end class _Int32_BE

class _UInt32_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.UInt32("value") ]
# end class _UInt32_LE

class _UInt32_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.UInt32("value") ]
# end class _UInt32_BE

class _Int64_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Int64("value") ]
# end class _Int64_LE

class _Int64_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.Int64("value") ]
# end class _Int64_LE

class _UInt64_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.UInt64("value") ]
# end class _UInt64_LE

class _UInt64_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.UInt64("value") ]
# end class _UInt64_BE

class _Float32_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Float32("value") ]
# end class _Float32_LE

class _Float32_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.Float32("value") ]
# end class _Float32_BE

class _Float64_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Float64("value") ]
# end class _Float64_LE

class _Float64_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ datatype.Float64("value") ]
# end class _Float64_BE

class _Char(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Char("value") ]
# end class _Char

class _Bool(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ datatype.Bool("value") ]
# end class _Bool

int8 = factory.make(_Int8())
uint8 = factory.make(_UInt8())
int16_le = factory.make(_Int16_LE())
int16_be = factory.make(_Int16_BE())
uint16_le = factory.make(_UInt16_LE())
uint16_be = factory.make(_UInt16_BE())
int32_le = factory.make(_Int32_LE())
int32_be = factory.make(_Int32_BE())
uint32_le = factory.make(_UInt32_LE())
uint32_be = factory.make(_UInt32_BE())
int64_le = factory.make(_Int64_LE())
int64_be = factory.make(_Int64_BE())
uint64_le = factory.make(_UInt64_LE())
uint64_be = factory.make(_UInt64_BE())
float32_le = factory.make(_Float32_LE())
float32_be = factory.make(_Float32_BE())
float64_le = factory.make(_Float64_LE())
float64_be = factory.make(_Float64_BE())
char = factory.make(_Char())
bool = factory.make(_Bool())
