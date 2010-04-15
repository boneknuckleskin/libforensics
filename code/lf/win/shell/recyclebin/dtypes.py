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

"""Data structures to read recycle bin INFO2 files."""

# local imports
from lf.dtypes import raw, LERecord
from lf.win.dtypes import DWORD, FILETIME_LE

__docformat__ = "restructuredtext en"
__all__ = [
    "INFO2Header", "INFO2Item"
]

class INFO2Header(LERecord):
    version = DWORD
    unknown1 = DWORD
    unknown2 = DWORD  # Number of entries in file?
    item_size = DWORD
    unknown3 = DWORD  # Varies per file, a timestamp?
# end class Header

class INFO2Item(LERecord):
    name_asc = raw(260)
    id = DWORD  # DcXX (this is the XX)
    drive_num = DWORD  # 0 = A, 1 = B, 2 = C, ...
    dtime = FILETIME_LE
    file_size = DWORD
    name_uni = raw(520)
# end class Item
