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
Data structures to read recycle bin files (INFO2).

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

from lf.datastruct import raw, DataStruct_LE
from lf.windows.types import DWORD, FILETIME

class Header(DataStruct_LE):
    fields = [
        DWORD("unknown"), # Perhaps version?
        DWORD("unknown"),
        DWORD("count"), # Number of entries in file
        DWORD("item_size"), # Size of an item
        DWORD("unknown") # Varies per file, a timestamp?
    ]
# end class Header

class Item(DataStruct_LE):
    fields = [
        raw("name_asc", 260),
        DWORD("index"), # DcXX (this is the XX)
        DWORD("drive_num"), # 0 = A, 1 = B, 2 = C, ...
        FILETIME("dtime"),
        DWORD("phys_size"),
        raw("name_uni", 520)
    ]
# end class Item
