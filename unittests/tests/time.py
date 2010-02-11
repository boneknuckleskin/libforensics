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

"""Unit tests for the lf.time module."""

# stdlib imports
from unittest import TestCase, main
from datetime import datetime, timedelta

# local imports
from lf.dec import ByteIStream
from lf.dtypes import LITTLE_ENDIAN, BIG_ENDIAN
from lf.win.ctypes import filetime_le
from lf.time import (
    FILETIMEToUnixTime, UnixTimeToFILETIME, FILETIMETodatetime,
    DOSDateTimeTodatetime, VariantTimeTodatetime
)

__docformat__ = "restructuredtext en"
__all__ = [
    "FILETIMEToUnixTimeTestCase", "UnixTimeToFILETIMETestCase",
    "FILETIMETodatetimeTestCase", "DOSDateTimeTodatetimeTestCase",
    "VariantTimeTodatetimeTestCase"
]

class FILETIMEToUnixTimeTestCase(TestCase):
    def test_from_int(self):
        ae = self.assertEqual

        ae(FILETIMEToUnixTime.from_int(0x01C295C491150E00), 0x3DE43B0C)
    # end def test_from_int
# end class FILETIMEToUnixTimeTestCase

class UnixTimeToFILETIMETestCase(TestCase):
    def test_from_int(self):
        ae = self.assertEqual

        ae(UnixTimeToFILETIME.from_int(0x3DE43B0C), 0x01C295C491150E00)
    # end def test_from_int
# end class UnixTimeToFILETIMETestCase

class FILETIMETodatetimeTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        ar = self.assertRaises

        data_le = b"\x00\x0E\x15\x91\xC4\x95\xC2\x01"
        data_be = data_le[::-1]
        data_bad = b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

        stream = ByteIStream(data_le)
        filetime1 = FILETIMETodatetime.from_stream(
            stream, byte_order=LITTLE_ENDIAN
        )
        filetime2 = FILETIMETodatetime.from_stream(stream, 0, LITTLE_ENDIAN)

        stream = ByteIStream(data_be)
        filetime3 = FILETIMETodatetime.from_stream(
            stream, byte_order=BIG_ENDIAN
        )
        filetime4 = FILETIMETodatetime.from_stream(stream, 0, BIG_ENDIAN)

        ae(filetime1, datetime(2002, 11, 27, 3, 25, 0))
        ae(filetime2, datetime(2002, 11, 27, 3, 25, 0))
        ae(filetime3, datetime(2002, 11, 27, 3, 25, 0))
        ae(filetime4, datetime(2002, 11, 27, 3, 25, 0))

        stream = ByteIStream(data_bad)
        ar(ValueError, FILETIMETodatetime.from_stream, stream)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual
        ar = self.assertRaises

        data = b"\x00\x0E\x15\x91\xC4\x95\xC2\x01"
        data_bad = b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

        filetime = filetime_le.from_buffer_copy(data)
        filetime = FILETIMETodatetime.from_ctype(filetime)

        ae(filetime, datetime(2002, 11, 27, 3, 25, 0))

        filetime = filetime_le.from_buffer_copy(data_bad)
        ar(ValueError, FILETIMETodatetime.from_ctype, filetime)
    # end def test_from_ctype

    def test_from_int(self):
        ae = self.assertEqual
        ar = self.assertRaises

        filetime = FILETIMETodatetime.from_int(0x01C295C491150E00)
        ae(filetime, datetime(2002, 11, 27, 3, 25, 0))
        ar(ValueError, FILETIMETodatetime.from_int, 0xFFFFFFFFFFFFFFFF)
    # end def test_from_int
# end class FILETIMETodatetimeTestCase

class DOSDateTimeTodatetimeTestCase(TestCase):
    def test_from_ints(self):
        ae = self.assertEqual
        ar = self.assertRaises

        value = DOSDateTimeTodatetime.from_ints(0x2D7A, 0x9B20)
        ae(value, datetime(2002, 11, 26, 19, 25, 0))

        value = DOSDateTimeTodatetime.from_ints(dos_time=0x9B20)
        ae(value, datetime(1, 1, 1, 19, 25, 0))

        value = DOSDateTimeTodatetime.from_ints(0x2D7A)
        ae(value, datetime(2002, 11, 26, 0, 0, 0))

        ar(ValueError, DOSDateTimeTodatetime.from_ints)
    # end def test_from_ints
# end class DOSDateTimeTodatetimeTestCase

class VariantTimeTodatetimeTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        datetime_3_25 = datetime(1900, 1, 2, 6, 0, 0)

        data_le = b"\x00\x00\x00\x00\x00\x00\x0A\x40"
        data_be = b"\x40\x0A\x00\x00\x00\x00\x00\x00"

        stream = ByteIStream(data_le)
        value = \
            VariantTimeTodatetime.from_stream(stream, byte_order=LITTLE_ENDIAN)
        ae(value, datetime_3_25)

        value = VariantTimeTodatetime.from_stream(stream, 0, LITTLE_ENDIAN)
        ae(value, datetime_3_25)


        stream = ByteIStream(data_be)
        value = \
            VariantTimeTodatetime.from_stream(stream, byte_order=BIG_ENDIAN)
        ae(value, datetime_3_25)

        value = VariantTimeTodatetime.from_stream(stream, 0, BIG_ENDIAN)
        ae(value, datetime_3_25)
    # end def test_from_stream

    def test_from_float(self):
        ae = self.assertEqual

        value = VariantTimeTodatetime.from_float(3.25)
        ae(value, datetime(1900, 1, 2, 6, 0, 0))
    # end def teest_from_float
# end class VariantTimeTodatetimeTestCase
