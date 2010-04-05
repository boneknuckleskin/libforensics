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

"""Shared objects for Microsoft Office property sets."""

# stdlib imports
from codecs import getdecoder

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import ActiveStructuple
from lf.dtypes.ctypes import uint32_le

from lf.win.codepage.consts import CP_WINUNICODE, code_page_names

from lf.win.ole.ps.consts import (
    PropertyType, FMTID_SummaryInformation, FMTID_DocSummaryInformation,
    CODEPAGE_PROPERTY_IDENTIFIER, DICTIONARY_PROPERTY_IDENTIFIER
)
from lf.win.ole.ps import (
    ClipboardData, VT_CF, CodePageString, ValuePacket, UnicodeString,
    TypedPropertyValue, Sequence, VT_I4, Dictionary, Vector, BLOB
)
from lf.win.ole.ps import (
    PropertySetStreamHeader as _oleps_PropertySetStreamHeader,
    PropertyFactory as _oleps_PropertyFactory,
    Builder as _oleps_Builder
)

from lf.apps.msoffice.shared.consts import PIDSI, PIDDSI
from lf.apps.msoffice.shared.ctypes import (
    property_set_system_identifier, dig_sig_info_serialized_header,
    dig_sig_blob_header, vt_hyperlink_header
)

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertySetSystemIdentifier", "VtThumbnailValue", "VtThumbnail", "Lpstr",
    "UnalignedLpstr", "VtVecUnalignedLpstrValue", "VtVecUnalignedLpstr",
    "Lpwstr", "VtVecLpwstrValue", "VtVecLpwstr", "VtString",
    "VtUnalignedString", "VtHeadingPair", "VtVecHeadingPairValue",
    "VtVecHeadingPair", "VtDigSigValue", "VtDigSig", "VtHyperlink",
    "VtHyperlinkValue", "VecVtHyperlink", "VtHyperlinkValue", "VtHyperlinks",
    "DigSigBlob", "DigSigInfoSerialized", "PropertySetStreamHeader",
    "PropertyFactory", "Builder"
]

# module globals
_utf16_le_decoder = getdecoder("utf_16_le")

class PropertySetSystemIdentifier(ActiveStructuple):
    """Represents a PropertySetSystemIdentifier structure.

    .. attribute:: os_ver_major

        The major version number of the operating system that wrote the
        property set.

    .. attribute:: os_ver_minor

        The minor version number of the operating system that wrote the
        property set.

    .. attribute:: os_type

        The os type field.

    """
    _fields_ = ("os_ver_major", "os_ver_minor", "os_type")
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`PropertySetSystemIdentifier` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`PropertySetSystemIdentifier`
        :returns: The corresponding :class:`PropertySetSystemIdentifier`
                  object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        pssi = property_set_system_identifier.from_buffer_copy(stream.read(4))

        return cls((pssi.os_ver_major, pssi.os_ver_minor, pssi.os_type))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a :class:`PropertySetSystemIdentifier` from a ctype.

        :type ctype: |pssid|
        :param ctype: An instance of a |pssid|

        """
        return cls((ctype.os_ver_major, ctype.os_ver_minor, ctype.os_type))
    # end def from_ctype
# end class PropertySetSystemIdentifier

class VtThumbnailValue(ClipboardData):
    """ Represents a VtThumbnailValue structure.

    .. attribute:: data

        The data for the thumbnail image.  If :attr:`tag` is 0, then this field
        will contain whatever data is between the :attr:`tag` field and the end
        of the packet.

    .. attribute:: tag

        The value of the cftag field. This is the format field from the
        :class:`~lf.win.ole.ps.VT_CF` type.  If this value is 0, then the
        :attr:`format_id` attribute is ``None``.

    .. attribute:: format_id

        The format of the data in :attr:`data`.

    .. attribute:: value

        An alias for the :attr:`data` attribute.

    .. attribute:: format

        An alias for the :attr:`tag` attribute.

    """
    _fields_ = ("data", "tag", "format_id")
    _aliases_ = {"value": "data", "format": "tag"}
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`VtThumbnailValue` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`VtThumbnailValue`
        :returns: The corresponding :class:`VtThumbnailValue` object.

        """
        cd = super(VtThumbnailValue, cls).from_stream(stream, offset)

        format = uint32_le.from_buffer_copy(cd.format).value

        if format != 0:
            format_id = uint32_le.from_buffer_copy(cd.data[:4]).value
            data = cd.data[4:]
        else:
            format_id = None
            data = cd.data
        # end if

        format = uint32_le.from_buffer_copy(cd.format).value

        return cls((cd.size, data, format, format_id))
    # end def from_stream
