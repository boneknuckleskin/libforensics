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
Unit tests for the lf.datatype.bits module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from unittest import TestCase
from lf.datatype.bits import (
    bit, bits, BitType8, BitTypeU8, BitType16, BitTypeU16, BitType32,
    BitTypeU32, BitType64, BitTypeU64
)

__docformat__ = "restructuredtext en"

class DataTypeMixin():
    """Mixin for testing DataType classes and subclasses"""

    def test_size_(self):
        for (index, datatype) in enumerate(self.datatypes):
            self.assertEqual(datatype._size_, self.sizes[index])
        # end for
    # end def test_size_
# end class DataTypeMixin

class PrimitiveMixin(DataTypeMixin):
    """Mixin for testing Primitive classes"""

    pass
# end class PrimitiveMixin

class BasicMixin(PrimitiveMixin):
    """Mixin for testing Basic classes"""

    def test_format_(self):
        for (index, datatype) in enumerate(self.datatypes):
            self.assertEqual(datatype._format_, self.formats[index])
        # end for
    # end def test_format_
# end class BasicMixin

class BitTypeMixin(BasicMixin):
    """Mixin for testing BitType classes"""

    def test__init__(self):
        ar = self.assertRaises

        class TestBitTypeClass1(self.datatypes[0].__class__):
            class1_field = bits((self.datatypes[0]._size_ * 8) + 1)
        # end class TestBitTypeClass1

        ar(OverflowError, TestBitTypeClass1)
    # end def test__init__

    def test_decoder_(self):
        ae = self.assertEqual

        for (index, datatype) in enumerate(self.datatypes):
            decoder = datatype._decoder_
            bit_shifts = self.bit_shifts[index]
            bit_masks = self.bit_masks[index]

            for (bit_index, bit_shift) in enumerate(bit_shifts):
                ae(decoder.bit_shifts[bit_index], bit_shift)
                ae(decoder.bit_masks[bit_index], bit_masks[bit_index])
            # end for
        # end for
    # end def test_decoder_

    def test_fields_(self):
        ae = self.assertEqual

        iterator = enumerate(zip(self.datatypes, self.bits_objs))
        for index, (datatype, bits_obj) in iterator:
            ae(len(datatype._fields_), (len(bits_obj) + 1))

            for counter in range(len(bits_obj)):
                ae(datatype._fields_[counter], bits_obj[counter])
            # end for

            ae(datatype._fields_[-1][0], "bits_pad_")
            ae(datatype._fields_[-1][1]._size_, self.bits_pad_sizes[index])
        # end for
    # end def test_fields_
# end class BitTypeMixin

class bitTestCase(TestCase, DataTypeMixin):
    def setUp(self):
        self.datatypes = [bit, bits(2), bits(13)]
        self.sizes = [1, 2, 13]
    # end def setUp
# end class bitTestCase

class BitType8TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitType8_0(BitType8):
            field1 = bit
        # end class TestBitType8_0

        class TestBitType8_1(BitType8):
            field1 = bit
            field2 = bit
        # end class TestBitType8_1

        class TestBitType8_2(BitType8):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitType8_2

        class TestBitType8_3(TestBitType8_2):
            field4 = bits_obj2
        # end class TestBitType8_3

        datatype0 = TestBitType8_0()
        datatype1 = TestBitType8_1()
        datatype2 = TestBitType8_2()
        datatype3 = TestBitType8_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [1, 1, 1, 1]
        self.formats = ["b", "b", "b", "b"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [7, 6, 4, 1]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFE],
            [1, 2, 0xFC],
            [1, 2, 12, 0xF0],
            [1, 2, 12, 0x70, 0x80]
        ]
    # end def setUp
# end class BitType8TestCase

class BitTypeU8TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitTypeU8_0(BitTypeU8):
            field1 = bit
        # end class TestBitTypeU8_0

        class TestBitTypeU8_1(BitTypeU8):
            field1 = bit
            field2 = bit
        # end class TestBitTypeU8_1

        class TestBitTypeU8_2(BitTypeU8):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitTypeU8_2

        class TestBitTypeU8_3(TestBitTypeU8_2):
            field4 = bits_obj2
        # end class TestBitTypeU8_3

        datatype0 = TestBitTypeU8_0()
        datatype1 = TestBitTypeU8_1()
        datatype2 = TestBitTypeU8_2()
        datatype3 = TestBitTypeU8_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [1, 1, 1, 1]
        self.formats = ["B", "B", "B", "B"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [7, 6, 4, 1]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFE],
            [1, 2, 0xFC],
            [1, 2, 12, 0xF0],
            [1, 2, 12, 0x70, 0x80]
        ]
    # end def setUp
# end class BitTypeU8TestCase

class BitType16TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitType16_0(BitType16):
            field1 = bit
        # end class TestBitType16_0

        class TestBitType16_1(BitType16):
            field1 = bit
            field2 = bit
        # end class TestBitType16_1

        class TestBitType16_2(BitType16):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitType16_2

        class TestBitType16_3(TestBitType16_2):
            field4 = bits_obj2
        # end class TestBitType16_3

        datatype0 = TestBitType16_0()
        datatype1 = TestBitType16_1()
        datatype2 = TestBitType16_2()
        datatype3 = TestBitType16_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [2, 2, 2, 2]
        self.formats = ["h", "h", "h", "h"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [15, 14, 12, 9]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFFFE],
            [1, 2, 0xFFFC],
            [1, 2, 12, 0xFFF0],
            [1, 2, 12, 0x70, 0xFF80]
        ]
    # end def setUp
# end class BitType16TestCase

