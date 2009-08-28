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
Data structures for Microsoft OLE Property Sets.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.datatype import raw, LERecord

from lf.windows.datatypes import (
    WORD, DWORD, BYTE, INT8, INT16, REAL, DOUBLE, DATE, CURRENCY, INT32, INT64,
    UINT32, UINT64, VARIANT_BOOL, UINT8, UINT16, FILETIME, UINT,
    GUID, CLSID, DECIMAL
)

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertyIdentifier", "PropertyType",

    "FMTID", "FormatIDOffset", "PropertySetStreamHeader", "PropertySetHeader",
    "PropertyIDOffset", "TypedPropertyValueHeader", "VT_I2", "VT_BOOL", "VT_I1",
    "VT_U1", "VT_UI2", "ClipboardDataHeader", "ArrayDimension", "ArrayHeader",
    "DictionaryEntryHeader",
    "TypedPropertyValue_VT_I2", "TypedPropertyValue_VT_I4",
    "TypedPropertyValue_VT_R4", "TypedPropertyValue_VT_R8",
    "TypedPropertyValue_VT_CY", "TypedPropertyValue_VT_DATE",
    "TypedPropertyValue_VT_ERROR", "TypedPropertyValue_VT_BOOL",
    "TypedPropertyValue_VT_DECIMAL", "TypedPropertyValue_VT_I1",
    "TypedPropertyValue_VT_UI1", "TypedPropertyValue_VT_UI2",
    "TypedPropertyValue_VT_UI4", "TypedPropertyValue_VT_I8",
    "TypedPropertyValue_VT_UI8", "TypedPropertyValue_VT_INT",
    "TypedPropertyValue_VT_UINT", "TypedPropertyValue_VT_FILETIME",
    "TypedPropertyValue_VT_CLSID",
    "HyperlinkHeader"
]

class PropertyIdentifier(UINT):
    pass
# end class PropertyIdentifier

class PropertyType(UINT):
    pass
# end class PropertyType

class FMTID(GUID):
    pass
# end class FMTID

class FormatIDOffset(LERecord):
    fmtid = FMTID
    offset = DWORD
# end class FormatIDOffset

class PropertySetStreamHeader(LERecord):
    byte_order = WORD
    version = WORD
    sys_id = DWORD
    clsid = CLSID
    prop_set_count = DWORD
    fmtid0 = FMTID
    offset0 = DWORD
# end class PropertySetStreamHeader

class PropertySetHeader(LERecord):
    size = DWORD
    prop_count = DWORD
# end class PropertySetHeader

class PropertyIDOffset(LERecord):
    p_id = DWORD
    offset = DWORD
# end class PropertyIDOffset

class TypedPropertyValueHeader(LERecord):
    p_type = UINT16
    pad = raw(2)
# end class TypedPropertyValueHeader

class VT_I2(LERecord):
    value = INT16
    pad = raw(2)
# end class VT_I2

class VT_BOOL(LERecord):
    value = VARIANT_BOOL
    pad = raw(2)
# end class VT_BOOL

class VT_I1(LERecord):
    value = INT8
    pad = raw(3)
# end class VT_I1

class VT_UI1(LERecord):
    value = UINT8
    pad = raw(3)
# end class VT_UI1

class VT_UI2(LERecord):
    value = UINT16
    pad = raw(2)
# end class VT_UI2

class ClipboardDataHeader(LERecord):
    size = DWORD
    format = DWORD
# end class ClipboardDataHeader

class ArrayDimension(LERecord):
    size = DWORD
    index_offset = INT32
# end class ArrayDimension

class ArrayHeader(LERecord):
    p_type = PropertyType
    dim_count = DWORD
# end class ArrayHeader

class DictionaryEntryHeader(LERecord):
    p_id = DWORD
    length = DWORD
# end class DictionaryEntryHeader


# Convenience structures
class TPVHeader(LERecord):
    header = TypedPropertyValueHeader
# end class TPVHeader

class TypedPropertyValue_VT_I2(TPVHeader):
    value = INT16
    pad = raw(2)
# end class TypedPropertyValue_VT_I2

class TypedPropertyValue_VT_I4(TPVHeader):
    value = INT32
# end class TypedPropertyValue_VT_I4

class TypedPropertyValue_VT_R4(TPVHeader):
    value = REAL
# end class TypedPropertyValue_VT_R4

class TypedPropertyValue_VT_R8(TPVHeader):
    value = DOUBLE
# end class TypedPropertyValue_VT_R8

class TypedPropertyValue_VT_CY(TPVHeader):
    value = INT64
# end class TypedPropertyValue_VT_CY

class TypedPropertyValue_VT_DATE(TPVHeader):
    value = DATE
# end class TypedPropertyValue_VT_DATE

class TypedPropertyValue_VT_ERROR(TPVHeader):
    value = UINT32
# end class TypedPropertyValue_VT_ERROR

class TypedPropertyValue_VT_BOOL(TPVHeader):
    value = VARIANT_BOOL
    pad = raw(2)
# end class TypedPropertyValue_VT_BOOL

class TypedPropertyValue_VT_DECIMAL(TPVHeader):
    value = DECIMAL
# end class TypedPropertyValue_VT_DECIMAL

class TypedPropertyValue_VT_I1(TPVHeader):
    value = INT8
    pad = raw(3)
# end class TypedPropertyValue_VT_I1

class TypedPropertyValue_VT_UI1(TPVHeader):
    value = UINT8
    pad = raw(3)
# end class TypedPropertyValue_VT_UI1

class TypedPropertyValue_VT_UI2(TPVHeader):
    value = UINT16
    pad = raw(2)
# end class TypedPropertyValue_VT_UI2

class TypedPropertyValue_VT_UI4(TPVHeader):
    value = UINT32
# end class TypedPropertyValue_VT_UI4

class TypedPropertyValue_VT_I8(TPVHeader):
    value = INT64
# end class TypedPropertyValue_VT_I8

class TypedPropertyValue_VT_UI8(TPVHeader):
    value = UINT64
# end class TypedPropertyValue_VT_UI8

class TypedPropertyValue_VT_INT(TPVHeader):
    value = INT32
# end class TypedPropertyValue_VT_INT

class TypedPropertyValue_VT_UINT(TPVHeader):
    value = UINT32
# end class TypedPropertyValue_VT_UINT

class TypedPropertyValue_VT_FILETIME(TPVHeader):
    value = FILETIME
# end class TypedPropertyValue_VT_FILETIME

class TypedPropertyValue_VT_CLSID(TPVHeader):
    value = CLSID
# end class TypedPropertyValue_VT_CLSID


# Data structures beyond your standard property set types

class HyperlinkHeader(LERecord):
    hash = TypedPropertyValue_VT_I4
    app = TypedPropertyValue_VT_I4
    office_art = TypedPropertyValue_VT_I4
    info = TypedPropertyValue_VT_I4
# end class HyperlinkHeader
