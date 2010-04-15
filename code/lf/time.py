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

"""Converters for various time formats"""

# stdlib imports
from datetime import datetime, date, time
from math import ceil, floor
from calendar import isleap


# local imports
from lf.dec import SEEK_SET
from lf.dtypes import Converter, StdLibConverter, LITTLE_ENDIAN
from lf.dtypes.ctypes import float64_le, float64_be, uint64_le, uint64_be

__docformat__ = "restructuredtext en"
__all__ = [
    "FILETIMEToPOSIXTime", "FILETIMEToUnixTime", "POSIXTimeToFILETIME",
    "UnixTimeToFILETIME", "POSIXTimeTodatetime", "FILETIMETodatetime",
    "DOSDateTimeTodatetime", "VariantTimeTodatetime"
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

class FILETIMEToPOSIXTime(Converter):
    """Converts a FILETIME timestamp to a POSIX (unix) timestamp."""

    @classmethod
    def from_int(cls, timestamp):
        """Converts a Microsoft Windows FILETIME timestamp to a POSIX timestamp.

        :type timestamp: ``int``
        :param timestamp: The FILETIME timestamp.

        :rtype: ``int``
        :returns: The time as a POSIX timestamp.

        """
        return (timestamp - 116444736000000000) // 10000000
    # end def from_int
# end class FILETIMEToPOSIXtime

FILETIMEToUnixTime = FILETIMEToPOSIXTime

class POSIXTimeToFILETIME(Converter):
    """Converts a POSIX (unix) timestamp to a FILETIME timestamp."""

    @classmethod
    def from_int(cls, timestamp):
        """Converts a POSIX timestamp to a Microsoft Windows FILETIME timestamp.

        :type timestamp: ``int``
        :param timestamp: The POSIX timestamp.

        :rtype: ``int``
        :returns: The time as a FILETIME timestamp.

        """
        return (timestamp * 10000000) + 116444736000000000
    # end def from_int
# end class POSIXTimeToFILETIME

UnixTimeToFILETIME = POSIXTimeToFILETIME

class POSIXTimeTodatetime(StdLibConverter):
    """Converts a POSIX timestamp to a ``datetime``."""

    @classmethod
    def from_int(cls, timestamp):
        """Creates a ``datetime`` object from a POSIX (unix) timestamp.

        :type timestamp: ``int``
        :param timestamp: The timestamp as an integer.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """
        return datetime.utcfromtimestamp(timestamp)
    # end def from_int
# end class POSIXTimeTodatetime

UnixTimeTodatetime = POSIXTimeTodatetime

class FILETIMETodatetime(StdLibConverter):
    """Converts a FILETIME to a ``datetime``."""

    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a ``datetime`` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the FILETIME structure.

        :type offset: ``int`` or ``None``
        :param offset: The start of the FILETIME structure in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :raises ValueError: If the FILETIME structure is invalid.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        data = stream.read(8)

        if byte_order == LITTLE_ENDIAN:
            filetime = uint64_le.from_buffer_copy(data).value
        else:
            filetime = uint64_be.from_buffer_copy(data).value
        # end if

        return cls.from_int(filetime)
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a ``datetime`` object from a ctype.

        :type ctype: :class:`lf.win.ctypes.filetime_le` or
                     :class:`lf.win.ctypes.filetime_be`
        :param ctype: A FILETIME object.

        :raises ValueError: If the FILETIME object is invalid.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """
        return cls.from_int((ctype.hi << 32) | ctype.lo)
    # end def from_ctype

    @classmethod
    def from_int(cls, timestamp):
        """Converts a Microsoft FILETIME timestamp to a ``datetime`` object.

        :type timestamp: ``int``
        :param timestamp: The timestamp as a 64 bit integer.

        :raises ValueError: If :attr:`timestamp` is an invalid value.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """
        # This algorithm was adapted from ReactOS's FileTimeToSystemTime
        # function so it's a bit more precise than just doing
        # utcfromtimestamp(timestamp_to_unix_time(timestamp)).

        if timestamp & 0x8000000000000000:
            raise ValueError("invalid timestamp {0}".format(timestamp))
        # end if

        # RtlTimeToFileFields
        milli_secs =  0xFFFF & ((timestamp % TICKS_PER_SEC) // TICKS_PER_MSEC)
        timestamp = timestamp // TICKS_PER_SEC

        days = timestamp // SECS_PER_DAY
        seconds_in_day = timestamp % SECS_PER_DAY

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

        return datetime(
            year, month, days, hours, mins, secs, milli_secs * 1000
        )
    # end def from_int
# end class FILETIMETodatetime

class DOSDateTimeTodatetime(StdLibConverter):
    """Converts DOS date and times to a ``datetime``."""

    @classmethod
    def from_ints(cls, dos_date=None, dos_time=None):
        """Converts DOS date and time values to a ``datetime``.

        :type dos_date: ``int``
        :param dos_date: An MS-DOS date.  If this is None, it defaults to 1/1/1

        :type dos_time: ``int``
        :param dos_time: An MS-DOS time.

        :raises ValueError: if both :attr:`dos_date` and :attr:`dos_time` are
                            ``None``.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """
        if (dos_date is None) and (dos_time is None):
            raise ValueError("dos_date and dos_time are both None")
        # end if

        if dos_time is not None:
            secs = (dos_time & 0x1F) * 2
            mins = (dos_time & 0x7E0) >> 5
            hours = (dos_time & 0xF800) >> 11
        else:
            secs = 0
            mins = 0
            hours = 0
        # end if

        if dos_date is not None:
            day = dos_date & 0x1F
            month = (dos_date & 0x1E0) >> 5
            year = ((dos_date & 0xFE00) >> 9) + 1980
        else:
            day = 1
            month = 1
            year = 1
        # end if

        return datetime(year, month, day, hours, mins, secs)
    # end def from_ints
# end class DOSDateTimeTodatetime

class VariantTimeTodatetime(StdLibConverter):
    """Converts variant timestamp (OLE date) to a ``datetime``."""

    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None, byte_order=LITTLE_ENDIAN):
        """Creates a ``datetime`` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the Variant timestamp.

        :type offset: ``int`` or ``None``
        :param offset: The start of the Variant timestamp in the stream.

        :type byte_order: constant
        :param byte_order: The byte order to use (from :mod:`lf.dtypes`)

        :raises ValueError: If the Variant timestamp is invalid.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        if byte_order == LITTLE_ENDIAN:
            vtime = float64_le.from_buffer_copy(stream.read(8)).value
        else:
            vtime = float64_be.from_buffer_copy(stream.read(8)).value
        # end if

        return cls.from_float(vtime)
    # end def from_stream

    @classmethod
    def from_float(cls, timestamp):
        """Converts a Variant timestamp to a ``datetime``.

        :type timestamp: float
        :param timestamp: The Variant timestamp.

        :raises ValueError: If :attr:`timestamp` is an invalid value.

        :rtype: ``datetime``
        :returns: The corresponding ``datetime`` object.

        """
        # This algorithm was adapted from Wine's VarUdateFromDate function.
        DATE_MIN = -657434
        DATE_MAX = 2958465

        if( (timestamp <= (DATE_MIN - 1.0)) or (timestamp >= (DATE_MAX + 1.0))):
            raise ValueError("invalid variant time {0}".format(timestamp))
        # end if

        if timestamp < 0:
            date_part = ceil(timestamp)
        else:
            date_part = floor(timestamp)
        # end if

        time_part = (timestamp - date_part) + 0.00000000001
        if time_part >= 1:
            time_part -= 0.00000000001
        # end if

        # VARIANT_JulianFromDate
        julian_days = int(timestamp)
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
                                0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30,
                                31
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

                                err_msg = \
                                    "variant time {0} invalid".format(
                                        timestamp
                                    )
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
    # end def from_float
# end class VariantTimeTodatetime
