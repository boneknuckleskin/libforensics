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

"""Base classes for Digital Evidence Containers (DECs)"""

# stdlib imports
from io import RawIOBase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END

__docformat__ = "restructuredtext en"
__all__ = [
    "Container", "SingleStreamContainer", "StreamInfo", "IStream",
    "ManagedIStream", "IStreamWrapper"
]

class Container():
    """Base class for container files.

    Subclasses are required to implement the :meth:`list` and :meth:`open`
    methods.

    .. attribute:: stream

        If a container type only supports a single evidence stream (e.g. raw/dd
        files) then this is the stream.  Otherwise this is ``None``.

    """

    def __init__(self):
        """Initializes a Container object."""
        self.stream = None
    # end def __init__

    def list(self):
        """Lists streams inside container

        :rtype: list
        :returns: A list of StreamInfo objects that describe the streams.

        """
        raise NotImplementedError
    # end def list

    def open(self):
        """Opens a stream for use.

        :rtype: IStream
        :returns: The appropriate stream.

        """
        raise NotImplementedError
    # end def open
# end class Container

class SingleStreamContainer(Container):
    """A convenience class for containers that only have a single stream.

    Subclasses are required to set the :attr:``stream`` attribute.

    """

    def list(self):
        """Lists streams inside the container.

        :rtype: list
        :returns: A list of StreamInfo objects that describe the stream.

        """
        return [StreamInfo(0)]
    # end def list

    def open(self):
        """Opens a stream for use.

        :rtype: IStream
        :returns: The stream.

        """
        return self.stream
    # end def open
# end class SingleStreamContainer

class StreamInfo():
    """Represents information about a stream.

    .. attribute:: id

        A container-unique identifier for the stream.

    """

    def __init__(self, id=0):
        """
        :type id: int
        :param id: An identifier for the stream.

        """
        self.id = id
    # end def __init__

    def __str__(self):
        """A string representation of the StreamInfo object."""

        return "{0}(id={1})".format(self.__class__.__name__, self.id)
    # end def __str__

    def __eq__(a, b):
        """a == b"""

        if isinstance(b, StreamInfo):
            return a.id == b.id
        # end if

        return False
    # end def __eq__

    def __ne__(a, b):
        """a != b"""

        return not a.__eq__(b)
    # end def __ne__
# end class StreamInfo

class IStream(RawIOBase):
    """Base class for input streams.

    All input streams are erquired to be seekable (random access).  Subclasses
    are required to implement the :meth:`seek`, :meth:`tell`, and
    :meth:`readinto` methods.

    .. attribute:: size

        The size of the stream in bytes.  If this value is not known, it is
        ``None``.
    """

    def __init__(self):
        """Initializes an IStream object."""
        self.size = None
    # end def __init__

    def seekable(self):
        """True if the stream is seekable."""

        return True
    # end def seekable

    def readable(self):
        """True if the stream is readable."""
        return True
    # end def readable

    def seek(offset, whence=SEEK_SET):
        """Positions the stream at offset, relative to whence.

        Valid values for whence are the same as the Python :mod:`io` module.
        The are:
            * SEEK_SET - The start of the stream.
            * SEEK_CUR - Current stream position.
            * SEEK_END - The end of the stream.

        :type offset: int
        :param offset: The position of the cursor

        :type whence: int
        :param whence: Tells :meth:`seek` how to interpret ``offset``.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The new position in the stream.
        """
        raise NotImplementedError
    # end def seek

    def tell(self):
        """Reads up to len(b) bytes into b.

        :type b: bytearray
        :param b: A bytearray to hold the bytes read from the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The number of bytes read.

        """
        raise NotImplementedError
    # end def tell
# end class IStream

