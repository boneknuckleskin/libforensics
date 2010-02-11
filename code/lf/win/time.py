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

# The algorithms for variant_time_to_datetime and filetime_to_datetime are
# based on the algorithms in the Wine project.

"""Time related utilities for Microsoft Windows. (Deprecated)"""

# stdlib imports
import warnings
warnings.warn(
    "the lf.win.time module is deprecated; use lf.utils.time instead",
    DeprecationWarning
)

# local imports
from lf.utils.time import (
    filetime_to_unix_time, unix_time_to_filetime, filetime_to_datetime,
    variant_time_to_datetime, dos_datetime_to_datetime, dos_date_to_date,
    dos_time_to_time, dos_date_time_to_datetime
)

from datetime import datetime, date, time
from math import ceil, floor
from calendar import isleap

__docformat__ = "restructuredtext en"
__all__ = [
    "filetime_to_unix_time", "unix_time_to_filetime", "filetime_to_datetime",
    "variant_time_to_datetime" "dos_date_time_to_datetime", "dos_date_to_date",
    "dos_time_to_time"
]

# Number of 100ns ticks per clock tick (second).
TICKS_PER_MIN = 600000000
TICKS_PER_SEC = 10000000
TICKS_PER_MSEC = 10000
SECS_PER_DAY = 86400
SECS_PER_HOUR = 3600
SECS_PER_MIN = 60
MINS_PER_HOUR = 60
HOURS_PER_DAY = 24
EPOCH_WEEKDAY = 1
EPOCH_YEAR = 1601
DAYS_PER_NORMAL_YEAR = 365
DAYS_PER_LEAP_YEAR = 366
MONTHS_PER_YEAR = 12

_YearLengths = [ DAYS_PER_NORMAL_YEAR, DAYS_PER_LEAP_YEAR ]
_MonthLengths = [
    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
]
