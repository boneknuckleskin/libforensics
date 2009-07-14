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
Objects to work with thumbs.db files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "ThumbsDb", "Catalog", "CatalogEntry"
]

from lf.io.consts import SEEK_SET
from lf.windows.time import filetime_to_datetime

from lf.windows.shell.thumbsdb.extractors import (
    catalog_header, catalog_entry_header, entry_header, entry_header_old
)

class Catalog():
    """
    Represents the catalog of file names

    .. attribute:: width

        The width (in pixels) of the thumbnails.

    .. attribute:: height

        The height (in pixels) of the thumbnails.

    .. attribute:: entries
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a Catalog object.

        :parameters:
            stream
                A stream that contains the catalog.

            offset
                The start of the catalog, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = catalog_header.extract(stream.read(16))
        offset += 16

        entries = list()
        for index in range(header.count):
            entries.append(CatalogEntry(stream, offset))
            offset += entries[-1].size
        # end for

        self.width = header.width
        self.height = header.height
        self.entries = entries
    # end def __init__
# end class Catalog

class CatalogEntry():
    """
    Represents an entry in the Catalog.

    .. attribute:: index

        The index number of the thumbnail.

    .. attribute:: name

        The name of the file the thumbnail is associated with.

    .. attribute:: mtime

        The time the thumbnail was last modified.

    .. attribute:: size

        The total size of the catalog entry.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a CatalogEntry object.

        :parameters:
            stream
                A stream that contains the catalog entry.

            offset
                The start of the catalog entry, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = catalog_entry_header.extract(stream.read(16))
        name = stream.read(header.size - 16).decode("utf_16_le").rstrip("\x00")

        self.index = header.index
        self.name = name
        try:
            self.mtime = filetime_to_datetime(header.mtime)
        except KeyboardInterrupt:
            raise
        except:
            self.mtime = header.mtime
        # end try
        self.size = header.size
    # end def __init__
# end class CatalogEntry

class Thumbnail():
    """
    Represents the information in a Thumbnail stream.

    .. attribute:: size

        The total size of the entry.

    .. attribute:: data

        The raw thumbnail data.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a Thumbnail object.

        :parameters:
            stream
                A stream that contains the thumbnail entry.

            offset
                The start of the thumbnail entry, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = entry_header.extract(stream.read(12))
        offset += 12
        size = header.size

        if stream.read(2) != b"\xFF\xD8":
            stream.seek(offset, SEEK_SET)
            old_header = entry_header_old.extract(stream.read(16))
            offset += 16
            size = old_header.size
        else:
            stream.seek(offset, SEEK_SET)
        # end if

        self.data = stream.read(stream.size - offset)
        self.size = size
    # end def __init__
# end class Thumbnail

class ThumbsDb():
    """
    Represents the information in a thumbs.db file.

    .. attribute:: catalog

        A Catalog object.

    .. attribute:: thumbnails

        A dictionary of the thumbnails.  The keys are the numeric indices.
    """

    def __init__(self, cfb):
        """
        Initializes a ThumbsDb object.

        :parameters:
            cfb
                A CompoundFile that represents the thumbs.db file.
        """

        names = dict()
        for entry in cfb.dir_entries.values():
            names[entry.name] = entry.sid
        # end for

        stream = cfb.get_stream(names["Catalog"])

        catalog = Catalog(stream)
        thumbnails = dict()

        for entry in catalog.entries:
            stream_name = "{0}".format(entry.index)[::-1]

            if stream_name in names:
                thumbnail_entry = Thumbnail(cfb.get_stream(names[stream_name]))
                thumbnails[entry.index] = thumbnail_entry
            # end if
        # end for

        self.catalog = catalog
        self.thumbnails = thumbnails
    # end def __init__
# end class ThumbsDb
