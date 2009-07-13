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
Unit tests for the lf.datastruct.structuple module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase
from lf.datastruct.structuple import make

class makeTestCase(TestCase):
    def test_make(self):
        fu = self.failUnless
        fue = self.failUnlessEqual
        fur = self.failUnlessRaises

        fields_list = [
            {"a": 0, "b": 1, "c": 2, "d": 3},
            {"a": 0, "b": 1, "c": 3, "d": 5},
            "a b c d",
            "a, b, c, d",
            "a,b,c,d",
            ["a", "b", "c", "d"]
        ]

        _fields_attrs = [
            ("a", "b", "c", "d"),
            ("a", "b", "c", "d"),
            ("a", "b", "c", "d"),
            ("a", "b", "c", "d"),
            ("a", "b", "c", "d"),
            ("a", "b", "c", "d")
        ]

        _indices_attrs = [
            (0, 1, 2, 3),
            (0, 1, 3, 5),
            (0, 1, 2, 3),
            (0, 1, 2, 3),
            (0, 1, 2, 3),
            (0, 1, 2, 3)
        ]

        data = [x for x in range(10)]

        for (index, fields) in enumerate(fields_list):
            factory = make("factory", fields)
            st = factory(data)

            _fields = _fields_attrs[index]
            _indices = _indices_attrs[index]


            fue(len(st._fields), len(_fields))

            for field in _fields:
                fu(field in st._fields)
            # end for

            for field in _fields:
                st_index = st._fields.index(field)
                field_index = _fields.index(field)

                fue(st._indices[st_index], _indices[field_index])
            # end for
        # end for

        fur(ValueError, make, "name", "a b c d a")
        fur(TypeError, make, "name", 1)
        fur(ValueError, make, "name", "1a")
        fur(ValueError, make, "name", "for")
        fur(ValueError, make, "name", "s*")
    # end def test_make
# end class makeTestCase
