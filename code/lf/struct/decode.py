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

from collections import namedtuple

class Decoder():
    """
    Decodes bit fields.

    .. attribute:: named_tuple

        A named tuple applied to the extracted bits.

    .. attribute:: bit_masks

        A list of bit masks used to extract the various bit fields.

    .. attribute:: bit_shifts

        A list of the bit shifts used to extract the various bit fields.
    """

    def __init__(self, tuple_name, bit_fields):
        """
        Initializes a Decoder object.

        :parameters:
            tuple_name
                The name for the created namedtuple type.

            bit_fields
                An iterable of fields describing bits.  The fields are tuples
                of ("field name", bit start, bit stop)
        """

        field_names = list()
        bit_masks = list()
        bit_shifts = list()

        for field in bit_fields:
            bit_mask = 0
            name, start, stop = field
            field_names.append(name)

            for index in range(start, stop):
                bit_mask |= 2**index
            # end for

            bit_masks.append(bit_mask)
            bit_shifts.append(start)
        # end for

        self.bit_shifts = bit_shifts
        self.bit_masks = bit_masks
        self.named_tuple = namedtuple(tuple_name, field_names)
    # end def __init__

    def decode(self, value, use_named_tuple=True):
        """
        Decodes individual bits from a value.

        :parameters:
            value
                The value to extract bits from.

            use_named_tuple
                If True, creates a named tuple from the resulting values.

        :rtype: tuple
        :returns: The extracted bit fields.
        """

        field_values = list()

        for index, bit_mask in enumerate(self.bit_masks):
            field_values.append((value & bit_mask) >> self.bit_shifts[index])
        # end for

        if not use_named_tuple:
            return tuple(field_values)
        # end if

        return self.named_tuple._make(field_values)
    # end def decode
# end class Decoder
