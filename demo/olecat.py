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
Extracts the contents of a stream from an OLE file.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

import io
import sys
from os.path import join, normpath, split
from optparse import OptionParser

from lf.io import raw
from lf.windows.ole.compoundfile.objects import CompoundFile

parser = OptionParser()
parser.set_usage("Usage: %prog [options] <ole file>")
parser.add_option(
    "-i", "--id", dest="stream_id", action="store", metavar="ID",
    help="Find stream at location ID"
)

parser.add_option(
    "-n", "--name", dest="stream_name", action="store", metavar="NAME",
    help="Find stream called NAME"
)

parser.add_option(
    "-a", "--all", dest="extract_all", action="store_true", default=False,
    help="Extract all streams (to files named BASE.#)"
)

parser.add_option(
    "-r", "--root", dest="include_root", action="store_true", default=False,
    help="Extract root stream (when extracting all streams)"
)

parser.add_option(
    "-b", "--base", dest="name_base", action="store", metavar="BASE",
    help="Create files BASE.1, BASE.2, ... (def: <ole file>)", default=""
)

parser.add_option(
    "-o", "--output-dir", dest="output_dir", action="store", metavar="DIR",
    help="Save files to DIR", default="."
)

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("you must specify an ole file")
# end if

if (options.extract_all and (options.stream_id or options.stream_name)):
    parser.error("you can't specify both all and a stream id/name")
# end if

if not (options.extract_all or options.stream_id or options.stream_name):
    parser.error("you must specify a stream id, name, or all")
# end if

cfb = CompoundFile(raw.open(args[0]))

if options.name_base:
    name_base = options.name_base
else:
    name_base = split(args[0])[1]
# end if

if options.extract_all:
    for entry in cfb.dir_entries.values():
        if (entry.sid == 0) and (not options.include_root):
            continue
        # end if

        outfile_name = ".".join([name_base, "{0}".format(entry.sid)])
        outfile_name = normpath(join(options.output_dir, outfile_name))

        outfile = io.open(outfile_name, "wb", buffering=0)
        stream = cfb.get_stream(entry.sid)
        outfile.write(stream.read(stream.size))
        outfile.close()
    # end for
else:
    if options.stream_id is not None:
        identifier = int(options.stream_id)
        attr = "sid"
    else:
        identifier = options.stream_name
        attr = "name"
    # end if

    for entry in cfb.dir_entries.values():
        if identifier == getattr(entry, attr):
            stream = cfb.get_stream(entry.sid)
            sys.stdout.buffer.write(stream.read(stream.size))
            break
        # end if
    else:
        sys.stderr.write("error: stream {0} not found".format(identifier))
        sys.exit(-2)
    # end for
# end if
