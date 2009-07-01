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

from lf.struct.consts import LITTLE_ENDIAN
from lf.struct.datastruct import DataStruct_LE
from lf.struct.datatype import Bytes

from lf.windows.structs import FILETIME, GUID, CLSID, DECIMAL
from lf.windows.types import (
    WORD, DWORD, BYTE, INT8, INT16, REAL, DOUBLE, DATE, CURRENCY, INT32, INT64,
    UINT32, UINT64, VARIANT_BOOL, UINT8, UINT16
)

from lf.windows.ole.propertyset.types import PropertyType

__docformat__ = "restructuredtext en"
__all__ = [
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

class FMTID(GUID):
    pass
# end class FMTID

class FormatIDOffset(DataStruct_LE):
    fields = [
        FMTID("fmtid"),
        DWORD("offset")
    ]
# end class FormatIDOffset

class PropertySetStreamHeader(DataStruct_LE):
    fields = [
        WORD("byte_order"),
        WORD("version"),
        DWORD("sys_id"),
        CLSID("clsid"),
        DWORD("prop_set_count"),
        FMTID("fmtid0"),
        DWORD("offset0")
    ]
# end class PropertySetStreamHeader

class PropertySetHeader(DataStruct_LE):
    fields = [
        DWORD("size"),
        DWORD("prop_count")
    ]
# end class PropertySetHeader

class PropertyIDOffset(DataStruct_LE):
    fields = [
        DWORD("p_id"),
        DWORD("offset")
    ]
# end class PropertyIDOffset

class TypedPropertyValueHeader(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad")
    ]
# end class TypedPropertyValueHeader

class VT_I2(DataStruct_LE):
    fields = [
        INT16("value"),
        Bytes(2, "pad")
    ]
# end class VT_I2

class VT_BOOL(DataStruct_LE):
    fields = [
        VARIANT_BOOL("value"),
        Bytes(2, "pad")
    ]
# end class VT_BOOL

class VT_I1(DataStruct_LE):
    fields = [
        INT8("value"),
        Bytes(3, "pad")
    ]
# end class VT_I1

class VT_UI1(DataStruct_LE):
    fields = [
        UINT8("value"),
        Bytes(3, "pad")
    ]
# end class VT_UI1

class VT_UI2(DataStruct_LE):
    fields = [
        UINT16("value"),
        Bytes(2, "pad")
    ]
# end class VT_UI2

class ClipboardDataHeader(DataStruct_LE):
    fields = [
        DWORD("size"),
        DWORD("format")
    ]
# end class ClipboardDataHeader

class ArrayDimension(DataStruct_LE):
    fields = [
        DWORD("size"),
        INT32("index_offset")
    ]
# end class ArrayDimension

class ArrayHeader(DataStruct_LE):
    fields = [
        PropertyType("p_type"),
        DWORD("dim_count")
    ]
# end class ArrayHeader

class DictionaryEntryHeader(DataStruct_LE):
    fields = [
        DWORD("p_id"),
        DWORD("length")
    ]
# end class DictionaryEntryHeader


# Convenience structures
class TypedPropertyValue_VT_I2(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad1"),
        INT16("value"),
        Bytes(2, "pad2")
    ]
# end class TypedPropertyValue_VT_I2

class TypedPropertyValue_VT_I4(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        INT32("value")
    ]
# end class TypedPropertyValue_VT_I4

class TypedPropertyValue_VT_R4(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        REAL("value")
    ]
# end class TypedPropertyValue_VT_R4

class TypedPropertyValue_VT_R8(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        DOUBLE("value")
    ]
# end class TypedPropertyValue_VT_R8

class TypedPropertyValue_VT_CY(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        INT64("value")
    ]
# end class TypedPropertyValue_VT_CY

class TypedPropertyValue_VT_DATE(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        DATE("value")
    ]
# end class TypedPropertyValue_VT_DATE

class TypedPropertyValue_VT_ERROR(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        UINT32("value")
    ]
# end class TypedPropertyValue_VT_ERROR

class TypedPropertyValue_VT_BOOL(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad1"),
        VARIANT_BOOL("value"),
        Bytes(2, "pad2")
    ]
# end class TypedPropertyValue_VT_BOOL

class TypedPropertyValue_VT_DECIMAL(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        DECIMAL("value")
    ]
# end class TypedPropertyValue_VT_DECIMAL

class TypedPropertyValue_VT_I1(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad1"),
        INT8("value"),
        Bytes(3, "pad2")
    ]
# end class TypedPropertyValue_VT_I1

class TypedPropertyValue_VT_UI1(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad1"),
        UINT8("value"),
        Bytes(3, "pad2")
    ]
# end class TypedPropertyValue_VT_UI1

class TypedPropertyValue_VT_UI2(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad1"),
        UINT16("value"),
        Bytes(2, "pad2")
    ]
# end class TypedPropertyValue_VT_UI2

class TypedPropertyValue_VT_UI4(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        UINT32("value")
    ]
# end class TypedPropertyValue_VT_UI4

class TypedPropertyValue_VT_I8(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        INT64("value")
    ]
# end class TypedPropertyValue_VT_I8

class TypedPropertyValue_VT_UI8(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        UINT64("value")
    ]
# end class TypedPropertyValue_VT_UI8

class TypedPropertyValue_VT_INT(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        INT32("value")
    ]
# end class TypedPropertyValue_VT_INT

class TypedPropertyValue_VT_UINT(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        UINT32("value")
    ]
# end class TypedPropertyValue_VT_UINT

class TypedPropertyValue_VT_FILETIME(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        FILETIME("value")
    ]
# end class TypedPropertyValue_VT_FILETIME

class TypedPropertyValue_VT_CLSID(DataStruct_LE):
    fields = [
        UINT16("p_type"),
        Bytes(2, "pad"),
        CLSID("value")
    ]
# end class TypedPropertyValue_VT_CLSID


# Data structures beyond your standard property set types

class HyperlinkHeader(DataStruct_LE):
    fields = [
        TypedPropertyValue_VT_I4("hash"),
        TypedPropertyValue_VT_I4("app"),
        TypedPropertyValue_VT_I4("office_art"),
        TypedPropertyValue_VT_I4("info")
    ]
# end class HyperlinkHeader
