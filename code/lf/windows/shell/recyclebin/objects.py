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
Classes to work with recycle bin (INFO2) files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

from lf.io.consts import SEEK_SET
from lf.utils.time import filetime_to_datetime
from lf.windows.shell.recyclebin.extractors import header, item

class INFO2():
    """
    Represents an INFO2 file.

    .. attribute:: item_size

        The size of an INFO2 item.

    .. attribute:: count

        The total number of items (from the file header).

    .. attribute:: items

        A list of items, as Item objects.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes an INFO2 object.

        :parameters:
            stream
                A stream that points to the INFO2 file.

            offset
                The start of the INFO2 file, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        info2_header = header.extract(stream.read(20))
        offset += 20

        if header.size > item.size:
            skip  = (header.size - item.size)
        else:
            skip = 0
        # end if

        calc_count = stream.size // item.size

        items = list()
        for counter in range(calc_count):
            items.append(Item(stream, offset))
            offset += (800 + skip)
        # end for

        self.item_size = info2_header.item_size
        self.count = info2_header.count
        self.items = items
    # end def __init__
# end class INFO2

class Item():
    """
    Represents an item in an INFO2 file.

    .. attribute:: index

        The numeric index that corresponds to the deleted file.

    .. attribute:: name_asc

        The name (and full path) in ASCII

    .. attribute: name_uni

        The name (and full path) in 16-bit, little endian unicode.

    .. attribute:: drive_num

        The drive number the file was deleted from.

    .. attribute:: dtime

        The time the file was deleted.

    .. attribute:: phys_size

        The physical size of the deleted file.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes an item object.

        :parameters:
            stream
                A stream that contains the INFO2 item.

            offset
                The start of the INFO2 item, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        info2_item = item.extract(stream.read(800))

        self.index = info2_item.index
        self.drive_num = info2_item.drive_num
        try:
            self.dtime = filetime_to_datetime(info2_item.dtime)
        except KeyboardInterrupt:
            raise
        except:
            self.dtime = info2_item.dtime
        # end try

        # Sometimes the first character is not the drive letter, so swap it in
        name_asc = info2_item.name_asc
        first_char = (chr(ord("A") + info2_item.drive_num)).encode("ascii")
        name_asc = b"".join([first_char, name_asc[1:]])
        name_asc = name_asc[:name_asc.find(b"\x00")]

        name_uni = info2_item.name_uni
        name_uni = name_uni[:name_uni.find(b"\x00\x00")+1]

        self.name_asc = name_asc.decode("ascii")
        self.name_uni = name_uni.decode("utf_16_le")
        self.phys_size = info2_item.phys_size
    # end def __init__
# end class Item
