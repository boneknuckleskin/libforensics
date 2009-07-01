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
Extractors for OLE property sets.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from lf.struct.extract import extractor_factory as factory
from lf.windows.ole.propertyset.structs import (
    PropertyIDOffset,
    PropertySetHeader,
    PropertySetStreamHeader,
    FormatIDOffset,
    VT_I1, VT_I2, VT_BOOL, VT_UI1, VT_UI2,
    TypedPropertyValueHeader,
    ClipboardDataHeader,
    ArrayHeader, ArrayDimension, DictionaryEntryHeader,
    TypedPropertyValue_VT_I2, TypedPropertyValue_VT_I4,
    TypedPropertyValue_VT_R4, TypedPropertyValue_VT_R8,
    TypedPropertyValue_VT_CY, TypedPropertyValue_VT_DATE,
    TypedPropertyValue_VT_ERROR, TypedPropertyValue_VT_BOOL,
    TypedPropertyValue_VT_DECIMAL, TypedPropertyValue_VT_I1,
    TypedPropertyValue_VT_UI1, TypedPropertyValue_VT_UI2,
    TypedPropertyValue_VT_UI4, TypedPropertyValue_VT_I8,
    TypedPropertyValue_VT_UI8, TypedPropertyValue_VT_INT,
    TypedPropertyValue_VT_UINT, TypedPropertyValue_VT_FILETIME,
    TypedPropertyValue_VT_CLSID,
    HyperlinkHeader

)

__docformat__ = "restructuredtext en"
__all__ = [
    "property_id_offset",
    "property_set_header",
    "property_set_stream_header",
    "format_id_offset",
    "typed_property_value_header",
    "vt_i1", "vt_i2", "vt_bool", "vt_ui1", "vt_ui2",
    "clipboard_data_header",
    "array_dimension", "array_header", "dictionary_entry_header",
    "typed_property_value_vt_i2", "typed_property_value_vt_i4",
    "typed_property_value_vt_r4", "typed_property_value_vt_r8",
    "typed_property_value_vt_cy", "typed_property_value_vt_date",
    "typed_property_value_vt_error", "typed_property_value_vt_bool",
    "typed_property_value_vt_decimal", "typed_property_value_vt_i1",
    "typed_property_value_vt_ui1", "typed_property_value_vt_ui2",
    "typed_property_value_vt_ui4", "typed_property_value_vt_i8",
    "typed_property_value_vt_ui8", "typed_property_value_vt_int",
    "typed_property_value_vt_uint", "typed_property_value_vt_filetime",
    "typed_property_value_vt_clsid",
    "hyperlink_header"
]

property_id_offset = factory.make(PropertyIDOffset())
property_set_header = factory.make(PropertySetHeader())
property_set_stream_header = factory.make(PropertySetStreamHeader())
format_id_offset = factory.make(FormatIDOffset())
vt_i1 = factory.make(VT_I1())
vt_i2 = factory.make(VT_I2())
vt_bool = factory.make(VT_BOOL())
vt_ui1 = factory.make(VT_UI1())
vt_ui2 = factory.make(VT_UI2())
typed_property_value_header = factory.make(TypedPropertyValueHeader())
clipboard_data_header = factory.make(ClipboardDataHeader())
array_dimension = factory.make(ArrayDimension())
array_header = factory.make(ArrayHeader())
dictionary_entry_header = factory.make(DictionaryEntryHeader())

typed_property_value_vt_i2 = factory.make(TypedPropertyValue_VT_I2())
typed_property_value_vt_i4 = factory.make(TypedPropertyValue_VT_I4())
typed_property_value_vt_r4 = factory.make(TypedPropertyValue_VT_R4())
typed_property_value_vt_r8 = factory.make(TypedPropertyValue_VT_R8())
typed_property_value_vt_cy = factory.make(TypedPropertyValue_VT_CY())
typed_property_value_vt_date = factory.make(TypedPropertyValue_VT_DATE())
typed_property_value_vt_error = factory.make(TypedPropertyValue_VT_ERROR())
typed_property_value_vt_bool = factory.make(TypedPropertyValue_VT_BOOL())
typed_property_value_vt_decimal = factory.make(TypedPropertyValue_VT_DECIMAL())
typed_property_value_vt_i1 = factory.make(TypedPropertyValue_VT_I1())
typed_property_value_vt_ui1 = factory.make(TypedPropertyValue_VT_UI1())
typed_property_value_vt_ui2 = factory.make(TypedPropertyValue_VT_UI2())
typed_property_value_vt_ui4 = factory.make(TypedPropertyValue_VT_UI4())
typed_property_value_vt_i8 = factory.make(TypedPropertyValue_VT_I8())
typed_property_value_vt_ui8 = factory.make(TypedPropertyValue_VT_UI8())
typed_property_value_vt_int = factory.make(TypedPropertyValue_VT_INT())
typed_property_value_vt_uint = factory.make(TypedPropertyValue_VT_UINT())
typed_property_value_vt_filetime = factory.make(
    TypedPropertyValue_VT_FILETIME())
typed_property_value_vt_clsid = factory.make(TypedPropertyValue_VT_CLSID())

hyperlink_header = factory.make(HyperlinkHeader())
