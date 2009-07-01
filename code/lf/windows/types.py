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
Common data types for Microsoft data structures.

A lot of this information can be found at:
http://spreadsheets.google.com/ccc?key=pK5CEcdG9GYGeO7K2dmEcBg

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from lf.struct.datatype import Bool, Int8, UInt8, Int16, UInt16, Int32
from lf.struct.datatype import UInt32, Int64, UInt64, Float32, Float64

class BYTE(UInt8):
    pass
# end class BYTE

class CHAR(Int8):
    pass
# end class CHAR

class DOUBLE(Float64):
    pass
# end class DOUBLE

class DWORD(UInt32):
    pass
# end class DWORD

class DWORD32(UInt32):
    pass
# end class DWORD32

class DWORD64(UInt64):
    pass
# end class DWORD64

class DWORDLONG(UInt64):
    pass
# end class DWORDLONG

class HFILE(Int32):
    pass
# end class HFILE

class INT(Int32):
    pass
# end class INT

class INT8(Int8):
    pass
# end class INT8

class INT16(Int16):
    pass
# end class INT16

class INT32(Int32):
    pass
# end class INT32

class INT64(Int64):
    pass
# end class INT64

class LARGE_INTEGER(Int64):
    pass
# end class LARGE_INTEGER

class LONG(Int32):
    pass
# end class LONG

class LONG32(Int32):
    pass
# end class LONG32

class LONG64(Int64):
    pass
# end class LONG64

class LONGLONG(Int64):
    pass
# end class LONGLONG

class POINTER_32(UInt32):
    pass
# end class POINTER_32

class POINTER_64(UInt64):
    pass
# end class POINTER_64

class REAL(Float32):
    pass
# end class REAL

class REAL32(Float32):
    pass
# end class REAL32

class SHORT(Int16):
    pass
# end class SHORT

class UCHAR(UInt8):
    pass
# end class UCHAR

class UINT(UInt32):
    pass
# end class UINT

class UINT8(UInt8):
    pass
# end class UINT8

class UINT16(UInt16):
    pass
# end class UINT16

class UINT32(UInt32):
    pass
# end class UINT32

class UINT64(UInt64):
    pass
# end class UINT64

class ULONG(UInt32):
    pass
# end class ULONG

class ULONG32(UInt32):
    pass
# end class ULONG32

class ULONG64(UInt64):
    pass
# end class ULONG64

class ULONGLONG(UInt64):
    pass
# end class ULONGLONG

class UNSIGNED32(UInt32):
    pass
# end class UNSIGNED32

class UNSIGNED64(UInt64):
    pass
# end class UNSIGNED64

class USHORT(UInt16):
    pass
# end class USHORT

class UTIME(UInt32):
    pass
# end clas UTIME

class WCHAR(UInt16):
    pass
# end class WCHAR

class WORD(UInt16):
    pass
# end class WORD

class QWORD(UInt64):
    pass
# end class QWORD

class SHORT(Int16):
    pass
# end class SHORT


class ATOM(WORD):
    pass
# end class ATOM

class ATTRIBUTE_TYPE_CODE(ULONG):
    pass
# end class ATTRIBUTE_TYPE_CODE

class BOOLEAN(BYTE):
    pass
# end class BOOLEAN

class COLORRREF(DWORD):
    pass
# end class COLORREF

class CURRENCY(INT64):
    pass
# end class CURRENCY

class DATE(DOUBLE):
    pass
# end class DATE

class HRESULT(LONG):
    pass
# end class HRESULT

class LANGID(WORD):
    pass
# end class LANGID

class LCID(DWORD):
    pass
# end class LCID

class LCN(LONGLONG):
    pass
# end class LCN

class LGRPID(DWORD):
    pass
# end class LGRPID

class USN(LONGLONG):
    pass
# end class USN

class VARIANT_BOOL(SHORT):
    pass
# end class VARIANT_BOOL

class VCN(LONGLONG):
    pass
# end class VCN
