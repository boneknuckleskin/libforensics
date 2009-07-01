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
Utilities for working with UUIDs.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from uuid import UUID

__docformat__ = "restructuredtext en"
__all__ = [
    "guid_to_uuid"
]

def guid_to_uuid(data1, data2, data3, data4):
    """
    Converts a Microsoft GUID to Python UUID object.

    :parameters:
        data1
            The first 8 hexadecimal digits (32 bits)

        data2
            The first group of 4 hexadecimal digits (16 bits)

        data3
            The second group of 4 hexadecimal digits (16 bits)

        data4
            An iterable of 8 bytes, of the last hexadecimal digits.

    :rtype: UUID
    :returns: A Python UUID object that matches the GUID.
    """

    node = (data4[2] << 40) | (data4[3] << 32) | (data4[4] << 24)
    node = node | (data4[5] << 16) | (data4[6] << 8) | data4[7]

    return UUID(fields=(data1, data2, data3, data4[0], data4[1], node))
# end def guid_to_uuid
