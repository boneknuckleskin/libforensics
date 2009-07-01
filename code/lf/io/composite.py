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
Evidence streams composed of pieces of multiple other streams.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "CompositeIStream", "open"
]

from lf.io.base import Stream, ManagedIStream

class CompositeIStream(ManagedIStream):
    """
    Input stream composed of pieces of multiple other streams.

    .. attribute:: _segments (for internal use only)

        A list of (stream, start offset, count) tuples.  These describe the
        pieces of the underlying streams that comprise the composite stream.

    .. attribute:: _virt_bounds

        A list of tuples containing the min and max elements (relative to the
        composite stream) for each segment.
    """

    def __init__(self, segments: list) -> None:
        """
        Intiailizes a CompositeIStream object.

        :parameters:
            segments
                A list of tuples that describe the pieces of the composite
                stream.  The values of the tuple are (stream, start, count)
                where stream is the underlying stream, start is the (absolute)
                offset of the start of the segment in the underlying stream,
                and count is the length of the segment in the underlying
                stream.
        """

        super(CompositeIStream, self).__init__()

        element_counter = 0
        virt_bounds = list()

        for (stream, offset, count) in segments:
            virt_bounds.append((element_counter, element_counter + count - 1))
            element_counter += count
        # end for

        self._segments = segments
        self._virt_bounds = virt_bounds
        self._size = virt_bounds[-1][1] + 1
    # end def __init__

    def readinto(self, b: bytearray) -> int:
        """
        Reads up to len(b) bytes into b.

        :parameters:
            b
                The bytearray to hold the data.

        :rtype: int
        :returns: The number of bytes read, or 0 for EOF.
        """

        if self._closed:
            raise IOError("Operation on a closed stream")
        # end if

        offset = self._offset
        size = self._size
        bytes_left = 0

        if (offset >= size) or (len(b) == 0):
            return 0
        # end if

        if len(b) >= (size - offset):
            bytes_left = size - offset
        else:
            bytes_left = len(b)
        # end if

        ret_val = bytes_left

        for index, (min_element, max_element) in enumerate(self._virt_bounds):
            if min_element <= offset <= max_element:
                break
            # end if
        # end for

        # Process the first stream
        (stream, seg_start, seg_count) = self._segments[index]
        (min_element, max_element) = self._virt_bounds[index]

        cur_seg_count = max_element - offset + 1
        if cur_seg_count > bytes_left:
            read_count = bytes_left
        else:
            read_count = cur_seg_count
        # end if

        temp_buf = bytearray(read_count)
        stream.seek((offset - min_element) + seg_start, 0)
        stream.readinto(temp_buf)
        b[:read_count] = temp_buf
        bytes_left -= read_count
        b_index = read_count
        index += 1

        # Process the rest of the segments
        while bytes_left > 0:
            for index, seg_info in enumerate(self._segments[index:], index):
                (stream, seg_start, seg_count) = seg_info
                (min_element, max_element) = self._virt_bounds[index]

                if seg_count > bytes_left:
                    read_count = bytes_left
                else:
                    read_count = seg_count
                # end if

                temp_buf = bytearray(read_count)
                stream.seek(seg_start, 0)
                stream.readinto(temp_buf)
                b[b_index:(b_index + read_count)] = temp_buf
                b_index += read_count
                bytes_left -= read_count
            # end for
        # end while

        offset += ret_val
        self._offset = offset

        return ret_val
    # end def readinto
# end class CompositeIStream

def open(segments: list) -> Stream:
    """
    Creates a composite stream.

    :parameters:
        segments
            A list of tuples that describe the pieces of the composite
            stream.  The values of the tuple are (stream, start, count)
            where stream is the underlying stream, start is the (absolute)
            offset of the start of the segment in the underlying stream,
            and count is the length of the segment in the underlying
            stream.
    """

    return CompositeIStream(segments)
# end def open
