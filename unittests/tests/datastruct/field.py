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
Unit tests for the lf.datastruct.field module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase
from lf.datastruct.field import (
    int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32, float64,
    char, raw, array, DataStruct, bit, Bits8, UBits8, Bits16, UBits16, Bits32,
    UBits32, Bits64, UBits64
)

class FieldMixin():
    """Mixin for testing Field classes and subclasses"""

    def test_name(self):
        for (index, field) in enumerate(self.fields):
            self.assertEqual(field.name, self.names[index])
        # end for
    # end def test_name

    def test_size(self):
        for (index, field) in enumerate(self.fields):
            self.assertEqual(field.size, self.sizes[index])
        # end for
    # end def test_size
# end class FieldMixin

class IntegralSizedMixin(FieldMixin):
    """Mixin for testing IntegralSized classes and subclasses"""

    pass
# end class IntegralSizedMixin

class PrimitiveMixin(IntegralSizedMixin):
    """Mixin for testing Primitive classes"""

    def test_format_str(self):
        for (index, field) in enumerate(self.fields):
            self.assertEqual(field.format_str, self.format_strs[index])
        # end for
    # end def test_format_str
# end class PrimitiveMixin

class BuiltInMixin(PrimitiveMixin):
    pass
# end class BuiltInMixin

class CompositeMixin(IntegralSizedMixin):
    """Mixin for testing Composite classes and subclasses"""

    def test_flatten(self):
        ae = self.assertEqual
        ade = self.assertDictEqual

        for (index, field) in enumerate(self.fields):
            expected = self.flattened[index]
            actual = dict(field.flatten(expand_bits=False))
            ae(len(actual), len(expected))
            ade(actual, expected)

            expected = self.flattened_expand_bits[index]
            actual = dict(field.flatten(expand_bits=True))
            ae(len(actual), len(expected))
            ade(actual, expected)
        # end for
    # end def test_flatten

    def test_tuple_factory(self):
        ae = self.assertEqual
        at = self.assertTrue
        ain = self.assertIsNone
        ainn = self.assertIsNotNone

        for (index, field) in enumerate(self.fields):
            tuple_fields = self.tuple_fields[index]
            tuple_indices = self.tuple_indices[index]
            tuple_data = self.tuple_data[index]

            tuple_factory = field.tuple_factory

            new_tuple = tuple_factory(tuple_data)
            _fields = new_tuple._fields
            _indices = new_tuple._indices

            ae(len(_fields), len(tuple_fields))
            ae(len(_indices), len(tuple_indices))

            for tuple_field in tuple_fields:
                at(tuple_field in new_tuple._fields)

                nt_index = _fields.index(tuple_field)
                t_index = tuple_fields.index(tuple_field)

                ae(_indices[nt_index], tuple_indices[t_index])
            # end for
        # end for
    # end def test_tuple_factory
# end class CompositeMixin

class BitsMixin(PrimitiveMixin):

    def test__init__(self):
        ar = self.assertRaises

        class TestBitsClass0(self.fields[0].__class__):
            bits = [ int32("field") ]
        # end class TestBitsClass0

        class TestBitsClass1(self.fields[0].__class__):
            bits = [bit("bit0", (self.fields[0].size * 8) + 1)]
        # end class TestBitsClass1

        ar(TypeError, TestBitsClass0)
        ar(OverflowError, TestBitsClass1)
    # end def test__init__

    def test_size(self):
        ae = self.assertEqual

        for field, size in zip(self.fields, self.sizes):
            ae(field.size, size)
        # end for
    # end def test_size

    def test_decoder(self):
        ae = self.assertEqual

        for (index, field) in enumerate(self.fields):
            decoder = field.decoder
            bit_shifts = self.bit_shifts[index]
            bit_masks = self.bit_masks[index]

            for (bit_index, bit_shift) in enumerate(bit_shifts):
                ae(decoder.bit_shifts[bit_index], bit_shift)
                ae(decoder.bit_masks[bit_index], bit_masks[bit_index])
            # end for
        # end for
    # end def test_decoder

    def test_bits(self):
        ae = self.assertEqual

        for index, (fields, bits) in enumerate(zip(self.fields, self.bits)):
            ae(len(fields.bits), (len(bits) + 1))

            for counter in range(len(bits)):
                ae(fields.bits[counter], bits[counter])
            # end for

            ae(fields.bits[-1].name, "bits_pad_")
            ae(fields.bits[-1].size, self.bits_pad_sizes[index])
        # end for
    # end def test_bits
