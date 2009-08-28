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
Unit tests for the lf.datatype.composite module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase
from lf.datatype.builtin import int8, int16, int32
from lf.datatype.bits import BitTypeU16, bit, bits
from lf.datatype.composite import (
    Record, array, ExtractableArray,
)

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

class CompositeMixin(PrimitiveMixin):
    """Mixin for Composite classes"""

    def test_fields_(self):
        ae = self.assertEqual

        for (index, dtype) in enumerate(self.datatypes):
            ae(dtype._fields_, self.fields[index])
        # end for
    # end def test_fields_

    def test_flatten(self):
        ae = self.assertEqual
        ade = self.assertDictEqual

        for (index, dtype) in enumerate(self.datatypes):
            expected = self.flattened[index]
            actual = dict(dtype._flatten(expand_bits=False))
            ae(len(actual), len(expected))
            ade(actual, expected)

            expected = self.flattened_expand_bits[index]
            actual = dict(dtype._flatten(expand_bits=True))
            ae(len(actual), len(expected))
            ade(actual, expected)
        # end for
    # end def test_flatten
# end class CompositeMixin

class ExtractableMixin():
    """Mixin for testing Composite classes and subclasses"""

    def test_factory_(self):
        ae = self.assertEqual
        at = self.assertTrue
        ain = self.assertIsNone
        ainn = self.assertIsNotNone

        for (index, dtype) in enumerate(self.datatypes):
            tuple_fields = self.tuple_fields[index]
            tuple_indices = self.tuple_indices[index]
            tuple_data = self.tuple_data[index]

            factory = dtype._factory_

            new_tuple = factory(tuple_data)
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
    # end def test_factory_
# end class ExtractableMixin

class RecordTestCase(TestCase, CompositeMixin, ExtractableMixin):
    def setUp(self):
        class TestBits0(BitTypeU16):
            bit0 = bits(2)
            bit1 = bit
            bit2 = bit
        # end class TestBits0

        class TestRecord0(Record):
            int8_0 = int8
            bit_field = TestBits0
            int16_0 = int16
        # end class TestRecord0

        class TestRecord1(Record):
            int8_1 = int8
            test_record0_1 = TestRecord0
            int16_1 = int16
            bit_field = TestBits0
        # end class TestRecord1

        class TestRecord2(TestRecord0):
            int16_2 = int16
            test_record0_2 = TestRecord0
        # end class TestRecord2

        record0 = TestRecord0
        record1 = TestRecord1
        record2 = TestRecord2

        flattened0 = [
            (1, record0),
            (2, record0._fields_[0][1]),
            (5, record0._fields_[1][1]),
            (11, record0._fields_[2][1])
        ]

        flattened0_expand_bits = [
            (1, record0),
            (2, record0._fields_[0][1]),
            (5, TestBits0._fields_[0][1]),
            (11, TestBits0._fields_[1][1]),
            (23, TestBits0._fields_[2][1]),
            (47, TestBits0._fields_[3][1]),
            (95, record0._fields_[2][1])
        ]

        flattened1 = [
            (1, record1),
            (2, record1._fields_[0][1]),

            (5, record1._fields_[1][1]),
            (10, record1._fields_[1][1]._fields_[0][1]),
            (21, record1._fields_[1][1]._fields_[1][1]),
            (43, record1._fields_[1][1]._fields_[2][1]),

            (11, record1._fields_[2][1]),
            (23, record1._fields_[3][1])
        ]

        flattened1_expand_bits = [
            (1, record1),
            (2, record1._fields_[0][1]),

            (5, record1._fields_[1][1]),
            (10, record1._fields_[1][1]._fields_[0][1]),
            (21, TestBits0._fields_[0][1]),
            (43, TestBits0._fields_[1][1]),
            (87, TestBits0._fields_[2][1]),
            (175, TestBits0._fields_[3][1]),
            (351, record1._fields_[1][1]._fields_[2][1]),

            (11, record1._fields_[2][1]),
            (23, TestBits0._fields_[0][1]),
            (47, TestBits0._fields_[1][1]),
            (95, TestBits0._fields_[2][1]),
            (191, TestBits0._fields_[3][1])
        ]

        flattened2 = [
            (1, record2),

            (2, record2._fields_[0][1]),
            (5, record2._fields_[1][1]),
            (11, record2._fields_[2][1]),
            (23, record2._fields_[3][1]),

            (47, record2._fields_[4][1]),
            (94, record2._fields_[4][1]._fields_[0][1]),
            (189, record2._fields_[4][1]._fields_[1][1]),
            (379, record2._fields_[4][1]._fields_[2][1]),
        ]

        flattened2_expand_bits = [
            (1, record2),
            (2, record2._fields_[0][1]),
            (5, TestBits0._fields_[0][1]),
            (11, TestBits0._fields_[1][1]),
            (23, TestBits0._fields_[2][1]),
            (47, TestBits0._fields_[3][1]),
            (95, record2._fields_[2][1]),
            (191, record2._fields_[3][1]),

            (383, record2._fields_[4][1]),
            (766, record2._fields_[4][1]._fields_[0][1]),
            (1533, TestBits0._fields_[0][1]),
            (3067, TestBits0._fields_[1][1]),
            (6135, TestBits0._fields_[2][1]),
            (12271, TestBits0._fields_[3][1]),
            (24543, record2._fields_[4][1]._fields_[2][1])
        ]

        self.datatypes = [record0, record1, record2]
        self.tuple_fields = [
            ("int8_0", "bit0", "bit1", "bit2", "bits_pad_", "int16_0"),
            (
                "int8_1", "test_record0_1", "int16_1", "bit0", "bit1",
                "bit2", "bits_pad_"
            ),
            (
                "int8_0", "bit0", "bit1", "bit2", "bits_pad_", "int16_0",
                "int16_2", "test_record0_2"
            )
        ]
        self.tuple_data = [ list(range(7)), list(range(7)), list(range(100)) ]
        self.sizes = [5, 10, 12]
        self.flattened = [dict(flattened0), dict(flattened1), dict(flattened2)]
        self.flattened_expand_bits = [
            dict(flattened0_expand_bits),
            dict(flattened1_expand_bits),
            dict(flattened2_expand_bits)
        ]
        self.tuple_indices = [list(range(6)), list(range(7)), list(range(8))]
        self.fields = [
            [
                ("int8_0", int8),
                ("bit_field", TestBits0),
                ("int16_0", int16)
            ],
            [
                ("int8_1", int8),
                ("test_record0_1", TestRecord0),
                ("int16_1", int16),
                ("bit_field", TestBits0),
            ],
            [
                ("int8_0", int8),
                ("bit_field", TestBits0),
                ("int16_0", int16),
                ("int16_2", int16),
                ("test_record0_2", TestRecord0)
            ],
        ]
    # end def setUp
