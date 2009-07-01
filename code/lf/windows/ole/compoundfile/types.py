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
Data types for OLE structured storage files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "OFFSET", "SECT", "FSINDEX", "FSOFFSET", "DFSIGNATURE", "DFPROPTYPE", "SID"
]

from lf.windows.types import ULONG, USHORT, WORD, SHORT

class OFFSET(SHORT):
    pass
# end class OFFSET

class SECT(ULONG):
    pass
# end class SECT

class FSINDEX(ULONG):
    pass
# end class FSINDEX

class FSOFFSET(USHORT):
    pass
# end class FSOFFSET

class DFSIGNATURE(ULONG):
    pass
# end class DFSIGNATURE

class DFPROPTYPE(WORD):
    pass
# end class DFPROPTYPE

class SID(ULONG):
    pass
# end class SID
