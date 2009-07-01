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
Code to unit test the interface of the various lf.core.stream.* modules.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

import unittest
from os.path import join

from io import BytesIO
from lf.io import base, byte, composite, raw, splitraw, subset

class TestMethods():
    def test__init__(self):
        io_obj = self.io_obj
        ae = self.assertEqual

        ae(io_obj.size, 26)
        ae(io_obj.closed, False)
    # end def test__init__

    def test_len(self):
        self.assertEqual(len(self.io_obj), 26)
    # end def test_len

    def test_readable(self):
        self.assertTrue(self.io_obj.readable())
    # end def test_readable

    def test_seekable(self):
        self.assertTrue(self.io_obj.seekable())
    # end def test_seekable

    def test_close(self):
        io_obj = self.io_obj
        io_obj.seek(12, 0)
        io_obj.close()

        self.assertEqual(io_obj.size, 0)
        self.assertEqual(io_obj.closed, True)
        self.assertRaises((IOError, ValueError), io_obj.seek, 12, 0)
    # end def test_close

    def test_seek(self):
        io_obj = self.io_obj
        ae = self.assertEqual
        ar = self.assertRaises

        barray = bytearray(5)
        retval = io_obj.seek(-5, 2)
        ae(retval, 21)
        ae(io_obj.tell(), 21)

        io_obj.readinto(barray)
        ae(barray, b"vwxyz")

        retval = io_obj.seek(10, 0)
        ae(retval, 10)
        ae(io_obj.tell(), 10)

        io_obj.readinto(barray)
        ae(barray, b"klmno")

        retval = io_obj.seek(2, 1)
        ae(retval, 17)
        ae(io_obj.tell(), 17)

        io_obj.readinto(barray)
        ae(barray, b"rstuv")

        ar((IOError, ValueError), io_obj.seek, -1, 0)
        ar((IOError, ValueError), io_obj.seek, 3, 5)
    # end def test_seek

    def test_tell(self):
        io_obj = self.io_obj
        ae = self.assertEqual

        io_obj.seek(5, 0)
        ae(io_obj.tell(), 5)

        io_obj.seek(5, 1)
        ae(io_obj.tell(), 10)
    # end def test_tell

    def test_readinto(self):
        io_obj = self.io_obj
        ae = self.assertEqual
        barray0 = bytearray(5)
        barray1 = bytearray(10)
        barray2 = bytearray(26)

        io_obj.seek(-12, 2)
        retval0 = io_obj.readinto(barray0)
        retval1 = io_obj.readinto(barray1)

        io_obj.seek(0, 0)
        retval2 = io_obj.readinto(barray2)

        ae(retval0, 5)
        ae(retval1, 7)
        ae(retval2, 26)

        ae(len(barray0), 5)
        ae(len(barray1), 10)
        ae(len(barray2), 26)

        ae(barray0, b"opqrs")
        ae(barray1, b"tuvwxyz\x00\x00\x00")
        ae(barray2, b"abcdefghijklmnopqrstuvwxyz")
    # end def test_readinto
# end class TestMethods

class IStreamWrapperTestCase(unittest.TestCase, TestMethods):
    def setUp(self):
        self.io_obj = \
            base.IStreamWrapper(BytesIO(b"abcdefghijklmnopqrstuvwxyz"), 26)
    # end def setUp
# end class IStreamWrapperTestCase

class ByteTestCase(unittest.TestCase, TestMethods):
    def setUp(self):
        self.io_obj = byte.open(b"abcdefghijklmnopqrstuvwxyz")
    # end def setUp
# end class ByteTestCase


class SubsetTestCase(unittest.TestCase, TestMethods):
    def setUp(self):
        io_obj = byte.open(b"***abcdefghijklmnopqrstuvwxyz***")
        self.io_obj = subset.open(io_obj, 3, 26)
    # end def setUp
# end class SubsetTestCase

class DDTestCase(unittest.TestCase, TestMethods):
    def setUp(self):
        self.io_obj = raw.open("tests/io/alpha.txt")
    # end def setUp

    def tearDown(self):
        self.io_obj.close()
    # end def tearDown
# end class DDTestCase

class CompositeTestCase(unittest.TestCase, TestMethods):
    def setUp(self):
        segments = [
            (byte.open(b"*******abcde**************"), 7, 5),
            (byte.open(b"******fghi****************"), 6, 4),
            (byte.open(b"jklmn*********************"), 0, 5),
            (byte.open(b"*****************opqrstuvw"), 17, 9),
            (byte.open(b"*******************xy*****"), 19, 2),
            (byte.open(b"z"), 0, 1)
        ]

        self.io_obj = composite.open(segments)
    # end def setUp
# end class CompositeTestCase

class SplitDDTestCase(unittest.TestCase, TestMethods):
    def setUp(self):
        file_names = ["alpha{0}.txt".format(x) for x in range(1,7)]
        file_names = [join("tests", "io", name) for name in file_names]

        self.io_obj = splitraw.open(file_names)
    # end def setUp

    def tearDown(self):
        self.io_obj.close()
    # end def tearDown
# end class SplitDDTestCase

if __name__ == "__main__":
    unittest.main()
# end if
