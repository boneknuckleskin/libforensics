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

# The algorithms for variant_time_to_datetime and filetime_to_datetime are
# based on the algorithms in the Wine project.

"""
Time related utilities for Microsoft Windows.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from datetime import datetime, date, time
from math import ceil, floor
from calendar import isleap

__docformat__ = "restructuredtext en"
__all__ = [
    "filetime_to_unix_time", "unix_time_to_filetime", "filetime_to_datetime",
    "variant_time_to_datetime" "dos_datetime_to_datetime", "dos_date_to_date",
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

def filetime_to_unix_time(filetime):
    """
    Converts a Microsoft FILETIME integer to a Unix time integer.

    :parameters:
        filetime
            The time in FILETIME format.

    :rtype: int
    :returns: The time in Unix time.
    """

    return (filetime - 116444736000000000) // 10000000
# end def filetime_to_unix_time

def unix_time_to_filetime(unix_time):
    """
    Converts a Unix time integer to a Microsoft FILETIME integer.

    :parameters:
        unix_time
            The time in Unix time format.

    :rtype: int
    :returns: The time in FILETIME.
    """

    return (unix_time * 10000000) + 116444736000000000
# end def unix_time_to_filetime

def filetime_to_datetime(filetime):
    """
    Converts a Microsoft FILETIME timestamp to a Python datetime object.

    :parameters:
        The time in FILETIME format.

    :raises:
        ValueError
            If filetime is an invalid value.

    :rtype: datetime
    :returns: The timestamp as a datetime object.
    """

    # This algorithm was adapted from ReactOS's FileTimeToSystemTime function
    # so it's a bit more precise than just doing
    # utcfromtimestamp(filetime_to_unix_time(filetime)).

    if filetime & 0x8000000000000000:
        raise ValueError("invalid filetime {0}".format(filetime))
    # end if

    # RtlTimeToFileFields
    milli_secs =  0xFFFF & ((filetime % TICKS_PER_SEC) // TICKS_PER_MSEC)
    filetime = filetime // TICKS_PER_SEC

    days = filetime // SECS_PER_DAY
    seconds_in_day = filetime % SECS_PER_DAY

    while seconds_in_day < 0:
        seconds_in_day += SECS_PER_DAY
        days -= 1
    # end while

    while seconds_in_day >= SECS_PER_DAY:
        seconds_in_day -= SECS_PER_DAY
        days += 1
    # end while

    hours = 0xFFFF & (seconds_in_day // SECS_PER_HOUR)
    seconds_in_day = seconds_in_day % SECS_PER_HOUR
    mins = 0xFFFF & (seconds_in_day // SECS_PER_MIN)
    secs = 0xFF & (seconds_in_day % SECS_PER_MIN)

    year = EPOCH_YEAR
    year += days // DAYS_PER_LEAP_YEAR

    year_temp = year - 1
    days_since_epoch = (
        (year_temp * DAYS_PER_NORMAL_YEAR) + (year_temp // 4) -
        (year_temp // 100) + (year_temp // 400)
    )

    epoch_temp = EPOCH_YEAR - 1
    days_since_epoch -= (
        (epoch_temp * DAYS_PER_NORMAL_YEAR) + (epoch_temp // 4) -
        (epoch_temp // 100) + (epoch_temp // 400)
    )

    days -= days_since_epoch
    while 1:
        leap_year = isleap(year)
        if days < _YearLengths[leap_year]:
            break
        # end if

        year += 1
        days -= _YearLengths[leap_year]
    # end while

    leap_year = isleap(year)
    months = _MonthLengths[leap_year]
    month = 0
    while days >= months[month]:
        days -= months[month]
        month += 1
    # end while

    month += 1
    days += 1

    return datetime(year, month, days, hours, mins, secs, milli_secs * 1000)
# end def filetime_to_datetime

def variant_time_to_datetime(vtime):
    """
    Converts a variant time (OLE date/time) to a Python datetime object.

    :parameters:
        vtime
            The time in OLE date format.

    :raises:
        ValueError
            If vtime is an invalid value.

    :rtype: datetime
    :returns: The time as a Python datetime object.
    """

    # This algorithm was adapted from Wine's VarUdateFromDate function.

    DATE_MIN = -657434
    DATE_MAX = 2958465

    if( (vtime <= (DATE_MIN - 1.0)) or (vtime >= (DATE_MAX + 1.0))):
        raise ValueError("invalid variant time {0}".format(vtime))
    # end if

    if vtime < 0:
        date_part = ceil(vtime)
    else:
        date_part = floor(vtime)
    # end if

    time_part = (vtime - date_part) + 0.00000000001
    if time_part >= 1:
        time_part -= 0.00000000001
    # end if

    # VARIANT_JulianFromDate
    julian_days = int(vtime)
    julian_days = julian_days - DATE_MIN
    julian_days = julian_days + 1757585

    # VARIANT_DMYFromJulian
    l = julian_days + 68569
    n = l * 4 // 146097
    l -= (n * 146097 + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l += 31 - (i * 1461) // 4
    j = (l * 80) // 2447
    day = l - (j * 2447) // 80
    l = j // 11
    month = (j + 2) - (12 * l)
    year = 100 * (n - 49) + i + 1

    time_part *= 24.0
    hours = int(time_part)
    time_part -= hours

    time_part *= 60.0
    mins = int(time_part)
    time_part -= mins

    time_part *= 60.0
    secs = int(time_part)
    time_part -= secs

    if time_part > 0.5:
        if secs < 49:
            secs += 1
        else:
            secs = 0

            if mins < 59:
                mins += 1
            else:
                mins = 0

                if hours < 23:
                    hours += 1
                else:
                    hours = 0

                    if (day + 1) > 28:
                        # VARIANT_RollUDate
                        last_days = [
                            0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
                        ]

                        if year < 100:
                            year += 1900
                        # end if

                        if not month:
                            month = 12
                            year -= 1
                        else:
                            while month > 12:
                                year += 1
                                month -= 12
                            # end while
                        # end if

                        if( (year > 9999) or (hours > 23) or (mins > 59) or
                            (secs > 59)):

                            err_msg = "variant time {0} invalid".format(vtime)
                            raise ValueError(err_msg)
                        # end if

                        if not day:
                            if month == 1:
                                day = 31
                                month = 12
                                year -= 1
                            else:
                                month -= 1
                                if (month == 2) and isleap(year):
                                    day = 29
                                else:
                                    day = last_days[month]
                            # end if
                        elif day > 28:
                            rollForward = 0

                            if (month == 2) and isleap(year):
                                rollForward = day - 29
                            else:
                                rollForward = day - last_days[month]
                            # end if

                            if rollForward > 0:
                                day = rollForward
                                month += 1

                                if month > 12:
                                    month = 1
                                    year += 1
                                # end if
                            # end if
                        # end if
                    # end if
                # end if
            # end if
        # end if
    # end if

    return datetime(year, month, day, hours, mins, secs)
# end def variant_time_to_datetime

def dos_datetime_to_datetime(date_time):
    """
    Converts an MS-DOS date and time stamp into a Python datetime object.

    :parameters:
        date_time
            A combination of an MS-DOS date and time stamp.  The date is in the
            high 16 bits.

    :rtype: datetime
    :returns: The date and time in a datetime object.
    """

    secs = (date_time & 0x1F) * 2
    mins = (date_time & 0x7E0) >> 5
    hours = (date_time & 0xF800) >> 11

    day = (date_time & 0x1F0000) >> 16
    month = (date_time & 0x1E00000) >> 21
    year = ((date_time & 0xFE000000) >> 25) + 1980

    return datetime(year, month, day, hours, mins, secs)
# end def dos_datetime_to_datetime

def dos_date_to_date(dos_date):
    """
    Converts an MS-DOS date stamp into a Python datetime.date object.

    :parameters:
        dos_date
            An MS-DOS date stamp.

    :rtype: date
    :returns: The date in a datetime.date object.
    """

    full_time = dos_datetime_to_datetime(dos_date << 16)
    return date(full_time.year, full_time.month, full_time.day)
# end def dos_date_to_date

def dos_time_to_time(dos_time):
    """
    Converts an MS-DOS time stamp into a Python datetime.time object.

    :parameters:
        dos_time
            An MS-DOS time stamp.

    :rtype: time
    :returns The date in a datetime.time object.
    """

    full_time = dos_datetime_to_datetime(0x015A0000 | dos_time)
    return time(full_time.hour, full_time.minute, full_time.second)
# end def dos_time_to_time
