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

"""Unit tests for the lf.win.objects module."""

# stdlib imports
from unittest import TestCase

# local imports
from lf.dec import ByteIStream, SEEK_SET
from lf.dtypes import BIG_ENDIAN, LITTLE_ENDIAN
from lf.win.con.ctypes import coord_le
from lf.win.con.objects import COORD

__docformat__ = "restructuredtext en"
__all__ = [
    "COORDTestCase"
]

class COORDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = b"\x00\x01\x02\x03"

        stream = ByteIStream(data)
        coord1 = COORD.from_stream(stream, byte_order=LITTLE_ENDIAN)
        coord2 = COORD.from_stream(stream, 0, byte_order=LITTLE_ENDIAN)

        stream.seek(0, SEEK_SET)
        coord3 = COORD.from_stream(stream, byte_order=BIG_ENDIAN)
        coord4 = COORD.from_stream(stream, 0, byte_order=BIG_ENDIAN)

        ae(coord1.x, 0x0100)
        ae(coord1.y, 0x0302)
        ae(coord2.x, 0x0100)
        ae(coord2.y, 0x0302)
        ae(coord3.x, 0x0001)
        ae(coord3.y, 0x0203)
        ae(coord4.x, 0x0001)
        ae(coord4.y, 0x0203)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        coord = coord_le.from_buffer_copy(b"\x00\x01\x02\x03")
        coord = COORD.from_ctype(coord)
        ae(coord, COORD((0x0100, 0x0302)))
    # end def test_from_ctype
# end class COORDTestCase
