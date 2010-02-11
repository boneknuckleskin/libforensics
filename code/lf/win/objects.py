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

"""Value objects (and factories) for common Microsoft data types."""

# stdlib imports
from uuid import UUID
from decimal import Decimal

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import LITTLE_ENDIAN, ActiveStructuple, StdLibConverter
from lf.dtypes.ctypes import uint64_le, uint64_be, int64_le, int64_be
from lf.win.ctypes import (
    guid_le, lcid_le, hresult_le, coord_le, decimal_le,
    guid_be, lcid_be, hresult_be, coord_be, decimal_be,
)

__docformat__ = "restructuredtext en"
__all__ = [
    "GUIDToUUID", "CLSIDToUUID", "COORD", "LCID", "HRESULT",
    "DECIMALToDecimal", "CURRENCYToDecimal"
]


class GUIDToUUID(StdLibConverter):
    """Converts a GUID to a ``UUID``."""

    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a ``UUID`` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the GUID structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the GUID structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: ``UUID``
        :returns: The corresponding ``UUID`` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(16)

        if byte_order == LITTLE_ENDIAN:
            return UUID(bytes_le=data)
        else:
            return UUID(bytes=data)
        # end if
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a ``UUID`` object from a ctype.

        :type ctype: :class:`lf.win.ctypes.guid_le` or
                     :class:`lf.win.ctypes.guid_be`
        :param ctype: A GUID object.

        :rtype: ``UUID``
        :returns: The corresponding ``UUID`` object.

        """
        return cls.from_guid(
            ctype.data1, ctype.data2, ctype.data3, ctype.data4
        )
    # end def from_ctype

    @classmethod
    def from_guid(cls, data1, data2, data3, data4):
        """Creates a ``UUID`` object from individual GUID fields.

        :type data1: ``int``
        :param data1: The first 8 hexadecimal digits (32 bits).

        :type data2: ``int``
        :param data2: The first group of 4 hexadecimal digits (16 bits).

        :type data3: ``int``
        :param data3: The second group of 4 hexadecimal digits (16 bits).

        :type data4: ``bytes`` or ``bytearray``
        :param data4: The last 8 bytes.

        :rtype: ``UUID``
        :returns: The corresponding ``UUID`` object.

        """
        node = (data4[2] << 40) | (data4[3] << 32) | (data4[4] << 24)
        node = node | (data4[5] << 16) | (data4[6] << 8) | data4[7]

        return UUID(fields=(data1, data2, data3, data4[0], data4[1], node))
    # end def from_guid
# end class GUIDToUUID

class CLSIDToUUID(GUIDToUUID):
    """Converts a CLSID to a ``UUID``."""

    pass
# end class CLSIDToUUID

class DECIMALToDecimal(StdLibConverter):
    """Converts a DECIMAL to a ``Decimal``."""

    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a ``Decimal`` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the DECIMAL structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the DECIMAL structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: ``Decimal``
        :returns: The corresponding ``Decimal`` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(16)

        if byte_order == LITTLE_ENDIAN:
            ctype_value = decimal_le.from_buffer_copy(data)
        else:
            ctype_value = decimal_be.from_buffer_copy(data)
        # end if

        value = (ctype_value.hi32 << 64) | ctype_value.lo64
        if ctype_value.sign:
            value = -value
        # end if

        return Decimal(value) / Decimal(10**ctype_value.scale)
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a ``Decimal`` object from a ctype.

        :type ctype: :class:`lf.win.ctypes.decimal_le` or
                     :class:`lf.win.ctypes.decimal_be`
        :param ctype: A DECIMAL object.

        :raises ValueError: If the DECIMAL object is invalid.

        :rtype: ``Decmial``
        :returns: The corresponding ``Decimal`` object.

        """
        value = (ctype.hi32 << 64) | ctype.lo64
        if ctype.sign:
            value = -value
        # end if

        return Decimal(value) / Decimal(10**ctype.scale)
    # end def from_ctype
# end class DECIMALToDecimal

class CURRENCYToDecimal(StdLibConverter):
    """Converts a CURRENCY data type to a ``Decimal``."""

    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a ``Decimal`` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the CURRENCY structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the CURRENCY structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: ``Decimal``
        :returns: The corresponding ``Decmial`` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(8)

        if byte_order == LITTLE_ENDIAN:
            value = int64_le.from_buffer_copy(data).value
        else:
            value = int64_be.from_buffer_copy(data).value
        # end if

        return Decimal(value) / Decimal(10000)
    # end def from_stream

    @classmethod
    def from_int(cls, integer):
        """Creates a ``Decimal`` object from an ``int``.

        :type integer: ``int``
        :param integer: The value of the CURRENCY object.

        :rtype: ``Decimal``
        :returns: The corresponding ``Decimal`` object.

        """
        return Decimal(integer) / Decimal(10000)
    # end def from_ctype