# end class RecordTestCase

class arrayTestCase(TestCase, CompositeMixin):
    def setUp(self):
        class TestArrayBits(BitTypeU16):
            bit0 = bits(2)
            bit1 = bit
            bit2 = bits(3)
        # end class TestArrayBits

        class TestRecord(Record):
            int8 = int8
            bit_field = TestArrayBits
            int16 = int16
        # end class TestRecord

        array0 = array(TestRecord, 3)
        array1 = array(int32, 5)

        flattened0 = [
            (1, array0),

            (2, array0._fields_[0][1]),
            (4, array0._fields_[0][1]._fields_[0][1]),
            (9, array0._fields_[0][1]._fields_[1][1]),
            (19, array0._fields_[0][1]._fields_[2][1]),

            (5, array0._fields_[1][1]),
            (10, array0._fields_[1][1]._fields_[0][1]),
            (21, array0._fields_[1][1]._fields_[1][1]),
            (43, array0._fields_[1][1]._fields_[2][1]),

            (11, array0._fields_[2][1]),
            (22, array0._fields_[2][1]._fields_[0][1]),
            (45, array0._fields_[2][1]._fields_[1][1]),
            (91, array0._fields_[2][1]._fields_[2][1])
        ]

        flattened0_expand_bits = [
            (1, array0),

            (2, array0._fields_[0][1]),
            (4, array0._fields_[0][1]._fields_[0][1]),
            (9, TestArrayBits._fields_[0][1]),
            (19, TestArrayBits._fields_[1][1]),
            (39, TestArrayBits._fields_[2][1]),
            (79, TestArrayBits._fields_[3][1]),
            (159, array0._fields_[0][1]._fields_[2][1]),

            (5, array0._fields_[1][1]),
            (10, array0._fields_[1][1]._fields_[0][1]),
            (21, TestArrayBits._fields_[0][1]),
            (43, TestArrayBits._fields_[1][1]),
            (87, TestArrayBits._fields_[2][1]),
            (175, TestArrayBits._fields_[3][1]),
            (351, array0._fields_[1][1]._fields_[2][1]),

            (11, array0._fields_[2][1]),
            (22, array0._fields_[2][1]._fields_[0][1]),
            (45, TestArrayBits._fields_[0][1]),
            (91, TestArrayBits._fields_[1][1]),
            (183, TestArrayBits._fields_[2][1]),
            (367, TestArrayBits._fields_[3][1]),
            (735, array0._fields_[2][1]._fields_[2][1]),
        ]

        flattened1 = [
            (1, array1),
            (2, int32),
            (5, int32),
            (11, int32),
            (23, int32),
            (47, int32)
        ]

        self.record = TestRecord
        self.datatypes = [array0, array1]
        self.sizes = [15, 20]
        self.flattened = [dict(flattened0), dict(flattened1)]
        self.flattened_expand_bits = [
            dict(flattened0_expand_bits), dict(flattened1)
        ]
        self.fields = [
            [("", TestRecord)] * 3,
            [("", int32)] * 5
        ]
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(len(self.datatypes[0]._fields_), 3)
        ae(len(self.datatypes[1]._fields_), 5)

        for (fname, dtype) in self.datatypes[0]._fields_:
            ae(dtype, self.record)
            ae(fname, "")
        # end for

        for (fname, dtype) in self.datatypes[1]._fields_:
            ae(dtype, int32),
            ae(fname, "")
        # end for
    # end def test__init__
