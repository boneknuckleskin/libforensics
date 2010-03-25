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

"""Data types to read thumbs.db files."""

# local imports
from lf.dtypes import raw, LERecord
from lf.win.dtypes import UINT32, FILETIME_LE

__docformat__ = "restructuredtext en"
__all__ = [
    "CatalogHeader", "CatalogEntryHeader", "EntryHeader", "EntryHeaderOld"
]

class CatalogHeader(LERecord):
    unknown1 = raw(2)  # Header Size?  Identifier?
    unknown2 = raw(2)  # Appears to be a version number?
    item_count = UINT32
    width = UINT32
    height = UINT32
# end class CatalogHeader

class CatalogEntryHeader(LERecord):
    size = UINT32  # Size of the entry
    id = UINT32
    mtime = FILETIME_LE
# end class CatalogEntryHeader

class EntryHeader(LERecord):
    unknown1 = raw(4)  # header length?
    unknown2 = raw(4)  # identifier?
    size = UINT32  # Size of the data
# end class EntryHeader

# For older style thumbs.db files
class EntryHeaderOld(LERecord):
    unknown1 = raw(4)  # identifier?
    size = UINT32
    unknown2 = raw(4)  # width?
    unknown3 = raw(4)  # height?
# end class EntryHeaderOld
