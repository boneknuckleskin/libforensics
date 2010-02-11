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

"""Unit tests for the lf.dtypes.native module."""

# stdlib imports
from unittest import TestCase
from ctypes import (
    c_int8, c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_int64, c_uint64,
    c_float, c_double
)

# local imports
from lf.dtypes.native import (
    int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32, float64
)

__docformat__ = "restructuredtext en"
__all__ = [
    "int8TestCase", "uint8TestCase", "int16TestCase", "uint16TestCase",
    "int32TestCase", "uint32TestCase", "int64TestCase", "uint64TestCase",
    "float32TestCase", "float64TestCase"
]

class NativeMixin():
    def test_size_(self):
        ae = self.assertEqual

        ae(self.dtype._size_, self.size)
    # end def test_size_

    def test_ctype_(self):
        ae = self.assertEqual

        ae(self.dtype._ctype_, self.ctype)
    # end def test_ctype_
# end class NativeMixin

class int8TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = int8
        self.size = 1
        self.ctype = c_int8
    # end def setUp
# end class int8TestCase

class uint8TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = uint8
        self.size = 1
        self.ctype = c_uint8
    # end def setUp
# end class uint8TestCase

class int16TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = int16
        self.size = 2
        self.ctype = c_int16
    # end def setUp
# end class int16TestCase

class uint16TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = uint16
        self.size = 2
        self.ctype = c_uint16
    # end def setUp
# end class uint16TestCase

class int32TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = int32
        self.size = 4
        self.ctype = c_int32
    # end def setUp
# end class int32TestCase

class uint32TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = uint32
        self.size = 4
        self.ctype = c_uint32
    # end def setUp
# end class uint32TestCase

class int64TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = int64
        self.size = 8
        self.ctype = c_int64
    # end def setUp
# end class int64TestCase

class uint64TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = uint64
        self.size = 8
        self.ctype = c_uint64
    # end def setUp
# end class uint64TestCase

class float32TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = float32
        self.size = 4
        self.ctype = c_float
    # end def setUp
# end class float32TestCase(TestCase, NativeMixin):

class float64TestCase(TestCase, NativeMixin):
    def setUp(self):
        self.dtype = float64
        self.size = 8
        self.ctype = c_double
    # end def setUp
# end class float64TestCase
# end class int16TestCase
