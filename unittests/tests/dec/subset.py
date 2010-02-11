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

"""Unit tests for the lf.dec.subset module."""

# stdlib imports
from unittest import TestCase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import StreamInfo
from lf.dec.byte import ByteIStream
from lf.dec.subset import Subset, SubsetIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "SubsetTestCase", "SubsetIStreamTestCase"
]

class SubsetTestCase(TestCase):
    def setUp(self):
        data = b"**abcdefghijklmnopqrstuvwxyz"
        stream = ByteIStream(data)
        self.subset = Subset(stream, 2, 26)
    # end def setUp

    def test_list(self):
        ae = self.assertEqual
        ae(self.subset.list(), [StreamInfo(0)])
    # end def test_list

    def test_open(self):
        ae = self.assertEqual
        ae(self.subset.open(), self.subset.stream)
    # end def test_open
# end class SubsetTestCase

class SubsetIStreamTestCase(TestCase):
    def setUp(self):
        data = b"**abcdefghijklmnopqrstuvwxyz"
        stream = ByteIStream(data)

        self.byte_istream = stream
        self.sis = SubsetIStream(stream, 2, 26)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.sis.size, 26)
        ae(self.sis._stream, self.byte_istream)
        ae(self.sis._start, 2)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        sis = self.sis

        ae(sis.seek(10, SEEK_SET), 10)
        ae(sis._position, 10)
        ar(ValueError, sis.seek, -10, SEEK_SET)

        sis.seek(3, SEEK_SET)
        ae(sis.seek(5, SEEK_CUR), 8)
        ae(sis._position, 8)

        ae(sis.seek(-2, SEEK_CUR), 6)
        ae(sis._position, 6)

        ae(sis.seek(-3, SEEK_END), 23)
        ae(sis._position, 23)

        ae(sis.seek(3, SEEK_END), 29)
        ae(sis._position, 29)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        sis = self.sis

        sis._position = 0
        ae(sis.tell(), 0)

        sis._position = 2
        ae(sis.tell(), 2)
    # end def test_tell

    def test_read(self):
        ae = self.assertEqual

        self.sis.seek(0, SEEK_SET)
        ae(self.sis.read(0), b"")
        ae(self.sis.read(1), b"a")
        ae(self.sis.read(2), b"bc")
        ae(self.sis.read(), b"defghijklmnopqrstuvwxyz")

        self.sis.seek(-3, SEEK_END)
        ae(self.sis.read(5), b"xyz")

        self.sis.seek(30, SEEK_SET)
        ae(self.sis.read(), b"")
    # end def test_read

    def test_readall(self):
        ae = self.assertEqual

        self.sis.seek(0, SEEK_SET)
        ae(self.sis.readall(), b"abcdefghijklmnopqrstuvwxyz")
        self.sis.seek(3, SEEK_SET)
        ae(self.sis.readall(), b"defghijklmnopqrstuvwxyz")
    # end def test_readall

    def test_readinto(self):
        ae = self.assertEqual
        sis = self.sis

        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)
        barray3 = bytearray(1)

        sis.seek(-12, SEEK_END)
        retval0 = sis.readinto(barray0)
        retval1 = sis.readinto(barray1)

        sis.seek(0, SEEK_SET)
        retval2 = sis.readinto(barray2)

        sis.seek(30, SEEK_SET)
        retval3 = sis.readinto(barray3)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)
        ae(retval3, 0)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
        ae(barray3, b"\x00")
    # end def test_readinto
# end class SubsetIStreamTestCase
