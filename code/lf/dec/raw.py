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

"""Digital Evidence Container for raw/dd files."""

# stdlib imports
import io
import os

# local imports
from lf.dec.base import SingleStreamContainer, IStreamWrapper

__docformat__ = "restructuredtext en"
__all__ = [
    "Raw", "RawIStream"
]

class Raw(SingleStreamContainer):
    """A container for raw/dd files."""

    def __init__(self, name):
        """Initializes a Raw object.

        :type name: str
        :param name: The name of the raw/dd file.

        """
        super(Raw, self).__init__()
        self.stream = RawIStream(name)
    # end def __init__
# end class Raw

class RawIStream(IStreamWrapper):
    """A stream for raw/dd files.

    .. attribute:: name

        The name of the raw/dd file.

    .. note::

        This class raises :exc:`IOError` (instead of :exc:`ValueError`) in the
        :meth:`seek` method if the ``offset`` parameter is negative, and
        ``whence`` is :const:`SEEK_SET`.

    """

    def __init__(self, name):
        """Initializes a RawIStream object.

        :type name: str
        :param name: The name of the raw/dd file.

        """
        statinfo = os.stat(name)
        stream = io.open(name, "rb")

        super(RawIStream, self).__init__(stream, statinfo.st_size)
        self.name = name
    # end def __init__
# end class RawIStream
