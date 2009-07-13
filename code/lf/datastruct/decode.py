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
Decode bit fields

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = ["Decoder"]

class Decoder():
    """
    Decodes bit fields.

    .. attribute:: bit_masks

        A list of bit masks used to extract the various bit fields.

    .. attribute:: bit_shifts

        A list of the bit shifts used to extract the various bit fields.

    .. attribute:: size

        The total number of bits that get decoded.

    .. attribute:: count

        The number of individual fields that get decoded.
    """

    def __init__(self, bits):
        """
        Initializes a Decoder object.

        :parameters:
            bits
                An iterable of bit objects.
        """

        bit_masks = list()
        bit_shifts = list()
        offset = 0

        for (index, bit_field) in enumerate(bits):
            bit_mask = 0
            bit_shift = 0

            for index in range(bit_field.size):
                bit_mask |= 2**index
            # end for
            bit_mask = bit_mask << offset

            bit_masks.append(bit_mask)
            bit_shifts.append(offset)

            offset += bit_field.size
        # end for

        self.size = offset
        self.count = len(bits)
        self.bit_shifts = bit_shifts
        self.bit_masks = bit_masks
    # end def __init__

    def decode(self, value):
        """
        Decodes individual bits from a value.

        :parameters:
            value
                The value to extract bits from.

        :rtype: tuple
        :returns: The extracted bit fields.
        """

        field_values = list()
        bit_info_iter = zip(self.bit_masks, self.bit_shifts)

        for (bit_mask, bit_shift) in bit_info_iter:
            field_values.append((value & bit_mask) >> bit_shift)
        # end for

        return tuple(field_values)
    # end def decode
# end class Decoder
