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
Unit tests for the lf.utils.time module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from unittest import TestCase, main
from datetime import datetime, timedelta

from lf.utils.time import (
    filetime_to_unix_time, unix_time_to_filetime, variant_time_to_datetime,
    filetime_to_datetime, dos_date_time_to_datetime
)

__docformat__ = "restructuredtext en"
__all__ = [
    "TimeTestCase"
]

class TimeTestCase(TestCase):
    def setUp(self):
        self.control = datetime(2002, 11, 26, 19, 25, 0)
    # end def setUp

    def test_dos_date_time_to_datetime(self):
        dos_date = 0x2D7A
        dos_time = 0x9B20
        self.assertEqual(
            dos_date_time_to_datetime(dos_date, dos_time), self.control
        )
    # end def test_dos_date_time_to_datetime

    def test_variant_time_to_datetime(self):
        datetime_3_25 = datetime(1900, 1, 2, 6, 0, 0)
        self.assertEqual(variant_time_to_datetime(3.25), datetime_3_25)
    # end def test_variant_time_to_datetime

    def test_filetime_to_datetime(self):
        value = filetime_to_datetime(0x01C295C491150E00)
        value = value - timedelta(hours=8)
        self.assertEqual(value, self.control)
    # end def test_filetime_to_datetime

    def test_unix_time_to_filetime(self):
        value = unix_time_to_filetime(0x3DE43B0C)
        self.assertEqual(0x01C295C491150E00, value)
    # end def test_unix_time_to_filetime

    def test_filetime_to_unix_time(self):
        value = filetime_to_unix_time(0x01C295C491150E00)
        self.assertEqual(value, 0x3DE43B0C)
    # end def test_filetime_to_unix_time
# end class VariantTimeToDatetimeTestCase
