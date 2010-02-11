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

"""Digital evidence container for raw/dd files."""

# stdlib imports
from io import BytesIO

# local imports
from lf.dec.base import SingleStreamContainer, IStreamWrapper

__docformat__ = "restructuredtext en"
__all__ = [
    "Byte", "ByteIStream"
]

class Byte(SingleStreamContainer):
    """A container file for a bytes or bytearray object.

    .. attribute:: stream

        The corresponding ByteIStream object.

    """

    def __init__(self, bytes_):
        """Initializes a Byte object.

        :type bytes_: bytes or bytearray
        :param bytes_: The bytes or bytearray object to wrap around.

        """
        self.stream = ByteIStream(bytes_)
    # end def __init__
# end class Byte

class ByteIStream(IStreamWrapper):
    """A stream for a bytes or bytearray object."""

    def __init__(self, bytes_):
        """Initializes a ByteIStream object.

        :type bytes_: bytes or bytearray
        :param bytes_: The bytes or bytearray object to read from.

        """
        stream = BytesIO(bytes_)
        super(ByteIStream, self).__init__(stream, len(bytes_))
    # end def __init__

    def readinto(self, b):
        """Reads up to len(b) bytes into b.

        :type b: bytearray
        :param b: A bytearray to hold the bytes read from the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The number of bytes read.

        """
        data = self._stream.read(len(b))
        len_data = len(data)
        b[:len_data] = data

        return len_data
    # end def readinto
# end class ByteIStream
