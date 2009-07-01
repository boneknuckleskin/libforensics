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
Decoders for Microsoft Word.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "fib_flags1", "fib_flags2", "fib_flags3", "dttm", "fnpi", "fnfb"
]

from lf.struct.decode import Decoder

_fib_flags_1_fields = (
    ("dot", 0, 1), ("glsy", 1, 2), ("complex", 2, 3), ("hasPic", 3, 4),
    ("quickSaves", 4, 9)
)

_fib_flags_2_fields = (
    ("encrypted", 0, 1), ("whichTblStm", 1, 2),
    ("readOnlyRecommended", 2, 3), ("writeReservation", 3, 4),
    ("extChar", 4, 5), ("loadOverride", 5, 6), ("farEast", 6, 7),
    ("crypto", 7, 8)
)

_fib_flags_3_fields = (
    ("mac", 0, 1), ("emptySpecial", 1, 2), ("loadOverridePage", 2, 3),
    ("futureSavedUndo", 3, 4), ("word97Saved", 4, 5), ("spare0", 5, 8)
)

_dttm_fields = (
    ("mins", 0, 6), ("hours", 6, 11), ("day", 11, 16),
    ("month", 16, 20), ("year", 20, 29), ("day_of_week", 29, 32)
)

_fnpi_fields = (
    ("fnpt", 0, 4), ("fnpd", 4, 16)
)

_fnfb_fields = (
    ("fat", 0, 1), ("unused1", 1, 2), ("unused2", 2, 3), ("ntfs", 3, 4),
    ("nonFileSys", 4, 5), ("unused3", 5, 7), ("unused4", 7, 8)
)

fib_flags1 = Decoder("FibFlags1", _fib_flags_1_fields)
fib_flags2 = Decoder("FibFlags2", _fib_flags_2_fields)
fib_flags3 = Decoder("FibFlags3", _fib_flags_3_fields)
dttm = Decoder("Dttm", _dttm_fields)
fnpi = Decoder("FNPI", _fnpi_fields)
fnfb = Decoder("FNFB", _fnfb_fields)
