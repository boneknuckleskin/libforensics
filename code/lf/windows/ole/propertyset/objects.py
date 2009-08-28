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
Objects for Microsole OLE property sets.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

import operator
from functools import reduce

from lf.io import byte

from lf.windows.time import (
    filetime_to_datetime, variant_time_to_datetime
)

from lf.windows.guid import guid_to_uuid
from lf.io import subset
from lf.io.consts import SEEK_SET
from lf.datatype import Extractor, LEExtractableArray
from lf.datatype.extractors import (
    int8, uint8, int16_le, uint16_le, int32_le, uint32_le, float32_le,
    float64_le, int64_le, uint64_le
)

from lf.windows import extractors as ms_extractors
from lf.windows.consts.codepage import (
    CP_UNKNOWN, CP_WINUNICODE, code_page_names
)

from lf.windows.ole.propertyset.extractors import (
    property_id_offset, property_set_header, property_set_stream_header,
    format_id_offset, typed_property_value_header, vt_i1, vt_i2, vt_bool,
    vt_ui1, vt_ui2, clipboard_data_header, array_dimension, array_header,
    dictionary_entry_header, hyperlink_header
)

from lf.windows.ole.propertyset.datatypes import PropertyIDOffset
from lf.windows.ole.varenum import (
    VT_EMPTY, VT_NULL, VT_I2, VT_I4, VT_R4, VT_R8, VT_CY, VT_DATE, VT_BSTR,
    VT_ERROR, VT_DECIMAL, VT_I1, VT_UI1, VT_UI2, VT_UI4, VT_I8, VT_UI8, VT_INT,
    VT_UINT, VT_LPSTR, VT_LPWSTR, VT_FILETIME, VT_BLOB, VT_STREAM, VT_STORAGE,
    VT_STREAMED_OBJECT, VT_STORED_OBJECT, VT_BLOB_OBJECT, VT_CF, VT_CLSID,
    VT_VERSIONED_STREAM, VT_VECTOR, VT_ARRAY, VT_BOOL, VT_VARIANT
)

from lf.windows.ole.propertyset.consts import (
    PID_CODEPAGE, PID_DICTIONARY
)

# Tuple of variant types that need to create a code page string property
_code_page_string_property_types = (
    VT_BSTR, VT_LPSTR, VT_STREAM, VT_STORAGE, VT_STREAMED_OBJECT,
    VT_STORED_OBJECT
)

