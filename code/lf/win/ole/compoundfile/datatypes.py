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
Data types for OLE structured storage files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.datatype import raw, array, LERecord
from lf.windows.datatypes import (
    ULONG, USHORT, WORD, SHORT, BYTE, DWORD, ULONGLONG, FILETIME, CLSID, GUID
)

__docformat__ = "restructuredtext en"
__all__ = [
    "OFFSET", "SECT", "FSINDEX", "FSOFFSET", "DFSIGNATURE", "DFPROPTYPE",
    "SID",

    "TIME_T", "Header", "DirEntry"
]

from lf.windows.datatypes import (
    ULONG, USHORT, WORD, SHORT
)

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
    clsid = CLSID
    ver_minor = USHORT
    ver_major = USHORT
    byte_order = USHORT
    sect_shift = USHORT
    mini_sect_shift = USHORT
    rsvd = raw(6)
    dir_count = FSINDEX
    fat_count = FSINDEX
    dir_sect = SECT
    trans_num = DFSIGNATURE
    mini_stream_cutoff = ULONG
    mini_fat_sect = SECT
    mini_fat_count = FSINDEX
    di_fat_sect = SECT
    di_fat_count = FSINDEX
    di_fat = array(SECT, 109)
# end class Header

class DirEntry(LERecord):
    name = raw(64)
    name_size = WORD
    type = BYTE
    color = BYTE
    left_sid = SID
    right_sid = SID
    child_sid = SID
    clsid = CLSID
    state = DWORD
    btime = TIME_T
    mtime = TIME_T
    first_sect = SECT
    size = ULONGLONG
# end class DirEntry

class FATEntry(LERecord):
    entry = DWORD
# end class FATEntry

class MiniFATEntry(LERecord):
    entry = DWORD
# end class MiniFATEntry

class DIFATEntry(LERecord):
    entry = DWORD
# end class DIFATEntry
