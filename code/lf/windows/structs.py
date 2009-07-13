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

from lf.datastruct import DataStruct_LE, array, BIG_ENDIAN
from lf.windows.types import WORD, DWORD, BYTE, ULONG, ULONGLONG

__docformat__ = "restructuredtext en"
__all__ = [
    "GUID", "CLSID", "DECIMAL"
]

class GUID(DataStruct_LE):
    fields = [
        DWORD("data1"),
        WORD("data2"),
        WORD("data3"),
        array("data4", BYTE(""), 8)
    ]
# end class GUID

class CLSID(GUID):
    pass
# end class CLSID

class DECIMAL(DataStruct_LE):
    fields = [
        WORD("rsvd"),
        BYTE("scale"),
        BYTE("sign"),
        ULONG("hi32"),
        ULONGLONG("lo64")
    ]
# end class DECIMAL
