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
Base classes for data types.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "Type", "Primitive", "Basic"
]

class DataType():
    """
    Base class for data types supported by the framework.

    .. attribute:: _size_

        The size of the data type.  The units associated are dependent on the
        subclass.
    """

    _size_ = 0

    def __init__(self):
        """Initializes a Type object."""

        pass
    # end def __init__
# end class DataType

class Primitive(DataType):
    """
    Base class for data types that can be used for composition.

    .. attribute:: _size_

        The number of bytes required to represent the data type.
    """

    pass
# end class Primitive

class Basic(Primitive):
    """
    Data types that are "basic building blocks".

    .. attribute:: _format_

        A format string for the standard library's struct module.
    """

    pass
# end class Basic
