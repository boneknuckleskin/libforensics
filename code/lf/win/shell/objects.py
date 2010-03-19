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

"""Objects for working with shell data types"""


# local imports
from lf.dec import SEEK_SET
from lf.dtypes import ActiveStructuple
from lf.dtypes.ctypes import uint16_le

__docformat__ = "restructuredtext en"
__all__ = [
    "SHITEMID", "ITEMIDLIST"
]

class SHITEMID(ActiveStructuple):
    """Represents a SHITEMID structure.

    .. attribute:: size

        The size of the SHITEMID structure. (calculated)

    .. attribute:: cb

        The count of bytes of the structure. (extracted)

    .. attribute:: abID

        An application defined BLOB of data.

    .. attribute:: id

        An alias for the :attr:`abID` attribute.
    """

    _fields_ = (
        "size", "cb", "abID"
    )
    _aliases_ = {
        "id": "abID"
    }
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`SHITEMID` from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`

        :rtype: :class:`SHITEMID`
        :returns: The corresponding :class:`SHITEMID` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(2)
        if len(data) < 2:
            return cls((len(data), 0, None))
        # end if

        size = uint16_le.from_buffer_copy(data).value
        if size <= 2:
            return cls((2, size, None))
        # end if

        data_size = size - 2
        data = stream.read(data_size)

        return cls((len(data) + 2, size, data))
    # end def from_stream
# end class SHITEMID

class ITEMIDLIST(ActiveStructuple):
    """Represents an ITEMIDLIST structure.

    .. attribute:: mkid

        A list of :class:`SHITEMID` structures.
    """

    _fields_ = ("mkid",)
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None, max_bytes=None):
        """Creates an :class:`ITEMIDLIST` from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`

        :type max_bytes: ``int``
        :param max_bytes: The maximum number of bytes to read from the stream.
                          If this is ``None`` then it is ignored.

        :rtype: :class:`ITEMIDLIST`
        :returns: The corresponding :class:`ITEMIDLIST` object.

        """
        mkid = list()

        if offset is None:
            offset = stream.tell()
        # end if

        itemid = SHITEMID.from_stream(stream, offset)
        mkid.append(itemid)

        if max_bytes is None:
            while itemid.cb >= 2:
                offset += itemid.size
                itemid = SHITEMID.from_stream(stream, offset)
                mkid.append(itemid)
            # end while
        else:
            offset += itemid.size
            bytes_read = itemid.size

            while (itemid.cb >= 2) and (bytes_read < max_bytes):
                itemid = SHITEMID.from_stream(stream, offset)
                offset += itemid.cb
                bytes_read += itemid.cb

                if bytes_read <= max_bytes:
                    mkid.append(itemid)
                else:
                    break
                # end if
            # end while
        # end if

        return cls((mkid,))
    # end def from_stream
# end class ITEMIDLIST