# end class BitsMixin

class int8TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ int8("name") ]
        self.names = [ "name" ]
        self.sizes = [ 1 ]
        self.format_strs = [ "b" ]
    # end def setUp
# end class int8TestCase

class uint8TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ uint8("name") ]
        self.names = [ "name" ]
        self.sizes = [ 1 ]
        self.format_strs = [ "B" ]
    # end def setUp
# end class uint8TestCase

class int16TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ int16("name") ]
        self.names = [ "name" ]
        self.sizes = [ 2 ]
        self.format_strs = [ "h" ]
    # end def setUp
# end class int16TestCase

class uint16TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ uint16("name") ]
        self.names = [ "name" ]
        self.sizes = [ 2 ]
        self.format_strs = [ "H" ]
    # end def setUp
# end class uint16TestCase

class int32TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ int32("name") ]
        self.names = [ "name" ]
        self.sizes = [ 4 ]
        self.format_strs = [ "i" ]
    # end def setUp
# end class int32TestCase

class uint32TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ uint32("name") ]
        self.names = [ "name" ]
        self.sizes = [ 4 ]
        self.format_strs = [ "I" ]
    # end def setUp
# end class uint32TestCase

class int64TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ int64("name") ]
        self.names = [ "name" ]
        self.sizes = [ 8 ]
        self.format_strs = [ "q" ]
    # end def setUp
# end class int64TestCase

class uint64TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ uint64("name") ]
        self.names = [ "name" ]
        self.sizes = [ 8 ]
        self.format_strs = [ "Q" ]
    # end def setUp
# end class uint64TestCase

class float32TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ float32("name") ]
        self.names = [ "name" ]
        self.sizes = [ 4 ]
        self.format_strs = [ "f" ]
    # end def setUp
# end class float32TestCase

class float64TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ float64("name") ]
        self.names = [ "name" ]
        self.sizes = [ 8 ]
        self.format_strs = [ "d" ]
    # end def setUp
# end class float64TestCase

class charTestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ char("name") ]
        self.names = [ "name" ]
        self.sizes = [ 1 ]
        self.format_strs = [ "c" ]
    # end def setUp
# end class charTestCase

class rawTestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.fields = [ raw("name", 10) ]
        self.names = [ "name" ]
        self.sizes = [ 10 ]
        self.format_strs = [ "10s" ]
    # end def setUp
# end class rawTestCase

