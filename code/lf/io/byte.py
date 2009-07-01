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
Evidence streams for bytes and byte arrays.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "open"
]

import io
from lf.io.base import Stream, IStreamWrapper

def open(data: bytes) -> Stream:
    """
    Creates a new evidence I/O stream from a bytes/bytearray object.

    :parameters:
        data
            The bytes/bytearray object to use.

    :rtype: Stream
    :returns: A newly created IStream.
    """

    return IStreamWrapper(io.BytesIO(data), len(data))
# end def open
