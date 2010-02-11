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

"""Unit tests for the lf.dtypes.reader module."""

# stdlib imports
from unittest import TestCase

# local imports
from lf.dec import ByteIStream
from lf.dtypes.reader import Reader, BoundReader

__docformat__ = "restructuredtext en"
__all__ = [
    "ReaderTestCase", "BoundReaderTestCase"
]

class ReaderMixin():
    def test_int8(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int8"]:
            ae(self.reader.int8(**args), retval)
        # end for
    # end def test_int8

    def test_uint8(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint8"]:
            ae(self.reader.uint8(**args), retval)
        # end for
    # end def test_uint8

    def test_int16_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int16_le"]:
            ae(self.reader.int16_le(**args), retval)
        # end for
    # end def test_int16_le

    def test_uint16_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint16_le"]:
            ae(self.reader.uint16_le(**args), retval)
        # end for
    # end def test_uint16_le

    def test_int16_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int16_be"]:
            ae(self.reader.int16_be(**args), retval)
        # end for
    # end def test_int16_be

    def test_uint16_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint16_be"]:
            ae(self.reader.uint16_be(**args), retval)
        # end for
    # end def test_uint16_be

    def test_int32_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int32_le"]:
            ae(self.reader.int32_le(**args), retval)
        # end for
    # end def test_int32_le

    def test_uint32_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint32_le"]:
            ae(self.reader.uint32_le(**args), retval)
        # end for
    # end def test_uint32_le

    def test_int32_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int32_be"]:
            ae(self.reader.int32_be(**args), retval)
        # end for
    # end def test_int32_be

    def test_uint32_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint32_be"]:
            ae(self.reader.uint32_be(**args), retval)
        # end for
    # end def test_uint32_be

    def test_int64_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int64_le"]:
            ae(self.reader.int64_le(**args), retval)
        # end for
    # end def test_int64_le

    def test_uint64_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint64_le"]:
            ae(self.reader.uint64_le(**args), retval)
        # end for
    # end def test_uint64_le

    def test_int64_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["int64_be"]:
            ae(self.reader.int64_be(**args), retval)
        # end for
    # end def test_int64_be

    def test_uint64_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["uint64_be"]:
            ae(self.reader.uint64_be(**args), retval)
        # end for
    # end def test_uint64_be

    def test_float32_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["float32_le"]:
            ae(self.reader.float32_le(**args), retval)
        # end for
    # end def test_float32_le

    def test_float32_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["float32_be"]:
            ae(self.reader.float32_be(**args), retval)
        # end for
    # end def test_float32_be

    def test_float64_le(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["float64_le"]:
            ae(self.reader.float64_le(**args), retval)
        # end for
    # end def test_float64_le

    def test_float64_be(self):
        ae = self.assertEqual

        for (args, retval) in self.arg_sets["float64_be"]:
            ae(self.reader.float64_be(**args), retval)
        # end for
    # end def test_float64_be
# end class ReaderMixin

class ReaderTestCase(ReaderMixin, TestCase):
    def setUp(self):
        data = bytearray()

        # Padding
        data.extend(b"\x64\x53")

        # int8
        data.extend(b"\xFE\xFD")

        # uint8
        data.extend(b"\xFE\xFD")

        # int16_le
        data.extend(b"\x55\xFF\x55\xFA")

        # uint16_le
        data.extend(b"\x55\xFF\x55\xFA")

        # int16_be
        data.extend(b"\xFF\x55\xFA\x55")

        # uint16_be
        data.extend(b"\xFF\x55\xFA\x55")

        # int32_le
        data.extend(b"\x55\xFF\x55\xFF\x55\xFF\x55\xFA")

        # uint32_le
        data.extend(b"\x55\xFF\x55\xFF\x55\xFF\x55\xFA")

        # int32_be
        data.extend(b"\xFF\x55\xFF\x55\xFA\x55\xFF\x55")

        # uint32_be
        data.extend(b"\xFF\x55\xFF\x55\xFA\x55\xFF\x55")

        # int64_le
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFF")
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFA")

        # uint64_le
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFF")
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFA")

        # int64_be
        data.extend(b"\xFF\x55\x55\x55\x55\x55\x55\x55")
        data.extend(b"\xFA\x55\x55\x55\x55\x55\x55\x55")

        # uint64_be
        data.extend(b"\xFF\x55\x55\x55\x55\x55\x55\x55")
        data.extend(b"\xFA\x55\x55\x55\x55\x55\x55\x55")

        # float32_le
        data.extend(b"\x55\xAA\x55\xFF")
        data.extend(b"\x55\xAA\x55\xFA")

        # float32_be
        data.extend(b"\xFF\x55\xAA\x55")
        data.extend(b"\xFA\x55\xAA\x55")

        # float64_le
        data.extend(b"\x55\xAA\x55\xAA\x55\xAA\x55\xFF")
        data.extend(b"\x55\xAA\x55\xAA\x55\xAA\x55\xFA")

        # float64_be
        data.extend(b"\xFF\x55\xAA\x55\xAA\x55\xAA\x55")
        data.extend(b"\xFA\x55\xAA\x55\xAA\x55\xAA\x55")

        stream = ByteIStream(data)

        self.arg_sets = {
            "int8": [
                ({"stream": stream, "offset": 2}, -2),
                ({"stream": stream, "offset": None}, -3),
            ],

            "uint8": [
                ({"stream": stream, "offset": 4}, 0xFE),
                ({"stream": stream, "offset": None}, 0xFD)
            ],

            "int16_le": [
                ({"stream": stream, "offset": 6}, -171),
                ({"stream": stream, "offset": None}, -1451)
            ],

            "uint16_le": [
                ({"stream": stream, "offset": 10}, 0xFF55),
                ({"stream": stream, "offset": None}, 0xFA55)
            ],

            "int16_be": [
                ({"stream": stream, "offset": 14}, -171),
                ({"stream": stream, "offset": None}, -1451)
            ],

            "uint16_be": [
                ({"stream": stream, "offset": 18}, 0xFF55),
                ({"stream": stream, "offset": None}, 0xFA55)
            ],

            "int32_le": [
                ({"stream": stream, "offset": 22}, -11141291),
                ({"stream": stream, "offset": None}, -95027371),
            ],

            "uint32_le": [
                ({"stream": stream, "offset": 30}, 0xFF55FF55),
                ({"stream": stream, "offset": None}, 0xFA55FF55)
            ],

            "int32_be": [
                ({"stream": stream, "offset": 38}, -11141291),
                ({"stream": stream, "offset": None}, -95027371)
            ],

            "uint32_be": [
                ({"stream": stream, "offset": 46}, 0xFF55FF55),
                ({"stream": stream, "offset": None}, 0xFA55FF55)
            ],

            "int64_le": [
                ({"stream": stream, "offset": 54}, -48038396025285291),
                ({"stream": stream, "offset": None}, -408326366214924971)
            ],

            "uint64_le": [
                ({"stream": stream, "offset": 70}, 0xFF55555555555555),
                ({"stream": stream, "offset": None}, 0xFA55555555555555)
            ],

            "int64_be": [
                ({"stream": stream, "offset": 86}, -48038396025285291),
                ({"stream": stream, "offset": None}, -408326366214924971)
            ],

            "uint64_be": [
                ({"stream": stream, "offset": 102}, 0xFF55555555555555),
                ({"stream": stream, "offset": None}, 0xFA55555555555555)
            ],

            "float32_le": [
                ({"stream": stream, "offset": 118}, -2.840099775729543e+38),
                ({"stream": stream, "offset": None}, -2.773534937235882e+35)
            ],

            "float32_be": [
                ({"stream": stream, "offset": 126}, -2.840099775729543e+38),
                ({"stream": stream, "offset": None}, -2.773534937235882e+35)
            ],

            "float64_le": [
                ({"stream": stream, "offset": 134}, -2.377178117902199e+305),
                ({"stream": stream, "offset": None}, -1.9663556517139943e+281)
            ],

            "float64_be": [
                ({"stream": stream, "offset": 150}, -2.377178117902199e+305),
                ({"stream": stream, "offset": None}, -1.9663556517139943e+281)
            ]

        }

        self.reader = Reader
    # end def setUp
# end class ReaderTestCase

class BoundReaderTestCase(ReaderMixin, TestCase):
    def setUp(self):
        data = bytearray()

        # Padding
        data.extend(b"\x64\x53")

        # int8
        data.extend(b"\xFE\xFD")

        # uint8
        data.extend(b"\xFE\xFD")

        # int16_le
        data.extend(b"\x55\xFF\x55\xFA")

        # uint16_le
        data.extend(b"\x55\xFF\x55\xFA")

        # int16_be
        data.extend(b"\xFF\x55\xFA\x55")

        # uint16_be
        data.extend(b"\xFF\x55\xFA\x55")

        # int32_le
        data.extend(b"\x55\xFF\x55\xFF\x55\xFF\x55\xFA")

        # uint32_le
        data.extend(b"\x55\xFF\x55\xFF\x55\xFF\x55\xFA")

        # int32_be
        data.extend(b"\xFF\x55\xFF\x55\xFA\x55\xFF\x55")

        # uint32_be
        data.extend(b"\xFF\x55\xFF\x55\xFA\x55\xFF\x55")

        # int64_le
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFF")
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFA")

        # uint64_le
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFF")
        data.extend(b"\x55\x55\x55\x55\x55\x55\x55\xFA")

        # int64_be
        data.extend(b"\xFF\x55\x55\x55\x55\x55\x55\x55")
        data.extend(b"\xFA\x55\x55\x55\x55\x55\x55\x55")

        # uint64_be
        data.extend(b"\xFF\x55\x55\x55\x55\x55\x55\x55")
        data.extend(b"\xFA\x55\x55\x55\x55\x55\x55\x55")

        # float32_le
        data.extend(b"\x55\xAA\x55\xFF")
        data.extend(b"\x55\xAA\x55\xFA")

        # float32_be
        data.extend(b"\xFF\x55\xAA\x55")
        data.extend(b"\xFA\x55\xAA\x55")

        # float64_le
        data.extend(b"\x55\xAA\x55\xAA\x55\xAA\x55\xFF")
        data.extend(b"\x55\xAA\x55\xAA\x55\xAA\x55\xFA")

        # float64_be
        data.extend(b"\xFF\x55\xAA\x55\xAA\x55\xAA\x55")
        data.extend(b"\xFA\x55\xAA\x55\xAA\x55\xAA\x55")

        stream = ByteIStream(data)

        self.arg_sets = {
            "int8": [
                ({"offset": 2}, -2),
                ({"offset": None}, -3),
            ],

            "uint8": [
                ({"offset": 4}, 0xFE),
                ({"offset": None}, 0xFD)
            ],

            "int16_le": [
                ({"offset": 6}, -171),
                ({"offset": None}, -1451)
            ],

            "uint16_le": [
                ({"offset": 10}, 0xFF55),
                ({"offset": None}, 0xFA55)
            ],

            "int16_be": [
                ({"offset": 14}, -171),
                ({"offset": None}, -1451)
            ],

            "uint16_be": [
                ({"offset": 18}, 0xFF55),
                ({"offset": None}, 0xFA55)
            ],

            "int32_le": [
                ({"offset": 22}, -11141291),
                ({"offset": None}, -95027371),
            ],

            "uint32_le": [
                ({"offset": 30}, 0xFF55FF55),
                ({"offset": None}, 0xFA55FF55)
            ],

            "int32_be": [
                ({"offset": 38}, -11141291),
                ({"offset": None}, -95027371)
            ],

            "uint32_be": [
                ({"offset": 46}, 0xFF55FF55),
                ({"offset": None}, 0xFA55FF55)
            ],

            "int64_le": [
                ({"offset": 54}, -48038396025285291),
                ({"offset": None}, -408326366214924971)
            ],

            "uint64_le": [
                ({"offset": 70}, 0xFF55555555555555),
                ({"offset": None}, 0xFA55555555555555)
            ],

            "int64_be": [
                ({"offset": 86}, -48038396025285291),
                ({"offset": None}, -408326366214924971)
            ],

            "uint64_be": [
                ({"offset": 102}, 0xFF55555555555555),
                ({"offset": None}, 0xFA55555555555555)
            ],

            "float32_le": [
                ({"offset": 118}, -2.840099775729543e+38),
                ({"offset": None}, -2.773534937235882e+35)
            ],

            "float32_be": [
                ({"offset": 126}, -2.840099775729543e+38),
                ({"offset": None}, -2.773534937235882e+35)
            ],

            "float64_le": [
                ({"offset": 134}, -2.377178117902199e+305),
                ({"offset": None}, -1.9663556517139943e+281)
            ],

            "float64_be": [
                ({"offset": 150}, -2.377178117902199e+305),
                ({"offset": None}, -1.9663556517139943e+281)
            ]

        }

        self.reader = BoundReader(stream)
    # end def setUp
# end class BoundReaderTestCase
