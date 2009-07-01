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
Exceptions used in the framework.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
    "LFException", "RuntimeError", "InvalidFormatError"
]

class LFException(Exception):
    """Base class for all framework related exceptions"""

    pass
# end class BaseLFException

class RuntimeError(LFException):
    """For errors that occur during runtime"""

    pass
# end class RuntimeError

class InvalidFormatError(LFException):
    """For errors that occur for invalid file formats"""

    pass
# end class InvalidFormatError
