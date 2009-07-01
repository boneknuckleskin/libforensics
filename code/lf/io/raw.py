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
Evidence I/O streams for raw (dd) file.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "open"
]

import io
import os
from lf.io.base import Stream, IStreamWrapper

def open(filename: str) -> Stream:
    """
    Creates a new stream to work with dd-style (raw) evidence files.

    :parameters:
        filename
            The name of the dd file.

    :rtype: Stream
    :returns: The newly created stream.
    """

    statinfo = os.stat(filename)
    file_stream = io.open(filename, "rb")
    size = statinfo.st_size

    return IStreamWrapper(file_stream, size)
# end def open