class BitTypeU16TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitTypeU16_0(BitTypeU16):
            field1 = bit
        # end class TestBitTypeU16_0

        class TestBitTypeU16_1(BitTypeU16):
            field1 = bit
            field2 = bit
        # end class TestBitTypeU16_1

        class TestBitTypeU16_2(BitTypeU16):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitTypeU16_2

        class TestBitTypeU16_3(TestBitTypeU16_2):
            field4 = bits_obj2
        # end class TestBitTypeU16_3

        datatype0 = TestBitTypeU16_0()
        datatype1 = TestBitTypeU16_1()
        datatype2 = TestBitTypeU16_2()
        datatype3 = TestBitTypeU16_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [2, 2, 2, 2]
        self.formats = ["H", "H", "H", "H"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [15, 14, 12, 9]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFFFE],
            [1, 2, 0xFFFC],
            [1, 2, 12, 0xFFF0],
            [1, 2, 12, 0x70, 0xFF80]
        ]
    # end def setUp
# end class BitTypeU16TestCase

class BitType32TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitType32_0(BitType32):
            field1 = bit
        # end class TestBitType32_0

        class TestBitType32_1(BitType32):
            field1 = bit
            field2 = bit
        # end class TestBitType32_1

        class TestBitType32_2(BitType32):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitType32_2

        class TestBitType32_3(TestBitType32_2):
            field4 = bits_obj2
        # end class TestBitType32_3

        datatype0 = TestBitType32_0()
        datatype1 = TestBitType32_1()
        datatype2 = TestBitType32_2()
        datatype3 = TestBitType32_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [4, 4, 4, 4]
        self.formats = ["i", "i", "i", "i"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [31, 30, 28, 25]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFE],
            [1, 2, 0xFFFFFFFC],
            [1, 2, 12, 0xFFFFFFF0],
            [1, 2, 12, 0x70, 0xFFFFFF80]
        ]
    # end def setUp
# end class BitType32TestCase

class BitTypeU32TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitTypeU32_0(BitTypeU32):
            field1 = bit
        # end class TestBitTypeU32_0

        class TestBitTypeU32_1(BitTypeU32):
            field1 = bit
            field2 = bit
        # end class TestBitTypeU32_1

        class TestBitTypeU32_2(BitTypeU32):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitTypeU32_2

        class TestBitTypeU32_3(TestBitTypeU32_2):
            field4 = bits_obj2
        # end class TestBitTypeU32_3

        datatype0 = TestBitTypeU32_0()
        datatype1 = TestBitTypeU32_1()
        datatype2 = TestBitTypeU32_2()
        datatype3 = TestBitTypeU32_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [4, 4, 4, 4]
        self.formats = ["I", "I", "I", "I"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [31, 30, 28, 25]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFE],
            [1, 2, 0xFFFFFFFC],
            [1, 2, 12, 0xFFFFFFF0],
            [1, 2, 12, 0x70, 0xFFFFFF80]
        ]
    # end def setUp
# end class BitTypeU32TestCase

class BitType64TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitType64_0(BitType64):
            field1 = bit
        # end class TestBitType64_0

        class TestBitType64_1(BitType64):
            field1 = bit
            field2 = bit
        # end class TestBitType64_1

        class TestBitType64_2(BitType64):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitType64_2

        class TestBitType64_3(TestBitType64_2):
            field4 = bits_obj2
        # end class TestBitType64_3

        datatype0 = TestBitType64_0()
        datatype1 = TestBitType64_1()
        datatype2 = TestBitType64_2()
        datatype3 = TestBitType64_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [8, 8, 8, 8]
        self.formats = ["q", "q", "q", "q"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [63, 62, 60, 57]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFFFFFFFFFE],
            [1, 2, 0xFFFFFFFFFFFFFFFC],
            [1, 2, 12, 0xFFFFFFFFFFFFFFF0],
            [1, 2, 12, 0x70, 0xFFFFFFFFFFFFFF80]
        ]
    # end def setUp
# end class BitType64TestCase

class BitTypeU64TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        bits_obj1 = bits(2)
        bits_obj2 = bits(3)

        class TestBitTypeU64_0(BitTypeU64):
            field1 = bit
        # end class TestBitTypeU64_0

        class TestBitTypeU64_1(BitTypeU64):
            field1 = bit
            field2 = bit
        # end class TestBitTypeU64_1

        class TestBitTypeU64_2(BitTypeU64):
            field1 = bit
            field2 = bit
            field3 = bits_obj1
        # end class TestBitTypeU64_2

        class TestBitTypeU64_3(TestBitTypeU64_2):
            field4 = bits_obj2
        # end class TestBitTypeU64_3

        datatype0 = TestBitTypeU64_0()
        datatype1 = TestBitTypeU64_1()
        datatype2 = TestBitTypeU64_2()
        datatype3 = TestBitTypeU64_3()

        self.datatypes = [datatype0, datatype1, datatype2, datatype3]

        self.sizes = [8, 8, 8, 8]
        self.formats = ["Q", "Q", "Q", "Q"]
        self.bits_objs = [
            [("field1", bit)],
            [("field1", bit), ("field2", bit)],
            [("field1", bit), ("field2", bit), ("field3", bits_obj1)],
            [
                ("field1", bit),
                ("field2", bit),
                ("field3", bits_obj1),
                ("field4", bits_obj2)
            ]
        ]

        self.bits_pad_sizes = [63, 62, 60, 57]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4],
            [0, 1, 2, 4, 7]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFFFFFFFFFE],
            [1, 2, 0xFFFFFFFFFFFFFFFC],
            [1, 2, 12, 0xFFFFFFFFFFFFFFF0],
            [1, 2, 12, 0x70, 0xFFFFFFFFFFFFFF80]
        ]
    # end def setUp
# end class BitTypeU64TestCase
