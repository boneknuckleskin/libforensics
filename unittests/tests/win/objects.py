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
from datetime import datetime
from uuid import UUID
from unittest import TestCase
from decimal import Decimal

# local imports
from lf.dec import ByteIStream
from lf.dec.consts import SEEK_SET
from lf.dtypes import BIG_ENDIAN, LITTLE_ENDIAN
from lf.win.ctypes import (
    guid_be, filetime_le, coord_le, lcid_le, hresult_le, decimal_le, decimal_be
)
from lf.win.objects import (
    GUIDToUUID, CLSIDToUUID, COORD, LCID, HRESULT, DECIMALToDecimal,
    CURRENCYToDecimal
)

__docformat__ = "restructuredtext en"
__all__ = [
    "GUIDToUUIDTestCase", "CLSIDToUUIDTestCase", "COORDTestCase",
    "LCIDTestCase", "HRESULTTestCase", "DECIMALToDecimalTestCase",
    "CURRENCYToDecimalTestCase"
]

class GUIDToUUIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(17)]))
        uuid1 = GUIDToUUID.from_stream(stream, byte_order=LITTLE_ENDIAN)
        uuid2 = GUIDToUUID.from_stream(stream, 1, byte_order=LITTLE_ENDIAN)

        stream.seek(0, SEEK_SET)
        uuid3 = GUIDToUUID.from_stream(stream, byte_order=BIG_ENDIAN)
        uuid4 = GUIDToUUID.from_stream(stream, 1, byte_order=BIG_ENDIAN)

        ae(uuid1, UUID(bytes_le=bytes([x for x in range(16)])))
        ae(uuid2, UUID(bytes_le=bytes([x for x in range(1, 17)])))
        ae(uuid3, UUID(bytes=bytes([x for x in range(16)])))
        ae(uuid4, UUID(bytes=bytes([x for x in range(1, 17)])))
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(16)]))
        uuid1 = guid_be.from_buffer_copy(stream.read(16))
        uuid1 = GUIDToUUID.from_ctype(uuid1)

        ae(uuid1, UUID(bytes=bytes([x for x in range(16)])))
    # end def test_from_ctype

    def test_from_guid(self):
        ae = self.assertEqual

        uuid = GUIDToUUID.from_guid(
            0x00010203, 0x0405, 0x0607, b"\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
        )

        ae(uuid, UUID(bytes=bytes([x for x in range(16)])))
    # end def test_from_guid
# end class GUIDToUUIDTestCase

class CLSIDToUUIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(17)]))
        uuid1 = CLSIDToUUID.from_stream(stream, byte_order=LITTLE_ENDIAN)
        uuid2 = CLSIDToUUID.from_stream(stream, 1, byte_order=LITTLE_ENDIAN)

        stream.seek(0, SEEK_SET)
        uuid3 = CLSIDToUUID.from_stream(stream, byte_order=BIG_ENDIAN)
        uuid4 = CLSIDToUUID.from_stream(stream, 1, byte_order=BIG_ENDIAN)

        ae(uuid1, UUID(bytes_le=bytes([x for x in range(16)])))
        ae(uuid2, UUID(bytes_le=bytes([x for x in range(1, 17)])))
        ae(uuid3, UUID(bytes=bytes([x for x in range(16)])))
        ae(uuid4, UUID(bytes=bytes([x for x in range(1, 17)])))
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(16)]))
        uuid1 = guid_be.from_buffer_copy(stream.read(16))
        uuid1 = CLSIDToUUID.from_ctype(uuid1)

        ae(uuid1, UUID(bytes=bytes([x for x in range(16)])))
    # end def test_from_ctype
# end class CLSIDToUUIDTestCase

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

class LCIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data_le = b"\x07\x04\xE1\x9C"
        data_be = b"\x9C\xE1\x04\x07"

        stream = ByteIStream(data_le)
        lcid1 = LCID.from_stream(stream, byte_order=LITTLE_ENDIAN)
        lcid2 = LCID.from_stream(stream, 0, byte_order=LITTLE_ENDIAN)

        stream = ByteIStream(data_be)
        lcid3 = LCID.from_stream(stream, byte_order=BIG_ENDIAN)
        lcid4 = LCID.from_stream(stream, 0, byte_order=BIG_ENDIAN)

        ae(lcid1.rsvd, 0x9CE)
        ae(lcid1.sort_id, 1)
        ae(lcid1.lang_id, 0x0407)
        ae(lcid2.rsvd, 0x9CE)
        ae(lcid2.sort_id, 1)
        ae(lcid2.lang_id, 0x0407)
        ae(lcid3.rsvd, 0x9CE)
        ae(lcid3.sort_id, 1)
        ae(lcid3.lang_id, 0x0407)
        ae(lcid4.rsvd, 0x9CE)
        ae(lcid4.sort_id, 1)
        ae(lcid4.lang_id, 0x0407)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        data = b"\x07\x04\xE1\x9C"
        lcid = LCID.from_ctype(lcid_le.from_buffer_copy(data))
        lcid = LCID.from_ctype(lcid)

        ae(lcid.rsvd, 0x9CE)
        ae(lcid.sort_id, 1)
        ae(lcid.lang_id, 0x0407)
    # end def test_from_ctype
# end class LCIDTestCase

class HRESULTTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data_le = b"\xBD\x42\x57\xAE"
        data_be = b"\xAE\x57\x42\xBD"

        stream = ByteIStream(data_le)
        hresult1 = HRESULT.from_stream(stream, byte_order=LITTLE_ENDIAN)
        hresult2 = HRESULT.from_stream(stream, 0, byte_order=LITTLE_ENDIAN)

        stream = ByteIStream(data_be)
        hresult3 = HRESULT.from_stream(stream, byte_order=BIG_ENDIAN)
        hresult4 = HRESULT.from_stream(stream, 0, byte_order=BIG_ENDIAN)

        ae(hresult1.s, 1)
        ae(hresult1.r, 0)
        ae(hresult1.c, 1)
        ae(hresult1.n, 0)
        ae(hresult1.x, 1)
        ae(hresult1.facility, 0x0657)
        ae(hresult1.code, 0x42BD)

        ae(hresult2.s, 1)
        ae(hresult2.r, 0)
        ae(hresult2.c, 1)
        ae(hresult2.n, 0)
        ae(hresult2.x, 1)
        ae(hresult2.facility, 0x0657)
        ae(hresult2.code, 0x42BD)

        ae(hresult3.s, 1)
        ae(hresult3.r, 0)
        ae(hresult3.c, 1)
        ae(hresult3.n, 0)
        ae(hresult3.x, 1)
        ae(hresult3.facility, 0x0657)
        ae(hresult3.code, 0x42BD)

        ae(hresult4.s, 1)
        ae(hresult4.r, 0)
        ae(hresult4.c, 1)
        ae(hresult4.n, 0)
        ae(hresult4.x, 1)
        ae(hresult4.facility, 0x0657)
        ae(hresult4.code, 0x42BD)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        data_le = b"\xBD\x42\x57\xAE"
        hresult = hresult_le.from_buffer_copy(data_le)
        hresult = HRESULT.from_ctype(hresult)

        ae(hresult.s, 1)
        ae(hresult.r, 0)
        ae(hresult.c, 1)
        ae(hresult.n, 0)
        ae(hresult.x, 1)
        ae(hresult.facility, 0x0657)
        ae(hresult.code, 0x42BD)
    # end def test_from_ctype

    def test_from_int(self):
        ae = self.assertEqual

        hresult = HRESULT.from_int(0xAE5742BD)
        ae(hresult.s, 1)
        ae(hresult.r, 0)
        ae(hresult.c, 1)
        ae(hresult.n, 0)
        ae(hresult.x, 1)
        ae(hresult.facility, 0x0657)
        ae(hresult.code, 0x42BD)
    # end def test_from_int
# end class HRESULTTestCase

class CURRENCYToDecimalTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data_le = b"\x4C\x27\xF6\xFF\xFF\xFF\xFF\xFF"
        data_be = data_le[::-1]

        value_le = CURRENCYToDecimal.from_stream(
            ByteIStream(data_le), byte_order=LITTLE_ENDIAN
        )

        value_be = CURRENCYToDecimal.from_stream(
            ByteIStream(data_be), byte_order=BIG_ENDIAN
        )

        value = Decimal("-64.53")
        ae(value_le, value)
        ae(value_be, value)
    # end def test_from_stream

    def test_from_int(self):
        ae = self.assertEqual

        ae(CURRENCYToDecimal.from_int(-645300), Decimal("-64.53"))
    # end def test_from_int
# end class CURRENCYToDecimalTestCase

class DECIMALToDecimalTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data_le = (
            b"\xFF\xFF"
            b"\x03"
            b"\x01"
            b"\x01\x02\x03\x04"
            b"\x05\x06\x07\x08\x09\x0A\x0B\x0C"
        )

        data_be = (
            b"\xFF\xFF"
            b"\x03"
            b"\x01"
            b"\x04\x03\x02\x01"
            b"\x0C\x0B\x0A\x09\x08\x07\x06\x05"
        )

        value = (0x04030201 << 64) | 0x0C0B0A0908070605
        value = -value
        value = Decimal(value) / Decimal(10**3)

        value_le = DECIMALToDecimal.from_stream(
            ByteIStream(data_le), byte_order=LITTLE_ENDIAN
        )

        value_be = DECIMALToDecimal.from_stream(
            ByteIStream(data_be), byte_order=BIG_ENDIAN
        )

        ae(value_le, value)
        ae(value_be, value)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        data_le = (
            b"\xFF\xFF"
            b"\x03"
            b"\x01"
            b"\x01\x02\x03\x04"
            b"\x05\x06\x07\x08\x09\x0A\x0B\x0C"
        )

        data_be = (
            b"\xFF\xFF"
            b"\x03"
            b"\x01"
            b"\x04\x03\x02\x01"
            b"\x0C\x0B\x0A\x09\x08\x07\x06\x05"
        )

        value = (0x04030201 << 64) | 0x0C0B0A0908070605
        value = -value
        value = Decimal(value) / Decimal(10**3)

        value_le = decimal_le.from_buffer_copy(data_le)
        value_le = DECIMALToDecimal.from_ctype(value_le)

        value_be = decimal_be.from_buffer_copy(data_be)
        value_be = DECIMALToDecimal.from_ctype(value_be)

        ae(value_le, value)
        ae(value_be, value)
    # end def test_from_ctype
# end class DECIMALToDecimalTestCase
