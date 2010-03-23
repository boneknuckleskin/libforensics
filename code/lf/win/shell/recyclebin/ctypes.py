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

"""Ctypes for the data types in lf.win.shell.recyclebin.dtypes"""

# local imports
from lf.win.shell.recyclebin.dtypes import INFO2Header, INFO2Item

__docformat__ = "restructuredtext en"
__all__ = [
    "info2_header", "info2_item"
]

info2_header = INFO2Header._ctype_
info2_item = INFO2Item._ctype_
