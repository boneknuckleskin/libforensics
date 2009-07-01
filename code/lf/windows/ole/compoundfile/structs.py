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
Data structures for OLE structured storage files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "TIME_T", "Header", "DirEntry"
]

from lf.struct.consts import LITTLE_ENDIAN
from lf.struct.datastruct import Array, DataStruct
from lf.struct.datatype import Bytes
from lf.windows.types import (
    ULONG, USHORT, BYTE, WORD, DWORD, ULONGLONG
)
from lf.windows.structs import CLSID, FILETIME, GUID
from lf.windows.ole.compoundfile.types import (
    OFFSET, SECT, FSINDEX, FSOFFSET, DFSIGNATURE, DFPROPTYPE, SID
)

class TIME_T(FILETIME):
    pass
# end class TIME_T

class Header(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Bytes(8, "sig"),
        CLSID("clsid"),
        USHORT("ver_minor"),
        USHORT("ver_major"),
        USHORT("byte_order"),
        USHORT("sect_shift"),
        USHORT("mini_sect_shift"),
        Bytes(6, "rsvd"),
        FSINDEX("dir_count"),
        FSINDEX("fat_count"),
        SECT("dir_sect"),
        DFSIGNATURE("trans_num"),
        ULONG("mini_stream_cutoff"),
        SECT("mini_fat_sect"),
        FSINDEX("mini_fat_count"),
        SECT("di_fat_sect"),
        FSINDEX("di_fat_count"),
        Array(109, SECT(), "di_fat")
    ]
# end class Header

class DirEntry(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Bytes(64, "name"),
        WORD("name_size"),
        BYTE("type"),
        BYTE("color"),
        SID("left_sid"),
        SID("right_sid"),
        SID("child_sid"),
        CLSID("clsid"),
        DWORD("state"),
        TIME_T("btime"),
        TIME_T("mtime"),
        SECT("first_sect"),
        ULONGLONG("size"),
    ]
# end class DirEntry

class FATEntry(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("entry")
    ]
# end class FATEntry

class MiniFATEntry(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("entry")
    ]
# end class MiniFATEntry

class DIFATEntry(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("entry")
    ]
# end class DIFATEntry
