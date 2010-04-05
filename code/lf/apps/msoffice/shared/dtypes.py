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

"""Common data types for Microsoft Office artifacts."""

# local imports
from lf.dtypes import LERecord
from lf.win.dtypes import UINT8, UINT16, UINT32
from lf.win.ole.ps.dtypes import TypedPropertyValue_VT_I4

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertySetSystemIdentifier",

    "VtHyperlinkHeader", "DigSigInfoSerializedHeader", "DigSigBlobHeader"
]

class PropertySetSystemIdentifier(LERecord):
    os_ver_major = UINT8
    os_ver_minor = UINT8
    os_type = UINT16
# end class PropertySetSystemIdentifier

class VtHyperlinkHeader(LERecord):
    hash = TypedPropertyValue_VT_I4
    app = TypedPropertyValue_VT_I4
    office_art = TypedPropertyValue_VT_I4
    info = TypedPropertyValue_VT_I4
# end class VtHyperlinkHeader

class DigSigInfoSerializedHeader(LERecord):
    sig_size = UINT32
    sig_offset = UINT32
    cert_store_size = UINT32
    cert_store_offset = UINT32
    proj_name_size = UINT32
    proj_name_offset = UINT32
    timestamp = UINT32
    timestamp_buf_size = UINT32
    timestamp_buf_offset = UINT32
# end class DigInfoSerializedHeader

class DigSigBlobHeader(LERecord):
    data_size = UINT32
    sig_info_offset = UINT32
# end class DigSigBlobHeader
