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
Constants for Variant data types.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from uuid import UUID

__docformat__ = "restructuredtext en"
__all__ = [
]

VT_EMPTY = 0
VT_NULL = 1
VT_I2 = 2
VT_I4 = 3
VT_R4 = 4
VT_R8 = 5
VT_CY = 6
VT_DATE = 7
VT_BSTR = 8
VT_ERROR = 0xA
VT_VARIANT = 0xC
VT_BOOL = 0xB
VT_DECIMAL = 0xE
VT_I1 = 0x10
VT_UI1 = 0x11
VT_UI2 = 0x12
VT_UI4 = 0x13
VT_I8 = 0x14
VT_UI8 = 0x15
VT_INT = 0x16
VT_UINT = 0x17
VT_LPSTR = 0x1E
VT_LPWSTR = 0x1F
VT_FILETIME = 0x40
VT_BLOB = 0x41
VT_STREAM = 0x42
VT_STORAGE = 0x43
VT_STREAMED_OBJECT = 0x44
VT_STORED_OBJECT = 0x45
VT_BLOB_OBJECT = 0x46
VT_CF = 0x47
VT_CLSID = 0x48
VT_VERSIONED_STREAM = 0x49
VT_VECTOR = 0x1000
VT_ARRAY = 0x2000
