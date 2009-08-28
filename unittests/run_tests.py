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

import unittest
import tests

names = [
    "windows.ole.compoundfile.datatypes", "windows.shell.recyclebin.objects",
    "windows.shell.link.objects",

    "datatype.decode", "datatype.bits", "datatype.structuple",
    "datatype.builtin", "datatype.composite", "datatype.extract",

    "utils.dict", "utils.time",

    "io.interfaces",

    # Uncomment the line below once you've download Word2007RTFSpec9.doc
    #"windows.ole.compoundfile.objects",

]

for index in range(len(names)):
    names[index] = ".".join(["tests", names[index]])
# end for
suite = unittest.TestLoader().loadTestsFromNames(names)
unittest.TextTestRunner().run(suite)
