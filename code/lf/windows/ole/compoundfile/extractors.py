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
Extractors for OLE structured storage files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "header", "dir_entry", "fat_entry", "mini_fat_entry", "di_fat_entry"
]

from lf.datatype import Extractor
from lf.windows.ole.compoundfile.datatypes import (
    Header, DirEntry, FATEntry, MiniFATEntry, DIFATEntry
)

header = Extractor(Header)
dir_entry = Extractor(DirEntry)
fat_entry = Extractor(FATEntry)
mini_fat_entry = Extractor(MiniFATEntry)
di_fat_entry = Extractor(DIFATEntry)
