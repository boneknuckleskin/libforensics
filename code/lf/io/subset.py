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
Evidence streams that are a subset of another stream.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "SubsetIStream", "open"
]

from lf.io.base import Stream, IStream, ManagedIStream

class SubsetIStream(ManagedIStream):
    """
    Class that creates an evidence stream from a subset of another stream.

    .. attribute:: _stream (for internal use only)

        The underlying stream

    .. attribute:: _start (for internal use only)

        The (absolute) offset of the start of the stream, in the underlying
        stream. (inclusive)
    """

    def __init__(self, stream: Stream, start: int, count: int) -> None:
        """
        Initializes a SubsetIStream object.

        :parameters:
            stream
                The underlying stream to read.
            start:
                The offset to start reading in the stream. (inclusive)
            count:
                The number of bytes to include from the underlying stream.

        :raises:
            TypeError
                If stream is not an instance of IStream
            ValueError
                If start or count are < 0, or (start + count) > stream.size
        """

        super(SubsetIStream, self).__init__()

        if not isinstance(stream, IStream):
            raise TypeError("stream is not an IStream")
        elif start < 0:
            raise ValueError("Invalid value for start: {0}".format(start))
        elif (start + count) > stream.size:
           raise ValueError("Invalid value for stop: {0}".format(stop))
        # end if

        self._stream = stream
        self._start = start
        self._size = count
    # end def __init__

    def readinto(self, b: bytearray) -> int:
        """
        Reads up to len(b) bytes into b.

        :paramaters:
            b
                A byte array to store the data that is read.

        :rtype: int
        :returns: The number of bytes read (0 for EOF).
        """

        if self.closed:
            raise IOError("Operation on a closed stream")
        # end if

        retval = 0
        offset = self._offset
        size = self._size

        if (offset >= size) or (len(b) == 0):
            return 0
        # end if

        bytes_left_count = size - offset

        if len(b) > bytes_left_count:
            temp_buf = bytearray(bytes_left_count)
            self._stream.seek(self._start + offset, 0)
            retval = self._stream.readinto(temp_buf)

            b[:len(temp_buf)] = temp_buf
        else:
            self._stream.seek(self._start + offset, 0)
            retval = self._stream.readinto(b)
        # end if

        self._offset += retval
        return retval
    # end def readinto
# end class SubsetIStream

def open(stream: Stream, start: int, count: int) -> Stream:
    """
    Creates a new Subset stream.

    :parameters:
        stream
            The underlying stream.
        start
            The starting byte. (inclusive)
        count
            The number of bytes to use from stream.

    :rtype: Stream
    :returns: A new Subset stream
    """

    return SubsetIStream(stream, start, count)
# end def open
