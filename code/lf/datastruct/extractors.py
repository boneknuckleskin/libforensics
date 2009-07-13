# Copyright 2009 Michael Murr
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

"""
Convenience modu_le that contains extractors for primitive data types.

.. modu_leauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.datastruct import field
from lf.datastruct.extract import Extractor

DataStruct_LE = field.DataStruct_LE
DataStruct_BE = field.DataStruct_BE

docformat = "restructuredtext en"
all = [
    "int8", "uint8", "int16_le", "uint16_le", "int32_le", "uint32_le",
    "int64_le", "uint64_le", "float32_le", "float64_le",
    "int16_be", "uint16_be", "int32_be", "uint32_be", "int64_be", "uint64_be",
    "float32_be", "float64_be", "char"
]

class Int8(DataStruct_LE):
    fields = [ field.int8("value") ]
# end class Int8

class UInt8(DataStruct_LE):
    fields = [ field.uint8("value") ]
# end class UInt8

class Int16_LE(DataStruct_LE):
    fields = [ field.int16("value") ]
# end class Int16LE

class Int16_BE(DataStruct_BE):
    fields = [ field.int16("value") ]
# end class Int16BE

class UInt16_LE(DataStruct_LE):
    fields = [ field.uint16("value") ]
# end class UInt16LE

class UInt16_BE(DataStruct_BE):
    fields = [ field.uint16("value") ]
# end class UInt16BE

class Int32_LE(DataStruct_LE):
    fields = [ field.int32("value") ]
# end class Int32LE

class Int32_BE(DataStruct_BE):
    fields = [ field.int32("value") ]
# end class Int32BE

class UInt32_LE(DataStruct_LE):
    fields = [ field.uint32("value") ]
# end class UInt32LE

class UInt32_BE(DataStruct_BE):
    fields = [ field.uint32("value") ]
# end class UInt32BE

class Int64_LE(DataStruct_LE):
    fields = [ field.int64("value") ]
# end class Int64LE

class Int64_BE(DataStruct_BE):
    fields = [ field.int64("value") ]
# end class Int64LE

class UInt64_LE(DataStruct_LE):
    fields = [ field.uint64("value") ]
# end class UInt64LE

class UInt64_BE(DataStruct_BE):
    fields = [ field.uint64("value") ]
# end class UInt64BE

class Float32_LE(DataStruct_LE):
    fields = [ field.float32("value") ]
# end class Float32LE

class Float32_BE(DataStruct_BE):
    fields = [ field.float32("value") ]
# end class Float32BE

class Float64_LE(DataStruct_LE):
    fields = [ field.float64("value") ]
# end class Float64LE

class Float64_BE(DataStruct_BE):
    fields = [ field.float64("value") ]
# end class Float64BE

class Char(DataStruct_LE):
    fields = [ field.char("value") ]
# end class Char

int8 = Extractor(Int8())
uint8 = Extractor(UInt8())
int16_le = Extractor(Int16_LE())
int16_be = Extractor(Int16_BE())
uint16_le = Extractor(UInt16_LE())
uint16_be = Extractor(UInt16_BE())
int32_le = Extractor(Int32_LE())
int32_be = Extractor(Int32_BE())
uint32_le = Extractor(UInt32_LE())
uint32_be = Extractor(UInt32_BE())
int64_le = Extractor(Int64_LE())
int64_be = Extractor(Int64_BE())
uint64_le = Extractor(UInt64_LE())
uint64_be = Extractor(UInt64_BE())
float32_le = Extractor(Float32_LE())
float32_be = Extractor(Float32_BE())
float64_le = Extractor(Float64_LE())
float64_be = Extractor(Float64_BE())
char = Extractor(Char())
