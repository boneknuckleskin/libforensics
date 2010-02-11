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

"""Base classes for data types."""

__docformat__ = "restructuredtext en"
__all__ = [
    "DataType", "Primitive"
]

class DataType():
    """Base class for data types supported by the framework.

    .. attribute:: _size_

        The size of the data type.  The units (e.g. bits or bytes) are
        dependent on the subclass.
    """

    _size_ = 0

    def __init__(self):
        """Initializes a DataType object."""
        pass
    # end def __init__
# end class DataType

class Primitive(DataType):
    """Base class for data types that can be used to create data types.

    .. attribute:: _ctype_

        A :mod:`ctypes` object that reflects the data type.

    """
    _ctype_ = None
# end class Primitive
