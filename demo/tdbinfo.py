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
Dumps information from a thumbs.db file.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

import sys

from lf.io import raw
from lf.windows.ole.compoundfile.objects import CompoundFile
from lf.windows.shell.thumbsdb.objects import ThumbsDb

if len(sys.argv) != 2:
    sys.stderr.write("Usage: {0} <thumbs.db file>\n".format(sys.argv[0]))
    sys.exit(-1)
# end if

field_names = ("Index", "Modified Time", "Original Name")
field_lines = ("-----", "-------------", "-------------")
format_str = "{0: <8} {1: <22} {2}"

thumbsdb = ThumbsDb(CompoundFile(raw.open(sys.argv[1])))
output = list()

output.append("File: {0}".format(sys.argv[1]))
output.append("Note: times are in UTC")
output.append("")

output.append(format_str.format(*field_names))
output.append(format_str.format(*field_lines))

for entry in thumbsdb.catalog.entries:
    mtime = entry.mtime.strftime("%m/%d/%Y %H:%M:%S")
    output.append(format_str.format(entry.index, mtime, entry.name))
# end for

print("\n".join(output))