# end class VtThumbnailValue

class VtThumbnail(VT_CF):
    """Represents a VtThumbnail structure (packet).

    .. attribute:: value

        An instance of :class:`VtThumbnailValue`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtThumbnail` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``None``
        :param decoder: This parameter is not used.

        :rtype: :class:`VtThumbnail`
        :returns: The corresponding :class:`VtThumbnail` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        vt_cf = super(VtThumbnail, cls).from_stream(stream, offset)
        vttv = VtThumbnailValue.from_stream(stream, offset+4)

        return cls((vt_cf.type, vttv.size + 4, vttv))
    # end def from_stream
# end class VtThumbnail

class Lpstr(CodePageString):
    """Represents an Lpstr structure (packet).

    .. note::

        This is essentially a :class:`~lf.win.ole.ps.CodePageString` that if
        properly decoded, is truncated at the first NULL character.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates an :class:`Lpstr` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`Lpstr`
        :returns: The corresponding :class:`Lpstr` object.

        """
        cps = super(Lpstr, cls).from_stream(stream, offset, decoder)

        if isinstance(cps.value, str):
            value = cps.value.split("\x00", 1)[0]
        else:
            value = cps.value
        # end if

        return cls((cps.size, value))
    # end def from_stream
# end class Lpstr

class UnalignedLpstr(CodePageString):
    """Represents an UnalignedLpstr structure (packet).

    .. note::

        This is similar to a :class:`~lf.win.ole.ps.CodePageString`, except
        that it is NULL terminated and does *not* have padding.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates an :class:`UnalignedLpstr` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`UnalignedLpstr`
        :returns: The corresponding :class:`UnalignedLpstr` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        size = uint32_le.from_buffer_copy(stream.read(4)).value
        value = stream.read(size)

        if decoder:
            new_value = decoder(value, "ignore")[0]
            if new_value:
                value = new_value.split("\x00", 1)[0]
            # end if
        # end if

        return cls((size + 4, value))
    # end def from_stream
# end class UnalignedLpstr


class VtVecUnalignedLpstrValue(Vector):
    """Represents a VtVecUnalignedLpstrValue structure (packet).

    .. note::

        This is effectively a
        (:class:`~lf.win.ole.ps.VT_VECTOR` | :class:`~lf.win.ole.ps.VT_LPSTR`)
        with :class:`UnalignedLpstr` strings.

    .. attribute:: value

        A list of (unaligned) strings.

    .. attribute:: scalar_count

        The number of strings in the data.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtVecUnalignedLpstrValue` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecUnalignedLpstrValue`
        :returns: The corresponding :class:`VtVecUnalignedLpstrValue` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        seq = Sequence.from_factory(
            stream, UnalignedLpstr.from_stream, count, offset + 4, decoder
        )

        return cls((seq.size + 4, seq.value, count))
    # end def from_stream
# end class VtVecUnalignedLpstrValue

class VtVecUnalignedLpstr(TypedPropertyValue):
    """Represents a VtVecUnalignedLpstr structure (packet).

    .. attribute:: value

        An instance of :class:`VtVecUnalignedLpstrValue`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtVecUnalignedLpstr` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecUnalignedLpstr`
        :returns: The corresponding :class:`VtVecUnalignedLpstr` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtVecUnalignedLpstr, cls).from_stream(
            stream, offset, decoder
        )

        if tpv.type == 0x101E:  # VT_VECTOR | VT_LPSTR
            value = VtVecUnalignedLpstrValue.from_stream(
                stream, offset + 4, decoder
            )
            size = value.size + 4
        else:
            size = tpv.size
            value = tpv.value
            count = None
        # end if

        return cls((tpv.type, size, value))
    # end def from_stream
# end class VtVecUnalignedLpstr:


class Lpwstr(UnicodeString):
    """ Represents a Lpwstr structure (packet).

    .. note::

        This class is essentially a :class:`~lf.win.ole.ps.UnicodeString`
        class, but was included for purposes of completeness.

    """
    pass
# end class Lpwstr

