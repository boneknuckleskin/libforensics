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
Unit tests for the lf.datatype.decode module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from unittest import TestCase
from lf.datatype.bits import bit, bits
from lf.datatype.decode import Decoder

__docformat__ = "restructuredtext en"

class DecoderTestCase(TestCase):
    def setUp(self):
        fields0 = [bit]
        fields1 = [bit, bit]
        fields2 = [bit, bits(2)]
        fields3 = [bits(3), bits(2), bits(2)]

        self.decoders = [
            Decoder(fields0), Decoder(fields1), Decoder(fields2),
            Decoder(fields3)
        ]

        self.bit_shifts = [
            [0],
            [0, 1],
            [0, 1],
            [0, 3, 5]
        ]

        self.bit_masks = [
            [1],
            [1, 2],
            [1, 6],
            [7, 0b11000, 0b1100000]
        ]

        self.decode_data = [1, 3, 5, 0x55]

        self.values = [
            (1,),
            (1, 1),
            (1, 2),
            (5, 2, 2)
        ]

        self.sizes = [1, 2, 3, 7]
        self.counts = [1, 2, 2, 3]
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        for (index, decoder) in enumerate(self.decoders):
            bit_shifts = self.bit_shifts[index]
            bit_masks = self.bit_masks[index]

            for (bit_index, bit_shift) in enumerate(decoder.bit_shifts):
                ae(bit_shift, bit_shifts[bit_index])
                ae(decoder.bit_masks[bit_index], bit_masks[bit_index])
            # end for
        # end for
    # end def test__init__

    def test_decode(self):
        ae = self.assertEqual

        for (index, decoder) in enumerate(self.decoders):
            values = self.values[index]
            test_values = decoder.decode(self.decode_data[index])

            ae(test_values, values)
        # end for
    # end def test_decode

    def test_size(self):
        ae = self.assertEqual

        for (decoder, size) in zip(self.decoders, self.sizes):
            ae(decoder.size, size)
        # end for
    # end def test_size

    def test_count(self):
        ae = self.assertEqual

        for (decoder, count) in zip(self.decoders, self.counts):
            ae(decoder.count, count)
        # end for
    # end def test_count
# end class DecoderTestCase
