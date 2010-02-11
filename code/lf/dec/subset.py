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

"""Digital evidence containers that are a subset of a stream."""

# local imports
from lf.dec.consts import SEEK_SET
from lf.dec.base import SingleStreamContainer, ManagedIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "Subset", "SubsetIStream"
]

class Subset(SingleStreamContainer):
    """A container for a stream that is a subset of another stream."""

    def __init__(self, stream, start, size):
        """Initializes a Subset object.

        :type stream: IStream
        :param stream: The stream to wrap around.

        :type start: int
        :param start: The start of the subset.

        :type size: int
        :param size: The size (in bytes) of the subset.

        """
        super(Subset, self).__init__()
        self.stream = SubsetIStream(stream, start, size)
    # end def __init__
# end class Subset

class SubsetIStream(ManagedIStream):
    """A stream that is a subset of another stream.

    .. attribute:: _stream

        The stream that is wrapped around.

    .. attribute:: _start

        The start of the subset, in the :attr:`_stream` attribute.

    """

    def __init__(self, stream, start, size):
        """Initializes a SubsetIStream object.

        :type stream: IStream
        :param stream: The stream to wrap around.

        :type start: int
        :param start: The start of the subset.

        :type size: int
        :param size: The size (in bytes) of the subset.


        """
        super(SubsetIStream, self).__init__()

        self.size = size
        self._stream = stream
        self._start = start
    # end def __init__

    def readinto(self, b: bytearray) -> int:
        """Reads upto len(b) bytes into b.

        :type b: bytearray
        :param b: A bytearray to hold the bytes read from the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The number of bytes read.

        """
        if self.closed:
            raise ValueError("readinto on closed stream")
        # end if

        stream = self._stream
        position = self._position
        size = self.size
        len_b = len(b)

        if (position >= size) or (len_b == 0):
            return 0
        # end if

        read_size = min(len_b, size - position)
        stream.seek(self._start + position, SEEK_SET)
        data = stream.read(read_size)
        len_data = len(data)
        b[:len_data] = data
        self._position = position + len_data

        return len_data
    # end def readinto
# end class SubsetIStream
