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

"""Digital Evidence Containers"""

# local imports
from lf.dec.consts import SEEK_SET, SEEK_CUR, SEEK_END
from lf.dec.base import Container, SingleStreamContainer, StreamInfo
from lf.dec.subset import Subset, SubsetIStream
from lf.dec.composite import Composite, CompositeIStream
from lf.dec.raw import Raw, RawIStream
from lf.dec.splitraw import SplitRaw, SplitRawIStream
from lf.dec.byte import Byte, ByteIStream

__docformat__ = "restructuredtext en"
__all__ = [
    "Container", "SingleStreamContainer", "StreamInfo",
    "Subset", "Composite", "Raw", "SplitRaw", "Byte",
    "SubsetIStream", "CompositeIStream", "RawIStream", "SplitRawIStream",
    "ByteIStream",
    "SEEK_SET", "SEEK_CUR", "SEEK_END"
]