class VtVecLpwstrValue(Vector):
    """ Represents a VtVecLpwstrValue structure (packet).

    .. note::

        This class is essentially a :class:`~lf.win.ole.ps.Vector` class that
        has a hard coded scalar type of :class:`Lpwstr`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtVecLpwstrValue` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecLpwstrValue`
        :returns: The corresponding :class:`VtVecLpwstrValue` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        seq = Sequence.from_factory(
            stream, Lpwstr.from_stream, count, offset + 4, decoder
        )
        values = [value.value for value in seq.value]

        return cls((seq.size + 4, values, count))
    # end def from_stream
# end class VtVecLpwstrValue

class VtVecLpwstr(TypedPropertyValue):
    """Represents a VtVecLpwstr structure (packet).

    .. note::

        This is essentially a (:class:`~lf.win.ole.ps.VT_VECTOR` |
        :class:`~lf.win.ole.ps.VT_LPWSTR`) TPV type, except
        :class:`VtVecLpwstrValue` objects are used instead.

    .. attribute:: value

        A list of :class:`VtVecLpwstrValue` objects.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtVecLpwstr` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecLpwstr`
        :returns: The corresponding :class:`VtVecLpwstr` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtVecLpwstr, cls).from_stream(stream, offset, decoder)

        if tpv.type == 0x101F:  # VT_VECTOR | VT_LPWSTR
            value = VtVecLpwstrValue.from_stream(stream, offset + 4, decoder)
            size = value.size + 4
        else:
            value = tpv.value
            size = tpv.size
        # end if

        return cls((tpv.type, size, value))
    # end def from_stream
# end class VtVecLpwstr:

class VtString(TypedPropertyValue):
    """Represents a VtString structure (packet).

    .. attribute:: value

        The value of either :class:`Lpstr` or :class:`Lpwstr` objects,
        depending on the :attr:`type` attribute.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtString` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtString`
        :returns: The corresponding :class:`VtString` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtString, cls).from_stream(stream, offset, decoder)

        if tpv.type == PropertyType.VT_LPSTR:
            string = Lpstr.from_stream(stream, offset + 4, decoder)
            size = string.size + 4
            value = string.value
        elif tpv.type == PropertyType.VT_LPWSTR:
            string = Lpwstr.from_stream(stream, offset + 4, decoder)
            size = string.size + 4
            value = string.value
        else:
            size = 4
            value = None
        # end if

        return cls((tpv.type, size, value))
    # end def from_stream
# end class VtString

class VtUnalignedString(TypedPropertyValue):
    """Represents a VtUnalignedString structure (packet).

    .. attribute:: value

        The value of either :class:`UnalignedLpstr` or :class:`Lpwstr` objects,
        depending on the :attr:`type` attribute.

    .. attribute:: str_type

        An alias for the :attr:`type` field.

    .. attribute:: str_value

        An alias for the :attr:`value` field.

    """
    _aliases_ = {"str_type": "type", "str_value": "value"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtUnalignedString` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtUnalignedString`
        :returns: The corresponding :class:`VtUnalignedString` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtUnalignedString, cls).from_stream(stream, offset, decoder)

        if tpv.type == PropertyType.VT_LPSTR:
            string = UnalignedLpstr.from_stream(stream, offset + 4, decoder)
            size = string.size + 4
            value = string.value
        elif tpv.type == PropertyType.VT_LPWSTR:
            string = Lpwstr.from_stream(stream, offset + 4, decoder)
            size = string.size + 4
            value = string.value
        else:
            size = 4
            value = None
        # end if

        return cls((tpv.type, size, value))
    # end def from_stream
# end class VtUnalignedString

class VtHeadingPair(ValuePacket):
    """Represents a VtHeadingPair structure (packet).

    .. attribute:: heading_str

        The header string as a :class:`VtUnalignedString`.

    .. attribute:: header_parts_count

        A :class:`~lf.win.ole.ps.VT_I4` instance, where the
        :attr:`~lf.win.ole.ps.VT_I4.value` attribute is the number of document
        parts associated with the header.

    .. attribute:: value

        An alias for the :attr:`heading_str` attribute.

    """
    _takes_stream = True
    _fields_ = ("heading_str", "header_parts")
    _aliases_ = {"value": "heading_str"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtHeadingPair` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtHeadingPair`
        :returns: The corresponding :class:`VtHeadingPair` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        vtus = VtUnalignedString.from_stream(stream, offset, decoder)
        vt_i4 = VT_I4.from_stream(stream, offset + vtus.size)

        return cls((vtus.size + 8, vtus, vt_i4))
    # end def from_stream
# end class VtHeadingPair


class VtVecHeadingPairValue(Vector):
    """Represents a VtVecHeadingPairValue structure (packet).

    .. note::

        This class is a :class:`~lf.win.ole.ps.Vector` class that has a hard
        coded scalar type of :class:`VtHeadingPair`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtVecHeadingPairValue` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecHeadingPairValue`
        :returns: The corresponding :class:`VtVecHeadingPairValue` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        seq_count = count // 2

        seq = Sequence.from_factory(
            stream, VtHeadingPair.from_stream, seq_count, offset + 4, decoder
        )

        return cls((seq.size + 4, seq.value, count))
    # end def from_stream
