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

"""A stream for a raw/dd file that has been split into multiple pieces."""

# local imports
from lf.dec.consts import SEEK_SET
from lf.dec.base import SingleStreamContainer
from lf.dec.composite import CompositeIStream
from lf.dec.raw import RawIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "SplitRaw", "SplitRawIStream"
]

class SplitRaw(SingleStreamContainer):
    """A container for a raw/dd file that has been split into pieces."""

    def __init__(self, names):
        """Initializes a SplitRaw object.

        :type names: list of strings
        :param names: A list of the names of the raw/dd files.

        """
        super(SplitRaw, self).__init__()
        self.stream = SplitRawIStream(names)
    # end def __init__
# end class SplitRaw

class SplitRawIStream(CompositeIStream):
    """A stream for a raw/dd file that has been split into pieces.

    .. attribute:: _names

        A list of the names of the raw/dd files.
    """

    def __init__(self, names):
        """Initializes a SplitRawIStream object.

        :type names: list of strings
        :param names: A list of the names of the raw/dd files.

        """
        raw_streams = list()
        for name in names:
            raw_stream = RawIStream(name)
            raw_streams.append((raw_stream, 0, raw_stream.size))
        # end for

        super(SplitRawIStream, self).__init__(raw_streams)
        self._names = names
    # end def __init__
# end class SplitRawIStream
