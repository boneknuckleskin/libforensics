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
Common data structures for Microsoft Windows.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.struct.consts import LITTLE_ENDIAN
from lf.struct.datastruct import DataStruct, Array
from lf.windows.types import WORD, DWORD, BYTE, ULONG, ULONGLONG

__docformat__ = "restructuredtext en"
__all__ = [
    "GUID", "CLSID", "DECIMAL", "FILETIME"
]

class GUID(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("data1"),
        WORD("data2"),
        WORD("data3"),
        Array(8, BYTE(), "data4")
    ]
# end class GUID

class CLSID(GUID):
    pass
# end class CLSID

class DECIMAL(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        WORD("rsvd"),
        BYTE("scale"),
        BYTE("sign"),
        ULONG("hi32"),
        ULONGLONG("lo64")
    ]
# end class DECIMAL

class FILETIME(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        ULONG("lo"),
        ULONG("hi")
    ]
# end class FILETIME
