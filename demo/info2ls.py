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

"""Tool to demonstrate some of the capabilities in lf.win.shell.recyclebin"""

# stdlib imports
import calendar
import sys
from copy import copy
from optparse import OptionParser
from datetime import datetime

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.shell.recyclebin import INFO2

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)


__docformat__ = "restructuredtext en"
__all__ = [
    "format_timestamp", "format_output", "main"
]

def format_timestamp(timestamp, options):
    if options.mactime_output:
        if isinstance(timestamp, datetime):
            new_timestamp = calendar.timegm(timestamp.timetuple())
            if new_timestamp < 0:
                new_timestamp = 0
            # end if
        else:
            try:
                new_timestamp = int(timestamp)
            except (ValueError, TypeError):
                new_timestamp = 0
            # end try
        # end if
    elif options.long_output or options.rifiuti_output:
        if isinstance(timestamp, datetime):
            new_timestamp = timestamp.replace(microsecond=0)
            new_timestamp = new_timestamp.isoformat(" ")
        else:
            new_timestamp = timestamp
        # end try
    else:
        new_timestamp = timestamp
    # end if

    return new_timestamp
# end def format_timestamp


def format_output(i2, options):
    output = list()
    seen = list()

    if options.mactime_output:
        format_str = "|".join([
            "0",  # MD5
            "{name}",  # name
            "{index}",  # inode (id)
            "{mode}",  # mode (as a string)
            "0",  # UID
            "0",  # GID
            "{size}",  # size
            "0",  # atime (n/a)
            "0",  # mtime (n/a)
            "{dtime}",  # ctime (really dtime)
            "0"  # btime (really dtime, time entry was created)
        ])
    elif options.long_output:
        format_str = "\t".join([
            "{mode}{del}{index}:",
            "{name}",
            "{dtime}",
            "{size}"
        ])
    elif options.rifiuti_output:
        format_str = "".join([
            "{index:<7}",
            "{dtime:<21}",
            "{drive_num:<14}",
            "{size:<12}",
            "{deleted:<9}",
            "{name}"
        ])

        output.append(format_str.format(
            index = "INDEX",
            dtime = "Deleted time",
            drive_num = "Drive number",
            size = "Size",
            deleted = "Deleted",
            name = "Original name"
        ))
    else:
        format_str = "{mode}{del}{index} {name}"
    # end if

    format_args = {
        "mode": "r/r"
    }

    for item in i2.items:
        seen.append(item.index)
        format_args["index"] = item.index
        format_args["drive_num"] = item.drive_num
        format_args["size"] = item.file_size

        if item.exists:
            format_args["deleted"] = "No"
        else:
            format_args["deleted"] = "Yes"
        # end if

        if item.exists:
            format_args["del"] = " "
        else:
            format_args["del"] = " * "
        # end if

        if item.name_uni:
            name = item.name_uni
        else:
            if item.exists:
                name = repr(item.name_asc)[2:-1]
            else:
                if item.drive_index < 26:
                    first_char = item.drive_index + 0x41
                else:
                    first_char = b"?"
                # end if

                name = b"".join([first_char, item.name_asc])
                name = repr(name)[2:-1]
            # end if
        # end if

        if options.mactime_output and not item.exists:
            name = "".join([name, " (deleted )"])
        # end if

        format_args["name"] = name

        dtime = format_timestamp(item.dtime, options)
        format_args["dtime"] = dtime

        output.append(format_str.format(**format_args))
    else:
        if not (options.mactime_output or options.rifiuti_output):
            # Add the header
            seen.sort()
            format_args["index"] = seen[-1] + 1
            format_args["size"] = 0
            format_args["del"] = " "
            format_args["name"] = "$HEADER"
            format_args["mode"] = "v/v"
            format_args["dtime"] = "0"

            output.append(format_str.format(**format_args))
        # end if
    # end for

    return output
# end def format_output

def main():
    usage = "%prog [options] info2file"
    description = "\n".join([
        "Lists the entries in an INFO2 file.",
        "",
        "If info2file is '-', then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-R",
        dest="rifiuti_output",
        action="store_true",
        help="Display details in Rifiuti-style format",
        default=False
    )

    parser.add_option(
        "-l",
        dest="long_output",
        action="store_true",
        help="Display details in long format",
        default=False
    )

    parser.add_option(
        "-m",
        dest="mactime_output",
        action="store_true",
        help="Display details in mactime format",
        default=False
    )

    (options, args) = parser.parse_args()

    if options.mactime_output and options.long_output:
        parser.error("You can't specify both -l and -m")
    elif options.mactime_output and options.rifiuti_output:
        parser.error("You can't specify both -m and -r")
    elif options.long_output and options.rifiuti_output:
        parser.error("You can't specify both -l and -r")
    elif len(args) == 0:
        parser.error("You must specify an INFO2 file or '-'")
    # end if

    if args[0] == "-":
        i2 = INFO2(ByteIStream(sys.stdin.buffer.read()))
    else:
        i2 = INFO2(RawIStream(args[0]))
    # end if

    output = format_output(i2, options)

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
