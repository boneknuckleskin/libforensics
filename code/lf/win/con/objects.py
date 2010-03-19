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

"""Value objects (and factories) for Microsoft Windows console structures"""

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import LITTLE_ENDIAN, ActiveStructuple
from lf.win.con.ctypes import coord_le, coord_be

__docformat__ = "restructuredtext en"
__all__ = [
    "COORD"
]


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

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :rtype: :class:`COORD`
        :returns: The corresponding :class:`COORD` object.

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

        :type ctype: :class:`~lf.win.con.ctypes.coord_le` or
                     :class:`~lf.win.con.ctypes.coord_be`
        :param ctype: An instance of a coord ctype.

        :rtype: :class:`COORD`
        :returns: The corresponding :class:`COORD` object.

        """
        return COORD((ctype.x, ctype.y))
    # end def from_ctype
# end class COORD