# end class VtVecHeadingPairValue

class VtVecHeadingPair(TypedPropertyValue):
    """ Represents a VtVecHeadingPair structure (packet).

    .. attribute:: value

        An instance of a :class:`VtVecHeadingPairValue`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtVecHeadingPair` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecHeadingPair`
        :returns: The corresponding :class:`VtVecHeadingPair` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtVecHeadingPair, cls).from_stream(stream, offset, decoder)

        if tpv.type == 0x100C:  # VT_VECTOR | VT_LPWSTR
            value = VtVecHeadingPairValue.from_stream(
                stream, offset + 4, decoder
            )
            count = value.scalar_count
            size = value.size + 4
        else:
            size = tpv.size
            value = tpv.value
            count = None
        # end if

        return cls((tpv.type, size, value))
    # end def from_stream
# end class VtVecHeadingPair:

class VtDigSigValue(ValuePacket):
    """Represents a VtDigSigValue structure (packet).

    .. attribute:: value

        An instance of :class:`DigSigBlob`.

    """
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=_utf16_le_decoder):
        """Creates a :class:`VtDigSigValue` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtDigSigValue`
        :returns: The corresponding :class:`VtDigSigValue` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        size = uint32_le.from_buffer_copy(stream.read(4)).value
        value = DigSigBlob.from_stream(stream, offset + 4, decoder)

        return cls((size, value))
    # end def from_stream
# end class VtDigSigValue

class VtDigSig(TypedPropertyValue):
    """Represents a VtDigSig structure (packet).

    .. attribute:: value

        An instance of :class:`VtDigSigValue`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=_utf16_le_decoder):
        """Creates a :class:`VtDigSig` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtDigSig`
        :returns: The corresponding :class:`VtDigSig` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtDigSig, cls).from_stream(stream, offset)
        value = VtDigSigValue.from_stream(stream, offset + 4, decoder)

        return cls((tpv.type, value.size + 4, value))
    # end def from_stream
# end class VtDigSig

