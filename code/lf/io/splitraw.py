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
Streams for split-raw (multiple raw file) evidence containers.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "open"
]

from lf.io.base import Stream
from lf.io import raw, composite

def open(filenames: list) -> Stream:
    """
    Creates a new evidence I/O stream, from a list of dd-style (raw) files.

    :parameters:
        filenames
            An iterable of file names of the dd files.
    """

    segments = list()
    for filename in filenames:
        raw_stream = raw.open(filename)
        segments.append((raw_stream, 0, raw_stream.size))
    # end for

    return composite.open(segments)
# end def open
