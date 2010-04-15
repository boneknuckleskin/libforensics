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

"""Decodes various date / timestamp formats."""

# stdlib imports
import sys
from datetime import datetime
from optparse import OptionParser
from binascii import hexlify
from struct import unpack, pack

# local imports
from lf.time import (
    FILETIMETodatetime, DOSDateTimeTodatetime, VariantTimeTodatetime,
    POSIXTimeTodatetime
)

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)


__docformat__ = "restructuredtext en"
__all__ = [
    "from_little_endian", "convert_timestamp", "main"
]

def from_little_endian(timestamp, timestamp_type):
    """Converts a timestamp from little endian format"""

    if timestamp_type in ("dosdate", "dostime"):  # 16 bit
        timestamp = ((timestamp & 0x00FF) << 8) | (timestamp >> 8)

    elif timestamp_type == "posix":  # 32 bit
        timestamp = (
            ((timestamp & 0x000000FF) << 24) |
            ((timestamp & 0x0000FF00) << 8) |
            ((timestamp & 0x00FF0000) >> 8) |
            ((timestamp & 0xFF000000) >> 24)
        )

    elif timestamp_type in ("filetime", "variant"):  # 64 bit
        timestamp = (
            ((timestamp & 0x00000000000000FF) << 56) |
            ((timestamp & 0x000000000000FF00) << 40) |
            ((timestamp & 0x0000000000FF0000) << 24) |
            ((timestamp & 0x00000000FF000000) << 8) |
            ((timestamp & 0x000000FF00000000) >> 8) |
            ((timestamp & 0x0000FF0000000000) >> 24) |
            ((timestamp & 0x00FF000000000000) >> 40) |
            ((timestamp & 0xFF00000000000000) >> 56)
        )
    # end if

    return timestamp
# end def from_little_endian

def convert_timestamp(timestamp, timestamp_type):
    """Converts a timestamp from an integer into a datetime object."""

    if timestamp_type == "posix":
        new_timestamp = POSIXTimeTodatetime.from_int(timestamp)

    elif timestamp_type == "dosdate":
        new_timestamp = DOSDateTimeTodatetime.from_ints(timestamp, None).date()

    elif timestamp_type == "dostime":
        new_timestamp = DOSDateTimeTodatetime.from_ints(None, timestamp).time()

    elif timestamp_type == "filetime":
        new_timestamp = FILETIMETodatetime.from_int(timestamp)

    elif timestamp_type == "variant":
        new_timestamp = VariantTimeTodatetime.from_float(timestamp)

    else:
        raise ValueError("Unknown timestamp type: {0}".format(timestamp_type))
    # end if

    return new_timestamp
# end def convert_timestamp

def main():
    usage = "%prog [options] timestamp"
    description = "\n".join([
        "Decodes various timestamp formats.",
        "",
        "If timestamp is '-' then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-b", "--base", dest="base", action="store", type="int", default=16,
        help="The numeric base for the input (def: %default).  This only "
            "applies when the input type is int."
    )

    parser.add_option(
        "-m", "--input-mode", dest="input_mode", action="store",
        choices=("binary", "text"), default="text",
        help="Set input to (binary, text) (def: %default).  Binary is "
        "only available when reading from stdin."
    )

    parser.add_option(
        "-i", "--input-type", metavar="TYPE", action="store",
        choices=("int", "float"), dest="input_type",
        help="The data type of timestamp (int, float).  The default for "
            "variant timestamps is float.  For all other timestamps the "
            "default is int."
    )

    parser.add_option(
        "-t", "--timestamp-type", dest="timestamp_type", action="store",
        type="choice", help="The type of timestamp "
            "(filetime, "
            "unix|posix, "
            "dosdate, "
            "dostime, "
            "variant).",
        choices=(
            "filetime",
            "unix",
            "posix",
            "dosdate",
            "dostime",
            "variant"
        )
    )

    parser.add_option(
        "-e", "--endian", dest="endian", action="store", type="choice",
        choices=("big", "little"), default="little",
        help="The byte order to use (big, little). (def: %default).  This "
            "only applies when the input type is int."
    )

    parser.add_option(
        "-s", "--format-str", dest="format_str", action="store", type="string",
        metavar="FORMAT",
        help="The format string to print the decoded timestamp.  If this is "
            "not specified ISO 8601 format is used."
    )

    parser.add_option(
        "-f", "--filetime", dest="timestamp_type", action="store_const",
        const="filetime",  help="Implies -t filetime"
    )

    parser.add_option(
        "-u", "--unix", dest="timestamp_type", action="store_const",
        const="unix", help="Implies -t unix"
    )

    parser.add_option(
        "-p", "--posix", dest="timestamp_type", action="store_const",
        const="posix", help="Implies -t posix"
    )

    parser.add_option(
        "-d", "--decimal", dest="base", help="Implies -b 10",
        action="store_const", const=10
    )

    parser.add_option(
        "-x", "--hex", dest="base", help="Implies -b 16", action="store_const",
        const=16,
    )

    (options, args) = parser.parse_args()

    if options.timestamp_type is None:
        parser.error("You must specify the type of timestamp")
    # end if

    if not args:
        parser.error("You must specify a timestamp or '-'")
    # end if

    if (options.input_mode == "binary") and (args[0] != "-"):
        parser.error("Binary mode is only valid when reading from stdin")
    # end if

    base = options.base
    input_mode = options.input_mode
    input_type = options.input_type
    timestamp_type = options.timestamp_type
    endian = options.endian
    format_str = options.format_str

    if input_type is None:
        if timestamp_type == "variant":
            input_type = "float"
        else:
            input_type = "int"
        # end if
    # end if

    if timestamp_type == "unix":
        timestamp_type = "posix"
    # end if

    if args[0] == "-":
        timestamp = sys.stdin.buffer.read()
    else:
        timestamp = "".join(args)
    # end if

    if input_mode == "text":
        timestamp = "".join(timestamp.split())  # Remove whitespace
        if input_type == "int":
            timestamp = int(timestamp, base)
        else:
            timestamp = float(timestamp)
        # end if
    else:
        timestamp = int(hexlify(timestamp), 16)
    # end if

    if (input_type == "int") and (endian == "little"):
        timestamp = from_little_endian(timestamp, timestamp_type)
    # end if

    if (timestamp_type == "variant") and isinstance(timestamp, int):
        timestamp = pack(">Q", timestamp)
        timestamp = unpack(">d", timestamp)[0]
    # end if

    timestamp = convert_timestamp(timestamp, timestamp_type)

    output = list()
    if format_str:
        output.append(timestamp.strftime(format_str))
    else:
        if isinstance(timestamp, datetime):
            output.append(timestamp.isoformat(" "))
        else:
            output.append(timestamp.isoformat())
        # end if
    # end if

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
