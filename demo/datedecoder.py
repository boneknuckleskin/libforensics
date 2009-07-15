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
Decodes various date / timestamp formats
"""

__docformat__ = "restructuredtext en"

import sys
from datetime import datetime
from optparse import OptionParser
from binascii import hexlify
from time import gmtime

from lf.windows.time import (
    filetime_to_datetime, variant_time_to_datetime, dos_datetime_to_datetime,
    dos_date_to_date, dos_time_to_time
)

def decode_timestamp(timestamp_type, timestamp, endian, format_str):
    """
    Decodes a timestamp value.

    :parameters:
        timestamp_type
            The type of timestamp (filetime, unix, dos, dosdate, dostime).

        timestamp
            The timestamp.

        endian
            The byte order (l, little, b, big)

        format_str
            The format string to print the timestamp with.

    :rtype: str
    :returns: A string representation of the timestamp.
    """

    if endian in ("l", "little"):
        if timestamp_type in ("dosdate", "dostime"): # 16 bit
            timestamp = \
                (((timestamp >> 0) & 0xFF) << 8) | \
                (((timestamp >> 8) & 0xFF) << 0)
        elif timestamp_type in ("unix", "dos"): # 32
            timestamp = \
                (((timestamp >> 0) & 0xFF) << 24) | \
                (((timestamp >> 8) & 0xFF) << 16) | \
                (((timestamp >> 16) & 0xFF) << 8) | \
                (((timestamp >> 32) & 0xFF) << 0)
        else: # 64 bit
            timestamp = \
                (((timestamp >> 0) & 0xFF) << 56) | \
                (((timestamp >> 8) & 0xFF) << 48) | \
                (((timestamp >> 16) & 0xFF) << 40) | \
                (((timestamp >> 24) & 0xFF) << 32) | \
                (((timestamp >> 32) & 0xFF) << 24) | \
                (((timestamp >> 40) & 0xFF) << 16) | \
                (((timestamp >> 48) & 0xFF) << 8) | \
                (((timestamp >> 56) & 0xFF) << 0)
    # end if

    if timestamp_type == "unix":
        struct_time = gmtime(timestamp)
        timestamp = datetime(
            struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday,
            struct_time.tm_hour, struct_time.tm_min, struct_time.tm_sec
        )
    elif timestamp_type == "filetime":
        timestamp = filetime_to_datetime(timestamp)
    elif timestamp_type == "dos":
        timestamp = dos_datetime_to_datetime(timestamp)
    elif timestamp_type == "dosdate":
        timestamp = dos_date_to_date(timestamp)

        if format_str == default_format_str:
            format_str = "%m/%d/%Y"
        # end if
    else:
        timestamp = dos_time_to_time(timestamp)

        if format_str == default_format_str:
            format_str = "%H:%M:%S"
        # end if
    # end if

    return timestamp.strftime(format_str)
# end def decode_timestamp

default_format_str = "%m/%d/%Y %H:%M:%S"

parser = OptionParser()
parser.set_usage("%prog [options] [timestamp]")
parser.add_option(
    "-b", "--base", dest="base", action="store", type="int",
    help="The numeric base for the input (def: 16)", default=16
)

parser.add_option(
    "-m", "--input-mode", dest="mode", action="store",
    choices=("b", "binary", "t", "text"), default="text",
    help="Set input to (b, binary, t, text) (def: %default) "
    "NOTE: binary only applies when reading from stdin"
)

parser.add_option(
    "-t", "--type", dest="type", action="store", type="choice",
    help="The type of timestamp (filetime, unix, dos, dosdate, dostime)",
    choices=("filetime", "unix", "dos", "dosdate", "dostime")
)

parser.add_option(
    "-e", "--endian", dest="endian", action="store", type="choice",
    help="The byte order to use (b, big, l, little) (def: little)",
    choices=("b", "big", "l", "little"), default="little"
)

parser.add_option(
    "-s", "--format-str", dest="format_str", action="store", type="string",
    help="The format string to print the decoded timestamp",
    default=default_format_str
)

parser.add_option(
    "-f", "--filetime", dest="type", action="store_const", const="filetime",
    help="Implies -t filetime"
)

parser.add_option(
    "-u", "--unix", dest="type", action="store_const", const="unix",
    help="Implies -t unix"
)

parser.add_option(
    "-d", "--decimal", dest="base", help="Implies -b 10", action="store_const",
    const=10
)

parser.add_option(
    "-x", "--hex", dest="base", help="Implies -b 16", action="store_const",
    const=16,
)

(options, args) = parser.parse_args()

if options.type is None:
    parser.error("you must specify the type of timestamp")
# end if

timestamp_type = options.type.lower()
format_str = options.format_str
endian = options.endian
output = list()

if not args:
    if options.mode.lower() in ("t", "text"):
        for line in sys.stdin:
            line = line.strip()
            timestamp = "".join(line.split())
            timestamp = int(timestamp, options.base)
            output.append(
                decode_timestamp(timestamp_type, timestamp, endian, format_str)
            )
        # end for
    else:
        timestamp = sys.stdin.buffer.read()
        timestamp = int(hexlify(timestamp), 16)
        output.append(
            decode_timestamp(timestamp_type, timestamp, endian, format_str)
        )
    # end if
else:
    timestamp = "".join(args)
    timestamp = int(timestamp, options.base)

    output.append(
        decode_timestamp(timestamp_type, timestamp, endian, format_str)
    )
# end if

print("\n".join(output))
