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

"""Unit tests for the lf.win.shell.recyclebin.objects module."""

__docformat__ = "restructuredtext en"

# stdlib imports
from unittest import TestCase
from datetime import datetime
from os.path import join

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.shell.recyclebin.objects import INFO2, INFO2Header, INFO2Item
from lf.win.shell.recyclebin.ctypes import info2_header, info2_item

__docformat__ = "restructuredtext en"
__all__ = [
    "INFO2TestCase", "INFO2HeaderTestCase", "INFO2ItemTestCase"
]

class INFO2TestCase(TestCase):
    def test__init__(self):
        ae = self.assertEqual

        file1 = join("data", "INFO2", "INFO2_1.bin")
        file2 = join("data", "INFO2", "INFO2_2.bin")

        stream1 = RawIStream(file1)
        stream2 = RawIStream(file2)
        stream2.seek(10)

        info2_1 = INFO2(stream1)
        info2_2 = INFO2(stream2, 0)

        header1 = INFO2Header.from_stream(stream1, 0)
        header2 = INFO2Header.from_stream(stream2, 0)

        items1 = [
            INFO2Item.from_stream(stream1, 0x14),
            INFO2Item.from_stream(stream1, 0x334),
            INFO2Item.from_stream(stream1, 0x654),
            INFO2Item.from_stream(stream1, 0x974)
        ]

        ae(info2_1.header, header1)
        ae(info2_2.header, header2)
        ae(info2_1.items, items1)
    # end def test__init__
# end class INFO2TestCase

class INFO2HeaderTestCase(TestCase):
    def test_from_ctype(self):
        ae = self.assertEqual

        data = bytearray(range(20))
        inst = info2_header.from_buffer_copy(data)
        header = INFO2Header.from_ctype(inst)

        ae(header.version, 0x03020100)
        ae(header.unknown1, 0x07060504)
        ae(header.unknown2, 0x0B0A0908)
        ae(header.item_size, 0x0F0E0D0C)
        ae(header.unknown3, 0x13121110)
    # end def test_from_ctype
# end class INFO2HeaderTestCase

class INFO2ItemTestCase(TestCase):
    def test_from_ctype(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"".join([b"abc123", b"\x00" * 254]))  # name_asc
        data.extend(b"\x00\x01\x02\x03")  # id
        data.extend(b"\x04\x05\x06\x07")  # drive_num
        data.extend(b"\x00\x0E\x15\x91\xC4\x95\xC2\x01")  # dtime
        data.extend(b"\x08\x09\x0A\x0B")  # file_size
        data.extend(b"".join([b"a\x00b", b"\x00" * 517]))  # name_uni
        inst = info2_item.from_buffer_copy(data)
        item = INFO2Item.from_ctype(inst)

        ae(item.name_asc, b"abc123")
        ae(item.id, 0x03020100)
        ae(item.drive_num, 0x07060504)
        ae(item.dtime, datetime(2002, 11, 27, 3, 25))
        ae(item.file_size, 0x0B0A0908)
        ae(item.name_uni, "ab")
        ae(item.exists, True)


        data[0] = 0
        data[268:276] = b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        data[280:282] = b"\x00\xD8"
        inst = info2_item.from_buffer_copy(data)
        item = INFO2Item.from_ctype(inst)

        ae(item.name_asc, b"\x00bc123")
        ae(item.id, 0x03020100)
        ae(item.drive_num, 0x07060504)
        ae(item.dtime, 0xFFFFFFFFFFFFFFFF)
        ae(item.file_size, 0x0B0A0908)
        ae(item.name_uni, "b")
        ae(item.exists, False)
    # end def test_from_ctype
# end class INFO2ItemTestCase
