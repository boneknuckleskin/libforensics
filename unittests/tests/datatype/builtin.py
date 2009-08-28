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
Unit tests for the lf.datatype.builtin module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase
from lf.datatype.builtin import (
    int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32, float64,
    char, raw
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

class BasicMixin(PrimitiveMixin):
    """Mixin for testing Basic classes"""

    def test_format_(self):
        for (index, datatype) in enumerate(self.datatypes):
            self.assertEqual(datatype._format_, self.formats[index])
        # end for
    # end def test_format_
# end class BasicMixin

class BuiltInMixin(BasicMixin):
    pass
# end class BuiltInMixin

class int8TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ int8 ]
        self.sizes = [ 1 ]
        self.formats = [ "b" ]
    # end def setUp
# end class int8TestCase

class uint8TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ uint8 ]
        self.sizes = [ 1 ]
        self.formats = [ "B" ]
    # end def setUp
# end class uint8TestCase

class int16TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ int16 ]
        self.sizes = [ 2 ]
        self.formats = [ "h" ]
    # end def setUp
# end class int16TestCase

class uint16TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ uint16 ]
        self.sizes = [ 2 ]
        self.formats = [ "H" ]
    # end def setUp
# end class uint16TestCase

class int32TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ int32 ]
        self.sizes = [ 4 ]
        self.formats = [ "i" ]
    # end def setUp
# end class int32TestCase

class uint32TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ uint32 ]
        self.sizes = [ 4 ]
        self.formats = [ "I" ]
    # end def setUp
# end class uint32TestCase

class int64TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ int64 ]
        self.sizes = [ 8 ]
        self.formats = [ "q" ]
    # end def setUp
# end class int64TestCase

class uint64TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ uint64 ]
        self.sizes = [ 8 ]
        self.formats = [ "Q" ]
    # end def setUp
# end class uint64TestCase

class float32TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ float32 ]
        self.sizes = [ 4 ]
        self.formats = [ "f" ]
    # end def setUp
# end class float32TestCase

class float64TestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ float64 ]
        self.sizes = [ 8 ]
        self.formats = [ "d" ]
    # end def setUp
# end class float64TestCase

class charTestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ char ]
        self.sizes = [ 1 ]
        self.formats = [ "c" ]
    # end def setUp
# end class charTestCase

class rawTestCase(TestCase, BuiltInMixin):
    def setUp(self):
        self.datatypes = [ raw(10) ]
        self.sizes = [ 10 ]
        self.formats = [ "10s" ]
    # end def setUp
# end class rawTestCase
