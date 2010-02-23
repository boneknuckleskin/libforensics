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

"""Tool to demonstrate some of the capabilities in LibForensics"""

# stdlib imports
import sys
from optparse import OptionParser

# local imports
from lf.dec import RawIStream, ByteIStream, SEEK_SET
from lf.win.ole.cfb import CompoundFile

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)


__docformat__ = "restructuredtext en"
__all__ = [
    "main", "VER_MAJOR", "VER_MINOR"
]

def main():
    usage = "%prog [options] olefile sid"
    description = "\n".join([
        "Displays the contents of an OLE stream to standard out."
        "",
        "If file is '-', then stdin is read.",
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-s",
        dest="include_slack",
        action="store_true",
        help="Include slack space",
        default=False
    )

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("Must specify both olefile and sid")
    # end if

    if args[0] == "-":
        cfb = CompoundFile(ByteIStream(sys.stdin.buffer.read()))
    else:
        cfb = CompoundFile(RawIStream(args[0]))
    # end if

    sid = int(args[1])

    if sid not in cfb.dir_entries:
        print("Can't find sid {0}".format(sid), file=sys.stderr)
        sys.exit(-2)
    # end if

    stream = cfb.get_stream(sid, options.include_slack)
    stream.seek(0, SEEK_SET)
    sys.stdout.buffer.write(stream.read())
# end def main

if __name__ == "__main__":
    main()
# end if
