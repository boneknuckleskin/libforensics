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

import unittest
import tests

names = [
    "dec.base", "dec.byte", "dec.raw", "dec.subset", "dec.composite",
    "dec.splitraw",

    "dtypes.basic", "dtypes.native", "dtypes.bits", "dtypes.composite",
    "dtypes.dal", "dtypes.reader",

    "win.objects", "win.con.objects", "time", "utils.time",

    "win.ole.cfb.objects", "win.ole.ps.objects", "win.ole.ps.metadata",

    "win.shell.objects", "win.shell.link.objects",

    "win.shell.recyclebin.objects"
]

for index in range(len(names)):
    names[index] = ".".join(["tests", names[index]])
# end for
suite = unittest.TestLoader().loadTestsFromNames(names)
unittest.TextTestRunner().run(suite)
