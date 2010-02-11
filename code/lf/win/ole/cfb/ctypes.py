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

"""Convenience ctypes classes for working with OLE structured storage files."""

# local imports
from lf.win.ole.cfb.dtypes import (
    Header, DirEntry, FATEntry, MiniFATEntry, DIFATEntry
)

__docformat__ = "restructuredtext en"
__all__ = [
    "header", "dir_entry", "fat_entry", "mini_fat_entry", "di_fat_entry"
]

header = Header._ctype_
dir_entry = DirEntry._ctype_
fat_entry = FATEntry._ctype_.__ctype_le__
mini_fat_entry = MiniFATEntry._ctype_.__ctype_le__
di_fat_entry = DIFATEntry._ctype_.__ctype_le__
