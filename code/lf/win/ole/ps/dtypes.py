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

"""Data types for OLE property sets."""

# local imports
from lf.dtypes import raw, LERecord

from lf.win.dtypes import (
    WORD, DWORD, BYTE, INT8, INT16, REAL, DOUBLE, DATE, CURRENCY, INT32, INT64,
    UINT32, UINT64, VARIANT_BOOL, UINT8, UINT16, FILETIME_LE, UINT,
    GUID_LE, CLSID_LE, DECIMAL_LE, HRESULT_LE
)

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertyIdentifier", "PropertyType",

    "PropertySetStreamHeader", "PropertySetHeader",
    "PropertyIdentifierAndOffset", "DictionaryEntryHeader", "ArrayHeader",
    "ArrayDimension",

    "TypedPropertyValueHeader", "TypedPropertyValue_VT_I2",
    "TypedPropertyValue_VT_R4", "TypedPropertyValue_VT_R8",
    "TypedPropertyValue_VT_CY", "TypedPropertyValue_VT_DATE",
    "TypedPropertyValue_VT_ERROR", "TypedPropertyValue_VT_UI2",
    "TypedPropertyValue_VT_DECIMAL", "TypedPropertyValue_VT_I1",
    "TypedPropertyValue_VT_UI1", "TypedPropertyValue_VT_UI4",
    "TypedPropertyValue_VT_I8", "TypedPropertyValue_VT_UI8",
    "TypedPropertyValue_VT_I4", "TypedPropertyValue_VT_FILETIME",
    "TypedPropertyValue_VT_CLSID"
]

class PropertyIdentifier(UINT):
    pass
# end class PropertyIdentifier

class PropertyType(UINT):
    pass
# end class PropertyType

class FMTID(GUID_LE):
    pass
# end class FMTID

class PropertySetStreamHeader(LERecord):
    byte_order = WORD
    version = WORD
    sys_id = raw(4)
    clsid = CLSID_LE
    property_set_count = DWORD
    fmtid0 = FMTID
    offset0 = DWORD
# end class PropertySetStreamHeader

class PropertySetHeader(LERecord):
    size = DWORD
    pair_count = DWORD
# end class PropertySetHeader

class PropertyIdentifierAndOffset(LERecord):
    pid = DWORD
    offset = DWORD
# end class PropertyIDOffset

class TypedPropertyValueHeader(LERecord):
    type = UINT16
    pad = raw(2)
# end class TypedPropertyValueHeader

class ArrayDimension(LERecord):
    size = DWORD
    index_offset = INT32
# end class ArrayDimension

class ArrayHeader(LERecord):
    scalar_type = PropertyType
    dimension_count = DWORD
# end class ArrayHeader

class DictionaryEntryHeader(LERecord):
    pid = DWORD
    length = DWORD
# end class DictionaryEntryHeader

class TypedPropertyValue_VT_I2(TypedPropertyValueHeader):
    value = INT16
    value_pad = raw(2)
# end class TypedPropertyValue_VT_I2

class TypedPropertyValue_VT_I4(TypedPropertyValueHeader):
    value = INT32
# end class TypedPropertyValue_VT_I4

class TypedPropertyValue_VT_R4(TypedPropertyValueHeader):
    value = REAL
# end class TypedPropertyValue_VT_R4

class TypedPropertyValue_VT_R8(TypedPropertyValueHeader):
    value = DOUBLE
# end class TypedPropertyValue_VT_R8

class TypedPropertyValue_VT_CY(TypedPropertyValueHeader):
    value = INT64
# end class TypedPropertyValue_VT_CY

class TypedPropertyValue_VT_DATE(TypedPropertyValueHeader):
    value = DATE
# end class TypedPropertyValue_VT_DATE

class TypedPropertyValue_VT_ERROR(TypedPropertyValueHeader):
    value = HRESULT_LE
# end class TypedPropertyValue_VT_ERROR

class TypedPropertyValue_VT_BOOL(TypedPropertyValueHeader):
    value = VARIANT_BOOL
    value_pad = raw(2)
# end class TypedPropertyValue_VT_BOOL

class TypedPropertyValue_VT_DECIMAL(TypedPropertyValueHeader):
    value = DECIMAL_LE
# end class TypedPropertyValue_VT_DECIMAL

class TypedPropertyValue_VT_I1(TypedPropertyValueHeader):
    value = INT8
    value_pad = raw(3)
# end class TypedPropertyValue_VT_I1

class TypedPropertyValue_VT_UI1(TypedPropertyValueHeader):
    value = UINT8
    value_pad = raw(3)
# end class TypedPropertyValue_VT_UI1

class TypedPropertyValue_VT_UI2(TypedPropertyValueHeader):
    value = UINT16
    value_pad = raw(2)
# end class TypedPropertyValue_VT_UI2

class TypedPropertyValue_VT_UI4(TypedPropertyValueHeader):
    value = UINT32
# end class TypedPropertyValue_VT_UI4

class TypedPropertyValue_VT_I8(TypedPropertyValueHeader):
    value = INT64
# end class TypedPropertyValue_VT_I8

class TypedPropertyValue_VT_UI8(TypedPropertyValueHeader):
    value = UINT64
# end class TypedPropertyValue_VT_UI8

class TypedPropertyValue_VT_INT(TypedPropertyValueHeader):
    value = INT32
# end class TypedPropertyValue_VT_INT

class TypedPropertyValue_VT_UINT(TypedPropertyValueHeader):
    value = UINT32
# end class TypedPropertyValue_VT_UINT

class TypedPropertyValue_VT_FILETIME(TypedPropertyValueHeader):
    value = FILETIME_LE
# end class TypedPropertyValue_VT_FILETIME

class TypedPropertyValue_VT_CLSID(TypedPropertyValueHeader):
    value = CLSID_LE
# end class TypedPropertyValue_VT_CLSID