class DataStructTestCase(TestCase, CompositeMixin):
    def setUp(self):
        class TestBits0(UBits16):
            bits = [
                bit("bit0", 2),
                bit("bit1", 1),
                bit("bit2", 1)
            ]
        # end class TestUBits0

        class TestDataStruct0(DataStruct):
            fields = [
                int8("int8_0"),
                TestBits0(),
                int16("int16_0")
            ]
        # end class TestDataStruct0

        class TestDataStruct1(DataStruct):
            fields = [
                int8("int8_1"),
                TestDataStruct0("test_data_struct0_1"),
                int16("int16_1"),
                TestBits0()
            ]
        # end class TestDataStruct1

        data_struct0 = TestDataStruct0("name0")
        data_struct1 = TestDataStruct1("name1")

        flattened0 = [
            (1, data_struct0),
            (2, data_struct0.fields[0]),
            (5, data_struct0.fields[1]),
            (11, data_struct0.fields[2])
        ]

        flattened0_expand_bits = [
            (1, data_struct0),
            (2, data_struct0.fields[0]),
            (5, TestBits0.bits[0]),
            (11, TestBits0.bits[1]),
            (23, TestBits0.bits[2]),
            (47, TestBits0.bits[3]),
            (95, data_struct0.fields[2])
        ]

        flattened1 = [
            (1, data_struct1),
            (2, data_struct1.fields[0]),

            (5, data_struct1.fields[1]),
            (10, data_struct1.fields[1].fields[0]),
            (21, data_struct1.fields[1].fields[1]),
            (43, data_struct1.fields[1].fields[2]),

            (11, data_struct1.fields[2]),
            (23, data_struct1.fields[3])
        ]

        flattened1_expand_bits = [
            (1, data_struct1),
            (2, data_struct1.fields[0]),

            (5, data_struct1.fields[1]),
            (10, data_struct1.fields[1].fields[0]),
            (21, TestBits0.bits[0]),
            (43, TestBits0.bits[1]),
            (87, TestBits0.bits[2]),
            (175, TestBits0.bits[3]),
            (351, data_struct1.fields[1].fields[2]),

            (11, data_struct1.fields[2]),
            (23, TestBits0.bits[0]),
            (47, TestBits0.bits[1]),
            (95, TestBits0.bits[2]),
            (191, TestBits0.bits[3])
        ]

        self.fields = [data_struct0, data_struct1]
        self.names = ["name0", "name1"]
        self.tuple_fields = [
            ("int8_0", "bit0", "bit1", "bit2", "bits_pad_", "int16_0"),
            (
                "int8_1", "test_data_struct0_1", "int16_1", "bit0", "bit1",
                "bit2", "bits_pad_"
            )
        ]
        self.tuple_data = [ (0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5, 6)]
        self.sizes = [5, 10]
        self.flattened = [dict(flattened0), dict(flattened1)]
        self.flattened_expand_bits = [
            dict(flattened0_expand_bits), dict(flattened1_expand_bits)
        ]
        self.tuple_indices = [(0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5, 6)]
    # end def setUp
# end class DataStructTestCase

class arrayTestCase(TestCase, CompositeMixin):
    def setUp(self):
        class TestArrayBits(UBits16):
            bits = [
                bit("bit0", 2),
                bit("bit1", 1),
                bit("bit2", 3)
            ]
        # end class TestArrayBits

        class TestDataStruct(DataStruct):
            fields = [
                int8("int8"), TestArrayBits(), int16("int16")
            ]
        # end class TestDataStruct
        data_struct = TestDataStruct()
        _int32 = int32("int32")

        array0 = array("array0", data_struct, 3)
        array1 = array("array1", _int32, 5)

        flattened0 = [
            (1, array0),
            (2, array0.fields[0]),
            (4, array0.fields[0].fields[0]),
            (9, array0.fields[0].fields[1]),
            (19, array0.fields[0].fields[2]),
            (5, array0.fields[1]),
            (10, array0.fields[1].fields[0]),
            (21, array0.fields[1].fields[1]),
            (43, array0.fields[1].fields[2]),
            (11, array0.fields[2]),
            (22, array0.fields[2].fields[0]),
            (45, array0.fields[2].fields[1]),
            (91, array0.fields[2].fields[2])
        ]

        flattened0_expand_bits = [
            (1, array0),
            (2, array0.fields[0]),
            (4, array0.fields[0].fields[0]),
            (9, TestArrayBits.bits[0]),
            (19, TestArrayBits.bits[1]),
            (39, TestArrayBits.bits[2]),
            (79, TestArrayBits.bits[3]),
            (159, array0.fields[0].fields[2]),
            (5, array0.fields[1]),
            (10, array0.fields[1].fields[0]),
            (21, TestArrayBits.bits[0]),
            (43, TestArrayBits.bits[1]),
            (87, TestArrayBits.bits[2]),
            (175, TestArrayBits.bits[3]),
            (351, array0.fields[1].fields[2]),
            (11, array0.fields[2]),
            (22, array0.fields[2].fields[0]),
            (45, TestArrayBits.bits[0]),
            (91, TestArrayBits.bits[1]),
            (183, TestArrayBits.bits[2]),
            (367, TestArrayBits.bits[3]),
            (735, array0.fields[2].fields[2]),
        ]

        flattened1 = [
            (1, array1),
            (2, array1.fields[0]),
            (5, array1.fields[1]),
            (11, array1.fields[2]),
            (23, array1.fields[3]),
            (47, array1.fields[4])
        ]

        self.int32 = _int32
        self.data_struct = data_struct
        self.fields = [array0, array1]
        self.sizes = [15, 20]
        self.names = ["array0", "array1"]
        self.flattened = [dict(flattened0), dict(flattened1)]
        self.flattened_expand_bits = [
            dict(flattened0_expand_bits), dict(flattened1)
        ]
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(len(self.fields[0].fields), 3)
        ae(len(self.fields[1].fields), 5)

        for field in self.fields[0].fields:
            ae(field.__class__, self.data_struct.__class__)
        # end for

        for field in self.fields[1].fields:
            ae(field.__class__, self.int32.__class__)
        # end for
    # end def test__init__

    def test_tuple_factory(self):
        ae = self.assertEqual
        ae(self.fields[0].tuple_factory, tuple)
        ae(self.fields[1].tuple_factory, tuple)
    # end def test_tuple_factory