class ManagedIStream(IStream):
    """An IStream that keeps track of stream position.


    This class is useful when implementing your own stream types.  The
    :meth:`seek`, and :meth:`tell` methods are provided.

    The :meth:`seek` and :meth:`tell` methods update the :attr:`_position`
    attribute.

    .. note::

        In order for this class to properly implement the :meth:`seek` method,
        subclasses are required to set the :attr:`size` attribute.

    .. attribute:: _position

        The absolute position of the stream.

    """

    def __init__(self):
        """Initializes a ManagedIStream object."""

        super(ManagedIStream, self).__init__()
        self._position = 0
    # end def __init__

    def seek(self, offset, whence=SEEK_SET):
        """Positions the stream at offset, relative to whence.

        Valid values for whence are the same as the Python :mod:`io` module.
        They are:

            * SEEK_SET - The start of the stream.
            * SEEK_CUR - Current stream position.
            * SEEK_END - The end of the stream.

        :type offset: int
        :param offset: The position of the cursor

        :type whence: int
        :param whence: Tells :meth:`seek` how to interpret ``offset``.

        :except ValueError: If the stream is closed, whence is not one of the
        SEEK_* constants, or whence is SEEK_SET and offset is negative.

        :rtype: int
        :returns: The new position in the stream.

        """

        if self.closed:
            raise ValueError("seek on closed stream")
        elif whence == SEEK_SET:
            if offset < 0:
                raise ValueError("negative seek value {0}".format(offset))
            # end if
            new_position = max(0, offset)
        elif whence == SEEK_CUR:
            new_position = max(0, self._position + offset)
        elif whence == SEEK_END:
            new_position = max(0, self.size + offset)
        else:
            raise ValueError("invalid whence: {0}".format(whence))
        # end if

        if new_position < 0:
            new_position = 0
        # end if

        self._position = new_position
        return new_position
    # end def seek

    def tell(self):
        """Returns the absolute position of the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The position in the stream.

        """

        if self.closed:
            raise ValueError("tell on closed stream")
        # end if

        return self._position
    # end def tell
# end class ManagedIStream

class IStreamWrapper(IStream):
    """An IStream that wraps around an existing Python :mod:`io` stream.

    .. attribute:: _stream

        The underlying stream to wrap around.

    """

    def __init__(self, stream, size=None):
        """Initializes an IStreamWrapper object.

        :type stream: IStream
        :param stream: The underlying stream to wrap around.

        :type size: int or None
        :param size: The size of the stream (in bytes) or None if not known.

        """
        super(IStreamWrapper, self).__init__()

        self.size = size
        self._stream = stream
    # end def __init__

    @property
    def closed(self):
        """True if the stream is closed."""

        return self._stream.closed
    # end def closed

    def close(self):
        """Closes the stream."""

        self._stream.close()
    # end def close

    def seek(self, offset, whence=SEEK_SET):
        """Positions the stream at offset, relative to whence.

        Valid values for whence are the same as the Python :mod:`io` module.
        They are:

            * SEEK_SET - The start of the stream.
            * SEEK_CUR - Current stream position.
            * SEEK_END - The end of the stream.

        :type offset: int
        :param offset: The position of the cursor

        :type whence: int
        :param whence: Tells :meth:`seek` how to interpret ``offset``.

        :except ValueError: If the stream is closed, whence is not one of the
            SEEK_* constants, or whence is SEEK_SET and offset is negative.

        :rtype: int
        :returns: The new position in the stream.

        """

        return self._stream.seek(offset, whence)
    # end def seek

    def tell(self):
        """Returns the absolute position of the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The position in the stream.

        """
        return self._stream.tell()
    # end def tell

    def read(self, n=-1):
        """Reads up to ``n`` bytes.

        :type n: int
        :param n: The number of bytes to read.  If this is -1, all bytes from
        the current position to EOF are read.

        :rtype: bytes
        :returns: The bytes read.

        """
        return self._stream.read(n)
    # end def read

    def readall(self):
        """Read and return all bytes in the stream, until EOF.

        :rtype: bytes
        :returns: The bytes read.

        """
        # Check if the underlying stream has readall(), and call it if it does,
        # otherwise use the inherited version.
        if hasattr(self._stream, "readall"):
            return self._stream.readall()
        # end if

        return super(IStreamWrapper, self).readall()
    # end def readall

    def readinto(self, b):
        """Reads upto len(b) bytes into b.

        :type b: bytearray
        :param b: A bytearray to hold the bytes read from the stream.

        :except ValueError: If the stream is closed.

        :rtype: int
        :returns: The number of bytes read.

        """
        return self._stream.readinto(b)
    # end def readinto
# end class IStreamWrapper
