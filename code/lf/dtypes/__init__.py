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

"""Describe and read data types."""

# local imports
from lf.dtypes.base import DataType, Primitive
from lf.dtypes.basic import Basic, raw
from lf.dtypes.native import (
    Native, int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32,
    float64
)
from lf.dtypes.bits import (
    bits, bit, BitType, BitType8, BitTypeU8, BitType16, BitTypeU16, BitType32,
    BitTypeU32, BitType64, BitTypeU64
)
from lf.dtypes.consts import LITTLE_ENDIAN, BIG_ENDIAN
from lf.dtypes.composite import Composite, Record, LERecord, BERecord
from lf.dtypes.dal import (
    structuple, Structuple, ActiveStructuple, CtypesWrapper, Converter,
    StdLibConverter
)
from lf.dtypes.reader import Reader, BoundReader

__docformat__ = "restructuredtext en"
__all__ = [
    "DataType", "Primitive", "Basic", "raw", "Native", "int8", "uint8",
    "int16", "uint16", "int32", "uint32", "int64", "uint64", "float32",
    "float64", "bits", "bit", "BitType", "BitType8", "BitTypeU8", "BitType16",
    "BitTypeU16", "BitType32", "BitTypeU32", "BitType64", "BitTypeU64",
    "LITTLE_ENDIAN", "BIG_ENDIAN", "Composite", "Record", "LERecord",
    "BERecord", "structuple", "Structuple", "ActiveStructuple",
    "CtypesWrapper", "Converter", "StdLibConverter", "Reader", "BoundReader"
]
