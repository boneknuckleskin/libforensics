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

"""Data types for OLE structured storage files."""

# local imports
from lf.dtypes import LERecord, raw
from lf.win.dtypes import (
    ULONG, USHORT, WORD, SHORT, BYTE, DWORD, ULONGLONG, FILETIME, CLSID_LE,
    FILETIME_LE
)

__docformat__ = "restructuredtext en"
__all__ = [
    "OFFSET", "SECT", "FSINDEX", "FSOFFSET", "DFSIGNATURE", "DFPROPTYPE",
    "SID", "TIME_T", "Header", "DirEntry", "FATEntry", "MiniFATEntry",
    "DIFATEntry"
]

class OFFSET(SHORT):
    pass
# end class OFFSET

class SECT(ULONG):
    pass
# end class SECT

class FSINDEX(ULONG):
    pass
# end class FSINDEX

class FSOFFSET(USHORT):
    pass
# end class FSOFFSET

class DFSIGNATURE(ULONG):
    pass
# end class DFSIGNATURE

class DFPROPTYPE(WORD):
    pass
# end class DFPROPTYPE

class SID(ULONG):
    pass
# end class SID

class TIME_T(FILETIME):
    pass
# end class TIME_T

class Header(LERecord):
    sig = raw(8)
    clsid = CLSID_LE
    ver_minor = USHORT
    ver_major = USHORT
    byte_order = USHORT
    sect_shift = USHORT
    mini_sect_shift = USHORT
    rsvd = raw(6)
    dir_sect_count = FSINDEX
    fat_sect_count = FSINDEX
    dir_sect_offset = SECT
    trans_num = DFSIGNATURE
    mini_stream_cutoff = ULONG
    mini_fat_sect_offset = SECT
    mini_fat_sect_count = FSINDEX
    di_fat_sect_offset = SECT
    di_fat_sect_count = FSINDEX
    di_fat = [SECT] * 109
# end class Header

class DirEntry(LERecord):
    name = raw(64)
    name_size = WORD
    type = BYTE
    color = BYTE
    left_sid = SID
    right_sid = SID
    child_sid = SID
    clsid = CLSID_LE
    state = DWORD
    btime = FILETIME_LE
    mtime = FILETIME_LE
    stream_sect_offset = SECT
    stream_size = ULONGLONG
# end class DirEntry

class FATEntry(DWORD):
    pass
# end class FATEntry

class MiniFATEntry(DWORD):
    pass
# end class MiniFATEntry

class DIFATEntry(DWORD):
    pass
# end class DIFATEntry
