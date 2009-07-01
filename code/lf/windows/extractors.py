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
Convenience class that contains extractors for the microsoft_structs module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)

"""

from lf.struct.consts import LITTLE_ENDIAN, BIG_ENDIAN
from lf.struct.datastruct import DataStruct
from lf.struct.extract import extractor_factory as factory
from lf.windows.structs import GUID, CLSID, DECIMAL, FILETIME

__docformat__ = "restructuredtext en"
__all__ = [
    "guid_le", "clsid_le", "decimal_le", "filetime_le", "guid_be", "clsid_be",
    "decimal_be", "filetime_be"
]

class _GUID_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ GUID("value") ]
# end class _GUID_LE

class _GUID_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ GUID("value") ]
# end class _GUID_BE

class _CLSID_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ CLSID("value") ]
# end class _CLSID_LE

class _CLSID_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ CLSID("value") ]
# end class _CLSID_BE

class _DECIMAL_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ DECIMAL("value") ]
# end class _DECIMAL_LE

class _DECIMAL_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ DECIMAL("value") ]
# end class _DECIMAL_BE

class _FILETIME_LE(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [ FILETIME("value") ]
# end class _FILETIME_LE

class _FILETIME_BE(DataStruct):
    byte_order = BIG_ENDIAN
    fields = [ FILETIME("value") ]
# end class _FILETIME_BE

guid_le = factory.make(_GUID_LE())
guid_be = factory.make(_GUID_BE())
clsid_le = factory.make(_CLSID_LE())
clsid_be = factory.make(_CLSID_BE())
decimal_le = factory.make(_DECIMAL_LE())
decimal_be = factory.make(_DECIMAL_BE())
filetime_le = factory.make(_FILETIME_LE())
filetime_be = factory.make(_FILETIME_BE())
