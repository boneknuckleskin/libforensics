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
Unit tests for the lf.struct.datatype module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase, main
from lf.struct.datatype import Bool, Int8, UInt8, Int16, UInt16, Int32
from lf.struct.datatype import UInt32, Int64, UInt64, Float32, Float64
from lf.struct.datatype import Bytes, Char

class TestMethods():
    """Mixin class for testing primitives"""

    def test_size(self):
        self.assertEqual(self.primitive.size, self.primitive_size)
    # end def test_size

    def test_format_str(self):
        self.assertEqual(self.primitive.format_str, self.primitive_format_str)
    # end def test_format_str

    def test__init__(self):
        self.assertEqual(self.primitive.field_name, self.primitive_field_name)
    # end def test___init__

    def test_flatten(self):
        self.assertEqual(self.primitive.flatten(4), [(4, self.primitive)])
    # end def test_flatten
# end class TestMethods

class BoolTestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = None
        self.primitive_format_str = "?"
        self.primitive_size = 1

        self.primitive = Bool()
    # end def setUp
# end class BoolTestCase

class BytesTestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "10s"
        self.primitive_size = 10

        self.primitive = Bytes(10, "field_name")
    # end def setUp
# end class BytesTestCase

class Int8TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "b"
        self.primitive_size = 1

        self.primitive = Int8("field_name")
    # end def setUp
# end class Int8TestCase

class UInt8TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "B"
        self.primitive_size = 1

        self.primitive = UInt8("field_name")
    # end def setUp
# end class UInt8TestCase

class Int16TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "h"
        self.primitive_size = 2

        self.primitive = Int16("field_name")
    # end def setUp
# end class Int16TestCase

class UInt16TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "H"
        self.primitive_size = 2

        self.primitive = UInt16("field_name")
    # end def setUp
# end class UInt16TestCase

class Int32TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "i"
        self.primitive_size = 4

        self.primitive = Int32("field_name")
    # end def setUp
# end class Int32TestCase

class UInt32TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "I"
        self.primitive_size = 4

        self.primitive = UInt32("field_name")
    # end def setUp
# end class UInt32TestCase

class Int64TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "q"
        self.primitive_size = 8

        self.primitive = Int64("field_name")
    # end def setUp
# end class Int64TestCase

class UInt64TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "Q"
        self.primitive_size = 8

        self.primitive = UInt64("field_name")
    # end def setUp
# end class UInt64TestCase

class Float32TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "f"
        self.primitive_size = 4

        self.primitive = Float32("field_name")
    # end def setUp
# end class Float32TestCase

class Float64TestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "d"
        self.primitive_size = 8

        self.primitive = Float64("field_name")
    # end def setUp
# end class Float64TestCase

class CharTestCase(TestCase, TestMethods):
    def setUp(self):
        self.primitive_field_name = "field_name"
        self.primitive_format_str = "c"
        self.primitive_size = 1

        self.primitive = Char("field_name")
    # end def setUp
# end class CharTestCase

if __name__ == "__main__":
    main()
# end if
