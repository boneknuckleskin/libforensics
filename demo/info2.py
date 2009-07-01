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
Extracts information from an INFO2 file.
"""

__docformat__ = "restructuredtext en"


import sys
from lf.io import raw
from lf.windows.shell.recyclebin.objects import INFO2

if len(sys.argv) != 2:
    print("Usage: {0} <INFO2 file>".format(sys.argv[0]))
    sys.exit(-1)
# end if

info2 = INFO2(raw.open(sys.argv[1]))

fields = ("Deleted name", "Deleted time", "Size", "Original name")
field_headers = ("------------", "------------", "----", "------------")
format_str = "{0: <15} {1: <22} {2: <12} {3}"

output = list()
output.append("File: {0}".format(sys.argv[1]))
output.append("Note: times are in UTC")
output.append("")

output.append(format_str.format(*fields))
output.append(format_str.format(*field_headers))

for item in info2.items:
    drive_letter = chr(ord("A") + item.drive_num).lower()
    name = item.name_uni

    try:
        del_name = "D{0}{1}{2}".format(
            drive_letter, item.index, name[name.rindex("."):]
        )
    except:
        del_name = "D{0}{1}".format(drive_letter, item.index)
    # end try

    dtime = item.dtime.strftime("%m/%d/%Y %H:%M:%S")

    output.append(format_str.format(del_name, dtime, item.phys_size, name))
# end for

print("\n".join(output))
