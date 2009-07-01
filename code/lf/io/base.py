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
Base classes for evidence I/O streams.
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "Stream", "IStream", "ManagedIStream"
]

import io
from abc import abstractmethod, abstractproperty, ABCMeta

from lf.io.consts import SEEK_SET, SEEK_CUR, SEEK_END

class Stream(io.RawIOBase):
    """
    Base class for all evidence streams.
    """

    pass
# end class Stream

class IStream(Stream, metaclass=ABCMeta):
    """
    Base class for seekable-readable evidence streams.

    .. attribute:: size (read-only)

        The size of the stream (in bytes)

    .. attribute:: _size (internal use only)

        Used to hold the size of the stream.
    """

    def __init__(self) -> None:
        """
        Initializes an IStream object.
        """

        self._size = 0
    # end def __init__

    @property
    def size(self) -> int:
        """
        Getter function to make self.size read-only
        """

        return self._size
    # end def size

    def __len__(self) -> int:
        """
        Returns the size of the stream in bytes
        """

        return self._size
    # end def __len__

    def readable(self) -> bool:
        """
        Returns if the stream is readable (always True)
        """

        return True
    # end def readable

    def seekable(self) -> bool:
        """
        Returns if the stream is seekable (always True)
        """

        return True
    # end def seekable

    @abstractproperty
    def closed(self) -> bool:
        """
        Returns true if the stream is closed
        """

        pass
    # end def closed

    @abstractmethod
    def close(self) -> None:
        """
        Closes the stream
        """

        pass
    # end def close

    @abstractmethod
    def seek(self, offset: int, whence: int = SEEK_SET) -> int:
        """
        Repositions the stream pointer.

        :parameters:
            offset
                The new position of the stream pointer.
            whence
                The reference point for the position of the stream pointer.
                Valid values are:

                * SEEK_SET (0) - start of the stream
                * SEEK_CUR (1) - current stream position
                * SEEK_END (2) - end of the stream

        :raises:
            IOError
                If the stream is currently closed.
            ValueError
                If the absolute position is before the start of the stream, or
                whence is an invalid value.

        :rtype: int
        :returns: The new (absolute) position of the stream pointer.
        """

        pass
    # end ddef seek

    @abstractmethod
    def tell(self) -> int:
        """
        Returns the (absolute) current position of the stream pointer.

        :rtype: int
        :returns: The (absolute) current position of the stream pointer.
        """

        pass
    # end def tell

    @abstractmethod
    def readinto(self, b: bytearray) -> int:
        """
        Reads up to len(b) bytes into b.

        :parameters:
            b
                A byte array to store the bytes read.

        :rtype: int
        :returns: The number of bytes read, or 0 for EOF.
        """

        pass
    # end def readinto
# end class IStream

class ManagedIStream(IStream):
    """
    Base class for read-only evidence streams, where we need to manage the
    stream pointer.

    .. attribute:: _offset (internal use only)

        The current (absolute) offset of the stream pointer.

    .. attribute:: _closed (internal use only)

        Whether or not the stream is currently closed
    """

    def __init__(self) -> None:
        """
        Initializes a ManagedIStream object.
        """

        super(ManagedIStream, self).__init__()
        self._offset = 0
        self._closed = False
    # end def __init__

    def close(self) -> None:
        """
        Closes the stream.
        """

        self._offset = 0
        self._size = 0
        self._closed = True
    # end def close

    @property
    def closed(self) -> bool:
        """
        Returns True if the stream is closed.
        """

        return self._closed
    # end def closed

    def seek(self, offset: int, whence: int = SEEK_SET) -> int:
        """
        Repositions the stream pointer.

        :parameters:
            offset
                The new position of the stream pointer.
            whence
                The reference point for the position of the stream pointer.
                Valid values are:

                * SEEK_SET (0) - start of the stream
                * SEEK_CUR (1) - current stream position
                * SEEK_END (2) - end of the stream

        :raises:
            IOError
                If the stream is currently closed.
            ValueError
                If the absolute position is before the start of the file, or
                whence is an invalid value.

        :rtype: int
        :returns: The new (absolute) position of the stream pointer.
        """

        if self.closed:
            raise IOError("Operation on a closed stream.")
        # end if self.closed

        if whence == SEEK_SET:
            pass
        elif whence == SEEK_CUR:
            offset = offset + self._offset
        elif whence == SEEK_END:
            offset = offset + self._size
        else:
            raise ValueError("Invalid value for whence: {0}".format(whence))
        # end if

        if offset < 0:
            raise ValueError("Invalid value for offset: {0}".format(offset))
        # end if

        self._offset = offset

        return offset
    # end def seek

    def tell(self) -> int:
        """
        Returns the (absolute) current offset of the stream pointer.
        """

        if self.closed:
            raise IOError("Operation on closed stream")
        # end if

        return self._offset
    # end def tell
# end class ManagedIStream

class IStreamWrapper(IStream):
    """
    An IStream class that wraps around an existing Python I/O stream.  This
    class just passes the appropriate calls to the underlying I/O stream.

    .. attribute:: _io_obj (for internal use only)

        The underlying I/O object
    """

    def __init__(self, io_obj: io.RawIOBase, size: int = 0) -> None:
        """
        Initializes an IStreamWrapper object.

        :parameters:
            io_obj
                An open I/O stream.

            size
                The size of the I/O stream.
        """

        self._io_obj = io_obj
        self._size = size
    # end def __init__

    @property
    def closed(self) -> bool:
        """
        Returns True if the stream is closed.
        """

        return self._io_obj.closed
    # end def closed

    def close(self) -> None:
        """
        Closes the stream
        """

        self._io_obj.close()
        self._size = 0
    # end def close

    def seek(self, offset: int, whence: int = 0) -> int:
        """
        Repositions the stream pointer.

        :parameters:
            offset
                The new position of the stream pointer.
            whence
                The reference point for the position of the stream pointer.
                Valid values are:

                * SEEK_SET (0) - start of the stream
                * SEEK_CUR (1) - current stream position
                * SEEK_END (2) - end of the stream

        :raises:
            IOError
                If the stream is currently closed.
            ValueError
                If the absolute position is before the start of the stream, or
                whence is an invalid value.

        :rtype: int
        :returns: The new (absolute) position of the stream pointer.
        """

        return self._io_obj.seek(offset, whence)
    # end def seek

    def tell(self) -> int:
        """
        Returns the (absolute) current position of the stream pointer.
        """

        return self._io_obj.tell()
    # end def tell

    def readinto(self, b: bytearray) -> int:
        """
        Reads up to len(b) bytes into b.

        :parameters:
            b
                A byte array to store the bytes read.

        :rtype: int
        :returns: The number of bytes read, or 0 for EOF.
        """

        return self._io_obj.readinto(b)
    # end def readinto
# end class IStreamWrapper

def open() -> Stream:
    """
    Creates a new evidence I/O stream.
    """

    pass
# end def open