# end class CURRENCYToDecimal

class COORD(ActiveStructuple):
    """Represents coordinates.

    .. attribute:: x

        The x coordinate.

    .. attribute:: y

        The y coordinate.

    """

    _fields_ = ("x", "y")
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a :class:`COORD` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the COORD structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the COORD structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: :class:`COORD`
        :returns: The extracted :class:`COORD` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(4)

        if byte_order == LITTLE_ENDIAN:
            coord = coord_le.from_buffer_copy(data)
        else:
            coord = coord_be.from_buffer_copy(data)
        # end if

        return COORD((coord.x, coord.y))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a :class:`COORD` object from a ctype.

        :type ctype: :class:`lf.win.ctypes.coord_le` or
                     :class:`lf.win.ctypes.coord_be`
        :param ctype: An instance of a coord ctype.

        :rtype: :class:`COORD`
        :returns: The corresponding :class:`COORD` object.

        """
        return COORD((ctype.x, ctype.y))
    # end def from_ctype
# end class COORD

class LCID(ActiveStructuple):
    """Represents a Locale ID data type.

    .. attribute:: rsvd

        The reserved field.

    .. attribute:: sort_id

        The sort ID field.

    .. attribute:: lang_id

        The language ID field.

    """

    _fields_ = ("lang_id", "sort_id", "rsvd")
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a :class:`LCID` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the LCID structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the LCID structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: :class:`LCID`
        :returns: The extracted :class:`LCID` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(4)

        if byte_order == LITTLE_ENDIAN:
            lcid = lcid_le.from_buffer_copy(data)
        else:
            lcid = lcid_be.from_buffer_copy(data)
        # end if

        return LCID((lcid.lang_id, lcid.sort_id, lcid.rsvd))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a :class:`LCID` object from a ctype.

        :type ctype: :class:`lf.win.ctypes.lcid_le` or
                     :class:`lf.win.ctypes.lcid_be`
        :param ctype: An instance of an lcid ctype.

        :rtype: :class:`LCID`
        :returns: The corresponding :class:`LCID` object.

        """
        return LCID((ctype.lang_id, ctype.sort_id, ctype.rsvd))
    # end def from_ctype
# end class LCID

class HRESULT(ActiveStructuple):
    """Represents and HRESULT data type.

    .. attribute:: s

        The severity bit.

    .. attribute:: r

        The reserved bit.

    .. attribute:: c

        The customer bit.

    .. attribute:: n

        The NTSTATUS bit.

    .. attribute:: x

        The x field.

    .. attribute:: facility

        Indicates the source of the error.

    .. attribute:: code

        The remaining part of the error code.

    """

    _fields_ = ("code", "facility", "x", "n", "c", "r", "s")
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a ``HRESULT`` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the HRESULT structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the HRESULT structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: :class:`HRESULT`
        :returns: The extracted :class:`HRESULT` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(4)

        if byte_order == LITTLE_ENDIAN:
            hresult = hresult_le.from_buffer_copy(data)
        else:
            hresult = hresult_be.from_buffer_copy(data)
        # end if

        return HRESULT((
            hresult.code,
            hresult.facility,
            hresult.x,
            hresult.n,
            hresult.c,
            hresult.r,
            hresult.s
        ))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a ``HRESULT`` object from a ctype.

        :type ctype: :class:`lf.win.ctypes.hresult_le` or
                     :class:`lf.win.ctypes.hresult_be`
        :param ctype: A hresult object.

        :rtype: :class:`HRESULT`
        :returns: The corresponding :class:`HRESULT` object.

        """
        return HRESULT((
            ctype.code,
            ctype.facility,
            ctype.x,
            ctype.n,
            ctype.c,
            ctype.r,
            ctype.s
        ))
    # end def from_ctype

    @classmethod
    def from_int(cls, hresult):
        """Creates a ``HRESULT`` object from an ``int``.

        :type hresult: ``int``
        :param hresult: The value of the HRESULT.

        :rtype: :class:`HRESULT`
        :returns: The corresponding :class:`HRESULT` object.

        """

        code = hresult & 0x0000FFFF
        facility = (hresult >> 16) & 0x000007FF
        x = (hresult >> 27) & 0x1
        n = (hresult >> 28) & 0x1
        c = (hresult >> 29) & 0x1
        r = (hresult >> 30) & 0x1
        s = (hresult >> 31) & 0x1

        return HRESULT((code, facility, x, n, c, r, s))
    # end def from_int
# end class HRESULT
