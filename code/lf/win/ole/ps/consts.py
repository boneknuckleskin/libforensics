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

"""Constants for OLE Property Sets."""

# stdlib imports
from uuid import UUID

__docformat__ = "restructuredtext en"
__all__ = [
    "FMTID_SummaryInformation", "FMTID_DocSummaryInformation",
    "FMTID_UserDefinedProperties", "FMTID_GlobalInfo", "FMTID_ImageContents",
    "FMTID_ImageInfo", "FMTID_PropertyBag",

    "DICTIONARY_PROPERTY_IDENTIFIER", "CODEPAGE_PROPERTY_IDENTIFIER",
    "LOCALE_PROPERTY_IDENTIFIER", "BEHAVIOR_PROPERTY_IDENTIFIER",
    "MAX_NORMAL_PROPERTY_IDENTIFIER",

    "PropertyType"
]

FMTID_SummaryInformation = UUID("{F29F85E0-4FF9-1068-AB91-08002B27B3D9}")
FMTID_DocSummaryInformation = UUID("{D5CDD502-2E9C-101B-9397-08002B2CF9AE}")
FMTID_UserDefinedProperties = UUID("{D5CDD505-2E9C-101B-9397-08002B2CF9AE}")
FMTID_GlobalInfo = UUID("{56616F00-C154-11CE-8553-00AA00A1F95B}")
FMTID_ImageContents = UUID("{56616400-C154-11CE-8553-00AA00A1F95B}")
FMTID_ImageInfo = UUID("{56616500-C154-11CE-8553-00AA00A1F95B}")
FMTID_PropertyBag = UUID("{20001801-5DE6-11D1-8E38-00C04FB9386D}")

DICTIONARY_PROPERTY_IDENTIFIER = 0
CODEPAGE_PROPERTY_IDENTIFIER = 1
LOCALE_PROPERTY_IDENTIFIER = 0x80000000
BEHAVIOR_PROPERTY_IDENTIFIER = 0x80000003
MAX_NORMAL_PROPERTY_IDENTIFIER = 0x7FFFFFFF

PID_DICTIONARY = DICTIONARY_PROPERTY_IDENTIFIER
PID_CODEPAGE = CODEPAGE_PROPERTY_IDENTIFIER
PID_LOCALE = LOCALE_PROPERTY_IDENTIFIER
PID_BEHAVIOR = BEHAVIOR_PROPERTY_IDENTIFIER
PID_MAX_NORMAL = MAX_NORMAL_PROPERTY_IDENTIFIER

class PropertyType():
    """Constants for the PropertyType enum."""

    VT_EMPTY = 0
    VT_NULL = 1
    VT_I2 = 2
    VT_I4 = 3
    VT_R4 = 4
    VT_R8 = 5
    VT_CY = 6
    VT_DATE = 7
    VT_BSTR = 8
    VT_ERROR = 0xA
    VT_BOOL = 0xB
    VT_VARIANT = 0xC
    VT_DECIMAL = 0xE
    VT_I1 = 0x10
    VT_UI1 = 0x11
    VT_UI2 = 0x12
    VT_UI4 = 0x13
    VT_I8 = 0x14
    VT_UI8 = 0x15
    VT_INT = 0x16
    VT_UINT = 0x17
    VT_LPSTR = 0x1E
    VT_LPWSTR = 0x1F
    VT_FILETIME = 0x40
    VT_BLOB = 0x41
    VT_STREAM = 0x42
    VT_STORAGE = 0x43
    VT_STREAMED_OBJECT = 0x44
    VT_STORED_OBJECT = 0x45
    VT_BLOB_OBJECT = 0x46
    VT_CF = 0x47
    VT_CLSID = 0x48
    VT_VERSIONED_STREAM = 0x49
    VT_VECTOR = 0x1000
    VT_ARRAY = 0x2000
# end class PropertyType
