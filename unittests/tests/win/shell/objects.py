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

"""Unit tests for the lf.win.shell.objects module."""


# stdlib imports
from io import BytesIO
from unittest import TestCase

# local imports
from lf.dec import ByteIStream
from lf.win.shell.objects import SHITEMID, ITEMIDLIST

__docformat__ = "restructuredtext en"
__all__ = [
    "SHITEMIDTestCase", "ITEMIDLISTTestcase"
]

class SHITEMIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        # good size
        stream = ByteIStream(b"\x06\x00abcd")
        item1 = SHITEMID.from_stream(stream)
        item2 = SHITEMID.from_stream(stream, 0)

        ae(item1.size, 6)
        ae(item1.cb, 6)
        ae(item1.abID, b"abcd")
        ae(item1.id, item1.abID)

        ae(item2.size, 6)
        ae(item2.cb, 6)
        ae(item2.abID, b"abcd")
        ae(item2.id, item2.abID)

        # good size
        stream = ByteIStream(b"\x04\x00abcd")
        item1 = SHITEMID.from_stream(stream)
        item2 = SHITEMID.from_stream(stream, 0)

        ae(item1.size, 4)
        ae(item1.cb, 4)
        ae(item1.abID, b"ab")
        ae(item1.id, item1.abID)

        ae(item2.size, 4)
        ae(item2.cb, 4)
        ae(item2.abID, b"ab")
        ae(item2.id, item2.abID)


        # bad size
        stream = ByteIStream(b"\x08\x00ab")
        item1 = SHITEMID.from_stream(stream)
        item2 = SHITEMID.from_stream(stream, 0)

        ae(item1.size, 4)
        ae(item1.cb, 8)
        ae(item1.abID, b"ab")
        ae(item1.id, item1.abID)

        ae(item2.size, 4)
        ae(item2.cb, 8)
        ae(item2.abID, b"ab")
        ae(item2.id, item2.abID)
    # end def test_from_stream
# end class SHITEMIDTestCase

class ITEMIDLISTTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        item1 = b"\x06\x00\x01\x02\x03\x04"
        item2 = b"\x05\x00\x05\x06\x07"
        item3 = b"\x04\x00\x08\x09"
        little_item = b"\x01\x00"
        big_item = b"\xFF\x00\x64\x53"
        null_item = b"\x00\x00"

        itemid1 = SHITEMID((6, 6, b"\x01\x02\x03\x04"))
        itemid2 = SHITEMID((5, 5, b"\x05\x06\x07"))
        itemid3 = SHITEMID((4, 4, b"\x08\x09"))
        little_itemid = SHITEMID((2, 1, None))
        big_itemid = SHITEMID((4, 0xFF, b"\x64\x53"))
        null_itemid = SHITEMID((2, 0, None))
        zero_itemid = SHITEMID((0, 0, None))


        stream = ByteIStream(b"".join([item1, item2, item3, null_item]))
        list1 = ITEMIDLIST.from_stream(stream, max_bytes=stream.size)
        list2 = ITEMIDLIST.from_stream(stream, 0, max_bytes=stream.size)
        list3 = ITEMIDLIST.from_stream(stream, 0)

        ae(list1.mkid, [itemid1, itemid2, itemid3, null_itemid])
        ae(list2.mkid, [itemid1, itemid2, itemid3, null_itemid])
        ae(list3.mkid, [itemid1, itemid2, itemid3, null_itemid])


        stream = ByteIStream(b"".join([item1, item2, item3, big_item]))
        list1 = ITEMIDLIST.from_stream(stream)
        ae(list1.mkid, [itemid1, itemid2, itemid3, big_itemid, zero_itemid])


        stream = ByteIStream(b"".join([item1, little_item, item2]))
        list1 = ITEMIDLIST.from_stream(stream)
        ae(list1.mkid, [itemid1, little_itemid])


        stream = ByteIStream(b"".join([item1, item2, item3]))
        list1 = ITEMIDLIST.from_stream(stream, max_bytes=13)
        list2 = ITEMIDLIST.from_stream(stream, 0, max_bytes=14)

        ae(list1.mkid, [itemid1, itemid2])
        ae(list2.mkid, [itemid1, itemid2])
    # end def test_from_stream
# end class ITEMIDLISTTestCase
