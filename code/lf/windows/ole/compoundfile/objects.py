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
Objects for Microsoft OLE structured storage files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "CompoundFile", "DirEntry"
]

from datetime import datetime

from lf.windows.guid import guid_to_uuid
from lf.windows.time import filetime_to_datetime
from lf.io import composite, byte, subset
from lf.io.consts import SEEK_SET
from lf.struct.extract import extractor_factory as factory

from lf.windows.ole.compoundfile.consts import (
    STREAM_ID_MAX, STREAM_ID_NONE, FAT_EOC, FAT_UNALLOC, FAT_FAT_SECT,
    FAT_DIF_SECT
)

from lf.windows.ole.compoundfile.structs import (
    FATEntry, MiniFATEntry, DIFATEntry
)

from lf.windows.ole.compoundfile.extractors import header, dir_entry

class CompoundFile():
    """
    An OLE structured storage file (compound file binary).

    .. attribute:: clsid

        The clsid of the file.

    .. attribute:: ver_minor

        The minor version number.

    .. attribute:: ver_major

        The major version number.

    .. attribute:: sect_size

        The number of bytes in a sector.

    .. attribute:: mini_sect_size

        The number of bytes in a mini sector.

    .. attribute:: trans_num

        The transaction number of the file.

    .. attribute:: mini_stream_cutoff

        The maximum size of a file (in bytes) in the mini stream.

    .. attribute:: fat

        A list of entries from the FAT.

    .. attribute:: mini_fat

        A list of entries from the mini FAT.

    .. attribute:: mini_stream

        A stream covering the contents of the mini stream.

    .. attribute:: dir_stream

        A stream covering the contents of the directory stream.

    .. attribute:: root_dir_entry

        A DirEntry object for the root directory entry.

    .. attribute:: cfb_stream

        A stream covering the contents of the file.

    .. attribute:: dir_entries

        A dictionary of directory entries.  The keys are the numeric position
        of the entry.
    """

    def __init__(self, cfb_stream, offset=None):
        """
        Initializes a CompoundFile object.

        :parameters:
            cfb_stream
                An IStream covering the contents of the file.

            offset
                The start of the compound file, in the stream.
        """

        byte_offset = self.byte_offset
        fat = list()
        mini_fat = list()
        di_fat = list()

        if offset is not None:
            cfb_stream.seek(offset, SEEK_SET)
        else:
            offset = cfb_stream.tell()
        # end if

        header_struct = header.extract(cfb_stream.read(512))

        sect_size = (1 << header_struct.sect_shift)
        self.sect_size = sect_size
        self.mini_sect_size = (1 << header_struct.mini_sect_shift)
        self.trans_num = header_struct.trans_num
        self.mini_stream_cutoff = header_struct.mini_stream_cutoff
        self.fat = fat
        self.mini_fat = mini_fat
        self.cfb_stream = cfb_stream

        guid = header_struct.clsid
        self.clsid = \
         guid_to_uuid(guid.data1, guid.data2, guid.data3, guid.data4)

        self.ver_major = header_struct.ver_major
        self.ver_minor = header_struct.ver_minor

        entries_per_sect = sect_size // 4

        # First thing is build the FAT.  To do this we need to build (and
        # parse) the double indirect FAT.

        # Gather all of the double indirect FAT entries into di_fat
        di_fat.extend(header_struct.di_fat)
        if header_struct.di_fat_count != 0:
            extractor = factory.make_list(entries_per_sect, DIFATEntry())
            next_di_fat_sect = header_struct.di_fat_sect

            while next_di_fat_sect != FAT_EOC:
                cfb_stream.seek(byte_offset(next_di_fat_sect), SEEK_SET)
                data = cfb_stream.read(sect_size)
                values = extractor.extract(data, flatten=True)
                di_fat.extend(values)
                next_di_fat_sect = di_fat.pop()
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
        segments = [(cfb_stream, run[0], run[1]) for run in runs]
        fat_stream = composite.open(segments)

        # Extract the entries of the FAT
        sect_count = fat_stream.size // sect_size
        extractor = factory.make_list(entries_per_sect, FATEntry())

        for sect_index in range(sect_count):
            fat_stream.seek(sect_index * sect_size, SEEK_SET)
            values = extractor.extract(fat_stream.read(sect_size), flatten=True)
            fat.extend(values)
        # end for


        # Create the mini fat
        if header_struct.mini_fat_count != 0:
            # First we need the sector chain
            mini_fat_chain = self.get_fat_chain(header_struct.mini_fat_sect)

            if len(mini_fat_chain) == 1:
                start = byte_offset(header_struct.mini_fat_sect)
                mini_fat_stream = subset.open(cfb_stream, start, sect_size)
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
                segments = [(cfb_stream, run[0], run[1]) for run in runs]
                mini_fat_stream = composite.open(segments)
            # end if

            # Extract the contents of the mini fat from the mini fat stream
            sect_count = mini_fat_stream.size // sect_size
            extractor = factory.make_list(entries_per_sect, MiniFATEntry())

            for sect_index in range(sect_count):
                mini_fat_stream.seek(sect_index * sect_size, SEEK_SET)
                data = mini_fat_stream.read(sect_size)
                values = extractor.extract(data, flatten=True)
                mini_fat.extend(values)
            # end for
        # end if


        # Create the directory stream.  First we need the sector chain.
        dir_chain = self.get_fat_chain(header_struct.dir_sect)

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
        segments = [(cfb_stream, run[0], run[1]) for run in runs]
        dir_stream = composite.open(segments)
        self.dir_stream = dir_stream


        # Create the root directory
        max_dir_entry = dir_stream.size // 128

        if max_dir_entry > STREAM_ID_MAX:
            max_dir_entry = STREAM_ID_MAX
        # end if

        # Create the dir_entries attribute by traversing the rb-tree
        dir_entries = dict()

        # List of stream id's we've already visited
        visited = [STREAM_ID_NONE]

        # Stack of stream id's
        sid_stack = [0]

        while sid_stack:
            sid = sid_stack.pop()

            if (sid in visited) or (sid > max_dir_entry):
                continue
            # end if

            dir_stream.seek(sid * 128, SEEK_SET)
            de = DirEntry(sid, dir_stream.read(128))

            dir_entries[sid] = de
            visited.append(sid)

            for sid in (de.left_sid, de.right_sid, de.child_sid):
                if (sid in visited) or (sid > max_dir_entry):
                    continue
                else:
                    sid_stack.append(sid)
                # end if
            # end for
        # end while

        self.root_dir_entry = dir_entries[0]
        self.dir_entries = dir_entries


        # Create the mini stream
        if header_struct.mini_fat_count != 0:
            self.mini_stream = self.get_stream(0)
        else:
            self.mini_stream = byte.open(b"")
        # end if
    # end def __init__

    def byte_offset(self, sect_num):
        """
        Calculates the byte offset of a sector number.

        :parameters:
            sect_num
                The sector number to calculate the byte offset for.

        :rtype: int
        :returns: The byte offset (in the file) of the sector number.
        """

        return (sect_num + 1) * self.sect_size
    # end def byte_offset

    def mini_byte_offset(self, mini_sect_num):
        """
        Calculates the byte offset of a mini sector number.

        :parameters:
            mini_sect_num
                The mini sector number to calculate the byte offset for.

        :rtype: int
        :returns: The byte offset (in the mini stream) of the sector number.
        """

        return mini_sect_num * self.mini_sect_size
    # end def mini_byte_offset

    def get_fat_chain(self, first_sect):
        """
        Gets a chain from the FAT.

        :parameters:
            first_sect
                The sector number of the first sector in the chain.

        :raises:
            IndexError
                If first_sect is beyond the size of the file

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
        """
        Gets a chain from the mini FAT.

        :parameters:
            first_mini_sect
                The sector number of the first sector in the chain.

        :raises:
            IndexError
                If first_mini_sect is beyond the size of the mini FAT.

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

    def get_dir_entry(self, stream_id):
        """
        Retrieves a directory entry.

        :parameters:
            stream_id
                The stream identifier of the directory entry.

        :raises:
            IndexError
                If stream_id is out of range.

        :rtype: DirEntry
        :returns: The directory entry.
        """

        if stream_id >= (self.dir_stream.size // 128):
            raise IndexError("stream {0} out of range".format(stream_id))
        # end if

        self.dir_stream.seek(stream_id * 128, SEEK_SET)
        return DirEntry(stream_id, self.dir_stream.read(128))
    # end def get_dir_entry

    def get_stream(self, stream_id, ignore_size=False):
        """
        Retrieves the contents of a stream.

        :parameters:
            stream_id
                The stream identifier of the stream.

            ignore_size
                If true, returns the contents of the entire chain (not just
                up to size bytes).

        :raises:
            IndexError
                If stream_id is out of range.

        :rtype: IStream
        :returns: An IStream covering the contents of the stream.
        """

        dir_entry = self.get_dir_entry(stream_id)

        if stream_id == 0:
            try:
                chain = self.get_fat_chain(dir_entry.first_sect)
            except IndexError:
                return byte.open(b"")
            # end try

            byte_offset = self.byte_offset
            sect_size = self.sect_size
            data_stream = self.cfb_stream
        elif dir_entry.size < self.mini_stream_cutoff:
            try:
                chain = self.get_mini_fat_chain(dir_entry.first_sect)
            except IndexError:
                return byte.open(b"")
            # end try

            byte_offset = self.mini_byte_offset
            sect_size = self.mini_sect_size
            data_stream = self.mini_stream
        else:
            try:
                chain = self.get_fat_chain(dir_entry.first_sect)
            except IndexError:
                return byte.open(b"")
            # end try

            byte_offset = self.byte_offset
            sect_size = self.sect_size
            data_stream = self.cfb_stream
        # end if

        if len(chain) == 1:
            start = byte_offset(chain[0])
            return subset.open(data_stream, start, dir_entry.size)
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

        segments = [(data_stream, run[0], run[1]) for run in runs]

        if ignore_size:
            return composite.open(segments)
        # end if

        return subset.open(composite.open(segments), 0, dir_entry.size)
    # end def get_stream
# end class CompoundFile

class DirEntry():
    """
    A directory entry in a CompoundFile.

    .. attribute:: sid

        The stream identifier for the directory entry.

    .. attribute:: name

        The name of the directory entry.

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

    .. attribute:: first_sect

        The first sector of the stream.

    .. attribute:: size

        The size in bytes of the stream.
    """

    def __init__(self, sid, bytestr):
        """
        Initializes a DirEntry object.

        :parameters:
            sid
                The stream identifier for the directory entry.

            bytestr
                A bytes object covering the contents of the directory entry.
        """

        self.sid = sid
        dir_entry_struct = dir_entry.extract(bytestr)

        name = dir_entry_struct.name[:dir_entry_struct.name_size]
        name = name.decode("utf_16_le").rstrip("\x00")

        self.name = name
        self.type = dir_entry_struct.type
        self.color = dir_entry_struct.color
        self.left_sid = dir_entry_struct.left_sid
        self.right_sid = dir_entry_struct.right_sid
        self.child_sid = dir_entry_struct.child_sid

        guid = dir_entry_struct.clsid
        self.clsid = \
         guid_to_uuid(guid.data1, guid.data2, guid.data3, guid.data4)

        self.state = dir_entry_struct.state
        self.first_sect = dir_entry_struct.first_sect
        self.size = dir_entry_struct.size

        btime = dir_entry_struct.btime
        btime = (btime.hi << 32) | btime.lo
        try:
            btime = filetime_to_datetime(btime)
        except KeyboardInterrupt:
            raise
        except:
            btime = None
        # end try
        self.btime = btime

        mtime = dir_entry_struct.mtime
        mtime = (mtime.hi << 32) | mtime.lo
        try:
            mtime = filetime_to_datetime(mtime)
        except KeyboardInterrupt:
            raise
        except:
            mtime = None
        # end try
        self.mtime = mtime
    # end def __init__
# end class DirEntry
