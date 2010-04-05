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

"""Objects for OLE property sets."""

# stdlib imports
from codecs import getdecoder
from decimal import Decimal
from ctypes import sizeof
from functools import reduce
from operator import mul

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import Structuple, ActiveStructuple
from lf.dtypes.ctypes import (
    int8, uint8, uint16_le, int16_le, int32_le, uint32_le, int64_le,
    uint64_le, float32_le, float64_le
)
from lf.time import VariantTimeTodatetime, FILETIMETodatetime
from lf.win.objects import (
    GUIDToUUID, DECIMALToDecimal, CURRENCYToDecimal, CLSIDToUUID
)
from lf.win.objects import HRESULT as HRESULT_
from lf.win.ctypes import guid_le
from lf.win.codepage.consts import CP_WINUNICODE, code_page_names
from lf.win.ole import varenum
from lf.win.ole.ps.consts import (
    CODEPAGE_PROPERTY_IDENTIFIER, DICTIONARY_PROPERTY_IDENTIFIER
)
from lf.win.ole.ps.ctypes import (
    property_set_stream_header, property_set_header,
    property_identifier_and_offset, dictionary_entry_header, array_header,
    array_dimension,

    typed_property_value_header, typed_property_value_vt_i2,
    typed_property_value_vt_r4, typed_property_value_vt_r8,
    typed_property_value_vt_cy, typed_property_value_vt_date,
    typed_property_value_vt_error, typed_property_value_vt_ui2,
    typed_property_value_vt_decimal, typed_property_value_vt_i1,
    typed_property_value_vt_ui1, typed_property_value_vt_ui4,
    typed_property_value_vt_i8, typed_property_value_vt_ui8,
    typed_property_value_vt_i4, typed_property_value_vt_filetime,
    typed_property_value_vt_clsid
)

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertySetStreamHeader", "PropertySetHeader", "Dictionary",

    "TypedPropertyValue", "VT_EMPTY", "VT_NULL", "VT_I2", "VT_I4", "VT_R4",
    "VT_R8", "VT_CY", "VT_DATE", "VT_LPSTR", "VT_ERROR", "VT_BOOL",
    "VT_DECIMAL", "VT_I1", "VT_UI1", "VT_UI2", "VT_UI4", "VT_I8", "VT_UI8",
    "VT_INT", "VT_UINT", "VT_BSTR", "VT_LPWSTR", "VT_FILETIME", "VT_BLOB",
    "VT_STREAM", "VT_STORAGE", "VT_STREAMED_OBJECT", "VT_BLOB_OBJECT", "VT_CF",
    "VT_CLSID", "VT_VERSIONED_STREAM", "VT_ARRAY", "VT_VECTOR", "Dictionary",

    "CodePageString", "UnicodeString", "DictionaryEntry",

    "PropertyFactory", "Builder"

]

_utf16_le_decoder = getdecoder("utf_16_le")

class Packet():
    """Base class for packet types."""

    pass
# end class Packet

class ActivePacket(Packet, ActiveStructuple):
    """Represents a packet type that can read from streams/ctypes."""

    pass
# end class ActivePacket

