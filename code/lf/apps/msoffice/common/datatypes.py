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
Common data structures for Microsoft Office applications.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

from lf.datatype import raw, LERecord
from lf.windows.datatypes import (
    WORD, DWORD, BYTE, INT8, INT16, REAL, DOUBLE, DATE, CURRENCY, INT32, INT64,
    UINT32, UINT64, VARIANT_BOOL, UINT8, UINT16
)

from lf.windows.ole.propertyset.datatypes import TypedPropertyValue_VT_I4

# Related to Visual Basic for Applications
class DigSigInfoSerializedHeader(LERecord):
    sig_size = UINT32
    sig_offset = UINT32
    sign_size = UINT32
    proj_size = UINT32
    proj_offset = UINT32
    rsvd = raw(4)
    timestamp_size = UINT32
    timestamp_offset = UINT32
# end class DigSigInfoSerializedHeader

class DigSigBlobHeader(LERecord):
    sig_info_size = UINT32
    sig_info_offset = UINT32
    sig_info_header = DigSigInfoSerializedHeader
# end class DigSigBlobHeader

class WordSigBlobHeader(LERecord):
    half_size = UINT16
    sig_info_size = UINT32
    sig_info_offset = UINT32
    sig_info_header = DigSigInfoSerializedHeader
# end class WordSigBlobHeader

# Stuff property set storage
class PropertySetSystemIdentifier(LERecord):
    os_major = UINT8
    os_minor = UINT8
    os_type = UINT16
# end class PropertySetSystemIdentifier

class VtThumbnailValueHeader(LERecord):
    size = UINT32
    tag = UINT32
    format = UINT32
# end class VtThumbnailValueHeader

class VtThumbnailHeader(LERecord):
    thumb_type = UINT16
    pad = raw(2)
    thumbnail_header = VtThumbnailValueHeader
# end class VtThumbnailHeader

class VtStringHeader(LERecord):
    str_type = UINT16
    pad = UINT16
# end class VtStringHeader

class VtUnalignedStringHeader(VtStringHeader):
    pass
# end class VtUnalignedStringHeader

class VtHyperlinkHeader(LERecord):
    hash = TypedPropertyValue_VT_I4
    app = TypedPropertyValue_VT_I4
    office_art = TypedPropertyValue_VT_I4
    info = TypedPropertyValue_VT_I4
# end class VtHyperlinkHeader
