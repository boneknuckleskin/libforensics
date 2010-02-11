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

"""Unit tests for the lf.dec.composite module."""

# stdlib imports
from unittest import TestCase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import StreamInfo
from lf.dec.byte import ByteIStream
from lf.dec.composite import Composite, CompositeIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "CompositeTestCase", "CompositeIStreamTestCase"
]

class CompositeTestCase(TestCase):
    def setUp(self):
        segments = [
            (ByteIStream(b"*******abcde**************"), 7, 5),
            (ByteIStream(b"******fghi****************"), 6, 4),
            (ByteIStream(b"jklmn*********************"), 0, 5),
            (ByteIStream(b"*****************opqrstuvw"), 17, 9),
            (ByteIStream(b"*******************xy*****"), 19, 2),
            (ByteIStream(b"z"), 0, 1)
        ]

        self.composite = Composite(segments)
    # end def setUp

    def test_list(self):
        ae = self.assertEqual
        ae(self.composite.list(), [StreamInfo(0)])
    # end def test_list

    def test_open(self):
        ae = self.assertEqual
        ae(self.composite.open(), self.composite.stream)
    # end def test_open
# end class CompositeTestCase

class CompositeIStreamTestCase(TestCase):
    def setUp(self):
        segments = [
            (ByteIStream(b"*******abcde**************"), 7, 5),
            (ByteIStream(b"******fghi****************"), 6, 4),
            (ByteIStream(b"jklmn*********************"), 0, 5),
            (ByteIStream(b"*****************opqrstuvw"), 17, 9),
            (ByteIStream(b"*******************xy*****"), 19, 2),
            (ByteIStream(b"z"), 0, 1)
        ]

        self.segments = segments
        self.cis = CompositeIStream(segments)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.cis.size, 26)
        ae(self.cis._segments, self.segments)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        cis = self.cis

        ae(cis.seek(10, SEEK_SET), 10)
        ae(cis._position, 10)
        ar(ValueError, cis.seek, -10, SEEK_SET)

        cis.seek(3, SEEK_SET)
        ae(cis.seek(5, SEEK_CUR), 8)
        ae(cis._position, 8)

        ae(cis.seek(-2, SEEK_CUR), 6)
        ae(cis._position, 6)

        ae(cis.seek(-3, SEEK_END), 23)
        ae(cis._position, 23)

        ae(cis.seek(3, SEEK_END), 29)
        ae(cis._position, 29)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        cis = self.cis

        cis._position = 0
        ae(cis.tell(), 0)

        cis._position = 2
        ae(cis.tell(), 2)
    # end def test_tell

    def test_read(self):
        ae = self.assertEqual

        self.cis.seek(0, SEEK_SET)
        ae(self.cis.read(0), b"")
        ae(self.cis.read(1), b"a")
        ae(self.cis.read(2), b"bc")
        ae(self.cis.read(), b"defghijklmnopqrstuvwxyz")

        self.cis.seek(-3, SEEK_END)
        ae(self.cis.read(5), b"xyz")

        self.cis.seek(30, SEEK_SET)
        ae(self.cis.read(), b"")
    # end def test_read

    def test_readall(self):
        ae = self.assertEqual

        self.cis.seek(0, SEEK_SET)
        ae(self.cis.readall(), b"abcdefghijklmnopqrstuvwxyz")
        self.cis.seek(3, SEEK_SET)
        ae(self.cis.readall(), b"defghijklmnopqrstuvwxyz")
    # end def test_readall

    def test_readinto(self):
        ae = self.assertEqual
        cis = self.cis

        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)
        barray3 = bytearray(1)

        cis.seek(-12, SEEK_END)
        retval0 = cis.readinto(barray0)
        retval1 = cis.readinto(barray1)

        cis.seek(0, SEEK_SET)
        retval2 = cis.readinto(barray2)

        cis.seek(30, SEEK_SET)
        retval3 = cis.readinto(barray3)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)
        ae(retval3, 0)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
        ae(barray3, b"\x00")
    # end def test_readinto
# end class CompositeIStreamTestCase
