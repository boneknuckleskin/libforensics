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

"""Ctypes classes for the record data types in lf.win.con.dtypes"""

# local imports
from lf.win.con.dtypes import COORD_LE, COORD_BE

__docformat__ = "restructuredtext en"
__all__ = [
    "coord_le", "coord_be"
]

coord_le = COORD_LE._ctype_
coord_be = COORD_BE._ctype_
