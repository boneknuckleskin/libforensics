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

"""Unit tests for the lf.dtypes.basic module."""

# stdlib imports
from unittest import TestCase
from ctypes import c_ubyte

# local imports
from lf.dtypes.basic import raw

__docformat__ = "restructuredtext en"
__all__ = [
    "rawTestCase"
]

class rawTestCase(TestCase):
    def setUp(self):
        self.raw = raw(5)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(self.raw._size_, 5)
        ae(self.raw._ctype_, (c_ubyte * 5))
    # end def test__init__
# end class rawTestCase
