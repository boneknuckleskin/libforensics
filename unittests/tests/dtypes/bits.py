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

"""Unit tests for the lf.dtypes.bits module."""

# stdlib imports
from unittest import TestCase
from ctypes import (
    c_int8, c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_int64, c_uint64
)

# local imports
from lf.dtypes.bits import (
    bit, bits, BitType8, BitTypeU8, BitType16, BitTypeU16, BitType32,
    BitTypeU32, BitType64, BitTypeU64
)

__docformat__ = "restructuredtext en"
__all__ = [
    "bitsTestCase", "bitTestCase", "BitType8TestCase", "BitTypeU8TestCase",
    "BitType16TestCase", "BitTypeU16TestCase", "BitType32TestCase",
    "BitTypeU32TestCase", "BitType64TestCase", "BitTypeU64TestCase"
]

class DataTypeMixin():
    def test_size_(self):
        ae = self.assertEqual

        ae(self.dtype._size_, self.size)
    # end def test_size_
# end class DataTypeMixin

class BitTypeMixin(DataTypeMixin):
    def test_int_type_(self):
        ae = self.assertEqual

        ae(self.dtype._int_type_, self.int_type)
    # end def test_int_type_

    def test_fields_(self):
        ae = self.assertEqual

        for (index, (name, size)) in enumerate(self.field_infos):
            ae(self.dtype._fields_[index][0], name)
            ae(self.dtype._fields_[index][1]._size_, size)
        # end for
    # end def test_fields_
# end class BitTypeMixin

class bitsTestCase(TestCase, DataTypeMixin):
    def setUp(self):
        self.dtype = bits(3)
        self.size = 3
    # end def setUp
# end class bitsTestCase

class bitTestCase(TestCase, DataTypeMixin):
    def setUp(self):
        self.dtype = bit
        self.size = 1
    # end def setUp
# end class bitTesCase

class BitType8TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitType8):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_int8
        self.size = 1
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType8TestCase

class BitTypeU8TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitTypeU8):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_uint8
        self.size = 1
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType8TestCase

class BitType16TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitType16):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_int16
        self.size = 2
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType16TestCase

class BitTypeU16TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitTypeU16):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_uint16
        self.size = 2
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType16TestCase

class BitType32TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitType32):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_int32
        self.size = 4
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType32TestCase

class BitTypeU32TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitTypeU32):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_uint32
        self.size = 4
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType32TestCase

class BitType64TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitType64):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_int64
        self.size = 8
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType64TestCase

class BitTypeU64TestCase(TestCase, BitTypeMixin):
    def setUp(self):
        class TestClass(BitTypeU64):
            field1 = bit
            field2 = bits(3)
        # end class TestClass

        self.dtype = TestClass
        self.int_type = c_uint64
        self.size = 8
        self.field_infos = [("field1", 1), ("field2", 3)]
    # end def setUp
# end class BitType64TestCase
