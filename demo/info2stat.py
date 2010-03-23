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
import sys
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
    "format_timestamp", "format_entry", "main"
]

def format_timestamp(timestamp):
    if isinstance(timestamp, datetime):
        new_timestamp = timestamp.replace(microsecond=0)
        new_timestamp = new_timestamp.isoformat(" ")
    else:
        new_timestamp = timestamp
    # end if

    return new_timestamp
# end def format_timestamp

def format_header(info2):
    output = list()
    header = info2.header

    output.append("Version: {0}".format(header.version))
    output.append("Item size: {0}".format(header.item_size))

    return output
# end def format_header

def format_entry(entry):
    output = list()

    drive_num = entry.drive_num
    if drive_num < 26:
        drive_letter = chr(ord("A") + drive_num)
        ext_index = entry.name_uni.rfind(".")

        if ext_index != -1:
            ext = entry.name_uni[ext_index:]
        else:
            ext = ""
        # end if

        del_name = "D{0}{1}{2}".format(drive_letter.lower(), entry.index, ext)
    else:
        drive_letter = "?"
        del_name = "Unknown"
    # end if

    if entry.exists:
        exists = "Yes"
    else:
        exists = "No"
    # end if

    dtime = format_timestamp(entry.dtime)

    name_asc = str(entry.name_asc)[2:-1]

    output.append("Deleted name: {0}".format(del_name))
    output.append("Index: {0}".format(entry.index))
    output.append("Drive number: {0} ({1}:)".format(drive_num, drive_letter))
    output.append("ASCII name: {0}".format(name_asc))
    output.append("Unicode name: {0}".format(entry.name_uni))
    output.append("File size: {0} bytes".format(entry.file_size))
    output.append("Deleted time: {0}".format(dtime))
    output.append("Exists on disk: {0}".format(exists))

    return output
# end def format_entry

def main():
    usage = "%prog info2file index"
    description = "\n".join([
        "Displays statistics about a specific entry in an INFO2 file."
        "",
        "If info2file is '-', then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("You must specify both an INFO2 file and an index")
    # end fi


    if args[0] == "-":
        i2 = INFO2(ByteIStream(sys.stdin.buffer.read()))
    else:
        i2 = INFO2(RawIStream(args[0]))
    # end if

    index = int(args[1])

    key_values = [(getattr(item, "index"), item) for item in i2.items]
    key_values = dict(key_values)
    indices = list(key_values.keys())
    indices.sort()
    indices.append(indices[-1] + 1)  # $HEADER

    if index not in indices:
        parser.error("Unknown index {0}".format(index))
    # end if

    if index == indices[-1]:
        output = format_header(i2)
    else:
        output = format_entry(key_values[index])
    # end if

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
