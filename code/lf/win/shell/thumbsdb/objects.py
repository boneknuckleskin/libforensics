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

"""Objects to work with thumbnail cache (thumbs.db) files."""

# stdlib imports
from codecs import getdecoder

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import ActiveStructuple
from lf.time import FILETIMETodatetime

from lf.win.shell.thumbsdb.ctypes import (
    catalog_header, catalog_entry_header, entry_header, entry_header_old
)

# module globals
_utf16_le_decoder = getdecoder("utf_16_le")

__docformat__ = "restructuredtext en"
__all__ = [
    "ThumbsDb", "Thumbnail", "Catalog", "CatalogEntry"
]

class ThumbsDb():
    """Represents a thumbs.db file.

    .. attribute:: catalog

        An instance of a :class:`Catalog` object.

    .. attribute:: thumbnails

        A dictionary of :class:`Thumbnail` objects.  The keys are the numeric
        indices.

    """

    def __init__(self, cfb, catalog_name="Catalog"):
        """Initializes a :class:`ThumbsDb` object.

        :type cfb: :class:`~lf.win.ole.cfb.CompoundFile`
        :param cfb: An OLE compound file that represents the thumbs.db file.

        :type catalog_name: ``str``
        :param catalog_name: The name of the Catalog OLE stream.

        :raises KeyError: If :attr:`catalog_name` is not found in :attr:`cfb`.

        """
        catalog_sid = None
        entry_map = dict()
        thumbnails = dict()

        for (sid, entry) in cfb.dir_entries.items():
            if entry.name == catalog_name:
                catalog_sid = sid
            else:
                entry_map[entry.name] = sid
            # end if
        # end for

        if catalog_sid is None:
            raise KeyError("Catalog {0} not found".format(catalog_name))
        # end for

        catalog = Catalog.from_stream(cfb.get_stream(catalog_sid))

        for catalog_entry in catalog.entries:
            sid = entry_map[catalog_entry.stream_name]
            thumbnail = Thumbnail.from_stream(cfb.get_stream(sid))
            thumbnails[catalog_entry.id] = thumbnail
        # end for

        self.catalog = catalog
        self.thumbnails = thumbnails
    # end def __init__
# end class ThumbsDb

class Thumbnail(ActiveStructuple):
    """Represents a thumbnail in a thumbs.db file.

    .. attribute:: size

        The total size of the entry.

    .. attribute:: data

        The raw thumbnail data.

    """
    _takes_stream = True
    _fields_ = ("size", "data")

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`Thumbnail` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`Thumbnail`
        :returns: The corresponding :class:`Thumbnail` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        stream.seek(offset + 12, SEEK_SET)
        if stream.read(2) != b"\xFF\xD8":  # Old style header?
            stream.seek(offset, SEEK_SET)
            header = entry_header_old.from_buffer_copy(stream.read(16))
            offset += 16
        else:
            stream.seek(offset, SEEK_SET)
            header = entry_header.from_buffer_copy(stream.read(12))
            offset += 12
        # end if

        data = stream.read(header.size)

        return cls((header.size, data))
    # end def from_stream
# end class Thumbnail

class Catalog(ActiveStructuple):
    """ Represents the catalog of information in a thumbs.db file.

    .. attribute:: width

        The width (in pixels) of the thumbnails.

    .. attribute:: height

        The height (in pixels) of the thumbnails.

    .. attribute:: item_count

        The number of catalog entries. (extracted)

    .. attribute:: entries

        A list of :class:`CatalogEntry` objects describing the thumbnails.

    """
    _takes_stream = True
    _fields_ = ("width", "height", "item_count", "entries")

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`Catalog` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`Catalog`
        :returns: The corresponding :class:`Catalog` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = catalog_header.from_buffer_copy(stream.read(16))
        offset += 16

        item_count = header.item_count
        entries = list()
        for counter in range(item_count):
            stream.seek(offset, SEEK_SET)
            data = stream.read(16)
            if len(data) != 16:  # Exit loop if EOF
                break
            # end if

            entry = CatalogEntry.from_stream(stream, offset)
            entries.append(entry)
            offset += entry.size
        # end for

        return cls((header.width, header.height, item_count, entries))
    # end def from_method
# end class Catalog

class CatalogEntry(ActiveStructuple):
    """Represents an entry in a :class:`Catalog`.

    .. attribute:: size

        The total size of the catalog entry.

    .. attribute:: id

        The numeric identifier of the thumbnail, used to determine the
        corresponding stream name.  Sometimes called the index.

    .. attribute:: mtime

        The time the thumbnail was last modified.

    .. attribute:: file_name

        The name of the file the thumbnail is associated with.

    .. attribute:: stream_name

        The name of the corresponding OLE stream. (computed)

    """
    _takes_stream = True
    _fields_ = ("size", "id", "mtime", "file_name", "stream_name")

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`CatalogEntry` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in :attr:`stream`.

        :rtype: :class:`CatalogEntry`
        :returns: The corresponding :class:`CatalogEntry` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        entry = catalog_entry_header.from_buffer_copy(stream.read(16))
        if entry.size > 16:
            file_name = stream.read(entry.size - 16)

            new_file_name = _utf16_le_decoder(file_name, "ignore")[0]
            if new_file_name:
                file_name = new_file_name.split("\x00", 1)[0]
            # end if
        else:
            file_name = None
        # end if

        try:
            mtime = FILETIMETodatetime.from_ctype(entry.mtime)
        except (TypeError, ValueError):
            mtime = (entry.mtime.hi << 32) | entry.mtime.lo
        # end try

        stream_name = "{0}".format(entry.id)
        stream_name = stream_name[::-1]

        return cls((entry.size, entry.id, mtime, file_name, stream_name))
    # end def from_stream
# end class CatalogEntry
