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

"""Adds support for Windows OEM code pages 720 and 858.

The Python standard library does not provide support for Microsoft Windows OEM
code pages 720 and 858.  This package adds supports for these two code pages.

.. note::

    Importing this module does not automatically register the new codecs with
    the global (system) :mod:`codec` registry.  To do this, call the
    :func:`add_codecs` function.

"""

# stdlib imports
import codecs

__docformat__ = "restructuredtext en"
__all__ = [
    "add_codecs"
]

import codecs
from lf.win.codepage import cp720, cp858

def search_function(encoding_name):
    """Passed to :func:`codecs.register` to locate cp720 and cp858 codecs.

    :type encoding_name: str
    :param encoding_name: The name of the encoding.

    :rtype: :class:`CodecInfo`
    :returns: A :class:`CodecInfo` object describing code pages 720 or 858.

    """
    if encoding_name == "cp720":
        return cp720.getregentry()
    elif encoding_name == "cp858":
        return cp858.getregentry()
    # end if

    return None
# end def search_function

def add_codecs():
    """Adds the cp720 and cp858 codecs to the global codec registry."""

    codecs.register(search_function)
# end def add_codecs