class PropertySetStreamHeader(ActivePacket):
    """    Represents the header of a PropertySetStream structure (packet).

    .. attribute:: byte_order

        The byte order field.

    .. attribute:: version

        The version of the OLE property set.

    .. attribute:: sys_id

        The system identifier field.

    .. attribute:: clsid

        The CLSID of the associated property set(s).

    .. attribute:: property_set_count

        The number of property sets in the stream.

    .. attribute:: fmtid0

        A GUID that identifies the property set format of the first property
        set.

    .. attribute:: offset0

        The offset of the first property set, relative to the start of the
        :class:`PropertySetStreamHeader` structure.

    .. attribute:: fmtid1

        A GUID that identifiers the property set format of the second property
        set.  If there is only one property set, this is set to ``None``.

        Represents the header of a PropertySetStream structure (packet).

    .. attribute:: byte_order

        The byte order field.

    .. attribute:: version

        The version of the OLE property set.

    .. attribute:: sys_id

        The system identifier field.

    .. attribute:: clsid

        The CLSID of the associated property set(s).

    .. attribute:: property_set_count

        The number of property sets in the stream.

    .. attribute:: fmtid0

        A GUID that identifies the property set format of the first property
        set.

    .. attribute:: offset0

        The offset of the first property set, relative to the start of the
        :class:`PropertySetStreamHeader` structure.

    .. attribute:: fmtid1

        A GUID that identifiers the property set format of the second property
        set.  If there is only one property set, this is set to ``None``.

    .. attribute:: offset1

        The offset of the second property set, relative to the start of the
        :class:`PropertySetStreamHeader` structure.  If there is only one
        property set, this is set to ``None``.

    """

    _fields_ = (
        "byte_order", "version", "sys_id", "clsid", "property_set_count",
        "fmtid0", "offset0", "fmtid1", "offset1"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`PropertySetStreamHeader` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the PropertySetStreamHeader
                       structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`PropertySetStreamHeader`
        :returns: The corresponding :class:`PropertySetStreamHeader` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        header = property_set_stream_header.from_buffer_copy(stream.read(48))

        if header.property_set_count > 1:
            fmtid1 = guid_le.from_buffer_copy(stream.read(16))
            offset1 = uint32_le.from_buffer_copy(stream.read(4)).value

            fmtid1 = GUIDToUUID.from_ctype(fmtid1)
        else:
            fmtid1 = None
            offset1 = None
        # end if

        fmtid0 = header.fmtid0
        fmtid0 = GUIDToUUID.from_ctype(fmtid0)

        clsid = header.clsid
        clsid = CLSIDToUUID.from_ctype(clsid)

        return cls((
            header.byte_order, header.version, bytes(header.sys_id),
            clsid, header.property_set_count, fmtid0, header.offset0, fmtid1,
            offset1
        ))
    # end def from_stream
# end class PropertySetStreamHeader

class PropertySetHeader(ActivePacket):
    """Represents the header of a PropertySet structure. (packet)

    .. attribute:: size

        The total size (in bytes) of the PropertySetHeader structure.

    .. attribute:: pair_count

        The number of pid/offset pairs.

    .. attribute:: pids_offsets

        A dictionary of property identifiers and the corresponding properties.

    """

    _fields_ = ("size", "pair_count", "pids_offsets")

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`PropertySetHeader` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the PropertySetHeader structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`PropertySetHeader`
        :returns: The corresponding :class:`PropertySetHeader` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = property_set_header.from_buffer_copy(stream.read(8))
        count = header.pair_count

        pids_offsets_ctype = property_identifier_and_offset * count
        pids_offsets_list = \
            pids_offsets_ctype.from_buffer_copy(stream.read(8 * count))
        pids_offsets = dict()

        for pid_offset in pids_offsets_list:
            pids_offsets[pid_offset.pid] = pid_offset.offset
        # end for

        return cls((header.size, count, pids_offsets))
    # end def from_stream
# end class PropertySetHeader

class PropertyPacket(ActivePacket):
    """
    Base class for packet types associated with a property.

    .. attribute:: size

        The total size of the packet (in bytes) including any header, value,
        and padding fields.

    .. attribute:: value

        The represented value.
    """
    _fields_ = ("size", "value")
# end class PropertyPacket

class ValuePacket(ActivePacket):
    """Base class for packet types associated with the value of a property.

    .. attribute:: size

        The total number of bytes in the packet, including any header, value,
        and padding fields.

    .. attribute:: value

        The represented value.

    """

    _fields_ = ("size", "value")
# end class ValuePacket

class Dictionary(PropertyPacket):
    """Represents a Dictionary property.

    .. attribute:: property_count

        A count of the number of properties in the mapping.  This is a field in
        the data type (i.e. not len(mapping)).

    .. attribute:: mapping

        A dictionary of property identifiers (keys) and names (values).

    .. attribute:: value

        An alias for the :attr:`mapping` attribute.

    """

    _fields_ = ("size", "mapping", "property_count")
    _aliases_ = {"value": "mapping"}

    @classmethod
    def from_stream(cls, stream, offset=None, code_page=None, decoder=None):
        """Creates a :class:`Dictionary` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the Dictionary property.

        :type offset: ``int``
        :param offset: The start of the property in :attr:`stream`.

        :type code_page: ``int``
        :param code_page: The value of the CodePage property.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the names.

        :rtype: :class:`Dictionary`
        :returns: The corresponding :class:`Dictionary` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        offset += 4

        entries = dict()
        counter = 0
        tot_size = 0
        stream_size = stream.size
        while (counter < count) and (offset < stream_size):
            entry = \
                DictionaryEntry.from_stream(stream, offset, code_page, decoder)
            entries[entry.pid] = entry.value
            offset += entry.size
            tot_size += entry.size
            counter += 1
        # end while

        tot_size = (tot_size + 3) & ~0x3

        return cls((tot_size + 4, entries, count))
    # end def from_stream
# end class Dictionary

class DictionaryEntry(ValuePacket):
    """Represents a DictionaryEntry structure (packet).

    .. attribute:: pid

        The property identifier

    .. attribute:: name

        The name associated with the property identifier.

    .. attribute:: value

        An alias for the :attr:`name` attribute.

    """

    _fields_ = ("size", "name", "pid")
    _aliases_ = {"value": "name"}

    @classmethod
    def from_stream(cls, stream, offset=None, code_page=None, decoder=None):
        """Creates a :class:`DictionaryEntry` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the DictionaryEntry property.

        :type offset: ``int``
        :param offset: The start of the property in :attr:`stream`.

        :type code_page: ``int``
        :param code_page: The value of the CodePage property.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the names.

        :rtype: :class:`DictionaryEntry`
        :returns: The corresponding :class:`DictionaryEntry` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        header = dictionary_entry_header.from_buffer_copy(stream.read(8))

        if code_page == CP_WINUNICODE:
            name_size = header.length * 2
            name = stream.read(name_size)
            name_size = (name_size + 3) & ~0x3
        else:
            name_size = header.length
            name = stream.read(name_size)
        # end if

        if decoder:
            new_name = decoder(name, "ignore")[0]
            if new_name:
                name = new_name

                stop = name.find("\x00")
                if stop != -1:
                    name = name[:stop]
                # end if
            # end if
        # end if

        return cls((name_size + 8, name, header.pid))
    # end def from_stream
# end class DictionaryEntry

class CURRENCY(ValuePacket):
    """Represents a CURRENCY structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`CURRENCY` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the CURRENCY structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`CURRENCY`
        :returns: The corresponding :class:`CURRENCY` object.

        """
        value = CURRENCYToDecimal.from_stream(stream, offset)

        return cls((8, value))
    # end def from_stream
# end class CURRENCY

class DATE(ValuePacket):
    """Represents a DATE structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`DATE` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the DATE structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`DATE`
        :returns: The corresponding :class:`DATE` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        value = float64_le.from_buffer_copy(stream.read(8)).value

        try:
            value = VariantTimeTodatetime.from_float(value)
        except ValueError:
            pass
        # end try

        return cls((8, value))
    # end def from_stream
# end class DATE

class CodePageString(ValuePacket):
    """Represents a CodePageString structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`CodePageString` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the CodePageString structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`CodePageString`
        :returns: The corresponding :class:`CodePageString` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        size = uint32_le.from_buffer_copy(stream.read(4)).value

        value = stream.read(size)
        size = (size + 3) & ~0x3

        if decoder:
            new_value = decoder(value, "ignore")[0]
            if new_value:
                value = new_value
            # end if
        # end if

        return cls((size + 4, value))
    # end def from_stream
# end class CodePageString

class DECIMAL(ValuePacket):
    """Represents a DECIMAL structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`DECIMAL` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the DECIMAL structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`DECIMAL`
        :returns: The corresponding :class:`DECIMAL` object.

        """
        value = DECIMALToDecimal.from_stream(stream, offset)

        return cls((16, value))
    # end def from_stream
# end class DECIMAL

class UnicodeString(ValuePacket):
    """Represents a UnicodeString structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`UnicodeString` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the UnicodeString structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`UnicodeString`
        :returns: The corresponding :class:`UnicodeString` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        size = count * 2

        value = stream.read(size)
        size = (size + 3) & ~0x3

        if decoder is None:
            decoder = _utf16_le_decoder
        # end if

        if decoder:
            new_value = decoder(value, "ignore")[0]
            if new_value:
                value = new_value
            # end if
        # end if

        return cls((size + 4, value))
    # end def from_stream
# end class UnicodeString

class FILETIME(ValuePacket):
    """Represents a FILETIME structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`FILETIME` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the FILETIME structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`FILETIME`
        :returns: The corresponding :class:`FILETIME` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        filetime = uint64_le.from_buffer_copy(stream.read(8)).value
        try:
            filetime = FILETIMETodatetime.from_int(filetime)
        except (TypeError, ValueError):
            pass
        # end try

        return cls((8, filetime))
    # end def from_stream
# end class FILETIME

class BLOB(ValuePacket):
    """Represents a BLOB structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`BLOB` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the BLOB structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`BLOB`
        :returns: The corresponding :class:`BLOB` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        size = uint32_le.from_buffer_copy(stream.read(4)).value
        value = stream.read(size)
        size = (size + 3) & ~0x3

        return cls((size + 4, value))
    # end def from_stream
# end class BLOB

class IndirectPropertyName(CodePageString):
    """Represents an IndirectPropertyName structure (packet)."""

    pass
# end class IndirectPropertyName

class ClipboardData(ValuePacket):
    """Represents a ClipboardData structure (packet).

    .. attribute:: format

        The format field.

    .. attribute:: data

        The data field.

    .. attribute:: value

        An alias for the :attr:`data` attribute.

    """

    _fields_ = ("size", "data", "format")
    _aliases_ = {"value": "data"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`ClipboardData` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the ClipboardData structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`ClipboardData`
        :returns: The corresponding :class:`ClipboardData` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        size = uint32_le.from_buffer_copy(stream.read(4)).value
        format = stream.read(4)
        data = stream.read(size - 4)
        size = (size + 3) & ~0x3

        return cls((size + 4, data, format))
    # end def from_stream
# end class ClipboardData

class GUID(ValuePacket):
    """Represents a GUID structure (packet)."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`GUID` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the GUID structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`GUID`
        :returns: The corresponding :class:`GUID` object.

        """
        value = GUIDToUUID.from_stream(stream, offset)

        return cls((16, value))
    # end def from_stream
# end class GUID

class VersionedStream(ValuePacket):
    """Represents a VersionedStream structure (packet).

    .. attribute:: version_guid

        The VersionGuid field.

    .. attribute:: stream_name

        The StreamName field.

    .. attribute:: value

        An alias for the :attr:`stream_name` attribute.

    """

    _fields_ = ("size", "stream_name", "version_guid")
    _aliases_ = {"value": "stream_name"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VersionedStream` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the VersionedStream structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the stream name.

        :rtype: :class:`VersionedStream`
        :returns: The corresponding :class:`VersionedStream` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        guid = GUIDToUUID.from_stream(stream, offset)
        stream_name = CodePageString.from_stream(stream, offset + 16, decoder)

        return cls((stream_name.size + 16, stream_name.value, guid))
    # end def from_stream
# end class VersionedStream

class HRESULT(ValuePacket):
    """Represents an HRESULT structure (packet).

    .. note::

        The :attr:`value` attribute is an instance of
        :class:`lf.win.objects.HRESULT`

    """

    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`HRESULT` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the HRESULT structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`HRESULT`
        :returns: The corresponding :class:`HRESULT` object.

        """
        value = HRESULT_.from_stream(stream, offset)

        return cls((4, value))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a :class:`HRESULT` object from a ctype.

        :type ctype: :class:`~lf.win.ctypes.hresult_le` or
                     :class:`~lf.win.ctypes.hresult_be`
        :param ctype: An hresult ctypes object.

        :rtype: :class:`HRESULT`
        :returns: The corresponding :class:`HRESULT` object.

        """
        value = HRESULT_.from_ctype(ctype)

        return cls((4, value))
    # end def from_ctype
# end class HRESULT

class Array(ValuePacket):
    """Represents the value from a VT_ARRAY property.

    .. attribute:: scalar_type

        The property type contained in the array.  This is an extracted value.

    .. attribute:: dimension_count

        The number of dimensions in the array.

    .. attribute:: dimensions

        A list of the (size, index_offset) attributes for each dimension.

    .. attribute:: value

        A flattened list of the values.

    """
    _fields_ = ("scalar_type", "dimension_count", "dimensions", "value")

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`Array` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the Array structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the string properties.

        :raises ValueError: If the extracted scalar type is an invalid property
                            type.

        :rtype: :class:`Array`
        :returns: The corresponding :class:`Array` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = array_header.from_buffer_copy(stream.read(8))
        scalar_type = header.scalar_type
        dim_count = header.dimension_count

        dims_ctype = array_dimension * dim_count
        dims_list = dims_ctype.from_buffer_copy(stream.read(8 * dim_count))

        dims = [(dim.size, dim.index_offset) for dim in dims_list]
        dim_sizes = [dim.size for dim in dims_list if dim.size != 0]
        count = reduce(mul, dim_sizes)

        seq = Sequence.from_stream(stream, scalar_type, count, decoder=decoder)
        size = seq.size + (dim_count * 8) + 8

        return cls((size, scalar_type, dim_count, dims, seq.value))
    # end def from_stream
# end class Array

class Vector(ValuePacket):
    """Represents the value from a VT_VECTOR packet.

    .. attribute:: scalar_count

        The number of elements in the vector.

    .. attribute:: value

        A list of elements in the vector.

    """
    _fields_ = ("scalar_count","value")

    @classmethod
    def from_stream(cls, stream, scalar_type, offset=None, decoder=None):
        """Creates a :class:`Vector` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the Vector structure.

        :type scalar_type: :const:`lf.win.ole.ps.consts.PropertyType`
        :param scalar_type: The type of the properties in the Vector structure.

        :type offset: int
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode the string properties.

        :raises ValueError: If :attr:`scalar_type` is an invalid property type.

        :rtype: :class:`Vector`
        :returns: The corresponding :class:`Vector` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        seq = Sequence.from_stream(
            stream, scalar_type, count, offset + 4, decoder
        )

        return cls((seq.size + 4, count, seq.value))
    # end def from_stream
# end class Vector

class Sequence(ValuePacket):
    """A :class:`ValuePacket` that is composed of a sequence of values.

    The :attr:`value` attribute is a list of (possibly more lists of)
    the values in the sequence.

    .. note::

        This is used internally by the :class:`Array` and :class:`Vector`
        classes to extract the individual elements.

    """

    @classmethod
    def from_stream(cls, stream, ptype, count, offset=None, decoder=None):
        """Creates a sequence of various properties from a stream.

        .. note::

            This method will round the size up to the nearest multiple of 4.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the sequence.

        :type ptype: :const:`lf.win.ole.ps.consts.PropertyType`
        :param ptype: The property type of the elements in the Sequence.

        :type count: ``int``
        :param count: The number of elements in the sequence.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode string properties.

        :raises ValueError: If :attr:`ptype` is an invalid property type.

        :rtype: :class:`Sequence`
        :returns: The corresponding :class:`Sequence` object.

        """
        is_lpstr = False

        if ptype in _simple_property_types:
            (size, _ctype) = _simple_property_types[ptype]

            if offset is not None:
                stream.seek(offset, SEEK_SET)
            else:
                offset = stream.tell()
            # end if

            stream_size = stream.size
            seq_size = count * size
            if seq_size > (stream_size - offset):
                count = (stream_size - offset) // size
                seq_size = count * size
            # end if

            _ctype = _ctype * count
            values = list(_ctype.from_buffer_copy(stream.read(seq_size)))
            seq_size = (seq_size + 3) & ~0x3
            return cls((seq_size, values))

        elif ptype == varenum.VT_EMPTY:
            factory_func = VT_EMPTY.from_stream

        elif ptype == varenum.VT_NULL:
            factory_func = VT_NULL.from_stream

        elif ptype == varenum.VT_CY:
            factory_func = CURRENCY.from_stream

        elif ptype == varenum.VT_DATE:
            factory_func = DATE.from_stream

        elif ptype == varenum.VT_BSTR:
            factory_func = CodePageString.from_stream

        elif ptype == varenum.VT_DECIMAL:
            factory_func = DECIMAL.from_stream

        elif ptype == varenum.VT_ERROR:
            factory_func = HRESULT.from_stream

        elif ptype == varenum.VT_LPSTR:
            factory_func = CodePageString.from_stream
            is_lpstr = True

        elif ptype == varenum.VT_LPWSTR:
            factory_func = UnicodeString.from_stream
            if decoder is False:
                decoder = _utf16_le_decoder
            # end if

        elif ptype == varenum.VT_FILETIME:
            factory_func = FILETIME.from_stream

        elif ptype == varenum.VT_BLOB:
            factory_func = BLOB.from_stream

        elif ptype == varenum.VT_STREAM:
            factory_func = IndirectPropertyName.from_stream

        elif ptype == varenum.VT_STORAGE:
            factory_func = IndirectPropertyName.from_stream

        elif ptype == varenum.VT_STREAMED_OBJECT:
            factory_func = IndirectPropertyName.from_stream

        elif ptype == varenum.VT_STORED_OBJECT:
            factory_func = IndirectPropertyName.from_stream

        elif ptype == varenum.VT_BLOB_OBJECT:
            factory_func = BLOB.from_stream

        elif ptype == varenum.VT_CF:
            factory_func = ClipboardData.from_stream

        elif ptype == varenum.VT_CLSID:
            factory_func = GUID.from_stream

        elif ptype == varenum.VT_VERSIONED_STREAM:
            factory_func = VersionedStream.from_stream

        elif ptype == varenum.VT_VARIANT:
            factory_func = PropertyFactory.make

        else:
            raise ValueError("Invalid property type 0x{0:X}".format(ptype))
        # end if

        values = list()
        counter = 0
        tot_size = 0

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        stream_size = stream.size
        try:
            while (counter < count) and (offset < stream_size):
                element = factory_func(stream, offset, decoder)
                offset += element.size
                tot_size += element.size

                if is_lpstr and isinstance(element.value, str):
                    element = CodePageString((
                        element.size, element.value.split("\x00", 1)[0]
                    ))
                    # end if
                # end if

                values.append(element)
                counter += 1
            # end while
        except ValueError:
            pass
        # end try

        tot_size = (tot_size + 3) & ~0x3

        return cls((tot_size, values))
    # end def from_stream

    @classmethod
    def from_factory(cls, stream, factory, count, offset=None, decoder=None):
        """Creates a sequence of various properties, given a factory.

        .. note::

            It is up to the calling function to round the size up to the
            nearest multiple of 4 (if necessary).

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the sequence.

        :type factory: ``function``
        :param factory: A factory function to create the properties.  This
                        function must accept the same arguments as
                        :func:`TypedPropertyValue.from_stream`.

        :type count: ``int``
        :param count: The number of elements in the sequence.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode string properties.

        :rtype: :class:`Sequence`
        :returns: The corresponding :class:`Sequence` object.

        """
        values = list()
        counter = 0
        tot_size = 0

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        stream_size = stream.size
        try:
            while (counter < count) and (offset < stream_size):
                element = factory(stream, offset, decoder)
                offset += element.size
                tot_size += element.size

                values.append(element)
                counter += 1
            # end while
        except ValueError:
            pass
        # end try

        return cls((tot_size, values))
    # end def from_factory
# end class Sequence

class TypedPropertyValue(PropertyPacket):
    """Base class for TypedPropertyValue packets.

    .. attribute:: type

        The property type.

    .. attribute:: _ctype

        A :class:`ctypes` ctype used to extract the various properties.

    """

    _fields_ = ("type", "size", "value")

    _takes_stream = True
    _ctype = typed_property_value_header

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a TypedPropertyValue object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`TypedPropertyValue`
        :returns: The corresponding :class:`TypedPropertyValue` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        size = sizeof(cls._ctype)
        header = cls._ctype.from_buffer_copy(stream.read(size))

        if hasattr(header, "value"):
            value = header.value
        else:
            value = None
        # end if

        return cls((header.type, size, value))
    # end def from_stream
# end class TypedPropertyValue

class VT_EMPTY(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_EMPTY`."""

    pass
# end class VT_EMPTY

class VT_NULL(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_NULL`."""

    pass
# end class VT_NULL

class VT_I2(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_I2`."""

    _ctype = typed_property_value_vt_i2
# end class VT_I2

class VT_I4(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_I4`."""

    _ctype = typed_property_value_vt_i4
# end class VT_I4

class VT_R4(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_R4`."""

    _ctype = typed_property_value_vt_r4
# end class VT_R4

class VT_R8(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_R8`."""

    _ctype = typed_property_value_vt_r8
# end class VT_R8

class VT_CY(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_CY`."""

    _ctype = typed_property_value_vt_cy

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_CY object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`VT_CY`
        :returns: The corresponding :class:`VT_CY` object.

        """
        tpv = super(VT_CY, cls).from_stream(stream, offset)

        value = Decimal(tpv.value) / Decimal(10000)
        return cls((tpv.type, tpv.size, value))
    # end def from_stream
# end class VT_CY

class VT_DATE(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_DATE`."""

    _ctype = typed_property_value_vt_date

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_DATE object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`VT_DATE`
        :returns: The corresponding :class:`VT_DATE` object.

        """
        tpv = super(VT_DATE, cls).from_stream(stream, offset, decoder)

        try:
            value = VariantTimeTodatetime.from_float(tpv.value)
        except (ValueError, TypeError):
            value = tpv.value
        # end try

        return cls((tpv.type, tpv.size, value))
    # end def from_stream
# end class VT_DATE

class VT_LPSTR(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_LPSTR`.

    .. note::

        The :attr:`value` attribute is the :attr:`value` attribute from a
        :class:`CodePageString` object.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_LPSTR object from a stream.

        .. note::

            If a decoder is specified, then the string will be decoded and
            trimmed to the first null terminator (if found).

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`VT_LPSTR`
        :returns: The corresponding :class:`VT_LPSTR` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_LPSTR, cls).from_stream(stream, offset, decoder)
        cps = CodePageString.from_stream(stream, offset + 4, decoder)
        value = cps.value

        if isinstance(value, str):
            value = value.split("\x00", 1)[0]
        # end if

        return cls((tpv.type, cps.size + 4, value))
    # end def from_stream
# end class VT_LPSTR

class VT_ERROR(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_ERROR`.

    .. note::

        The :attr:`value` attribute is an instance of a
        :class:`~lf.win.ctypes.HRESULT` class.

    """

    _ctype = typed_property_value_vt_error

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_ERROR object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`VT_ERROR`
        :returns: The corresponding :class:`VT_ERROR` object.

        """
        tpv = super(VT_ERROR, cls).from_stream(stream, offset)
        hresult = HRESULT.from_ctype(tpv.value)

        return cls((tpv.type, tpv.size, hresult.value))
    # end def from_stream
# end class VT_ERROR

class VT_BOOL(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_BOOL`."""

    _ctype = typed_property_value_vt_ui2
# end class VT_BOOL

class VT_DECIMAL(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_DECIMAL`."""

    _ctype = typed_property_value_vt_decimal

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_DECIMAL object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`VT_DECIMAL`
        :returns: The corresponding :class:`VT_DECIMAL` object.

        """
        tpv = super(VT_DECIMAL, cls).from_stream(stream, offset)
        decimal = DECIMALToDecimal.from_ctype(tpv.value)

        return cls((tpv.type, tpv.size, decimal))
    # end def from_stream
# end class VT_DECIMAL

class VT_I1(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_I1`."""

    _ctype = typed_property_value_vt_i1
# end class VT_I1

class VT_UI1(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_UI1`."""

    _ctype = typed_property_value_vt_ui1
# end class VT_UI1

class VT_UI2(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_UI2`."""

    _ctype = typed_property_value_vt_ui2
# end class VT_UI2

class VT_UI4(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_UI4`."""

    _ctype = typed_property_value_vt_ui4
# end class VT_UI4

class VT_I8(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_I8`."""

    _ctype = typed_property_value_vt_i8
# end class VT_I8

class VT_UI8(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_UI8`."""

    _ctype = typed_property_value_vt_ui8
# end class VT_UI8

class VT_INT(VT_I4):
    """Typed value :const:`~lf.win.ole.varenum.VT_INT`."""

    pass
# end class VT_INT

class VT_UINT(VT_UI4):
    """Typed value :const:`~lf.win.ole.varenum.VT_UINT`."""

    pass
# end class VT_UINT

class VT_BSTR(TypedPropertyValue):
    """
    Represents a TypedPropertyValue with type set to VT_BSTR

    NOTE: If a decoder is specified, then the string is attempted to be
    decoded.  However it is not trimmed, since the string may contain embedded
    NULLs.
    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_BSTR object from a stream.

        .. note::

            If a decoder is specified, then the string will be decoded.  Unlike
            :class:`VT_LPSTR` classes, the string is *not* trimmed, since it
            may contain embedded NULLs.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`VT_BSTR`
        :returns: The corresponding :class:`VT_BSTR` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_BSTR, cls).from_stream(stream, offset)
        cps = CodePageString.from_stream(stream, offset + 4, decoder)

        return cls((tpv.type, cps.size + 4, cps.value))
    # end def from_stream
# end class VT_BSTR

class VT_LPWSTR(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_LPWSTR`."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=_utf16_le_decoder):
        """Creates a VT_LPWSTR object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec, used only if the property requires a
                        decoder.

        :rtype: :class:`VT_LPWSTR`
        :returns: The corresponding :class:`VT_LPWSTR` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_LPWSTR, cls).from_stream(stream, offset)
        uni_str = UnicodeString.from_stream(stream, offset + 4, decoder)

        return cls((tpv.type, uni_str.size + 4, uni_str.value))
    # end def from_stream
# end class VT_LPWSTR

class VT_FILETIME(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_FILETIME`."""

    _ctype = typed_property_value_vt_filetime

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_FILETIME object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`VT_FILETIME`
        :returns: The corresponding :class:`VT_FILETIME` object.

        """
        tpv = super(VT_FILETIME, cls).from_stream(stream, offset)

        try:
            value = FILETIMETodatetime.from_ctype(tpv.value)
        except (ValueError, TypeError):
            value = (tpv.value.hi << 32) | tpv.value.lo
        # end try

        return cls((tpv.type, tpv.size, value))
    # end def from_stream
# end class VT_FILETIME

class VT_BLOB(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_BLOB`."""

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_BLOB object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`VT_BLOB`
        :returns: The corresponding :class:`VT_BLOB` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_BLOB, cls).from_stream(stream, offset)
        blob = BLOB.from_stream(stream, offset + 4)

        return cls((tpv.type, blob.size + 4, blob.value))
    # end def from_stream
# end class VT_BLOB

class VT_STREAM(VT_BSTR):
    """Typed value :const:`~lf.win.ole.varenum.VT_STREAM`."""

    pass
# end class VT_STREAM

class VT_STORAGE(VT_BSTR):
    """Typed value :const:`~lf.win.ole.varenum.VT_STORAGE`."""

    pass
# end class VT_STORAGE

class VT_STREAMED_OBJECT(VT_BSTR):
    """Typed value :const:`~lf.win.ole.varenum.VT_STREAMED_OBJECT`."""

    pass
# end class VT_STREAMED_OBJECT

class VT_STORED_OBJECT(VT_BSTR):
    """Typed value :const:`~lf.win.ole.varenum.VT_STORED_OBJECT`."""

    pass
# end class VT_STORED_OBJECT

class VT_BLOB_OBJECT(VT_BLOB):
    """Typed value :const:`~lf.win.ole.varenum.VT_BLOB_OBJECT`."""

    pass
# end class VT_BLOB_OBJECT

class VT_CF(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_CF`.

    .. attribute:: value

        An instance of :class:`ClipboardData`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_CF object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`VT_CF`
        :returns: The corresponding :class:`VT_CF` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_CF, cls).from_stream(stream, offset)
        cd = ClipboardData.from_stream(stream, offset + 4)

        return cls((tpv.type, cd.size + 4, cd))
    # end def from_stream
# end class VT_CF

class VT_CLSID(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_CLSID`."""

    _ctype = typed_property_value_vt_clsid

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_CLSID object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`VT_CLSID`
        :returns: The corresponding :class:`VT_CLSID` object.

        """
        tpv = super(VT_CLSID, cls).from_stream(stream, offset)
        guid = GUIDToUUID.from_ctype(tpv.value)

        return cls((tpv.type, tpv.size, guid))
    # end def from_stream
# end class VT_CLSID

class VT_VERSIONED_STREAM(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_VERSIONED_STREAM`.

    .. attribute:: value

        An instance of a :class:`VersionedStream` object.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_VERSIONED_STREAM object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode string properties.

        :rtype: :class:`VT_VERSIONED_STREAM`
        :returns: The corresponding :class:`VT_VERSIONED_STREAM` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_VERSIONED_STREAM, cls).from_stream(stream, offset)
        vs = VersionedStream.from_stream(stream, offset + 4, decoder)

        return cls((tpv.type, vs.size + 4, vs))
    # end def from_stream
# end class VT_VERSIONED_STREAM

class VT_ARRAY(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_ARRAY`.

    .. attribute:: value

        An instance of a :class:`Array` object.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_ARRAY object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode string properties.

        :rtype: :class:`VT_ARRAY`
        :returns: The corresponding :class:`VT_ARRAY` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_ARRAY, cls).from_stream(stream, offset)
        value = Array.from_stream(stream, offset + 4, decoder)

        return cls((tpv.type, value.size + 4, value))
    # end def from_stream
# end class VT_ARRAY

class VT_VECTOR(TypedPropertyValue):
    """Typed value :const:`~lf.win.ole.varenum.VT_VECTOR`.

    .. attribute:: value

        An instance of a :class:`Vector` object.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a VT_VECTOR object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode string properties.

        :rtype: :class:`VT_VECTOR`
        :returns: The corresponding :class:`VT_VECTOR` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VT_VECTOR, cls).from_stream(stream, offset)
        scalar_type = tpv.type & (~varenum.VT_VECTOR)
        vector = Vector.from_stream(stream, scalar_type, offset + 4, decoder)

        return cls((tpv.type, (vector.size + 4), vector))
    # end def from_stream
# end class VT_VECTOR

class PropertyFactory():
    """A class that makes properties."""

    @classmethod
    def make(cls, stream, offset=None, decoder=None):
        """Makes a property object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the property structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode string properties.

        :rtype: :class:`PropertyPacket`
        :returns: The corresponding :class:`PropertyPacket` (or subclass)
                  object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        property = TypedPropertyValue.from_stream(stream, offset)
        ptype = property.type

        if ptype & varenum.VT_VECTOR:
            property = VT_VECTOR.from_stream(stream, offset, decoder)
        elif ptype & varenum.VT_ARRAY:
            property = VT_ARRAY.from_stream(stream, offset, decoder)
        elif ptype in _property_dispatcher:
            factory_func = _property_dispatcher[ptype]
            property = factory_func(stream, offset, decoder)
        # end if

        return property
    # end def make
# end class PropertyFactory

# Class used by Builder
class PropertySet(Packet, Structuple):
    """Represents a PropertySet structure (packet).

    .. attribute:: size

        The size in bytes of the PropertySetHeader structure.

    .. attribute:: pair_count

        The nubmer of pid/offset pairs.

    .. attribute:: pids_offsets

        A dictionary of property identifiers and the offsets of the
        corresponding properties.

    .. attribute:: properties

        A dictionary of property identifiers and the corresponding properties.

    """

    _fields_ = ("size", "pair_count", "pids_offsets", "properties")
# end class PropertySet

class PropertySetStream(Packet, Structuple):
    """Represents a PropertySetStream structure (packet).

    .. attribute:: byte_order

        The byte order field.

    .. attribute:: version

        The version of the OLE property set.

    .. attribute:: sys_id

        The system identifier field.

    .. attribute:: clsid

        The CLSID of the associated property set(s).

    .. attribute:: property_set_count

        The number of property sets in the stream.

    .. attribute:: fmtid0

        A GUID that identifies the property set format of the first property
        set.  If there are no property sets, this should be ``None``.

    .. attribute:: offset0

        The offset of the first property set, relative to the start of the
        :class:`PropertySetStreamHeader` structure.  If there are no property

    .. attribute:: fmtid1

        A GUID that idientifies the property set format of the second property
        set.  If there is only one property set, this should be ``None``.

    .. attribute:: offset1

        The offset of the second property set, relative to the start of the
        :class:`PropertySetStreamHeader` structure.  If there is only one
        property set, this should be ``None``.

    .. attribute:: property_set_0

        An instance of :class:`PropertySet` that represents the first property
        set.  If there are no property sets, this should be ``None``.

    .. attribute:: property_set_1

        An instance of :class:`PropertySet` that represents the second property
        set.  If there are no property sets, this should be ``None``.

    """

    _fields_ = (
        "byte_order", "version", "sys_id", "clsid", "property_set_count",
        "fmtid0", "offset0", "fmtid1", "offset1", "property_set_0",
        "property_set_1"
    )
    __slots__ = tuple()
# end class PropertySetStream

class Builder():
    """Builds property set streams."""

    @classmethod
    def build(cls, stream, offset=None, decoder=None):
        """Builds property set streams from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the property (and related)
                       structures.

        :type offset: ``int``
        :param offset: The start of the structures in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: An optional codec to decode string properties.  If this
                        value is ``None``, one is guessed by using the CodePage
                        property.

        :rtype: :class:`PropertySetStream`
        :returns: The corresponding :class:`PropertySetStream` object.

        """
        fmtids = list()
        property_set_headers = list()
        property_set_offsets = list()
        property_sets = list()
        properties = list()

        if offset is None:
            offset = stream.tell()
        # end if

        header = cls.build_property_set_stream_header(stream, offset)

        if header.property_set_count:
            fmtids.append(header.fmtid0)
            property_set_offsets.append(offset + header.offset0)

            if header.property_set_count > 1:
                fmtids.append(header.fmtid1)
                property_set_offsets.append(offset + header.offset1)
            # end if
        # end if

        for (fmtid, property_set_offset) in zip(fmtids, property_set_offsets):
            property_set_headers.append(cls.build_property_set_header(
                stream, fmtid, property_set_offset
            ))
        # end for

        iter = zip(property_set_headers, fmtids)
        for (index, (property_set, fmtid)) in enumerate(iter):
            property_set_offset = property_set_offsets[index]

            properties.append(cls.build_properties(
                stream, fmtid, property_set, property_set_offset, decoder
            ))
        # end for

        for (index, property_set_header) in enumerate(property_set_headers):
            property_sets.append(PropertySet((
                property_set_header.size,
                property_set_header.pair_count,
                property_set_header.pids_offsets,
                properties[index]
            )))
        # end for

        property_set_0 = property_sets[0]
        if len(property_sets) > 1:
            property_set_1 = property_sets[1]
        else:
            property_set_1 = None
        # end if

        return PropertySetStream((
            header.byte_order,
            header.version,
            header.sys_id,
            header.clsid,
            header.property_set_count,
            header.fmtid0,
            header.offset0,
            header.fmtid1,
            header.offset1,
            property_set_0,
            property_set_1
        ))
    # end def build

    @classmethod
    def build_property_set_stream_header(cls, stream, offset=None):
        """Builds a :class:`PropertySetStreamHeader` object.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`PropertySetStreamHeader`
        :returns: The corresponding :class:`PropertySetStreamHeader` object.

        """

        return PropertySetStreamHeader.from_stream(stream, offset)
    # end def build_property_set_stream_header

    @classmethod
    def build_property_set_header(cls, stream, fmtid, offset=None):
        """Builds a :class:`PropertySetHeader` object.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the property set header
                       structure.

        :type fmtid: :class:`UUID`
        :param fmtid: The FMTID of the property set.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`PropertySetHeader`
        :returns: The corresponding :class:`PropertySetHeader` object.

        """

        return PropertySetHeader.from_stream(stream, offset)
    # end def build_property_set_header

    @classmethod
    def build_properties(
        cls, stream, fmtid, property_set, offset=None, decoder=None
    ):
        """Builds a dictionary of :class:`PropertyPacket` objects.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the property structures.

        :type fmtid: :class:`UUID`
        :param fmtid: The FMTID of the property set.

        :type property_set: :class:`PropertySetHeader`
        :param property_set: A :class:`PropertySetHeader` object that describes
                             the properties in the property set.

        :type offset: ``int``
        :param offset: The start of the structures in :attr:`stream`.

        :type decoder: :class:`codecs.codec`
        :param decoder: A codec to decode string properties.

        :rtype: ``dict``
        :returns: A dictionary of property identifiers (keys) and the
                  corresponding :class:`PropertyPacket` objects (values).

        """

        pids_offsets = property_set.pids_offsets
        make = PropertyFactory.make
        properties = dict()

        if offset is None:
            offset = stream.tell()
        # end if

        code_page = None
        if CODEPAGE_PROPERTY_IDENTIFIER in pids_offsets:
            property_offset = pids_offsets[CODEPAGE_PROPERTY_IDENTIFIER]
            code_page = make(stream, property_offset + offset)
            code_page = code_page.value

            if code_page < 0:  # Not sure why this isn't type VT_UI2
                code_page = 0xFFFF + code_page + 1
            # end if

            if (code_page in code_page_names) and (decoder is None):
                try:
                    decoder = getdecoder(code_page_names[code_page])
                except LookupError:
                    pass
                # end try
            # end if
        # end if

        for (pid, property_offset) in pids_offsets.items():
            property_offset += offset

            if pid == DICTIONARY_PROPERTY_IDENTIFIER:
                property = Dictionary.from_stream(
                    stream, property_offset, code_page, decoder
                )
            else:
                property = make(stream, property_offset, decoder)
            # end if

            properties[pid] = property
        # end for

        return properties
    # end def build_properties
# end class Builder

# Dispatcher: property type -> class
_property_dispatcher = {
    varenum.VT_EMPTY: VT_EMPTY.from_stream,
    varenum.VT_NULL: VT_NULL.from_stream,
    varenum.VT_I2: VT_I2.from_stream,
    varenum.VT_I4: VT_I4.from_stream,
    varenum.VT_R4: VT_R4.from_stream,
    varenum.VT_R8: VT_R8.from_stream,
    varenum.VT_CY: VT_CY.from_stream,
    varenum.VT_DATE: VT_DATE.from_stream,
    varenum.VT_BSTR: VT_BSTR.from_stream,
    varenum.VT_ERROR: VT_ERROR.from_stream,
    varenum.VT_BOOL: VT_BOOL.from_stream,
    varenum.VT_DECIMAL: VT_DECIMAL.from_stream,
    varenum.VT_I1: VT_I1.from_stream,
    varenum.VT_UI1: VT_UI1.from_stream,
    varenum.VT_UI2: VT_UI2.from_stream,
    varenum.VT_UI4: VT_UI4.from_stream,
    varenum.VT_I8: VT_I8.from_stream,
    varenum.VT_UI8: VT_UI8.from_stream,
    varenum.VT_INT: VT_INT.from_stream,
    varenum.VT_UINT: VT_UINT.from_stream,
    varenum.VT_LPSTR: VT_LPSTR.from_stream,
    varenum.VT_LPWSTR: VT_LPWSTR.from_stream,
    varenum.VT_FILETIME: VT_FILETIME.from_stream,
    varenum.VT_BLOB: VT_BLOB.from_stream,
    varenum.VT_STREAM: VT_STREAM.from_stream,
    varenum.VT_STORAGE: VT_STORAGE.from_stream,
    varenum.VT_STREAMED_OBJECT: VT_STREAMED_OBJECT.from_stream,
    varenum.VT_STORED_OBJECT: VT_STORED_OBJECT.from_stream,
    varenum.VT_BLOB_OBJECT: VT_BLOB_OBJECT.from_stream,
    varenum.VT_CF: VT_CF.from_stream,
    varenum.VT_CLSID: VT_CLSID.from_stream,
    varenum.VT_VERSIONED_STREAM: VT_VERSIONED_STREAM.from_stream,
    varenum.VT_VARIANT: PropertyFactory.make
}

# Property types that don't require special handling, when dealing with
# sequences.
_simple_property_types = {
    # type: (size in bytes, ctype)
    varenum.VT_I2: (2, int16_le),
    varenum.VT_I4: (4, int32_le),
    varenum.VT_R4: (4, float32_le),
    varenum.VT_R8: (8, float64_le),
    varenum.VT_BOOL: (2, uint16_le),
    varenum.VT_I1: (1, int8),
    varenum.VT_UI1: (1, uint8),
    varenum.VT_UI2: (2, uint16_le),
    varenum.VT_UI4: (4, uint32_le),
    varenum.VT_I8: (8, int64_le),
    varenum.VT_UI8: (8, uint64_le),
    varenum.VT_INT: (4, int32_le),
    varenum.VT_UINT: (4, uint32_le)
}