# end class arrayTestCase

class bitTestCase(TestCase, FieldMixin):
    def setUp(self):
        self.fields = [
            bit("bit0", 1),
            bit("bit1", 2),
            bit("bit2", 13)
        ]

        self.names = ["bit0", "bit1", "bit2"]
        self.sizes = [1, 2, 13]
    # end def setUp
# end class bitTestCase

class Bits8TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestBits8_0(Bits8):
            bits = [
                bit0_1
            ]
        # end class TestBits8_0

        class TestBits8_1(Bits8):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestBits8_1

        class TestBits8_2(Bits8):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestBits8_2

        test_bits8_0 = TestBits8_0()
        test_bits8_1 = TestBits8_1()
        test_bits8_2 = TestBits8_2()

        self.fields = [test_bits8_0, test_bits8_1, test_bits8_2]
        self.names = ["", "", ""]
        self.sizes = [1, 1, 1]
        self.format_strs = ["b", "b", "b"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [7, 6, 4]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFE],
            [1, 2, 0xFC],
            [1, 2, 12, 0xF0]
        ]
    # end def setUp
# end class Bits8TestCase

class UBits8TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestBits8_0(UBits8):
            bits = [
                bit0_1
            ]
        # end class TestBits8_0

        class TestBits8_1(UBits8):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestBits8_1

        class TestBits8_2(UBits8):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestBits8_2

        test_bits8_0 = TestBits8_0()
        test_bits8_1 = TestBits8_1()
        test_bits8_2 = TestBits8_2()

        self.fields = [test_bits8_0, test_bits8_1, test_bits8_2]
        self.names = ["", "", ""]
        self.sizes = [1, 1, 1]
        self.format_strs = ["B", "B", "B"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [7, 6, 4]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFE],
            [1, 2, 0xFC],
            [1, 2, 12, 0xF0]
        ]
    # end def setUp
# end class UBits8TestCase

class Bits16TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestBits16_0(Bits16):
            bits = [
                bit0_1
            ]
        # end class TestBits16_0

        class TestBits16_1(Bits16):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestBits16_1

        class TestBits16_2(Bits16):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestBits16_2

        test_bits16_0 = TestBits16_0()
        test_bits16_1 = TestBits16_1()
        test_bits16_2 = TestBits16_2()

        self.fields = [test_bits16_0, test_bits16_1, test_bits16_2]
        self.names = ["", "", ""]
        self.sizes = [2, 2, 2]
        self.format_strs = ["h", "h", "h"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [15, 14, 12]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFFFE],
            [1, 2, 0xFFFC],
            [1, 2, 12, 0xFFF0]
        ]
    # end def setUp
# end class Bits16TestCase

class UBits16TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestBits16_0(UBits16):
            bits = [
                bit0_1
            ]
        # end class TestBits16_0

        class TestBits16_1(UBits16):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestBits16_1

        class TestBits16_2(UBits16):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestBits16_2

        test_bits16_0 = TestBits16_0()
        test_bits16_1 = TestBits16_1()
        test_bits16_2 = TestBits16_2()

        self.fields = [test_bits16_0, test_bits16_1, test_bits16_2]
        self.names = ["", "", ""]
        self.sizes = [2, 2, 2]
        self.format_strs = ["H", "H", "H"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [15, 14, 12]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFFFE],
            [1, 2, 0xFFFC],
            [1, 2, 12, 0xFFF0]
        ]
    # end def setUp
