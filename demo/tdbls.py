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

"""Tool to demonstrate some of the capabilities in lf.win.shell.thumbsdb"""

# stdlib imports
import calendar
import sys
from copy import copy
from optparse import OptionParser
from datetime import datetime

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.ole.cfb import CompoundFile
from lf.win.shell.thumbsdb import ThumbsDb

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
    elif options.long_output or options.pretty_output:
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


def format_output(tdb, options):
    output = list()
    seen = list()

    if options.mactime_output:
        format_str = "|".join([
            "0",  # MD5
            "{file_name}",  # name
            "{id}",  # inode (id)
            "{mode}",  # mode (as a string)
            "0",  # UID
            "0",  # GID
            "{size}",  # size
            "0",  # atime (n/a)
            "{mtime}",  # mtime
            "0",  # ctime (n/a)
            "0"  # btime (n/a)
        ])
    elif options.long_output:
        format_str = "\t".join([
            "{mode} {id}:",
            "{file_name}",
            "{mtime}",
            "{size}"
        ])
    elif options.pretty_output:
        format_str = "".join([
            "{id:<4}",
            "{mtime:<21}",
            "{size:<8}",
            "{file_name}"
        ])

        output.append(format_str.format(
            id = "ID",
            mtime = "Modified time",
            size = "Size",
            file_name = "File name"
        ))
    else:
        format_str = "{mode} {id}: {file_name}"
    # end if

    format_args = {
        "mode": "r/r"
    }

    for entry in tdb.catalog.entries:
        seen.append(entry.id)
        format_args["size"] = tdb.thumbnails[entry.id].size
        format_args["id"] = entry.id
        format_args["file_name"] = entry.file_name
        format_args["mtime"] = format_timestamp(entry.mtime, options)

        output.append(format_str.format(**format_args))
    else:
        if not (options.mactime_output or options.pretty_output):
            # Add the header
            seen.sort()
            format_args["id"] = seen[-1] + 1
            format_args["size"] = 0
            format_args["file_name"] = "$Catalog"
            format_args["mode"] = "v/v"
            format_args["mtime"] = "0"

            output.append(format_str.format(**format_args))
        # end if
    # end for

    return output
# end def format_output

def main():
    usage = "%prog [options] thumbsdb"
    description = "\n".join([
        "Lists the entries in an thumbs.db file.",
        "",
        "If thumbsdb is '-', then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-p",
        dest="pretty_output",
        action="store_true",
        help="Display details in 'pretty-print' format",
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

    parser.add_option(
        "-c",
        dest="catalog_name",
        action="store",
        help="The name of the catalog stream (def: %default)",
        default="Catalog"
    )

    (options, args) = parser.parse_args()

    if options.mactime_output and options.long_output:
        parser.error("You can't specify both -l and -m")
    elif options.mactime_output and options.pretty_output:
        parser.error("You can't specify both -m and -p")
    elif options.long_output and options.pretty_output:
        parser.error("You can't specify both -l and -p")
    elif len(args) == 0:
        parser.error("You must specify a thumbs.db file or '-'")
    # end if

    if args[0] == "-":
        cfb = CompoundFile(ByteIStream(sys.stdin.buffer.read()))
    else:
        cfb = CompoundFile(RawIStream(args[0]))
    # end if

    tdb = ThumbsDb(cfb, options.catalog_name)
    output = format_output(tdb, options)

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
