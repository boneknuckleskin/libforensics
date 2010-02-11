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

"""Objects to work with OLE structured storage files."""

# local imports
from lf.dec import CompositeIStream, ByteIStream, SubsetIStream, SEEK_SET
from lf.time import FILETIMETodatetime
from lf.win.objects import CLSIDToUUID
from lf.dtypes import ActiveStructuple

from lf.win.ole.cfb.consts import (
    STREAM_ID_MAX, STREAM_ID_NONE, FAT_EOC, FAT_UNALLOC, FAT_FAT_SECT,
    FAT_DIF_SECT, MAX_REG_SECT
)
from lf.win.ole.cfb.ctypes import (
    header, dir_entry, fat_entry, mini_fat_entry, di_fat_entry
)

__docformat__ = "restructuredtext en"
__all__ = [
    "CompoundFile", "DirEntry", "Header"
]

_invalid_name_chars = set("/\:!")

class CompoundFile():
    """Represents an OLE structured storage file (compound file binary).

    .. attribute:: header

        A :class:`Header` object containing information from the compound file
        header.

    .. attribute:: sect_size

        The number of bytes in a sector.

    .. attribute:: mini_sect_size

        The number of bytes in a mini sector.

    .. attribute:: mini_stream_cutoff

        The maximum size of a file (in bytes) in the mini stream.

    .. attribute:: ver_major

        The major version number. (from the header)

    .. attribute:: ver_minor

        The minor version number. (from the header)

    .. attribute:: di_fat

        A list of entries from the double indirect FAT.

    .. attribute:: fat

        A list of entries from the FAT.

    .. attribute:: mini_fat

        A list of entries from the mini FAT.

    .. attribute:: mini_stream

        A stream covering the contents of the mini stream.  None if there is no
        mini stream.

    .. attribute:: dir_stream

        A stream covering the contents of the directory stream.  None if there
        is no directory stream.

    .. attribute:: root_dir_entry

        A DirEntry object for the root directory entry.  None if there is no
        root directory.

    .. attribute:: dir_entries

        A dictionary of directory entries, found by traversing the RB tree.

    .. attribute:: cfb_stream

        A stream covering the contents of the file.

    """

    def __init__(self, stream, offset=None):
        """Initializes a :class:`CompoundFile` object.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream covering the contents of the compound file.

        :type offset: ``int``
        :param offset: The start of the compound file in the stream.

        """
        byte_offset = self.byte_offset
        fat = list()
        mini_fat = list()
        di_fat = list()

        header = Header.from_stream(stream, offset)

        self.header = header
        self.ver_major = header.ver_major
        self.ver_minor = header.ver_minor

        sect_size = (1 << header.sect_shift)
        self.sect_size = sect_size

        self.mini_sect_size = (1 << header.mini_sect_shift)
        self.mini_stream_cutoff = header.mini_stream_cutoff
        self.di_fat = di_fat
        self.fat = fat
        self.mini_fat = mini_fat
        self.cfb_stream = stream
        stream_len = stream.size

        entries_per_sect = sect_size // 4
        max_sect = stream_len // sect_size

        # First thing is build the FAT.  To do this we need to build (and
        # parse) the double indirect FAT.

        # Gather all of the double indirect FAT entries into di_fat
        di_fat.extend(header.di_fat)
        if header.di_fat_sect_count and (header.di_fat_sect_offset < max_sect):
            di_fat_entries = di_fat_entry * entries_per_sect
            next_sect = header.di_fat_sect_offset

            while (next_sect <= MAX_REG_SECT) and (next_sect < max_sect):
                offset = (next_sect + 1) * sect_size
                stream.seek(offset, SEEK_SET)

                values = \
                    di_fat_entries.from_buffer_copy(stream.read(sect_size))
                di_fat.extend(values[:-1])  # Don't include next_sect in di_fat

                next_sect = values[-1]
            # end while
        # end if

        # Create a list of sector runs for the FAT (from di_fat)
        runs = list()
        start = byte_offset(di_fat[0])
        prev_entry = di_fat[0]
        count = 1

        for entry in di_fat[1:]:
            if (entry == FAT_EOC) or (entry == FAT_UNALLOC):
                break
            # end if

            if (entry - prev_entry) == 1:
                count += 1
            else:
                runs.append((start, count * sect_size))
                start = byte_offset(entry)
                count = 1
            # end if

            prev_entry = entry
        # end for

        runs.append((start, count * sect_size))

        # Create a composite stream of the FAT (so we can parse it)
        segments = [(stream, run[0], run[1]) for run in runs]
        fat_stream = CompositeIStream(segments)

        # Extract the entries of the FAT
        sect_count = fat_stream.size // sect_size
        fat_entries = fat_entry * entries_per_sect

        for sect_index in range(sect_count):
            fat_stream.seek(sect_index * sect_size, SEEK_SET)
            values = fat_entries.from_buffer_copy(fat_stream.read(sect_size))
            fat.extend(values)
        # end for


        # Create the mini fat
        if header.mini_fat_sect_count != 0:
            # First we need the sector chain
            mini_fat_chain = self.get_fat_chain(header.mini_fat_sect_offset)

            if len(mini_fat_chain) == 1:
                start = byte_offset(header.mini_fat_sect_offset)
                mini_fat_stream = SubsetIStream(stream, start, sect_size)
            else:
                # Create a list of sector runs from the mini fat chain
                runs = list()
                start = byte_offset(mini_fat_chain[0])
                prev_entry = mini_fat_chain[0]
                count = 1

                for entry in mini_fat_chain[1:]:
                    if (entry - prev_entry) == 1:
                        count += 1
                    else:
                        runs.append((start, count * sect_size))
                        start = byte_offset(entry)
                        count = 1
                    # end if

                    prev_entry = entry
                else:
                    runs.append((start, count * sect_size))
                # end for

                # Create a stream of the contents of the mini fat
                segments = [(stream, run[0], run[1]) for run in runs]
                mini_fat_stream = CompositeIStream(segments)
            # end if

            # Extract the contents of the mini fat from the mini fat stream
            sect_count = mini_fat_stream.size // sect_size
            mini_fat_entries = mini_fat_entry * entries_per_sect

            for sect_index in range(sect_count):
                mini_fat_stream.seek(sect_index * sect_size, SEEK_SET)
                data = mini_fat_stream.read(sect_size)
                values = mini_fat_entries.from_buffer_copy(data)
                mini_fat.extend(values)
            # end for
        # end if


        # Create the directory stream.  First we need the sector chain.
        dir_chain = self.get_fat_chain(header.dir_sect_offset)

        # Create a list of sector runs from the directory chain
        runs = list()
        start = byte_offset(dir_chain[0])
        count = 1

        for entry in dir_chain[1:]:
            if (entry - prev_entry) == 1:
                count += 1
            else:
                runs.append((start, count * sect_size))
                start = byte_offset(entry)
                count = 1
            # end if

            prev_entry = entry
        else:
            runs.append((start, count * sect_size))
        # end for

        # Create the dir_stream attribute
        segments = [(stream, run[0], run[1]) for run in runs]
        dir_stream = CompositeIStream(segments)
        self.dir_stream = dir_stream


        # Create the root directory
        max_dir_entry = dir_stream.size // 128

        if max_dir_entry > STREAM_ID_MAX:
            max_dir_entry = STREAM_ID_MAX
        # end if

        # Create the dir_entries attribute by traversing the rb-tree
        dir_entries = dict()
        for sid in range(max_dir_entry):
            dir_entries[sid] = DirEntry.from_stream(dir_stream, sid * 128)
        # end for

        self.root_dir_entry = dir_entries[0]
        self.dir_entries = dir_entries


        # Create the mini stream
        if header.mini_fat_sect_count:
            self.mini_stream = self.get_stream(0, slack=True)
        else:
            self.mini_stream = ByteIStream(b"")
        # end if
    # end def __init__

    def byte_offset(self, sect_num):
        """Calculates the byte offset of a sector number.

        :type sect_num: ``int``
        :param sect_num: The sector number.

        :rtype: ``int``
        :returns: The byte offset in the file of the sector.

        """
        return (sect_num + 1) * self.sect_size
    # end def byte_offset

    def mini_byte_offset(self, mini_sect_num):
        """Calculates the byte offset of a mini sector number.

        :type mini_sect_num: ``int``
        :param mini_sect_num: The mini sector number.

        :rtype: ``int``
        :returns: The byte offset in the mini stream of the mini sector number.

        """
        return mini_sect_num * self.mini_sect_size
    # end def mini_byte_offset

    def get_fat_chain(self, first_sect):
        """Retrieves a chain from the FAT.

        :type first_sect: ``int``
        :param first_sect: The sector number of the first sector in the chain.

        :raises IndexError: If :attr:`first_sect` is beyond the size of the
                            file.

        :rtype: list
        :returns: The sector chain from the FAT.

        """
        fat = self.fat
        fat_len = len(fat)

        if first_sect >= fat_len:
            raise IndexError("sector {0} out of range".format(first_sect))
        # end if

        chain = [first_sect]
        entry = fat[first_sect]

        while (entry < fat_len) and (entry not in \
         (FAT_EOC, FAT_UNALLOC, FAT_FAT_SECT, FAT_DIF_SECT)):

            chain.append(entry)
            entry = fat[entry]
        # end while

        return chain
    # end def get_fat_chain

    def get_mini_fat_chain(self, first_mini_sect):
        """Retrieves a chain from the mini FAT.

        :type first_mini_sect: ``int``
        :param first_mini_sect: The sector number of the first sector in the
                                chain.

        :raises IndexError: If :attr:`first_mini_sect` is beyond the size of
                            the mini FAT.

        :rtype: list
        :returns: The sector chain from the mini FAT.

        """
        mini_fat = self.mini_fat
        mini_fat_len = len(mini_fat)

        if first_mini_sect >= mini_fat_len:
            err_msg = "sector {0} out of range".format(first_mini_sect)
            raise IndexError(err_msg)
        # end if

        chain = [first_mini_sect]
        entry = mini_fat[first_mini_sect]

        while (entry < mini_fat_len) and (entry not in \
         (FAT_EOC, FAT_UNALLOC, FAT_FAT_SECT, FAT_DIF_SECT)):

            chain.append(entry)
            entry = mini_fat[entry]
        # end while

        return chain
    # end def get_mini_fat_chain

    def get_dir_entry(self, sid):
        """Retrieves a directory entry

        :type sid: ``int``
        :param sid: The stream identifier of the directory entry.

        :raises IndexError: If :attr:`sid` is out of range.

        :rtype: :class:`DirEntry`
        :returns: The directory entry.

        """
        if sid >= (self.dir_stream.size // 128):
            raise IndexError("stream {0} out of range".format(sid))
        # end if

        return DirEntry.from_stream(self.dir_stream, sid * 128)
    # end def get_dir_entry

    @classmethod
    def is_valid_dir_entry(cls, entry):
        """Determines if a :class:`DirEntry` object is valid.

        If :attr:`entry` matches any of the following tests, it is
        considered invalid:

            * if :attr:`entry.name` is empty
            * if :attr:`entry.name` contains invalid characters
            * if :attr:`entry.type` is not 0x0, 0x1, 0x2, or 0x5
            * if :attr:`entry.color` is not 0x0 or 0x1
            * if :attr:`entry.left_sid`, :attr:`entry.right_sid`, or
              :attr:`entry.child_sid` is not between :const:`STREAM_ID_MIN`
              and :const:`STREAM_ID_MAX`, and is not :const:`STREAM_ID_NONE`

        :type entry: :class:`DirEntry`
        :param entry: The :class:`DirEntry` object to examine

        :rtype: ``bool``
        :returns: ``True`` if :attr:`entry` is a valid directory entry.

        """
        if not entry.name:
            return False
        elif _invalid_name_chars.intersection(entry.name):
            return False
        elif entry.type not in (0, 1, 2, 5):
            return False
        elif entry.color not in (0, 1):
            return False
        # end if

        for sid in (entry.left_sid, entry.right_sid, entry.child_sid):
            if (sid > STREAM_ID_MAX) and (sid != STREAM_ID_NONE):
                return False
            # end if
        # end for

        return True
    # end def is_valid_dir_entry

    def get_stream(self, sid, slack=False):
        """Retrieves the contents of a stream.

        :type sid: ``int``
        :param sid: The stream identifier for the directory entry associated
                    with the stream.

        :type slack: ``bool``
        :param slack: If ``True``, the contents of the entire stream are
                      returned.  Otherwise the stream is truncated at the size
                      specified by the associated directory entry.

        :raises IndexError: If :attr:`sid` is out of range.

        :rtype: :class:`lf.dec.IStream`
        :returns: An :class:`lf.dec.IStream` covering the contents of the
                  stream.

        """
        dir_entry = self.get_dir_entry(sid)

        if sid == 0:
            try:
                chain = self.get_fat_chain(dir_entry.stream_sect_offset)
            except IndexError:
                return ByteIStream(b"")
            # end try

            byte_offset = self.byte_offset
            sect_size = self.sect_size
            stream = self.cfb_stream
        elif dir_entry.stream_size < self.mini_stream_cutoff:
            try:
                chain = self.get_mini_fat_chain(dir_entry.stream_sect_offset)
            except IndexError:
                return ByteIStream(b"")
            # end try

            byte_offset = self.mini_byte_offset
            sect_size = self.mini_sect_size
            stream = self.mini_stream
        else:
            try:
                chain = self.get_fat_chain(dir_entry.stream_sect_offset)
            except IndexError:
                return ByteIStream(b"")
            # end try

            byte_offset = self.byte_offset
            sect_size = self.sect_size
            stream = self.cfb_stream
        # end if

        if len(chain) == 1:
            start = byte_offset(chain[0])
            if not slack:
                return SubsetIStream(stream, start, dir_entry.stream_size)
            else:
                return SubsetIStream(stream, start, sect_size)
        # end if

        runs = list()
        start = byte_offset(chain[0])
        prev_entry = chain[0]
        count = 1

        for entry in chain[1:]:
            if (entry - prev_entry) == 1:
                count += 1
            else:
                runs.append((start, count * sect_size))
                start = byte_offset(entry)
                count = 1
            # end if

            prev_entry = entry
        else:
            runs.append((start, count * sect_size))
        # end for

        segments = [(stream, run[0], run[1]) for run in runs]

        if slack:
            return CompositeIStream(segments)
        # end if

        stream_size = dir_entry.stream_size
        if self.ver_major == 0x3:
            stream_size = dir_entry.stream_size & 0x00000000FFFFFFFF
        # end if

        return SubsetIStream(CompositeIStream(segments), 0, stream_size)
    # end def get_stream
# end class CompoundFile

class Header(ActiveStructuple):
    """Represents the header from a compound file binary.

    .. attribute:: sig

        The signature value.

    .. attribute:: clsid

        The class ID value.

    .. attribute:: ver_minor

        The minor version number.

    .. attribute:: ver_major

        The major version number.

    .. attribute:: byte_order

        The byte order mark value.

    .. attribute:: sect_shift

        The size of a sector, as a power of 2.

    .. attribute:: mini_sect_shift

        The size of a sector in the mini stream, as a power of 2.

    .. attribute:: rsvd

        The reserved value.

    .. attribute:: dir_sect_count

        The number of sectors that contain directory entries.

    .. attribute:: fat_sect_count

        The number of sectors that contain FAT entries.

    .. attribute:: dir_sect_offset

        The sector offset of the first directory entry.

    .. attribute:: trans_num

        The transaction signature number.

    .. attribute:: mini_stream_cutoff

        The maximum size of a user-defined data stream that can be allocated in
        the mini FAT.

    .. attribute:: mini_fat_sect_offset

        The sector offset of the first mini FAT entry.

    .. attribute:: mini_fat_sect_count

        The number of sectors in the mini FAT.

    .. attribute:: di_fat_sect_offset

        The sector offset of the first DIFAT entry (beyond the header).

    .. attribute:: di_fat_sect_count

        The number of sectors in the DIFAT.

    .. attribute:: di_fat

        The first 109 DIFAT entries.
    """

    _fields_ = (
        "sig", "clsid", "ver_minor", "ver_major", "byte_order", "sect_shift",
        "mini_sect_shift", "rsvd", "dir_sect_count", "fat_sect_count",
        "dir_sect_offset", "trans_num", "mini_stream_cutoff",
        "mini_fat_sect_offset", "mini_fat_sect_count", "di_fat_sect_offset",
        "di_fat_sect_count", "di_fat"
    )
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`Header` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the compound file header.

        :type offset: ``int``
        :param offset: The start of the header in :attr:`stream`.

        :rtype: :class:`Header`
        :returns: The corresponding :class:`Header` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        head = header.from_buffer_copy(stream.read(512))

        clsid = head.clsid
        clsid = CLSIDToUUID.from_ctype(clsid)

        return Header((
            bytes(head.sig), clsid, head.ver_minor, head.ver_major,
            head.byte_order, head.sect_shift, head.mini_sect_shift,
            bytes(head.rsvd), head.dir_sect_count, head.fat_sect_count,
            head.dir_sect_offset, head.trans_num, head.mini_stream_cutoff,
            head.mini_fat_sect_offset, head.mini_fat_sect_count,
            head.di_fat_sect_offset, head.di_fat_sect_count, list(head.di_fat)
        ))
    # end def from_stream
# end class Header

class DirEntry(ActiveStructuple):
    """Represents a directory entry in a compound file.

    .. attribute:: name

        The name of the directory entry.

    .. attribute:: name_size

        The length of the name field (in bytes).

    .. attribute:: type

        The type of directory entry.

    .. attribute:: color

        The color of the directory entry.

    .. attribute:: left_sid

        The stream identifier of the left sibling directory entry.

    .. attribute:: right_sid

        The stream identifier of the right sibling directory entry.

    .. attribute:: child_sid

        The stream identifier of the child directory entry.

    .. attribute:: clsid

        The CLSID of the directory entry.

    .. attribute:: state

        The user defined state bits.

    .. attribute:: btime

        The creation time of the directory entry.

    .. attribute:: mtime

        The last modification time of the directory entry.

    .. attribute:: stream_sect_offset

        The first sector of the stream.

    .. attribute:: stream_size

        The size in bytes of the stream.

        .. note::

            Per the spec. if ver_major is 0x3, the high 4 bytes of this value
            may be invalid, and must be ignored.  This is a responsibility of
            the calling function.
    """

    _fields_ = (
        "name", "name_size", "type", "color", "left_sid", "right_sid",
        "child_sid", "clsid", "state", "btime", "mtime", "stream_sect_offset",
        "stream_size"
    )
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`DirEntry` object from a stream.

        :type stream: :class:`lf.dec.IStream`
        :param stream: A stream that contains the directory entry.

        :type offset: ``int``
        :param offset: The start of the directory entry in :attr:`stream`.

        :rtype: :class:`DirEntry`
        :returns: The corresponding :class:`DirEntry` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        values = dir_entry.from_buffer_copy(stream.read(128))

        name = bytes(values.name)
        if values.name_size <= 64:
            name = name[:values.name_size]
        # end if

        new_name = name.decode("utf_16_le", "ignore")
        if new_name:
            name = new_name.split("\x00", 1)[0]
        # end if

        clsid = CLSIDToUUID.from_ctype(values.clsid)

        btime = values.btime
        try:
            btime = FILETIMETodatetime.from_ctype(btime)
        except (ValueError, TypeError):
            btime = (btime.hi << 32) | btime.lo
        # end try

        mtime = values.mtime
        try:
            mtime = FILETIMETodatetime.from_ctype(mtime)
        except (ValueError, TypeError):
            mtime = (mtime.hi << 32) | mtime.lo
        # end try

        return DirEntry((
            name, values.name_size, values.type, values.color, values.left_sid,
            values.right_sid, values.child_sid, clsid, values.state, btime,
            mtime, values.stream_sect_offset, values.stream_size
        ))
    # end def from_stream
# end class DirEntry
