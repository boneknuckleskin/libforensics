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

"""Read recycle bin INFO2 files."""

# stdlib imports
from ctypes import sizeof
from codecs import getdecoder

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import CtypesWrapper
from lf.time import FILETIMETodatetime
from lf.win.shell.recyclebin.ctypes import info2_header, info2_item

# module globals
_utf16_le_decoder = getdecoder("utf_16_le")

__docformat__ = "restructuredtext en"
__all__ = [
    "INFO2", "INFO2Header", "INFO2Item"
]

class INFO2():
    """Represents an INFO2 file.

    .. attribute:: header

        An instance of a :class:`INFO2Header`.

    .. attribute:: items

        A list of :class:`INFO2Item` objects.

    """

    def __init__(self, stream, offset=None):
        """Initializes an INFO2 file.

        :type stream: :class:`~lf.dec.IStream`.
        :param stream: A stream that contains the INFO2 file.

        :type offset: ``int``
        :param offset: The start of the INFO2 file in :attr:`stream`.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        header = INFO2Header.from_stream(stream, offset)
        offset += 20

        item_size = header.item_size
        if item_size < 800:
            pad = b"\x00" * (800 - item_size)
        else:
            pad = b""
        # end if

        items = list()
        stream.seek(offset, SEEK_SET)
        data = stream.read(item_size)

        while data:
            data = b"".join([data, pad])
            items.append(INFO2Item.from_bytes(data[:800]))

            offset += item_size
            stream.seek(offset, SEEK_SET)
            data = stream.read(item_size)
        # end while

        self.header = header
        self.items = items
    # end def __init__
# end class INFO2

class INFO2Header(CtypesWrapper):
    """Represents the header from an INFO2 file.

    .. attribute:: version

        The version of the INFO2 file.

    .. attribute:: item_size

        The size of an :class:`INFO2Item`.

    .. attribute:: unknown1

        The first unknown value (bytes 4-7)

    .. attribute:: unknown2

        The second unknown value (bytes 8-11)

    .. attribute:: unknown3

        The thirdunknown value (bytes 16-19)

    """

    _ctype_ = info2_header
    _fields_ = (
        "version", "unknown1", "unknown2", "item_size", "unknown3"
    )
# end class INFO2Header

class INFO2Item(CtypesWrapper):
    """Represents an item in an INFO2 file.

    .. attribute:: name_asc

        The name of the deleted file (ASCII).

    .. attribute:: index

        The index of the deleted file.

    .. attribute:: drive_num

        The drive number the file was deleted from.

    .. attribute:: dtime

        The time the file was deleted.

    .. attribute:: file_size

        The size of the deleted file.

    .. attribute:: name_uni

        The name of the deleted file (unicode), or ``None`` if not present.

    .. attribute:: exists

        ``True`` if the corresponding file exists on disk.

    """

    _ctype_ = info2_item
    _fields_ = (
        "name_asc", "index", "drive_num", "dtime", "file_size", "name_uni",
        "exists"
    )

    @classmethod
    def from_ctype(cls, ctype):
        """ Creates a :class:`INFO2Item` object from a ctype.

        :type ctype: :class:`~lf.win.shell.recyclebin.ctypes.info2_item`
        :param ctype: An info2_item object.

        :rtype: :class:`INFO2Item`
        :returns: The corresponding :class:`INFO2Item` object.

        """
        if ctype.name_asc[0] == 0:
            exists = False
            start = 1
        else:
            exists = True
            start = 0
        # end if

        name_asc = bytes(ctype.name_asc)
        null_term = name_asc.find(b"\x00", start)
        if null_term != -1:
            name_asc = name_asc[:null_term]
        # end if

        name_uni = bytes(ctype.name_uni)
        new_name_uni = _utf16_le_decoder(name_uni, "ignore")[0]
        if new_name_uni:
            name_uni = new_name_uni.split("\x00", 1)[0]
        else:
            name_uni = name_uni.split(b"\x00", 1)[0]
        # end if

        try:
            dtime = FILETIMETodatetime.from_ctype(ctype.dtime)
        except ValueError:
            dtime = (ctype.dtime.hi << 32) | ctype.dtime.lo
        # end try

        return cls((
            name_asc, ctype.index, ctype.drive_num, dtime, ctype.file_size,
            name_uni, exists
        ))
    # end def from_ctype
# end class INFO2Item
