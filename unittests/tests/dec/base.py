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

"""Unit tests for the lf.dec.base module."""

# stdlib imports
from _pyio import BytesIO
from unittest import TestCase

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import (
    SingleStreamContainer, StreamInfo, ManagedIStream, IStreamWrapper
)

__docformat__ = "restructuredtext en"
__all__ = [
    "SingleStreamContainerTestCase", "StreamInfoTestCase",
    "ManagedIStreamTestCase", "IStreamWrapperTestCase"
]

class SingleStreamContainerTestCase(TestCase):
    def setUp(self):
        class MockSSC(SingleStreamContainer):
            def __init__(self):
                self.stream = 1
            # end def __init__
        # end class MockSSC

        self.ssc = MockSSC()
    # end def setUp

    def test_list(self):
        ae = self.assertEqual
        ae(self.ssc.list(), [StreamInfo(0)])
    # end def test_list

    def test_open(self):
        ae = self.assertEqual
        ae(self.ssc.open(), self.ssc.stream)
    # end def test_open
# end class SingleStreamContainerTestCase

class StreamInfoTestCase(TestCase):
    def test__init__(self):
        ae = self.assertEqual

        si = StreamInfo(2)
        ae(si.id, 2)
    # end def test__init__

    def test__str__(self):
        ae = self.assertEqual

        si = StreamInfo(3)
        ae(str(si), "StreamInfo(id=3)")
    # end def test_str__

    def test__eq__(self):
        at = self.assertTrue
        af = self.assertFalse

        at(StreamInfo(0) == StreamInfo(0))
        af(StreamInfo(0) == StreamInfo(1))
    # end def test__eq__

    def test__ne__(self):
        at = self.assertTrue
        af = self.assertFalse

        at(StreamInfo(0) != StreamInfo(1))
        af(StreamInfo(0) != StreamInfo(0))
    # end def test__ne__
# end class StreamInfoTestCase

class ManagedIStreamTestCase(TestCase):
    def setUp(self):
        self.mis = ManagedIStream()
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        mis = self.mis

        ae(mis._position, 0)
        ae(mis.size, None)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        mis = self.mis

        ae(mis.seek(10, SEEK_SET), 10)
        ar(ValueError, mis.seek, -10, SEEK_SET)

        mis.seek(3, SEEK_SET)
        ae(mis.seek(5, SEEK_CUR), 8)
        ae(mis.seek(-2, SEEK_CUR), 6)

        mis.size = 10
        ae(mis.seek(-3, SEEK_END), 7)
        ae(mis.seek(3, SEEK_END), 13)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        mis = self.mis

        ae(mis.tell(), 0)
        mis._position = 10
        ae(mis.tell(), 10)
    # end def test_tell
# end class ManagedIStreamTestCase

class IStreamWrapperTestCase(TestCase):
    def setUp(self):
        data = b"abcdefghijklmnopqrstuvwxyz"
        bytes_io = BytesIO(data)

        self.bytes_io = bytes_io
        self.isw = IStreamWrapper(bytes_io, len(data))
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.isw.size, 26)
        ae(self.isw._stream, self.bytes_io)
    # end def test__init__

    def test_seek(self):
        ae = self.assertEqual
        ar = self.assertRaises
        isw = self.isw

        ae(isw.seek(10, SEEK_SET), 10)
        ae(isw._stream.tell(), 10)
        ar(ValueError, isw.seek, -10, SEEK_SET)

        isw.seek(3, SEEK_SET)
        ae(isw.seek(5, SEEK_CUR), 8)
        ae(isw._stream.tell(), 8)

        ae(isw.seek(-2, SEEK_CUR), 6)
        ae(isw._stream.tell(), 6)

        ae(isw.seek(-3, SEEK_END), 23)
        ae(isw._stream.tell(), 23)

        ae(isw.seek(3, SEEK_END), 29)
        ae(isw._stream.tell(), 29)
    # end def test_seek

    def test_tell(self):
        ae = self.assertEqual
        isw = self.isw
        bytes_io = self.bytes_io

        bytes_io.seek(0, SEEK_SET)
        ae(isw.tell(), 0)

        bytes_io.seek(2, SEEK_SET)
        ae(isw.tell(), 2)
    # end def test_tell

    def test_read(self):
        ae = self.assertEqual

        self.isw.seek(0, SEEK_SET)
        ae(self.isw.read(0), b"")
        ae(self.isw.read(1), b"a")
        ae(self.isw.read(2), b"bc")
        ae(self.isw.read(), b"defghijklmnopqrstuvwxyz")

        self.isw.seek(-3, SEEK_END)
        ae(self.isw.read(5), b"xyz")

        self.isw.seek(30, SEEK_SET)
        ae(self.isw.read(), b"")
    # end def test_read

    def test_readall(self):
        ae = self.assertEqual

        self.isw.seek(0, SEEK_SET)
        ae(self.isw.readall(), b"abcdefghijklmnopqrstuvwxyz")
        self.isw.seek(3, SEEK_SET)
        ae(self.isw.readall(), b"defghijklmnopqrstuvwxyz")
    # end def test_readall

    def test_readinto(self):
        ae = self.assertEqual
        isw = self.isw

        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)
        barray3 = bytearray(1)

        isw.seek(-12, SEEK_END)
        retval0 = isw.readinto(barray0)
        retval1 = isw.readinto(barray1)

        isw.seek(0, SEEK_SET)
        retval2 = isw.readinto(barray2)

        isw.seek(30, SEEK_SET)
        retval3 = isw.readinto(barray3)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)
        ae(retval3, 0)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
        ae(barray3, b"\x00")
    # end def test_readinto
# end class IStreamWrapperTestCase