class TypedPropertyValue():
    """
    Represents a TypedPropertyValue packet.

    .. attribute:: p_type

        The property type.

    .. attribute:: value

        The value of the property.  The Python datatype used depends on the
        p_type attribute.
    """

    def __init__(self, p_type, value):
        """
        Initalizes a TypedPropertyValue object.

        :parameters:
            p_type
                The property type.

            value
                The value of the property.
        """

        self.p_type = p_type
        self.value = value
    # end def __init__

    @staticmethod
    def get_property_value(p_type, code_page, stream, offset=None, align=True):
        """
        Gets the value of a property from a stream.

        :parameters:
            p_type
                The type of property.

            code_page
                The code page of the property set.

            stream
                A stream that contains the value.

            offset
                The start of the value, in stream.

            align
                If true, extracts padding so a multiple of 4 bytes is read.

        :raises:
            ValueError
                If p_type is invalid.

        :rtype: tuple
        :returns: A tuple of (number of bytes read, value)
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        bytes_read = 0

        if p_type in _code_page_string_property_types:
            char_count = uint32_le.extract(stream.read(4))[0]

            if code_page == CP_WINUNICODE:
                char_count *= 2
            # end if

            value = stream.read(char_count)
            bytes_read = len(value) + 4

        elif (p_type == VT_EMPTY) or (p_type == VT_NULL):
            value = None
            bytes_read = 0

        elif p_type == VT_I2:
            if not align:
                value = int16_le.extract(stream.read(2))[0]
                bytes_read = 2
            else:
                value = vt_i2.extract(stream.read(4))[0]
                bytes_read = 4
            # end if

        elif p_type == VT_I4:
            value = uint32_le.extract(stream.read(4))[0]
            bytes_read = 4

        elif p_type == VT_R4:
            value = float32_le.extract(stream.read(4))[0]
            bytes_read = 4

        elif p_type == VT_R8:
            value = float64_le.extract(stream.read(4))[0]
            bytes_read = 8

        elif p_type == VT_CY:
            value = int64_le.extract(stream.read(8))[0]
            value = value / 10000
            bytes_read = 8

        elif p_type == VT_DATE:
            value = float64_le.extract(stream.read(8))[0]
            value = variant_time_to_datetime(value)
            bytes_read = 8

        elif p_type == VT_ERROR:
            value = uint32_le.extract(stream.read(4))[0]
            bytes_read = 4

        elif p_type == VT_BOOL:
            if not align:
                value = int16_le.extract(stream.read(2))[0]
                bytes_read = 2
            else:
                value = vt_bool.extract(stream.read(4))[0]
                bytes_read = 4
            # end if

        elif p_type == VT_DECIMAL:
            decimal = ms_extractors.decimal_le.extract(stream.read(16))
            bytes_read = 16

            value = (decimal.hi32 << 64) | decimal.lo64
            value /= 10**decimal.scale

            if decimal.sign:
                value = -value
            # end if

        elif p_type == VT_I1:
            if not align:
                value = int8.extract(stream.read(1))[0]
                bytes_read = 1
            else:
                value = vt_i1.extract(stream.read(4))[0]
                bytes_read = 4
            # end if

        elif p_type == VT_UI1:
            if not align:
                value = uint8.extract(stream.read(1))[0]
                bytes_read = 1
            else:
                value = vt_ui1.extract(stream.read(4))[0]
                bytes_read = 4
            # end if

        elif p_type == VT_UI2:
            if not align:
                value = uint16_le.extract(stream.read(2))[0]
                bytes_read = 2
            else:
                value = vt_ui2.extract(stream.read(4))[0]
                bytes_read = 4
            # end if

        elif p_type == VT_UI4:
            value = uint32_le.extract(stream.read(4))[0]
            bytes_read = 4

        elif p_type == VT_I8:
            value = int64_le.extract(stream.read(8))[0]
            bytes_read = 8

        elif p_type == VT_UI8:
            value = uint64_le.extract(stream.read(8))[0]
            bytes_read = 8

        elif p_type == VT_INT:
            value = int32_le.extract(stream.read(4))[0]
            bytes_read = 4

        elif p_type == VT_UINT:
            value = uint32_le.extract(stream.read(4))[0]
            bytes_read = 4

        elif p_type == VT_LPWSTR:
            size = uint32_le.extract(stream.read(4))[0]
            size = size * 2
            value = stream.read(size)
            if align:
                bytes_read = len(value) + 4 + (size % 4)
            else:
                bytes_read = len(value) + 4
            # end if

            if size < len(value):
                value = value[:size]
            # end if

            value = value.decode("utf_16_le").rstrip("\x00")

        elif p_type == VT_FILETIME:
            value = uint64_le.extract(stream.read(8))[0]
            value = filetime_to_datetime(value)
            bytes_read = 8

        elif p_type in (VT_BLOB, VT_BLOB_OBJECT):
            size = uint32_le.extract(stream.read(4))[0]
            value = stream.read(size)
            bytes_read = len(value) + 4

        elif p_type == VT_CF:
            (size, fmt) = clipboard_data_header.extract(stream.read(8))
            value = (fmt, stream.read(size))
            bytes_read = len(value[1]) + 8

        elif p_type == VT_CLSID:
            guid = ms_extractors.guid_le.extract(stream.read(16))
            value = guid_to_uuid(
                guid.data1,
                guid.data2,
                guid.data3,
                guid.data4
            )
            bytes_read = 16

        elif p_type == VT_VERSIONED_STREAM:
            guid = ms_extractors.guid_le.extract(stream.read(16))[0]
            size = uint32_le.extract(stream.read(4))[0]
            value = (guid, stream.read(size))
            bytes_read = 20 + len(value[1])

        else:
            raise ValueError("invalid type {0}".format(p_type))
        # end if

        return (bytes_read, value)
    # end def get_property_value

    @staticmethod
    def make_vector(p_type, code_page, stream, offset=None):
        """
        Factory function to make a vector of TypedPropertyValue objects.

        :parameters:
            p_type
                The property type.

            code_page
                The code page of the property set.

            stream
                A stream that contains the vector.

            offset
                The offset into the stream of the start of the vector.

        :rtype: TypedPropertyValue
        :returns: A TypedPropertyValue, where value is a list of
                  TypedPropertyValue objects.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        values = list()
        count = uint32_le.extract(stream.read(4))[0]
        offset += 4

        elem_type = p_type & (~VT_VECTOR)

        if elem_type == VT_VARIANT:
            for index in range(count):
                stream.seek(offset, SEEK_SET)
                header = typed_property_value_header.extract(stream.read(4))
                offset += 4

                bytes_read, value = TypedPropertyValue.get_property_value(
                    header.p_type, code_page, stream, offset, True
                )
                values.append(value)

                offset += bytes_read
            # end for
        else:
            for index in range(count):
                stream.seek(offset, SEEK_SET)
                bytes_read, value = TypedPropertyValue.get_property_value(
                    elem_type, code_page, stream, offset, False
                )

                values.append(value)
                offset += bytes_read
            # end for
        # end if

        return TypedPropertyValue(p_type, values)
    # end def make_vector

    @staticmethod
    def make_array(p_type, code_page, stream, offset=None):
        """
        Factory function to make an array of TypedPropertyValue objects.

        :parameters:
            p_type
                The property type.

            code_page
                The code page of the property set.

            stream
                A stream that contains the array.

            offset
                The start of the array.

        :rtype: TypedPropertyValue
        :returns: A TypedPropertyValue object, where the value is a tuple of
                  (n_based, array).  The n_based is a list of the bases for
                  each dimension of the array (effectively making the dimension
                  n-based.)  The array is a list of lists, containing the
                  values.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        (elem_type, dim_count) = array_header.extract(stream.read(8))
        offset += 8


        n_bases = list()
        sizes = list()
        for index in range(dim_count):
            (size, n_base) = array_dimension.extract(stream.read(8))
            sizes.append(size)
            n_bases.append(n_base)
            offset += 8
        # end for


        elem_count = reduce(operator.mul, sizes)
        values = list()
        for counter in range(elem_count):
            bytes_read, value = TypedPropertyValue.get_property_value(
                elem_type, code_page, stream, offset, False
            )

            offset += bytes_read
            values.append(value)
        # end for

        for size in reversed(sizes[1:]):
            count = len(values) // size
            values = [
                values[index*size:index*size+size] for index in range(count)
            ]
        # end for

        return TypedPropertyValue(p_type, (n_based, values))
    # end def make_array

    @staticmethod
    def make(code_page, stream, offset=None):
        """
        Factory function to make a TypedPropertyValue object.

        :parameters:
            code_page
                The code page of the property set.

            stream
                A stream that contains the TypedPropertyValue.

            offset
                The byte offset into the stream of the start of the
                TypedPropertyValue.

        :rtype: TypedPropertyValue
        :returns: An instantiated TypedPropertyValue
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        p_type = typed_property_value_header.extract(stream.read(4))[0]
        offset += 4

        if p_type & VT_VECTOR:
            return TypedPropertyValue.make_vector(
                p_type, code_page, stream, offset
            )

        elif p_type & VT_ARRAY:
            return TypedPropertyValue.make_array(
                p_type, code_page, stream, offset
            )
        # end if

        value = TypedPropertyValue.get_property_value(
            p_type, code_page, stream, offset, True
        )[1]

        return TypedPropertyValue(p_type, value)
    # end def make
