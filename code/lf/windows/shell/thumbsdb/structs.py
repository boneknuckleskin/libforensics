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
Data structures to work with thumbs.db files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "CatalogHeader", "CatalogEntryHeader", "EntryHeader", "EntryHeaderOld"
]

from lf.datastruct import raw, DataStruct_LE
from lf.windows.types import UINT32, FILETIME

class CatalogHeader(DataStruct_LE):
    fields = [
        raw("unknown", 2),  # Header size?  Identifier?
        raw("unknown", 2),  # Appears to be a version number?
        UINT32("count"),
        UINT32("width"),
        UINT32("height")
    ]
# end class CatalogHeader

class CatalogEntryHeader(DataStruct_LE):
    fields = [
        UINT32("size"), # Size of the entry
        UINT32("index"),
        FILETIME("mtime")
    ]
# end class CatalogEntryHeader

class EntryHeader(DataStruct_LE):
    fields = [
        raw("unknown", 4),  # Perhaps header length?
        raw("unknown", 4),  # Perhaps an identifier?
        UINT32("size") # Size of the data
    ]
# end class EntryHeader

# For older style thumbs.db files
class EntryHeaderOld(DataStruct_LE):
    fields = [
        raw("unknown", 4),  # Identifier?
        UINT32("size"),
        raw("unknown", 4),  # width?
        raw("unknown", 4),  # height?
    ]
# end class EntryHeaderOld
