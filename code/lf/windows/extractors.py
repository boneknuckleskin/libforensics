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
Convenience class that contains extractors for the windows.datatypes module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)

"""

from lf.datatype import LERecord, BERecord, Extractor, BIG_ENDIAN
from lf.windows.datatypes import GUID, CLSID, DECIMAL, LCID

__docformat__ = "restructuredtext en"
__all__ = [
    "guid_le", "clsid_le", "decimal_le", "guid_be", "clsid_be", "decimal_be",
    "lcid_le", "lcid_be"
]

class _GUID_LE(GUID):
    pass
# end class _GUID_LE

class _GUID_BE(GUID):
    _byte_order_ = BIG_ENDIAN
# end class _GUID_BE

class _CLSID_LE(CLSID):
    pass
# end class _CLSID_LE

class _CLSID_BE(CLSID):
    _byte_order_ = BIG_ENDIAN
# end class _CLSID_BE

class _DECIMAL_LE(DECIMAL):
    pass
# end class _DECIMAL_LE

class _DECIMAL_BE(DECIMAL):
    _byte_order_ = BIG_ENDIAN
# end class _DECIMAL_BE

class _LCID_BE(LCID):
    _byte_order_ = BIG_ENDIAN
# end class _LCID_BE

guid_le = Extractor(_GUID_LE)
guid_be = Extractor(_GUID_BE)
clsid_le = Extractor(_CLSID_LE)
clsid_be = Extractor(_CLSID_BE)
decimal_le = Extractor(_DECIMAL_LE)
decimal_be = Extractor(_DECIMAL_BE)
lcid_le = Extractor(LCID)
lcid_be = Extractor(_LCID_BE)
