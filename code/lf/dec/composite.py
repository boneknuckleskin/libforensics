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

"""Digital evidence containers composed of subets of other streams."""

# local imports
from lf.dec.consts import SEEK_SET
from lf.dec.base import SingleStreamContainer, ManagedIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "Composite", "CompositeIStream"
]

class Composite(SingleStreamContainer):
    """A container for a stream composed of subsets of other streams."""

    def __init__(self, segments):
        """Initializes a Composite object.

        :type segments: list of tuples
        :param segments: A list of tuples, where the elements of each tuple
        are:

            1. The stream to read from.
            2. The offset in the stream for the start of the segment.
            3. The number of bytes in the segment.

        """
        super(Composite, self).__init__()
        self.stream = CompositeIStream(segments)
    # end def __init__
# end class Composite

class CompositeIStream(ManagedIStream):
    """A stream composed of subsets of other streams.

    .. attribute:: _segments

        A list of (stream, start, size) tuples.
    """

    def __init__(self, segments):
        """Intiailizes a CompositeIStream object.

        :type segments: list of tuples
        :param segments: A list of tuples where the elements of each tuple
        are:

            1. The stream to read from.
            2. The offset in the stream of the start of the segment.
            3. The number of bytes in the segment.

        """
        super(CompositeIStream, self).__init__()

        total_size = 0
        for (stream, start, size) in segments:
            total_size += size
        # end for

        self._segments = segments
        self.size = total_size
    # end def __init__

    def readinto(self, b):
        """Reads up to len(b) bytes into b.

        :type b: bytearray
        :param b: A bytearray to hold the bytes read from the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The number of bytes read.

        """
        if self.closed:
            raise ValueError("Operation on a closed stream")
        # end if

        position = self._position
        size = self.size
        len_b = len(b)

        if (position >= size) or (len_b == 0):
            return 0
        # end if

        bytes_left = min(len_b, size - position)

        ret_val = bytes_left
        ret_buf = bytearray()

        seg_iter = iter(self._segments)

        virt_seg_start = 0
        for (stream, seg_start, seg_size) in seg_iter:
            virt_seg_stop = virt_seg_start + seg_size
            if virt_seg_start <= position < virt_seg_stop:
                # We found the first stream, so process it and break
                read_size = min(bytes_left, virt_seg_stop - position)

                stream.seek(seg_start + (position - virt_seg_start), SEEK_SET)
                data = stream.read(read_size)
                ret_buf.extend(data)
                bytes_left -= len(data)

                break
            # end if

            virt_seg_start += seg_size
        # end for

        for (stream, seg_start, seg_size) in seg_iter:
            if bytes_left <= 0:
                break
            # end if

            read_size = min(bytes_left, seg_size)

            stream.seek(seg_start, SEEK_SET)
            data = stream.read(read_size)
            ret_buf.extend(data)
            bytes_left -= len(data)
        # end for

        len_ret_buf = len(ret_buf)
        b[:len_ret_buf] = ret_buf
        self._position = position + len_ret_buf

        return len_ret_buf
    # end def readinto
# end class CompositeIStream
