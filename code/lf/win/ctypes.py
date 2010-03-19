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

"""Ctypes classes for the record data types in lf.win.dtypes"""

# local imports
from lf.win import dtypes

__docformat__ = "restructuredtext en"
__all__ = [
    "GUID_LE", "GUID_BE", "CLSID_LE", "CLSID_BE", "LCID_LE", "LCID_BE",
    "FILETIME_LE", "FILETIME_BE", "HRESULT_LE", "HRESULT_BE",

    "guid_le", "guid_be", "clsid_le", "clsid_be", "lcid_le", "lcid_be",
    "filetime_le", "filetime_be", "hresult_le", "hresult_be", "decimal_le",
    "decimal_le", "decimal_be"
]

guid_le = dtypes.GUID_LE._ctype_
guid_be = dtypes.GUID_BE._ctype_
GUID_LE = guid_le
GUID_BE = guid_be

clsid_le = dtypes.CLSID_LE._ctype_
clsid_be = dtypes.CLSID_BE._ctype_
CLSID_LE = clsid_le
CLSID_BE = clsid_be

lcid_le = dtypes.LCID_LE._ctype_
lcid_be = dtypes.LCID_BE._ctype_
LCID_LE = lcid_le
LCID_BE = lcid_be

filetime_le = dtypes.FILETIME_LE._ctype_
filetime_be = dtypes.FILETIME_BE._ctype_
FILETIME_LE = filetime_le
FILETIME_BE = filetime_be

hresult_le = dtypes.HRESULT_LE._ctype_
hresult_be = dtypes.HRESULT_BE._ctype_
HRESULT_LE = hresult_le
HRESULT_BE = hresult_be

decimal_le = dtypes.DECIMAL_LE._ctype_
decimal_be = dtypes.DECIMAL_BE._ctype_
