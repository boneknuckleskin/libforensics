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

"""Common Microsoft Office ctypes."""

# local imports
from lf.apps.msoffice.shared.dtypes import (
    PropertySetSystemIdentifier,
    VtHyperlinkHeader, DigSigInfoSerializedHeader, DigSigBlobHeader
)

__docformat__ = "restructuredtext en"
__all__ = [
    "property_set_system_identifier",
    "vt_hyperlink_header", "dig_sig_info_serialized_header",
    "dig_sig_blob_header"
]

property_set_system_identifier = PropertySetSystemIdentifier._ctype_
vt_hyperlink_header = VtHyperlinkHeader._ctype_
dig_sig_info_serialized_header = DigSigInfoSerializedHeader._ctype_
dig_sig_blob_header = DigSigBlobHeader._ctype_
