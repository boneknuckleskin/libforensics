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

from lf.datastruct import raw, array, DataStruct_LE
from lf.windows.types import (
    ULONG, USHORT, BYTE, WORD, DWORD, ULONGLONG, FILETIME
)
from lf.windows.structs import CLSID, GUID
from lf.windows.ole.compoundfile.types import (
    OFFSET, SECT, FSINDEX, FSOFFSET, DFSIGNATURE, DFPROPTYPE, SID
)

class TIME_T(FILETIME):
    pass
# end class TIME_T

class Header(DataStruct_LE):
    fields = [
        raw("sig", 8),
        CLSID("clsid"),
        USHORT("ver_minor"),
        USHORT("ver_major"),
        USHORT("byte_order"),
        USHORT("sect_shift"),
        USHORT("mini_sect_shift"),
        raw("rsvd", 6),
        FSINDEX("dir_count"),
        FSINDEX("fat_count"),
        SECT("dir_sect"),
        DFSIGNATURE("trans_num"),
        ULONG("mini_stream_cutoff"),
        SECT("mini_fat_sect"),
        FSINDEX("mini_fat_count"),
        SECT("di_fat_sect"),
        FSINDEX("di_fat_count"),
        array("di_fat", SECT(""), 109)
    ]
# end class Header

class DirEntry(DataStruct_LE):
    fields = [
        raw("name", 64),
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

class FATEntry(DataStruct_LE):
    fields = [
        DWORD("entry")
    ]
# end class FATEntry

class MiniFATEntry(DataStruct_LE):
    fields = [
        DWORD("entry")
    ]
# end class MiniFATEntry

class DIFATEntry(DataStruct_LE):
    fields = [
        DWORD("entry")
    ]
# end class DIFATEntry
