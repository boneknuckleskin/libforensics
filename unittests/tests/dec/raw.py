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

"""Unit tests for the lf.dec.raw module."""

# stdlib imports
import os.path
from unittest import TestCase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import StreamInfo
from lf.dec.raw import Raw, RawIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "RawTestCase", "RawIStreamTestCase"
]

class RawTestCase(TestCase):
    def setUp(self):
        name = os.path.join("data", "txt", "alpha.txt")
        self.raw = Raw(name)
    # end def setUp

    def test_list(self):
        ae = self.assertEqual
        ae(self.raw.list(), [StreamInfo(0)])
    # end def test_list

    def test_open(self):
        ae = self.assertEqual
        ae(self.raw.open(), self.raw.stream)
    # end def test_open
# end class RawTestCase

class RawIStreamTestCase(TestCase):
    def setUp(self):
        name = os.path.join("data", "txt", "alpha.txt")
        self.ris = RawIStream(name)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.ris.size, 26)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        ris = self.ris

        ae(ris.seek(10, SEEK_SET), 10)
        ae(ris._stream.tell(), 10)
        ar(IOError, ris.seek, -10, SEEK_SET)

        ris.seek(3, SEEK_SET)
        ae(ris.seek(5, SEEK_CUR), 8)
        ae(ris._stream.tell(), 8)

        ae(ris.seek(-2, SEEK_CUR), 6)
        ae(ris._stream.tell(), 6)

        ae(ris.seek(-3, SEEK_END), 23)
        ae(ris._stream.tell(), 23)

        ae(ris.seek(3, SEEK_END), 29)
        ae(ris._stream.tell(), 29)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        ris = self.ris
        stream = self.ris._stream

        stream.seek(0, SEEK_SET)
        ae(ris.tell(), 0)

        stream.seek(2, SEEK_SET)
        ae(ris.tell(), 2)
    # end def test_tell

    def test_read(self):
        ae = self.assertEqual

        self.ris.seek(0, SEEK_SET)
        ae(self.ris.read(0), b"")
        ae(self.ris.read(1), b"a")
        ae(self.ris.read(2), b"bc")
        ae(self.ris.read(), b"defghijklmnopqrstuvwxyz")

        self.ris.seek(-3, SEEK_END)
        ae(self.ris.read(5), b"xyz")

        self.ris.seek(30, SEEK_SET)
        ae(self.ris.read(), b"")
    # end def test_read

    def test_readall(self):
        ae = self.assertEqual

        self.ris.seek(0, SEEK_SET)
        ae(self.ris.readall(), b"abcdefghijklmnopqrstuvwxyz")
        self.ris.seek(3, SEEK_SET)
        ae(self.ris.readall(), b"defghijklmnopqrstuvwxyz")
    # end def test_readall

    def test_readinto(self):
        ae = self.assertEqual
        ris = self.ris

        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)
        barray3 = bytearray(1)

        ris.seek(-12, SEEK_END)
        retval0 = ris.readinto(barray0)
        retval1 = ris.readinto(barray1)

        ris.seek(0, SEEK_SET)
        retval2 = ris.readinto(barray2)

        ris.seek(30, SEEK_SET)
        retval3 = ris.readinto(barray3)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)
        ae(retval3, 0)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
        ae(barray3, b"\x00")
    # end def test_readinto
# end class RawIStreamTestCase
