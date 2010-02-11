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

"""Unit tests for the lf.dec.splitraw module."""

# stdlib imports
import os.path
from unittest import TestCase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import StreamInfo
from lf.dec.splitraw import SplitRaw, SplitRawIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "SplitRawTestCase", "SplitRawIStreamTestCase"
]

class SplitRawTestCase(TestCase):
    def setUp(self):
        names = ["alpha{0}.txt".format(x) for x in range(1,7)]
        names = [os.path.join("data", "txt", name) for name in names]

        self.splitraw = SplitRaw(names)
    # end def setUp

    def test_list(self):
        ae = self.assertEqual
        ae(self.splitraw.list(), [StreamInfo(0)])
    # end def test_list

    def test_open(self):
        ae = self.assertEqual
        ae(self.splitraw.open(), self.splitraw.stream)
    # end def test_open
# end class SplitRawTestCase

class SplitRawIStreamTestCase(TestCase):
    def setUp(self):
        names = ["alpha{0}.txt".format(x) for x in range(1,7)]
        names = [os.path.join("data", "txt", name) for name in names]

        self.names = names
        self.sris = SplitRawIStream(names)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.sris.size, 26)
        ae(self.sris._names, self.names)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        sris = self.sris

        ae(sris.seek(10, SEEK_SET), 10)
        ae(sris._position, 10)
        ar(ValueError, sris.seek, -10, SEEK_SET)

        sris.seek(3, SEEK_SET)
        ae(sris.seek(5, SEEK_CUR), 8)
        ae(sris._position, 8)

        ae(sris.seek(-2, SEEK_CUR), 6)
        ae(sris._position, 6)

        ae(sris.seek(-3, SEEK_END), 23)
        ae(sris._position, 23)

        ae(sris.seek(3, SEEK_END), 29)
        ae(sris._position, 29)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        sris = self.sris

        sris._position = 0
        ae(sris.tell(), 0)

        sris._position = 2
        ae(sris.tell(), 2)
    # end def test_tell

    def test_read(self):
        ae = self.assertEqual

        self.sris.seek(0, SEEK_SET)
        ae(self.sris.read(0), b"")
        ae(self.sris.read(1), b"a")
        ae(self.sris.read(2), b"bc")
        ae(self.sris.read(), b"defghijklmnopqrstuvwxyz")

        self.sris.seek(-3, SEEK_END)
        ae(self.sris.read(5), b"xyz")

        self.sris.seek(30, SEEK_SET)
        ae(self.sris.read(), b"")
    # end def test_read

    def test_readall(self):
        ae = self.assertEqual

        self.sris.seek(0, SEEK_SET)
        ae(self.sris.readall(), b"abcdefghijklmnopqrstuvwxyz")
        self.sris.seek(3, SEEK_SET)
        ae(self.sris.readall(), b"defghijklmnopqrstuvwxyz")
    # end def test_readall

    def test_readinto(self):
        ae = self.assertEqual
        sris = self.sris

        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)
        barray3 = bytearray(1)

        sris.seek(-12, SEEK_END)
        retval0 = sris.readinto(barray0)
        retval1 = sris.readinto(barray1)

        sris.seek(0, SEEK_SET)
        retval2 = sris.readinto(barray2)

        sris.seek(30, SEEK_SET)
        retval3 = sris.readinto(barray3)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)
        ae(retval3, 0)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
        ae(barray3, b"\x00")
    # end def test_readinto
# end class SplitRawIStreamTestCase
