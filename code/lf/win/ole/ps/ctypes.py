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

"""Ctypes classes for record data types in lf.win.ole.ps.dtypes"""

# local imports
from lf.win.ole.ps.dtypes import (
    PropertySetStreamHeader, PropertySetHeader,
    PropertyIdentifierAndOffset, DictionaryEntryHeader, ArrayHeader,
    ArrayDimension,

    TypedPropertyValueHeader, TypedPropertyValue_VT_I2,
    TypedPropertyValue_VT_R4, TypedPropertyValue_VT_R8,
    TypedPropertyValue_VT_CY, TypedPropertyValue_VT_DATE,
    TypedPropertyValue_VT_ERROR, TypedPropertyValue_VT_UI2,
    TypedPropertyValue_VT_DECIMAL, TypedPropertyValue_VT_I1,
    TypedPropertyValue_VT_UI1, TypedPropertyValue_VT_UI4,
    TypedPropertyValue_VT_I8, TypedPropertyValue_VT_UI8,
    TypedPropertyValue_VT_I4, TypedPropertyValue_VT_FILETIME,
    TypedPropertyValue_VT_CLSID
)

__docformat__ = "restructuredtext en"
__all__ = [
    "property_set_stream_header", "property_set_header",
    "property_identifier_and_offset", "dictionary_entry_header",
    "array_header", "array_dimension",

    "typed_property_value_header", "typed_property_value_vt_i2",
    "typed_property_value_vt_r4", "typed_property_value_vt_r8",
    "typed_property_value_vt_cy", "typed_property_value_vt_date",
    "typed_property_value_vt_error", "typed_property_value_vt_ui2",
    "typed_property_value_vt_decimal", "typed_property_value_vt_i1",
    "typed_property_value_vt_ui1", "typed_property_value_vt_ui4",
    "typed_property_value_vt_i8", "typed_property_value_vt_ui8",
    "typed_property_value_vt_i4", "typed_property_value_vt_filetime",
    "typed_property_value_vt_clsid"

]

property_set_stream_header = PropertySetStreamHeader._ctype_
property_set_header = PropertySetHeader._ctype_
property_identifier_and_offset = PropertyIdentifierAndOffset._ctype_
dictionary_entry_header = DictionaryEntryHeader._ctype_
array_header = ArrayHeader._ctype_
array_dimension = ArrayDimension._ctype_

typed_property_value_header = TypedPropertyValueHeader._ctype_
typed_property_value_vt_i2 = TypedPropertyValue_VT_I2._ctype_
typed_property_value_vt_r4 = TypedPropertyValue_VT_R4._ctype_
typed_property_value_vt_r8 = TypedPropertyValue_VT_R8._ctype_
typed_property_value_vt_cy = TypedPropertyValue_VT_CY._ctype_
typed_property_value_vt_date = TypedPropertyValue_VT_DATE._ctype_
typed_property_value_vt_error = TypedPropertyValue_VT_ERROR._ctype_
typed_property_value_vt_ui2 = TypedPropertyValue_VT_UI2._ctype_
typed_property_value_vt_decimal = TypedPropertyValue_VT_DECIMAL._ctype_
typed_property_value_vt_i1 = TypedPropertyValue_VT_I1._ctype_
typed_property_value_vt_ui1 = TypedPropertyValue_VT_UI1._ctype_
typed_property_value_vt_ui4 = TypedPropertyValue_VT_UI4._ctype_
typed_property_value_vt_i8 = TypedPropertyValue_VT_I8._ctype_
typed_property_value_vt_ui8 = TypedPropertyValue_VT_UI8._ctype_
typed_property_value_vt_i4 = TypedPropertyValue_VT_I4._ctype_
typed_property_value_vt_filetime = TypedPropertyValue_VT_FILETIME._ctype_
typed_property_value_vt_clsid = TypedPropertyValue_VT_CLSID._ctype_
