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
Describe and read data types.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.datatype.builtin import (
    int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32, float64,
    raw, char
)

from lf.datatype.bits import (
    bit, bits, BitType, BitType8, BitTypeU8, BitType16, BitTypeU16, BitType32,
    BitTypeU32, BitType64, BitTypeU64
)

from lf.datatype.composite import (
    Record, LERecord, BERecord, ExtractableArray, LEExtractableArray,
    BEExtractableArray, array
)

from lf.datatype.consts import (
    BIG_ENDIAN, LITTLE_ENDIAN, NETWORK_ENDIAN, DEFAULT_ENDIAN
)

from lf.datatype.decode import Decoder
from lf.datatype.extract import Extractor

__docformat__ = "restructuredtext en"
__all__ = [
    "base", "bits", "builtin", "composite", "consts", "decode", "excepts",
    "extract", "structuple"
]
