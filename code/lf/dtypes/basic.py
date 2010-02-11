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

"""Base classes for data types"""

# stdlib imports
from ctypes import c_ubyte

# local imports
from lf.dtypes.base import Primitive

__docformat__ = "restructuredtext en"
__all__ = [
    "Basic", "raw"
]

class Basic(Primitive):
    """Base class for :class:`Basic` data types."""

    pass
# end class Basic

class raw(Basic):
    """A data type for a raw array of bytes.

    .. note::

        When using the :class:`raw` data type, the corresponding ctypes object
        is an array of c_ubyte (i.e. c_ubyte * size).  This means you will need
        to call :meth:`bytes` to get a :class:`bytes` object.

    """

    def __init__(self, size):
        """Initializes a raw object.

        :type size: int
        :param size: The number of bytes in the string.

        """
        self._ctype_ = c_ubyte * size
        self._size_ = size
    # end def __init__
# end class raw