# end class arrayTestCase

class ExtractableArrayTestCase(TestCase, CompositeMixin, ExtractableMixin):
    def setUp(self):
        class TestArrayBits(BitTypeU16):
            bit0 = bits(2)
            bit1 = bit
            bit2 = bits(3)
        # end class TestArrayBits

        class TestRecord(Record):
            int8 = int8
            bit_field = TestArrayBits
            int16 = int16
        # end class TestRecord

        array0 = ExtractableArray(TestRecord, 3)
        array1 = ExtractableArray(int32, 5)

        flattened0 = [
            (1, array0),

            (2, array0._fields_[0][1]),
            (4, array0._fields_[0][1]._fields_[0][1]),
            (9, array0._fields_[0][1]._fields_[1][1]),
            (19, array0._fields_[0][1]._fields_[2][1]),

            (5, array0._fields_[1][1]),
            (10, array0._fields_[1][1]._fields_[0][1]),
            (21, array0._fields_[1][1]._fields_[1][1]),
            (43, array0._fields_[1][1]._fields_[2][1]),

            (11, array0._fields_[2][1]),
            (22, array0._fields_[2][1]._fields_[0][1]),
            (45, array0._fields_[2][1]._fields_[1][1]),
            (91, array0._fields_[2][1]._fields_[2][1])
        ]

        flattened0_expand_bits = [
            (1, array0),

            (2, array0._fields_[0][1]),
            (4, array0._fields_[0][1]._fields_[0][1]),
            (9, TestArrayBits._fields_[0][1]),
            (19, TestArrayBits._fields_[1][1]),
            (39, TestArrayBits._fields_[2][1]),
            (79, TestArrayBits._fields_[3][1]),
            (159, array0._fields_[0][1]._fields_[2][1]),

            (5, array0._fields_[1][1]),
            (10, array0._fields_[1][1]._fields_[0][1]),
            (21, TestArrayBits._fields_[0][1]),
            (43, TestArrayBits._fields_[1][1]),
            (87, TestArrayBits._fields_[2][1]),
            (175, TestArrayBits._fields_[3][1]),
            (351, array0._fields_[1][1]._fields_[2][1]),

            (11, array0._fields_[2][1]),
            (22, array0._fields_[2][1]._fields_[0][1]),
            (45, TestArrayBits._fields_[0][1]),
            (91, TestArrayBits._fields_[1][1]),
            (183, TestArrayBits._fields_[2][1]),
            (367, TestArrayBits._fields_[3][1]),
            (735, array0._fields_[2][1]._fields_[2][1]),
        ]

        flattened1 = [
            (1, array1),
            (2, int32),
            (5, int32),
            (11, int32),
            (23, int32),
            (47, int32)
        ]

        self.record = TestRecord
        self.datatypes = [array0, array1]
        self.sizes = [15, 20]
        self.flattened = [dict(flattened0), dict(flattened1)]
        self.flattened_expand_bits = [
            dict(flattened0_expand_bits), dict(flattened1)
        ]
        self.fields = [
            [("", TestRecord)] * 3,
            [("", int32)] * 5
        ]
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(len(self.datatypes[0]._fields_), 3)
        ae(len(self.datatypes[1]._fields_), 5)

        for (fname, dtype) in self.datatypes[0]._fields_:
            ae(dtype, self.record)
            ae(fname, "")
        # end for

        for (fname, dtype) in self.datatypes[1]._fields_:
            ae(dtype, int32),
            ae(fname, "")
        # end for
    # end def test__init__

    def test_factory_(self):
        ae = self.assertEqual

        for dtype in self.datatypes:
            ae(dtype._factory_, list)
        # end for
    # end def test_factory_
# end class ExtractableArrayTestCase
