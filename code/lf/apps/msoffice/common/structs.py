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

from lf.struct.datastruct import DataStruct_LE
from lf.struct.datatype import Bytes

from lf.windows.structs import FILETIME
from lf.windows.types import (
    WORD, DWORD, BYTE, INT8, INT16, REAL, DOUBLE, DATE, CURRENCY, INT32, INT64,
    UINT32, UINT64, VARIANT_BOOL, UINT8, UINT16
)

from lf.windows.ole.propertyset.structs import TypedPropertyValue_VT_I4

# Related to Visual Basic for Applications
class DigSigInfoSerializedHeader(DataStruct_LE):
    fields = [
        UINT32("sig_size"),
        UINT32("sig_offset"),
        UINT32("sign_size"),
        UINT32("sign_offset"),
        UINT32("proj_size"),
        UINT32("proj_offset"),
        Bytes(4, "rsvd"),
        UINT32("timestamp_size"),
        UINT32("timestamp_offset")
    ]
# end class DigSigInfoSerializedHeader

class DigSigBlobHeader(DataStruct_LE):
    fields = [
        UINT32("sig_info_size"),
        UINT32("sig_info_offset"),
        DigSigInfoSerializedHeader("sig_info_header")
    ]
# end class DigSigBlobHeader

class WordSigBlobHeader(DataStruct_LE):
    fields = [
        UINT16("half_size"),
        UINT32("sig_info_size"),
        UINT32("sig_info_offset"),
        DigSigInfoSerializedHeader("sig_info_header")
    ]
# end class WordSigBlobHeader

# Stuff property set storage
class PropertySetSystemIdentifier(DataStruct_LE):
    fields = [
        UINT8("os_major"),
        UINT8("os_minor"),
        UINT16("os_type")
    ]
# end class PropertySetSystemIdentifier

class VtThumbnailValueHeader(DataStruct_LE):
    fields = [
        UINT32("size"),
        UINT32("tag"),
        UINT32("format"),
    ]
# end class VtThumbnailValueHeader

class VtThumbnailHeader(DataStruct_LE):
    fields = [
        UINT16("thumb_type"),
        Bytes(2, "pad"),
        VtThumbnailValueHeader("thumbnail_header")
    ]
# end class VtThumbnailHeader

class VtStringHeader(DataStruct_LE):
    fields = [
        UINT16("str_type"),
        UINT16("pad")
    ]
# end class VtStringHeader

class VtUnalignedStringHeader(VtStringHeader):
    pass
# end class VtUnalignedStringHeader

class VtHyperlinkHeader(DataStruct_LE):
    fields = [
        TypedPropertyValue_VT_I4("hash"),
        TypedPropertyValue_VT_I4("app"),
        TypedPropertyValue_VT_I4("office_art"),
        TypedPropertyValue_VT_I4("info")
    ]
# end class VtHyperlinkHeader
