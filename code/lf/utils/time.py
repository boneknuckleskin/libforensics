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

"""Time related utilities for Microsoft Windows (Deprecated)."""

# local imports
from lf.time import (
    FILETIMEToUnixTime, UnixTimeToFILETIME, FILETIMETodatetime,
    DOSDateTimeTodatetime, VariantTimeTodatetime
)

__docformat__ = "restructuredtext en"
__all__ = [
    "filetime_to_unix_time", "unix_time_to_filetime", "filetime_to_datetime",
    "variant_time_to_datetime" "dos_date_time_to_datetime", "dos_date_to_date",
    "dos_time_to_time"
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

    return FILETIMEToUnixTime.from_int(filetime)
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
    return UnixTimeToFILETIME.from_int(unix_time)
# end def unix_time_to_filetime

def filetime_to_datetime(filetime):
    """Converts a Microsoft FILETIME timestamp to a Python datetime object.

    :parameters:
        The time in FILETIME format.

    :raises:
        ValueError
            If filetime is an invalid value.

    :rtype: datetime
    :returns: The timestamp as a datetime object.

    """
    return FILETIMETodatetime.from_int(filetime)
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
    return VariantTimeTodatetime.from_float(vtime)
# end def variant_time_to_datetime

def dos_date_time_to_datetime(dos_date, dos_time):
    """
    Converts an MS-DOS date and time stamps into a Python datetime object.

    :parameters:
        dos_date
            An MS-DOS date.

        dos_time
            An MS-DOS time.

    :rtype: datetime
    :returns: The date and time.
    """
    return DOSDateTimeTodatetime.from_ints(dos_date, dos_time)
# end def dos_date_time_to_datetime

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

    return DOSDateTimeTodatetime.from_ints(dos_date).date()
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

    return DOSDateTimeTodatetime.from_ints(dos_time=dos_time).time()
# end def dos_time_to_time
