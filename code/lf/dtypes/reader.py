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

"""Reads builtin datatypes from a stream."""

# local imports
from lf.dec.consts import SEEK_SET
from lf.dtypes.ctypes import (
    int8, uint8,
    int16_le, uint16_le, int16_be, uint16_be,
    int32_le, uint32_le, int32_be, uint32_be,
    int64_le, uint64_le, int64_be, uint64_be,
    float32_le, float32_be, float64_le, float64_be
)

__docformat__ = "restructuredtext en"
__all__ = ["Reader", "BoundReader"]

class Reader():
    """Reads :class:`BuiltIn` data types from a stream."""

    @classmethod
    def int8(cls, stream, offset=None):
        """Reads a signed 8-bit integer from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int8.from_buffer_copy(stream.read(1)).value
    # end def int8

    @classmethod
    def uint8(cls, stream, offset=None):
        """Reads an unsigned 8-bit integer from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint8.from_buffer_copy(stream.read(1)).value
    # end def uint8

    @classmethod
    def int16_le(cls, stream, offset=None):
        """Reads a signed 16-bit integer (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int16_le.from_buffer_copy(stream.read(2)).value
    # end def int16_le

    @classmethod
    def uint16_le(cls, stream, offset=None):
        """Reads an unsigned 16-bit integer (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint16_le.from_buffer_copy(stream.read(2)).value
    # end def uint16_le

    @classmethod
    def int16_be(cls, stream, offset=None):
        """Reads a signed 16-bit integer (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int16_be.from_buffer_copy(stream.read(2)).value
    # end def int16_be

    @classmethod
    def uint16_be(cls, stream, offset=None):
        """Reads an unsigned 16-bit integer (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint16_be.from_buffer_copy(stream.read(2)).value
    # end def uint16_be

    @classmethod
    def int32_le(cls, stream, offset=None):
        """Reads a signed 32-bit integer (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int32_le.from_buffer_copy(stream.read(4)).value
    # end def int32_le

    @classmethod
    def uint32_le(cls, stream, offset=None):
        """Reads an unsigned 32-bit integer (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint32_le.from_buffer_copy(stream.read(4)).value
    # end def uint32_le

    @classmethod
    def int32_be(cls, stream, offset=None):
        """Reads a signed 32-bit integer (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int32_be.from_buffer_copy(stream.read(4)).value
    # end def int32_be

    @classmethod
    def uint32_be(cls, stream, offset=None):
        """Reads an unsigned 32-bit integer (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint32_be.from_buffer_copy(stream.read(4)).value
    # end def uint32_be

    @classmethod
    def int64_le(cls, stream, offset=None):
        """Reads a signed 64-bit integer (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int64_le.from_buffer_copy(stream.read(8)).value
    # end def int64_le

    @classmethod
    def uint64_le(cls, stream, offset=None):
        """Reads an unsigned 64-bit integer (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint64_le.from_buffer_copy(stream.read(8)).value
    # end def uint64_le

    @classmethod
    def int64_be(cls, stream, offset=None):
        """ Reads a signed 64-bit integer (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return int64_be.from_buffer_copy(stream.read(8)).value
    # end def int64_be

    @classmethod
    def uint64_be(cls, stream, offset=None):
        """Reads an unsigned 64-bit integer (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return uint64_be.from_buffer_copy(stream.read(8)).value
    # end def uint64_be

    @classmethod
    def float32_le(cls, stream, offset=None):
        """Reads a 32-bit floating point number (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return float32_le.from_buffer_copy(stream.read(4)).value
    # end def float_le

    @classmethod
    def float32_be(cls, stream, offset=None):
        """Reads a 32-bit floating point number (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return float32_be.from_buffer_copy(stream.read(4)).value
    # end def float32_be

    @classmethod
    def float64_le(cls, stream, offset=None):
        """Reads a 64-bit floating point number (little endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return float64_le.from_buffer_copy(stream.read(8)).value
    # end def float64_le

    @classmethod
    def float64_be(cls, stream, offset=None):
        """Reads a 64-bit floating point number (big endian) from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: The stream to read data from.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        return float64_be.from_buffer_copy(stream.read(8)).value
    # end def float64_be
# end class Reader

class BoundReader(Reader):
    """A :class:`Reader` that is bound to a :class:`lf.dec.IStream`.

    .. attribute:: stream

        A stream that contains the values to read.

    """

    def __init__(self, stream):
        """Initializes a :class:`BoundReader` object.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the values to read.

        """
        self.stream = stream
    # end def __init__

    def int8(self, offset=None):
        """Reads a signed 8-bit integer.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int8.from_buffer_copy(self.stream.read(1)).value
    # end def int8

    def uint8(self, offset=None):
        """Reads an unsigned 8-bit integer.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint8.from_buffer_copy(self.stream.read(1)).value
    # end def uint8

    def int16_le(self, offset=None):
        """Reads a signed 16-bit integer (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int16_le.from_buffer_copy(self.stream.read(2)).value
    # end def int16_le

    def uint16_le(self, offset=None):
        """ Reads an unsigned 16-bit integer (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint16_le.from_buffer_copy(self.stream.read(2)).value
    # end def uint16_le

    def int16_be(self, offset=None):
        """Reads a signed 16-bit integer (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int16_be.from_buffer_copy(self.stream.read(2)).value
    # end def int16_be

    def uint16_be(self, offset=None):
        """Reads an unsigned 16-bit integer (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint16_be.from_buffer_copy(self.stream.read(2)).value
    # end def uint16_be

    def int32_le(self, offset=None):
        """Reads a signed 32-bit integer (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int32_le.from_buffer_copy(self.stream.read(4)).value
    # end def int32_le

    def uint32_le(self, offset=None):
        """Reads an unsigned 32-bit integer (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint32_le.from_buffer_copy(self.stream.read(4)).value
    # end def uint32_le

    def int32_be(self, offset=None):
        """Reads a signed 32-bit integer (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int32_be.from_buffer_copy(self.stream.read(4)).value
    # end def int32_be

    def uint32_be(self, offset=None):
        """Reads an unsigned 32-bit integer (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint32_be.from_buffer_copy(self.stream.read(4)).value
    # end def uint32_be

    def int64_le(self, offset=None):
        """Reads a signed 64-bit integer (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int64_le.from_buffer_copy(self.stream.read(8)).value
    # end def int64_le

    def uint64_le(self, offset=None):
        """Reads an unsigned 64-bit integer (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint64_le.from_buffer_copy(self.stream.read(8)).value
    # end def uint64_le

    def int64_be(self, offset=None):
        """Reads a signed 64-bit integer (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return int64_be.from_buffer_copy(self.stream.read(8)).value
    # end def int64_be

    def uint64_be(self, offset=None):
        """Reads an unsigned 64-bit integer (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the integer.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`int`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return uint64_be.from_buffer_copy(self.stream.read(8)).value
    # end def uint64_be

    def float32_le(self, offset=None):
        """Reads a 32-bit floating point number (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return float32_le.from_buffer_copy(self.stream.read(4)).value
    # end def float_le

    def float32_be(self, offset=None):
        """Reads a 32-bit floating point number (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return float32_be.from_buffer_copy(self.stream.read(4)).value
    # end def float32_be

    def float64_le(self, offset=None):
        """Reads a 64-bit floating point number (little endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return float64_le.from_buffer_copy(self.stream.read(8)).value
    # end def float64_le

    def float64_be(self, offset=None):
        """Reads a 64-bit floating point number (big endian).

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the floating point number.

        :except ValueError: if :attr:`stream` (starting at :attr:`offset` is
                            too small.)

        :rtype: :class:`float`
        :returns: The corresponding value.

        """
        if offset is not None:
            self.stream.seek(offset, SEEK_SET)
        # end if

        return float64_be.from_buffer_copy(self.stream.read(8)).value
    # end def float64_be
# end class BoundReader
