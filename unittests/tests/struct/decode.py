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
Unit tests for the lf.struct.decode module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = ["DecoderTestCase"]

from unittest import TestCase, main

from lf.struct.decode import Decoder

class DecoderTestCase(TestCase):
    def setUp(self):
        bit_fields = [
            ("field0", 1, 3), ("field1", 4, 7), ("field2", 9, 12)
        ]

        self.decoder = Decoder("decoder", bit_fields)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        decoder = self.decoder

        ae(len(decoder.bit_masks), 3)
        ae(decoder.bit_masks[0], 0x6)
        ae(decoder.bit_masks[1], 0x70)
        ae(decoder.bit_masks[2], 0xE00)
    # end def test__init__

    def test_decode(self):
        ae = self.assertEqual
        values = self.decoder.decode(0x5A55, use_named_tuple=False)
        self.assertEqual(values, (2, 5, 5))

        values = self.decoder.decode(0x5A55, use_named_tuple=True)
        self.assertEqual(values._fields, ("field0", "field1", "field2"))
        self.assertEqual(values.field0, 2)
        self.assertEqual(values.field1, 5)
        self.assertEqual(values.field2, 5)
    # end def test_decode
# end class DecoderTestCase

if __name__ == "__main__":
    main()
# end if