class VtHyperlink(ValuePacket):
    """Represents a VtHyperlink structure (packet).

    .. attribute:: hash

        The value of the dwHash field (hash of :attr:`hlink1` and
        :attr:`hlink2`)

    .. attribute:: app

        The value of the dwApp field.

    .. attribute:: office_art

        The value of the dwOfficeArt field.

    .. attribute:: info

        The value of the dwInfo field.

    .. attribute:: hlink1

        The hyperlink target.

    .. attribute:: hlink2

        The hyperlink location.

    .. attribute:: value

        An alias for the :attr:`hlink2` attribute.

    """
    _takes_stream = True
    _fields_ = (
        "hash", "app", "office_art", "info", "hlink1", "hlink2"
    )
    _aliases_ = {"value": "hlink2"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtHyperlink` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtHyperlink`
        :returns: The corresponding :class:`VtHyperlink` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = vt_hyperlink_header.from_buffer_copy(stream.read(32))
        offset += 32

        hlink1 = PropertyFactory.make(stream, offset, decoder)
        offset += hlink1.size

        hlink2 = PropertyFactory.make(stream, offset, decoder)

        hash = VT_I4((3, 8, header.hash.value))
        app = VT_I4((3, 8, header.app.value))
        office_art = VT_I4((3, 8, header.office_art.value))
        info = VT_I4((3, 8, header.info.value))

        return cls((
            hlink1.size + hlink2.size + 32,
            hash,
            app,
            office_art,
            info,
            hlink1,
            hlink2
        ))
    # end def from_stream
# end class VtHyperlink

class VecVtHyperlink(Vector):
    """Represents a VecVtHyperlink structure (packet).

    .. note::

        This class is a :class:`~lf.win.ole.ps.Vector` class with a scalar type
        hardcoded to :class:`VtHyperlink`.

    .. attribute:: hyperlinks

        A list of :class:`VtHyperlink` objects.

    .. attribute:: value

        An alias for the :attr:`hyperlinks` attribute.

    """

    _fields_ = ("hyperlinks",)
    _aliases_ = {"value": "hyperlinks"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VecVtHyperlink` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VecVtHyperlink`
        :returns: The corresponding :class:`VecVtHyperlink` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        count = uint32_le.from_buffer_copy(stream.read(4)).value
        offset += 4

        seq_count = count // 6
        seq = Sequence.from_factory(
            stream, VtHyperlink.from_stream, seq_count, offset, decoder
        )

        return cls((seq.size + 4, count, seq.value))
    # end def from_stream
# end class VecVtHyperlink

class VtHyperlinkValue(BLOB):
    """ Represents a VtHyperlinkValue structure (packet).

    .. attribute:: vec_hyperlinks

        An instance of :class:`VecVtHyperlink`.

    .. attribute:: value

        An alias for the :attr:`vec_hyperlinks` attribute.

    """
    _fields_ = ("hyperlinks",)
    _aliases_ = {"value": "hyperlinks"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """Creates a :class:`VtHyperlinkValue` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtHyperlinkValue`
        :returns: The corresponding :class:`VtHyperlinkValue` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        size = uint32_le.from_buffer_copy(stream.read(4)).value
        offset += 4

        value = VecVtHyperlink.from_stream(stream, offset, decoder)

        return cls((size + 4, value))
    # end def from_stream
# end class VtHyperlinkValue

class VtHyperlinks(TypedPropertyValue):
    """Represents a VtHyperlinks structure (packet).

    .. attribute:: value

        An instance of :class:`VtHyperlinkValue`.

    """

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """ Creates a :class:`VtHyperlinks` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtHyperlinks`
        :returns: The corresponding :class:`VtHyperlinks` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        tpv = super(VtHyperlinks, cls).from_stream(stream, offset, decoder)
        value = VtHyperlinkValue.from_stream(stream, offset + 4, decoder)

        return cls((tpv.type, value.size + 4, value))
    # end def from_stream
# end class VtHyperlinks

class DigSigBlob(ValuePacket):
    """Represents a DigSigBlob structure (packet).

    .. attribute:: sig_info_offset

        The offset of the :attr:`sig_info` attribute.

    .. attribute:: sig_info

        An instance of :class:`DigSigInfoSeralized`.

    .. attribute:: value

        An alias for the :attr:`sig_info` attribute.

    """
    _takes_stream = True
    _fields_ = ("sig_info_offset", "sig_info",)
    _aliases_ = {"value": "sig_info"}

    @classmethod
    def from_stream(cls, stream, offset=None, decoder=None):
        """ Creates a :class:`DigSigBlob` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`DigSigBlob`
        :returns: The corresponding :class:`DigSigBlob` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = dig_sig_blob_header.from_buffer_copy(stream.read(8))
        value = DigSigInfoSerialized.from_stream(
            stream, 0, header.sig_info_offset, decoder
        )

        size = header.data_size + 8

        return cls((size, header.sig_info_offset, value))
    # end def from_stream
# end class DigSigBlob

class DigSigInfoSerialized(ValuePacket):
    """Represents a DigSigInfoSerialized structure (packet).

    .. attribute:: sig_size

        The size of the :attr:`sig_buf` attribute.

    .. attribute:: sig_offset

        The relative offset (from the parent structure) of the :attr:`sig_buf`
        attribute.  If the parent structure is a :class:`DigSigBlob` then the
        offset is relative to the start of the parent structure.  If the parent
        structure is a ``WordSigBlob`` Then the offset is relative to the
        :attr:`cbSigInfo` field of the parent structure.

    .. attribute:: cert_store_size

        The size of the :attr:`cert_store_buf` attribute.

    .. attribute:: cert_store_offset

        The relative offset (from the parent structure) of the
        :attr:`cert_store_buf` attribute.  If the parent structure is a
        :class:`DigSigBlob` then the offset is relative to the start of the
        parent structure.  If the parent structure is a ``WordSigBlob``
        Then the offset is relative to the :attr:`cbSigInfo` field of the
        parent structure.

    .. attribute:: proj_name_size

        The size of the :attr:`proj_name_buf` attribute.

    .. attribute:: proj_name_offset

        The relative offset (from the parent structure) of the
        :attr:`proj_name_buf` attribute.  If the parent structure is a
        :class:`DigSigBlob` then the offset is relative to the start of the
        parent structure.  If the parent structure is a ``WordSigBlob``
        Then the offset is relative to the :attr:`cbSigInfo` field of the
        parent structure.

    .. attribute:: timestamp

        The value of the fTimestamp field.

    .. attribute:: timestamp_buf_size

        The size of the :attr:`timestamp_buf` attribute.

    .. attribute:: timestamp_buf_offset

        The relative offset (from the parent structure) of the
        :attr:`timestamp_buf` attribute.  If the parent structure is a
        :class:`DigSigBlob` then the offset is relative to the start of the
        parent structure.  If the parent structure is a ``WordSigBlob``
        Then the offset is relative to the :attr:`cbSigInfo` field of the
        parent structure.

    .. attribute:: sig_buf

        The VBA digital signature.

    .. attribute:: cert_store_buf

        The digital certificate information of the certificate used to create
        the digital signature.

    .. attribute:: proj_name_buf

        The rchProjectNameBuffer field.

    .. attribute:: timestamp_buf

        The rchTimestampBuffer field.

    """
    _takes_stream = True
    _fields_ = (
        "sig_size", "sig_offset", "cert_store_size", "cert_store_offset",
        "proj_name_size", "proj_name_offset", "timestamp",
        "timestamp_buf_size", "timestamp_buf_offset", "sig_buf",
        "cert_store_buf", "proj_name_buf", "timestamp_buf"
    )
    _aliases_ = {"value": "sig_buf"}

    @classmethod
    def from_stream(cls, stream, field_base, offset=None, decoder=None):
        """Creates a :class:`DigSigInfoSerialized` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type field_base: ``int``
        :param field_base: A value to add to the various offset fields, to
                           determine where the corresponding fields start.  For
                           :class:`DigSigBlob` this is the start of the
                           :class:`DigSigBlob` structure.  For ``WordSigBlob``
                           this is the start of the :attr:`sig_info` field.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`VtVecHeadingPairValue`
        :returns: The corresponding :class:`VtVecHeadingPairValue` object.

        """
        if offset is not None:
            offset = stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        start_offset = offset
        stop_offset = 36

        header = \
            dig_sig_info_serialized_header.from_buffer_copy(stream.read(36))

        stream_size = stream.size

        if decoder is None:
            decoder = _utf16_le_decoder
        # end if

        sig_offset = field_base + header.sig_offset
        if sig_offset < stream_size:
            stream.seek(sig_offset, SEEK_SET)
            sig = stream.read(header.sig_size)

            field_len = len(sig)
            if (sig_offset + field_len) > stop_offset:
                stop_offset = sig_offset + field_len
            # end if
        else:
            sig = None
        # end if

        cert_store_offset = \
            field_base + header.cert_store_offset

        if cert_store_offset < stream_size:
            stream.seek(cert_store_offset, SEEK_SET)
            cert_store = stream.read(header.cert_store_size)

            field_len = len(cert_store)
            if (cert_store_offset + field_len) > stop_offset:
                stop_offset = cert_store_offset + field_len
            # end if
        else:
            cert_store = None
        # end if

        proj_name_offset = field_base + header.proj_name_offset
        if proj_name_offset < stream_size:
            stream.seek(proj_name_offset, SEEK_SET)
            proj_name = stream.read(header.proj_name_size)

            field_len = len(proj_name)
            if (proj_name_offset + field_len) > stop_offset:
                stop_offset = proj_name_offset + field_len
            # end if

            if decoder:
                new_proj_name = decoder(proj_name, "ignore")[0]

                if new_proj_name:
                    proj_name = new_proj_name.split("\x00", 1)[0]
                # end if
            # end if
        else:
            proj_name = None
        # end if

        timestamp_buf_offset = field_base + header.timestamp_buf_offset
        if timestamp_buf_offset < stream_size:
            stream.seek(timestamp_buf_offset, SEEK_SET)
            timestamp_buf = stream.read(header.timestamp_buf_size)

            field_len = len(timestamp_buf)
            if (timestamp_buf_offset + field_len) > stop_offset:
                stop_offset = timestamp_buf_offset + field_len
            # end if

            if decoder:
                new_timestamp_buf = decoder(timestamp_buf, "ignore")[0]

                if new_timestamp_buf:
                    timestamp_buf = new_timestamp_buf.split("\x00", 1)[0]
                # end if
            # end if
        else:
            timestamp_buf = None
        # end if

        return cls((
            (stop_offset - start_offset),
            header.sig_size,
            header.sig_offset,
            header.cert_store_size,
            header.cert_store_offset,
            header.proj_name_size,
            header.proj_name_offset,
            header.timestamp,
            header.timestamp_buf_size,
            header.timestamp_buf_offset,
            sig,
            cert_store,
            proj_name,
            timestamp_buf
        ))
    # end def from_stream
# end class DigSigInfoSerialized

class PropertySetStreamHeader(_oleps_PropertySetStreamHeader):
    """Subclasses :class:`lf.win.ole.ps.PropertySetStreamHeader`.

    This class overrides the :attr:`sys_id` attribute with an instance of a
    :class:`PropertySetSystemIdentifier`.

    .. attribute:: sys_id

        The system identifier field.

    """

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`PropertySetStreamHeader` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`PropertySetStreamHeader`
        :returns: The corresponding :class:`PropertySetStreamHeader` object.

        """
        pssh = super(PropertySetStreamHeader, cls).from_stream(stream, offset)
        sys_id = property_set_system_identifier.from_buffer_copy(pssh.sys_id)
        sys_id = PropertySetSystemIdentifier.from_ctype(sys_id)

        return cls((
            pssh.byte_order, pssh.version, sys_id, pssh.clsid,
            pssh.property_set_count, pssh.fmtid0, pssh.offset0, pssh.fmtid1,
            pssh.offset1
        ))
    # end def from_stream
# end class PropertySetStreamHeader

class PropertyFactory(_oleps_PropertyFactory):
    """Makes various property objects"""

    @classmethod
    def make(cls, stream, offset=None, decoder=None):
        """Makes a :class:`~lf.win.ole.ps.Packet` object.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :type decoder: ``codecs.codec``
        :param decoder: An optional codec to decode the string.

        :rtype: :class:`~lf.win.ole.ps.Packet`
        :returns: The corresponding :class:`~lf.win.ole.ps.Packet` (or
                  subclass) object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        property = TypedPropertyValue.from_stream(stream, offset)
        pt = property.type

        if (pt == PropertyType.VT_LPSTR) or (pt == PropertyType.VT_LPWSTR):
            return VtString.from_stream(stream, offset, decoder)
        # end if

        return super(PropertyFactory, cls).make(stream, offset, decoder)
    # end def make
# end class PropertyFactory

class Builder(_oleps_Builder):
    """Builds property set streams, property sets, and properties."""

    @classmethod
    def build_property_set_stream_header(cls, stream, offset=None):
        """Builds a :class:`PropertySetStreamHeader` from a stream.

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
    def build_properties(
        cls, stream, fmtid, property_set, offset=None, decoder=None
    ):
        """Builds a dictionary of :class:`~lf.win.ole.ps.PropertyPacket`

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
                  corresponding :class:`~lf.win.ole.ps.PropertyPacket` objects
                  (values).

        """
        pids_offsets = property_set.pids_offsets
        make = PropertyFactory.make
        properties = dict()

        if fmtid == FMTID_SummaryInformation:
            return cls.build_summary_info_properties(
                stream, fmtid, property_set, offset, decoder
            )
        elif fmtid == FMTID_DocSummaryInformation:
            return cls.build_doc_summary_info_properties(
                stream, fmtid, property_set, offset, decoder
            )
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
                decoder = getdecoder(code_page_names[code_page])
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

    @classmethod
    def build_summary_info_properties(
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
                  corresponding :class:`~lf.win.ole.ps.PropertyPacket` objects
                  (values).

        """
        pids_offsets = property_set.pids_offsets
        make = PropertyFactory.make
        properties = dict()

        VT_LPSTR = PropertyType.VT_LPSTR
        VT_LPWSTR = PropertyType.VT_LPWSTR
        VT_CF = PropertyType.VT_CF
        PIDSI_THUMBNAIL = PIDSI.THUMBNAIL

        code_page = None
        if CODEPAGE_PROPERTY_IDENTIFIER in pids_offsets:
            property_offset = pids_offsets[CODEPAGE_PROPERTY_IDENTIFIER]
            code_page = make(stream, property_offset + offset)
            code_page = code_page.value

            if code_page < 0:  # Not sure why this isn't type VT_UI2
                code_page = 0xFFFF + code_page + 1
            # end if

            if (code_page in code_page_names) and (decoder is None):
                decoder = getdecoder(code_page_names[code_page])
            # end if
        # end if

        for (pid, property_offset) in pids_offsets.items():
            property_offset += offset

            if pid == DICTIONARY_PROPERTY_IDENTIFIER:
                property = Dictionary.from_stream(
                    stream, property_offset, code_page, decoder
                )
            elif pid == PIDSI_THUMBNAIL:
                tpv = TypedPropertyValue.from_stream(
                    stream, property_offset, decoder
                )

                if tpv.type == VT_CF:
                    property = VtThumbnail.from_stream(
                        stream, property_offset, decoder
                    )
                else:
                    property = make(stream, property_offset, decoder)
                # end if
            else:
                property = make(stream, property_offset, decoder)
            # end if

            properties[pid] = property
        # end for

        return properties
    # end def build_summary_info_properties

    @classmethod
    def build_doc_summary_info_properties(
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
                  corresponding :class:`~lf.win.ole.ps.PropertyPacket` objects
                  (values).

        """
        pids_offsets = property_set.pids_offsets
        make = PropertyFactory.make
        properties = dict()


        VT_LPSTR = PropertyType.VT_LPSTR
        VT_LPWSTR = PropertyType.VT_LPWSTR
        VT_VECTOR = PropertyType.VT_VECTOR
        VT_VARIANT = PropertyType.VT_VARIANT
        PIDDSI_DOCPARTS = PIDDSI.DOCPARTS
        PIDDSI_HEADINGPAIR = PIDDSI.HEADINGPAIR

        code_page = None
        if CODEPAGE_PROPERTY_IDENTIFIER in pids_offsets:
            property_offset = pids_offsets[CODEPAGE_PROPERTY_IDENTIFIER]
            code_page = make(stream, property_offset + offset)
            code_page = code_page.value

            if code_page < 0:  # Not sure why this isn't type VT_UI2
                code_page = 0xFFFF + code_page + 1
            # end if

            if (code_page in code_page_names) and (decoder is None):
                decoder = getdecoder(code_page_names[code_page])
            # end if
        # end if

        for (pid, property_offset) in pids_offsets.items():
            property_offset += offset

            if pid == DICTIONARY_PROPERTY_IDENTIFIER:
                property = Dictionary.from_stream(
                    stream, property_offset, code_page, decoder
                )

            elif pid == PIDDSI_HEADINGPAIR:
                tpv = TypedPropertyValue.from_stream(
                    stream, property_offset, decoder
                )

                if tpv.type == (VT_VECTOR | VT_VARIANT):
                    property = VtVecHeadingPair.from_stream(
                        stream, property_offset, decoder
                    )
                else:
                    property = make(stream, property_offset, decoder)
                # end if

            elif pid == PIDDSI_DOCPARTS:
                tpv = TypedPropertyValue.from_stream(
                    stream, property_offset, decoder
                )

                if tpv.type == (VT_VECTOR | VT_LPSTR):
                    property = VtVecUnalignedLpstr.from_stream(
                        stream, property_offset, decoder
                    )
                elif tpv.type == (VT_VECTOR | VT_LPWSTR):
                    property = VtVecLpwstr.from_stream(
                        stream, property_offset, decoder
                    )
                else:
                    property = make(stream, property_offset, decoder)
                # end if

            else:
                property = make(stream, property_offset, decoder)
            # end if

            properties[pid] = property
        # end for

        return properties
    # end def build_doc_summary_info_properties
# end class Builder

# Property Identifiers of properties that should be a VtString instance...
_vt_string_pidsi = [
    PIDSI.TITLE, PIDSI.SUBJECT, PIDSI.AUTHOR, PIDSI.KEYWORDS, PIDSI.COMMENTS,
    PIDSI.TEMPLATE, PIDSI.LAST_AUTHOR, PIDSI.REVNUMBER, PIDSI.APPNAME
]

_vt_string_piddsi = [
    PIDDSI.CATEGORY, PIDDSI.PRESFORMAT, PIDDSI.MANAGER, PIDDSI.COMPANY,
    PIDDSI.CONTENTTYPE, PIDDSI.CONTENTSTATUS, PIDDSI.LANGUAGE,
    PIDDSI.DOCVERSION,
]
