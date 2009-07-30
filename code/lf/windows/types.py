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

from lf.datastruct import (
    int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32,
    float64
)

class BYTE(uint8):
    pass
# end class BYTE

class CHAR(int8):
    pass
# end class CHAR

class DOUBLE(float64):
    pass
# end class DOUBLE

class DWORD(uint32):
    pass
# end class DWORD

class DWORD32(uint32):
    pass
# end class DWORD32

class DWORD64(uint64):
    pass
# end class DWORD64

class DWORDLONG(uint64):
    pass
# end class DWORDLONG

class FILETIME(uint64):
    pass
# end class FILETIME

class HFILE(int32):
    pass
# end class HFILE

class INT(int32):
    pass
# end class INT

class INT8(int8):
    pass
# end class INT8

class INT16(int16):
    pass
# end class INT16

class INT32(int32):
    pass
# end class INT32

class INT64(int64):
    pass
# end class INT64

class LARGE_INTEGER(int64):
    pass
# end class LARGE_INTEGER

class LONG(int32):
    pass
# end class LONG

class LONG32(int32):
    pass
# end class LONG32

class LONG64(int64):
    pass
# end class LONG64

class LONGLONG(int64):
    pass
# end class LONGLONG

class POINTER_32(uint32):
    pass
# end class POINTER_32

class POINTER_64(uint64):
    pass
# end class POINTER_64

class REAL(float32):
    pass
# end class REAL

class REAL32(float32):
    pass
# end class REAL32

class SHORT(int16):
    pass
# end class SHORT

class UCHAR(uint8):
    pass
# end class UCHAR

class UINT(uint32):
    pass
# end class UINT

class UINT8(uint8):
    pass
# end class UINT8

class UINT16(uint16):
    pass
# end class UINT16

class UINT32(uint32):
    pass
# end class UINT32

class UINT64(uint64):
    pass
# end class UINT64

class ULONG(uint32):
    pass
# end class ULONG

class ULONG32(uint32):
    pass
# end class ULONG32

class ULONG64(uint64):
    pass
# end class ULONG64

class ULONGLONG(uint64):
    pass
# end class ULONGLONG

class UNSIGNED32(uint32):
    pass
# end class UNSIGNED32

class UNSIGNED64(uint64):
    pass
# end class UNSIGNED64

class USHORT(uint16):
    pass
# end class USHORT

class UTIME(uint32):
    pass
# end clas UTIME

class WCHAR(uint16):
    pass
# end class WCHAR

class WORD(uint16):
    pass
# end class WORD

class QWORD(uint64):
    pass
# end class QWORD

class SHORT(int16):
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

class COLORREF(DWORD):
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
