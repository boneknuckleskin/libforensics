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

"""Unit tests for the lf.dec.byte module."""

# stdlib imports
from unittest import TestCase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import StreamInfo
from lf.dec.byte import Byte, ByteIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "ByteTestCase", "ByteIStreamTestCase"
]

class ByteTestCase(TestCase):
    def setUp(self):
        self.byte = Byte(b"abcdefghijklmnopqrstuvwxyz")
    # end def setUp

    def test_list(self):
        ae = self.assertEqual
        ae(self.byte.list(), [StreamInfo(0)])
    # end def test_list

    def test_open(self):
        ae = self.assertEqual
        ae(self.byte.open(), self.byte.stream)
    # end def test_open
# end class ByteTestCase

class ByteIStreamTestCase(TestCase):
    def setUp(self):
        data = b"abcdefghijklmnopqrstuvwxyz"
        self.bis = ByteIStream(data)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.bis.size, 26)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        bis = self.bis

        ae(bis.seek(10, SEEK_SET), 10)
        ae(bis._stream.tell(), 10)
        ar(ValueError, bis.seek, -10, SEEK_SET)

        bis.seek(3, SEEK_SET)
        ae(bis.seek(5, SEEK_CUR), 8)
        ae(bis._stream.tell(), 8)

        ae(bis.seek(-2, SEEK_CUR), 6)
        ae(bis._stream.tell(), 6)

        ae(bis.seek(-3, SEEK_END), 23)
        ae(bis._stream.tell(), 23)

        ae(bis.seek(3, SEEK_END), 29)
        ae(bis._stream.tell(), 29)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        bis = self.bis
        stream = self.bis._stream

        stream.seek(0, SEEK_SET)
        ae(bis.tell(), 0)

        stream.seek(2, SEEK_SET)
        ae(bis.tell(), 2)
    # end def test_tell

    def test_read(self):
        ae = self.assertEqual

        self.bis.seek(0, SEEK_SET)
        ae(self.bis.read(0), b"")
        ae(self.bis.read(1), b"a")
        ae(self.bis.read(2), b"bc")
        ae(self.bis.read(), b"defghijklmnopqrstuvwxyz")

        self.bis.seek(30, SEEK_SET)
        ae(self.bis.read(), b"")

        self.bis.seek(-3, SEEK_END)
        ae(self.bis.read(5), b"xyz")
    # end def test_read

    def test_readall(self):
        ae = self.assertEqual

        self.bis.seek(0, SEEK_SET)
        ae(self.bis.readall(), b"abcdefghijklmnopqrstuvwxyz")
        self.bis.seek(3, SEEK_SET)
        ae(self.bis.readall(), b"defghijklmnopqrstuvwxyz")
    # end def test_readall

    def test_readinto(self):
        ae = self.assertEqual
        bis = self.bis

        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)
        barray3 = bytearray(1)

        bis.seek(-12, SEEK_END)
        retval0 = bis.readinto(barray0)
        retval1 = bis.readinto(barray1)

        bis.seek(0, SEEK_SET)
        retval2 = bis.readinto(barray2)

        bis.seek(30, SEEK_SET)
        retval3 = bis.readinto(barray3)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)
        ae(retval3, 0)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
        ae(barray3, b"\x00")
    # end def test_readinto
# end class ByteIStreamTestCase