# end class TypedPropertyValue

class Property():
    """
    Represents a single property.

    .. attribute:: p_id

        The property identifier.

    .. attribute:: p_type

        The property type.

    .. attribute:: value

        The value of the property.
    """

    def __init__(self, p_id, p_type, value):
        """
        Initializes a Property object.

        :parameters:
            p_id
                The property identifier.

            type
                The property type.

            value
                The value of the property.
        """

        self.p_id = p_id
        self.p_type = p_type
        self.value = value
    # end def __init__

    @staticmethod
    def make_dictionary(p_id, code_page, stream, offset=None):
        """
        Makes a dictionary property.

        :parameters:
            p_id
                The property identifier.

            code_page
                The code page of the property set.

            stream
                A stream that covers the dictionary.

            offset
                The byte offset into the stream, of the start of the
                dictionary.

        :rtype: dict
        :returns: A dictionary of property identifers (keys) and their text
                  names (values).
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.extract(stream.read(4))[0]
        entries = dict()
        offset += 4

        for index in range(count):
            stream.seek(offset, SEEK_SET)
            (entry_prop_id, name_count) = \
                dictionary_entry_header.extract(stream.read(8))

            if code_page == CP_WINUNICODE:
                name = stream.read(name_count * 2)
            else:
                name = stream.read(name_count)
            # end if

            entries[entry_prop_id] = name

            offset += 8 + len(name)
        # end for

        return entries
    # end def make_dictionary

    @staticmethod
    def make(p_id, code_page, stream, offset=None):
        """
        Factory function to make Property objects.

        :parameters:
            p_id
                The property identifier.

            code_page
                The code page for the property set.

            stream
                A stream that contains the property.

            offset
                The byte offset into the stream of the start of the property.

        :rtype: Property
        :returns: An instantiated Property object.
        """

        if p_id == PID_DICTIONARY:
            return Property.make_dictionary(p_id, code_page, stream, offset)
        # end if

        tv = TypedPropertyValue.make(code_page, stream, offset)

        return Property(p_id, tv.p_type, tv.value)
    # end def make
# end class Property

class HyperlinksProperty(Property):
    """
    Creates a property that represents the VtHyperlinks type.

    .. attribute:: value

        A list of tuples of the (hash, app, office_art, info, location, target)
        fields for each hyperlink.
    """

    @staticmethod
    def make(p_id, code_page, stream, offset=None):
        """
        Factory function to make a HyperlinksProperty object.

        :parameters:
            p_id
                The property identifier.

            code_page
                The code page of the property.

            stream
                A stream that contains the data of the property.

            offset
                The start of the VtHyperlinkValue, in the stream.

        :rtype: Property
        :returns: A HyperlinksProperty object.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        value = list()

        elem_count = uint32_le.extract(stream.read(4))[0]
        offset += 4

        for index in range(elem_count // 6):
            stream.seek(offset, SEEK_SET)
            header = hyperlink_header.extract(stream.read(32))
            offset += 32

            p_type = typed_property_value_header.extract(stream.read(4))[0]
            offset += 4

            (bytes_read, location) = TypedPropertyValue.get_property_value(
                p_type, code_page, stream, offset, align=True
            )
            offset += bytes_read

            stream.seek(offset, SEEK_SET)
            p_type = typed_property_value_header.extract(stream.read(4))[0]
            offset += 4

            (bytes_read, target) = TypedPropertyValue.get_property_value(
                p_type, code_page, stream, offset, align=True
            )
            offset += bytes_read

            value.append((
                header.hash.value, header.app.value, header.office_art.value,
                header.info.value, location, target
            ))
        # end for

        return HyperlinksProperty(p_id, VT_BLOB, value)
    # end def make
# end class HyperlinksProperty

class PropertySet():
    """
    A set (collection) of properties.

    .. attribute:: properties

        A dictionary of the properties in the property set.  The keys are the
        property identifiers.

    .. attribute:: fmtid

        The FMTID of the property set.
    """

    def __init__(self, fmtid, stream, offset=None):
        """
        Initializes a PropertySet object.

        :parameters:
            fmtid
                The FMTID of the property set.

            stream
                A stream that contains the property set.

            offset
                The offset in the stream of the start of the property set.
        """

        properties = dict()

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = property_set_header.extract(stream.read(8))

        if header.prop_count > 0:
            extractor = Extractor(
                LEExtractableArray(PropertyIDOffset, header.prop_count)
            )

            stream.seek(offset + 8, SEEK_SET)
            data = stream.read(header.prop_count * 8)
            property_id_offsets = list(extractor.extract(data))

            code_page = CP_UNKNOWN

            for index, (prop_id, prop_offset) in enumerate(property_id_offsets):
                if prop_id == PID_CODEPAGE:
                    prop_offset += offset
                    property = Property.make(
                        prop_id, code_page, stream, prop_offset
                    )
                    properties[prop_id] = property

                    code_page = property.value
                    del property_id_offsets[index]

                    break
                # end if
            # end for

            for (prop_id, prop_offset) in property_id_offsets:
                if prop_id == PID_CODEPAGE:
                    continue
                # end if

                prop_offset += offset

                property = Property.make(
                    prop_id, code_page, stream, prop_offset
                )

                properties[prop_id] = property
            # end for
        # end if

        self.fmtid = fmtid
        self.properties = properties

        # Decode any strings
        if code_page < 0:
            code_page = ~(code_page ^ 0xFFFF)
        # end if

        if code_page in code_page_names:
            code_page_name = code_page_names[code_page]

            for (prop_id, property) in properties.items():
                if prop_id == PID_DICTIONARY:
                    new_dict = dict()

                    for (key, value) in property.items():
                        value = value.decode(code_page_name).rstrip("\x00")
                        new_dict[key] = value
                    # end for

                    properties[prop_id] = new_dict
                elif property.p_type in _code_page_string_property_types:
                    value = property.value.decode(code_page_name)
                    property.value = value.rstrip("\x00")
                # end if
            # end for
        # end if
    # end def __init__
# end class PropertySet

class PropertySetStream():
    """
    A stream for simple property sets.

    .. attribute:: version

        The version number of the property set.

    .. attribute:: sys_id

        The system identifier field.

    .. attribute:: clsid

        The CLSID of the property set(s).

    .. attribute:: property_sets

        A list of PropertySet objects.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a PropertySetStream object.

        :parameters:
            stream
                An IStream object that covers the property set stream.

            offset
                The start of the PropertySetStream
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = property_set_stream_header.extract(stream.read(48))

        self.version = header.version
        self.sys_id = header.sys_id
        self.clsid = header.clsid

        property_sets = list()
        self.property_sets = property_sets

        if not (0 <= header.prop_set_count <= 2):
            err_msg = "invalid number of property sets: {0}".format(
                header.prop_set_count
            )
            raise ValueError(err_msg)
        # end if

        if header.prop_set_count == 0:
            return
        # end if

        fmtid0 = guid_to_uuid(
            header.fmtid0.data1,
            header.fmtid0.data2,
            header.fmtid0.data3,
            header.fmtid0.data4
        )

        prop_set_offset = header.offset0 + offset
        property_sets.append(PropertySet(fmtid0, stream, prop_set_offset))

        if header.prop_set_count == 2:
            stream.seek(offset + 48, SEEK_SET)
            data = stream.read(20)
            (fmtid1, offset1) = format_id_offset.extract(data)
            fmtid1 = guid_to_uuid(
                fmtid1.data1,
                fmtid1.data2,
                fmtid1.data3,
                fmtid1.data4
            )
            prop_set_offset = offset + offset1
            prop_set = PropertySet(fmtid1, stream, prop_set_offset)

            code_page = prop_set.properties[PID_CODEPAGE].value
            names = prop_set.properties[PID_DICTIONARY]

            for (p_id, name) in names.items():
                if name == "_PID_GUID":
                    prop = prop_set.properties[p_id]
                    prop.value = prop.value.decode("utf_16_le")
                    prop_set.properties[p_id] = prop
                elif name == "_PID_HLINKS":
                    prop = prop_set.properties[p_id]
                    stream = byte.open(prop.value)

                    new_prop = HyperlinksProperty.make(
                        prop.p_id, code_page, stream
                    )

                    prop_set.properties[p_id] = new_prop
                # end if
            # end for

            property_sets.append(prop_set)
        # end if
    # end def __init__
# end class PropertySetStream