# end class UBits16TestCase

class Bits32TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestBits32_0(Bits32):
            bits = [
                bit0_1
            ]
        # end class TestBits32_0

        class TestBits32_1(Bits32):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestBits32_1

        class TestBits32_2(Bits32):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestBits32_2

        test_bits32_0 = TestBits32_0()
        test_bits32_1 = TestBits32_1()
        test_bits32_2 = TestBits32_2()

        self.fields = [test_bits32_0, test_bits32_1, test_bits32_2]
        self.names = ["", "", ""]
        self.sizes = [4, 4, 4]
        self.format_strs = ["i", "i", "i"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [31, 30, 28]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFE],
            [1, 2, 0xFFFFFFFC],
            [1, 2, 12, 0xFFFFFFF0]
        ]
    # end def setUp
# end class Bits32TestCase

class UBits32TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestUBits32_0(UBits32):
            bits = [
                bit0_1
            ]
        # end class TestUBits32_0

        class TestUBits32_1(UBits32):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestUBits32_1

        class TestUBits32_2(UBits32):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestUBits32_2

        test_bits32_0 = TestUBits32_0()
        test_bits32_1 = TestUBits32_1()
        test_bits32_2 = TestUBits32_2()

        self.fields = [test_bits32_0, test_bits32_1, test_bits32_2]
        self.names = ["", "", ""]
        self.sizes = [4, 4, 4]
        self.format_strs = ["I", "I", "I"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [31, 30, 28]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFE],
            [1, 2, 0xFFFFFFFC],
            [1, 2, 12, 0xFFFFFFF0]
        ]
    # end def setUp
# end class UBits32TestCase

class Bits64TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestBits64_0(Bits64):
            bits = [
                bit0_1
            ]
        # end class TestBits64_0

        class TestBits64_1(Bits64):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestBits64_1

        class TestBits64_2(Bits64):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestBits64_2

        test_bits64_0 = TestBits64_0()
        test_bits64_1 = TestBits64_1()
        test_bits64_2 = TestBits64_2()

        self.fields = [test_bits64_0, test_bits64_1, test_bits64_2]
        self.names = ["", "", ""]
        self.sizes = [8, 8, 8]
        self.format_strs = ["q", "q", "q"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [63, 62, 60]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFFFFFFFFFE],
            [1, 2, 0xFFFFFFFFFFFFFFFC],
            [1, 2, 12, 0xFFFFFFFFFFFFFFF0]
        ]
    # end def setUp
# end class Bits64TestCase

class UBits64TestCase(TestCase, BitsMixin):
    def setUp(self):
        bit0_1 = bit("bit0", 1)
        bit1_1 = bit("bit1", 1)
        bit2_2 = bit("bit2", 2)

        class TestUBits64_0(UBits64):
            bits = [
                bit0_1
            ]
        # end class TestUBits64_0

        class TestUBits64_1(UBits64):
            bits = [
                bit0_1, bit1_1
            ]
        # end class TestUBits64_1

        class TestUBits64_2(UBits64):
            bits = [
                bit0_1, bit1_1, bit2_2
            ]
        # end class TestUBits64_2

        test_bits64_0 = TestUBits64_0()
        test_bits64_1 = TestUBits64_1()
        test_bits64_2 = TestUBits64_2()

        self.fields = [test_bits64_0, test_bits64_1, test_bits64_2]
        self.names = ["", "", ""]
        self.sizes = [8, 8, 8]
        self.format_strs = ["Q", "Q", "Q"]
        self.bits = [
            [bit0_1],
            [bit0_1, bit1_1],
            [bit0_1, bit1_1, bit2_2]
        ]

        self.bits_pad_sizes = [63, 62, 60]

        self.bit_shifts = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 4]
        ]

        self.bit_masks = [
            [1, 0xFFFFFFFFFFFFFFFE],
            [1, 2, 0xFFFFFFFFFFFFFFFC],
            [1, 2, 12, 0xFFFFFFFFFFFFFFF0]
        ]
    # end def setUp
# end class UBits64TestCase
