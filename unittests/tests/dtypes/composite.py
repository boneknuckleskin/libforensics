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

"""Unit tests for the lf.dtypes.composite module."""

# stdlib imports
from unittest import TestCase
from ctypes import (
    c_int8, c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_int64, c_uint64,
    c_float, c_double, LittleEndianStructure, BigEndianStructure
)

# local imports
from lf.dtypes import (
    int8, uint8, uint16, uint32, float32, BitTypeU16, bits, bit, LITTLE_ENDIAN,
    BIG_ENDIAN
)
from lf.dtypes.composite import LERecord, BERecord

__docformat__ = "restructuredtext en"
__all__ = [
    "RecordTestCase"
]

class RecordTestCase(TestCase):
    def test_size_(self):
        ae = self.assertEqual

        (
            record0, record1, record2, record3, record4, record5, record6,
            record7, record8, record9, record10, record11, record12, record13,
            record14
        ) = self.records

        ae(record0._size_, 0)
        ae(record1._size_, 2)
        ae(record2._size_, 3)
        ae(record3._size_, 7)
        ae(record4._size_, 3)
        ae(record5._size_, 2)
        ae(record6._size_, 3)
        ae(record7._size_, 4)
        ae(record8._size_, 4)
        ae(record9._size_, 4)
        ae(record10._size_, 5)
        ae(record11._size_, 3)
        ae(record12._size_, 7)
        ae(record13._size_, 9)
        ae(record14._size_, 9)
    # end def test_size_

    def test_fields_(self):
        ae = self.assertEqual

        (
            record0, record1, record2, record3, record4, record5, record6,
            record7, record8, record9, record10, record11, record12, record13,
            record14
        ) = self.records

        bittype = self.bittype
        bits_obj = self.bits_obj

        ae(record0._fields_, [])

        ae(record1._fields_[0], ("field0", int8))
        ae(record1._fields_[1], ("field1", uint8))

        ae(record2._fields_[0], ("field0", uint16))
        ae(record2._fields_[1], ("field1", int8))

        ae(record3._fields_[0], ("field0", float32))
        ae(record3._fields_[1], ("field1", record2))

        ae(record4._fields_[0], ("field0", record1))
        ae(record4._fields_[1], ("field1", record0))
        ae(record4._fields_[2], ("field2", int8))

        ae(record5._fields_[0], ("field0", bittype))

        ae(record6._fields_[0], ("field0", uint8))
        ae(record6._fields_[1], ("field1", bittype))

        ae(record7._fields_[0], ("field0", uint8))
        ae(record7._fields_[1], ("field1", bittype))
        ae(record7._fields_[2], ("field2", int8))

        ae(record8._fields_[0], ("field0", record1))
        ae(record8._fields_[1], ("field1", record0))
        ae(record8._fields_[2], ("field2", int8))
        ae(record8._fields_[3], ("field3", uint8))

        ae(record9._fields_[0], ("field0", uint8))
        ae(record9._fields_[1], ("field1", bittype))
        ae(record9._fields_[2], ("field2", int8))

        ae(record10._fields_[0], ("field0", record1))
        ae(record10._fields_[1], ("field1", record0))
        ae(record10._fields_[2], ("field2", int8))
        ae(record10._fields_[3], ("field3", bittype))

        ae(record11._fields_[0], ("field0", [int8] * 3))

        ae(record12._fields_[0], ("field0", [int8] * 3))
        ae(record12._fields_[1], ("field1", uint32))

        ae(record13._fields_[0], ("field0", [int8] * 3))
        ae(record13._fields_[1], ("field1", uint32))
        ae(record13._fields_[2], ("field2", uint16))

        ae(record14._fields_[0], ("field0", [int8] * 3))
        ae(record14._fields_[1], ("field1", [uint16] * 3))
    # end def test_fields_

    def test_pack_(self):
        ae = self.assertEqual

        for record in self.records:
            ae(record._pack_, 1)
        # end for

        class TestPack(LERecord):
            _pack_ = 2
        # end class TestPack

        ae(TestPack._pack_, 2)
    # end def test_pack_

    def test_anonymous_(self):
        ae = self.assertEqual

        class TestRecord(LERecord):
            field0 = int8
            field1 = uint8
        # end class TestRecord

        class TestAnonymous(LERecord):
            _anonymous_ = ["anon_field"]

            anon_field = TestRecord
            field1 = uint8
        # end class TestAnonymous

        ae(TestAnonymous._ctype_._anonymous_, ["anon_field"])
    # end def test_anonymous_

    def test_byte_order_(self):
        ae = self.assertEqual

        for record in self.records:
            ae(record._byte_order_, LITTLE_ENDIAN)
        # end for

        class TestBigEndian(BERecord):
            pass
        # end class TestBigEndian

        ae(TestBigEndian._byte_order_, BIG_ENDIAN)
    # end def test_byte_order

    def test_ctype_name_(self):
        ae = self.assertEqual

        class TestCtypeName(LERecord):
            _ctype_name_ = "ctype_name"

            field0 = int8
        # end class TestCtypeName

        ae(TestCtypeName._ctype_.__name__, "ctype_name")
    # end def test_ctype_name_

    def test_ctype_(self):
        ae = self.assertEqual
        at = self.assertTrue

        ctypes_ = [record._ctype_ for record in self.records]

        (
            ctype0, ctype1, ctype2, ctype3, ctype4, ctype5, ctype6, ctype7,
            ctype8, ctype9, ctype10, ctype11, ctype12, ctype13, ctype14
        ) = ctypes_

        for ctype in ctypes_:
            ae(ctype._pack_, 1)
            ae(ctype._anonymous_, [])
            at(issubclass(ctype, LittleEndianStructure))
        # end for


        ae(ctype0._fields_, [])
        ae(ctype1._fields_, [("field0", c_int8), ("field1", c_uint8)])
        ae(ctype2._fields_, [("field0", c_uint16), ("field1", c_int8)])
        ae(ctype3._fields_, [("field0", c_float), ("field1", ctype2)])

        ae(
            ctype4._fields_,
            [("field0", ctype1), ("field1", ctype0), ("field2", c_int8)]
        )

        ae(
            ctype5._fields_,
            [("bfield0", c_uint16, 2), ("bfield1", c_uint16, 1)]
        )

        ae(
            ctype6._fields_,
            [
                ("field0", c_uint8),
                ("bfield0", c_uint16, 2),
                ("bfield1", c_uint16, 1)
            ]
        )

        ae(
            ctype7._fields_,
            [
                ("field0", c_uint8),
                ("bfield0", c_uint16, 2),
                ("bfield1", c_uint16, 1),
                ("field2", c_int8)
            ]
        )

        ae(
            ctype8._fields_,
            [
                ("field0", ctype1),
                ("field1", ctype0),
                ("field2", c_int8),
                ("field3", c_uint8)
            ]
        )

        ae(
            ctype9._fields_,
            [
                ("field0", c_uint8),
                ("bfield0", c_uint16, 2),
                ("bfield1", c_uint16, 1),
                ("field2", c_int8)
            ]
        )

        ae(
            ctype10._fields_,
            [
                ("field0", ctype1),
                ("field1", ctype0),
                ("field2", c_int8),
                ("bfield0", c_uint16, 2),
                ("bfield1", c_uint16, 1)
            ]
        )

        ae(ctype11._fields_[0][0], "field0")
        ae(ctype11._fields_[0][1]._type_, c_int8)
        ae(ctype11._fields_[0][1]._length_, 3)

        ae(ctype12._fields_[0][0], "field0")
        ae(ctype12._fields_[0][1]._type_, c_int8)
        ae(ctype12._fields_[0][1]._length_, 3)
        ae(ctype12._fields_[1], ("field1", c_uint32))

        ae(ctype13._fields_[0][0], "field0")
        ae(ctype13._fields_[0][1]._type_, c_int8)
        ae(ctype13._fields_[0][1]._length_, 3)
        ae(ctype13._fields_[1], ("field1", c_uint32))
        ae(ctype13._fields_[2], ("field2", c_uint16))

        ae(ctype14._fields_[0][0], "field0")
        ae(ctype14._fields_[0][1]._type_, c_int8)
        ae(ctype14._fields_[0][1]._length_, 3)
        ae(ctype14._fields_[1][0], "field1")
        ae(ctype14._fields_[1][1]._type_, c_uint16)
        ae(ctype14._fields_[1][1]._length_, 3)

        class TestRecord(BERecord):
            _pack_ = 3
            field0 = int8
            field1 = uint8
        # end class TestRecord
        at(issubclass(TestRecord._ctype_, BigEndianStructure))
        ae(TestRecord._ctype_._pack_, 3)

    # end def test_ctype_

    def setUp(self):
        bits_obj = bits(2)

        class Record0(LERecord):
            pass
        # end class Record0

        class Record1(LERecord):
            field0 = int8
            field1 = uint8
        # end class Record1

        class Record2(LERecord):
            field0 = uint16
            field1 = int8
        # end class Record3

        class Record3(LERecord):
            field0 = float32
            field1 = Record2
        # end class Record3

        class Record4(LERecord):
            field0 = Record1
            field1 = Record0
            field2 = int8
        # end class Record4

        class TestBitType(BitTypeU16):
            bfield0 = bits_obj
            bfield1 = bit
        # end class TestBitType

        class Record5(LERecord):
            field0 = TestBitType
        # end class Record5

        class Record6(LERecord):
            field0 = uint8
            field1 = TestBitType
        # end class Record6

        class Record7(LERecord):
            field0 = uint8
            field1 = TestBitType
            field2 = int8
        # end class Record7

        class Record8(Record4):
            field3 = uint8
        # end class Record8

        class Record9(Record6):
            field2 = int8
        # end class Record9

        class Record10(Record4):
            field3 = TestBitType
        # end class Record10

        class Record11(LERecord):
            field0 = [int8] * 3
        # end class Record11

        class Record12(LERecord):
            field0 = [int8] * 3
            field1 = uint32
        # end class Record12

        class Record13(Record12):
            field2 = uint16
        # end class Record13

        class Record14(Record11):
            field1 = [uint16] * 3
        # end class Record14

        self.records = (
            Record0, Record1, Record2, Record3, Record4, Record5, Record6,
            Record7, Record8, Record9, Record10, Record11, Record12, Record13,
            Record14
        )

        self.bits_obj = bits_obj
        self.bittype = TestBitType
    # end def setUp
# end class RecordTestCase
