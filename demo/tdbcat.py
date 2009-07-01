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
Extracts thumbnails from a thumbs.db file.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

import sys
from optparse import OptionParser
from os.path import split, join, normpath

from lf.io import raw
from lf.windows.ole.compoundfile.objects import CompoundFile
from lf.windows.shell.thumbsdb.objects import ThumbsDb

parser = OptionParser()
parser.set_usage("%prog [options] <thumbs.db file>")

parser.add_option(
    "-i", "--index", dest="index", action="store",
    help="Thumbnail index to extract"
)

parser.add_option(
    "-a", "--all", dest="extract_all", action="store_true", default=False,
    help="Extract all thumbnails (to files named BASE.#)"
)

parser.add_option(
    "-b", "--base", dest="name_base", action="store", metavar="BASE",
    help="Create files BASE.1, BASE.2, ... (def: <thumbs.db file>)", default=""
)

parser.add_option(
    "-o", "--output-dir", dest="output_dir", action="store", metavar="DIR",
    help="Save files to DIR", default="."
)

(options, args) = parser.parse_args()

if len(args) < 1:
    parser.error("you must specify a thumbs.db file")
# end if

if (not options.extract_all) and (not options.index):
    parser.error("you must specify a thumbnail index (-i) or -a")
# end if

if options.extract_all and options.index:
    parser.error("you can't specify both a thumbnail index (-i) and -a")
# end if

if options.name_base:
    name_base = options.name_base
else:
    name_base = split(args[0])[1]
# end if

thumbsdb = ThumbsDb(CompoundFile(raw.open(args[0])))

if options.extract_all:
    for index, thumbnail in thumbsdb.thumbnails.items():
        outfile_name = ".".join([name_base, "{0}".format(index)])
        outfile_name = join(normpath(options.output_dir), outfile_name)
        outfile = open(outfile_name, "wb")
        outfile.write(thumbnail.data)
        outfile.close()
    # end for
else:
    index = int(options.index)

    if index not in thumbsdb.thumbnails:
        sys.stderr.write("Index {0} not found\n".format(index))
        sys.exit(-2)
    # end if

    sys.stdout.buffer.write(thumbsdb.thumbnails[index].data)
# end if
