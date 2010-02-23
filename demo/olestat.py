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

"""Tool to demonstrate some of the capabilities in lf.win.ole.cfb"""

# stdlib imports
import sys
from datetime import datetime
from optparse import OptionParser

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.ole.cfb import CompoundFile
from lf.win.ole.cfb.consts import (
    STGTY_STORAGE, STGTY_ROOT, STGTY_STREAM, STGTY_INVALID, STGTY_LOCKBYTES,
    STGTY_PROPERTY,

    BYTE_ORDER_LITTLE_ENDIAN, STREAM_ID_NONE,

    FAT_EOC, FAT_UNALLOC, FAT_FAT_SECT, FAT_DIF_SECT, DE_RED, DE_BLACK
)

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)

STGTY_NAMES = {
    STGTY_INVALID: "Invalid / Unknown (0x0)",
    STGTY_STORAGE: "STGTY_STORAGE (0x1)",
    STGTY_STREAM: "STGTY_STREAM (0x2)",
    STGTY_LOCKBYTES: "STGTY_LOCKBYTES (0x3)",
    STGTY_PROPERTY: "STGTY_PROPERTY (0x4)",
    STGTY_ROOT: "STGTY_ROOT (0x5)"
}

__docformat__ = "restructuredtext en"
__all__ = [
    "main", "format_entry", "format_header", "format_di_fat", "format_fat",
    "format_mini_fat", "VER_MAJOR", "VER_MINOR", "format_timestamp"
]

def format_timestamp(timestamp):
    """Formats a DirEntry's timestamp"""

    if isinstance(timestamp, datetime):
        new_timestamp = timestamp.isoformat(" ")
    else:
        new_timestamp = timestamp
    # end try

    return new_timestamp
# end def format_timestamp

def format_entry(cfb, sid):
    """Outputs a directory entry, given a sid"""

    output = list()
    entry = cfb.dir_entries[sid]

    if entry.type in STGTY_NAMES:
        type_str = STGTY_NAMES[entry.type]
    else:
        type_str = "Unknown (0x{0:X})".format(entry.type)
    # end if

    if entry.color == DE_RED:
        color_str = "Red (0x0)"
    elif entry.color == DE_BLACK:
        color_str = "Black (0x1)"
    else:
        color_str = "Unknown (0x{0:X})".format(entry.color)
    # end if

    if entry.left_sid == STREAM_ID_NONE:
        left_sid_str = "STREAM_ID_NONE (0xFFFFFFFF)"
    else:
        left_sid_str = "{0}".format(entry.left_sid)
    # end if

    if entry.right_sid == STREAM_ID_NONE:
        right_sid_str = "STREAM_ID_NONE (0xFFFFFFFF)"
    else:
        right_sid_str = "{0}".format(entry.right_sid)
    # end if

    if entry.child_sid == STREAM_ID_NONE:
        child_sid_str = "STREAM_ID_NONE (0xFFFFFFFF)"
    else:
        child_sid_str = "{0}".format(entry.child_sid)
    # end if

    btime = format_timestamp(entry.btime)
    mtime = format_timestamp(entry.mtime)

    stream_size = entry.stream_size
    if stream_size < cfb.mini_stream_cutoff:
        sector_type_str = "Mini stream sector(s)"
        chain = cfb.get_mini_fat_chain(entry.stream_sect_offset)
    else:
        sector_type_str = "Normal sector(s)"
        chain = cfb.get_fat_chain(entry.stream_sect_offset)
    # end if

    # Generate chain output in columns of 8
    chain_output = list()
    sect_count = len(chain)
    row_count = sect_count // 8
    for row_counter in range(row_count):
        row_start = row_counter * 8

        chain_output.append("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(
            *chain[row_start:row_start+8]
        ))
    else:
        leftover_count = sect_count % 8
        leftover_output = list()

        for counter in range(leftover_count):
            index = (row_count * 8) + counter
            leftover_output.append("{0}".format(chain[index]))
        # end for

        leftover_output = ", ".join(leftover_output)
        chain_output.append(leftover_output)
    # end for

    name = repr(entry.name)[1:-1]


    output.append("Stream id: {0}".format(sid))
    output.append("Name size: {0}".format(entry.name_size))
    output.append("Name: {0}".format(name))
    output.append("Type: {0}".format(type_str))
    output.append("Color: {0}".format(color_str))
    output.append("Left stream id: {0}".format(left_sid_str))
    output.append("Right stream id: {0}".format(right_sid_str))
    output.append("Child stream id: {0}".format(child_sid_str))
    output.append("CLSID: {0}".format(entry.clsid))
    output.append("State: 0x{0:X}".format(entry.state))
    output.append("Size: {0}".format(entry.stream_size))
    output.append("")
    output.append("Timestamps:")
    output.append("Stream creation time: {0}".format(btime))
    output.append("Stream modification time: {0}".format(mtime))
    output.append("")
    output.append("{0}:".format(sector_type_str))
    output.extend(chain_output)

    return output
# end def format_entry

def format_header(cfb):
    """Outputs the header"""

    output = list()
    header = cfb.header

    output.append("Signature: {0}".format(header.sig))
    output.append("CLSID: {0}".format(header.clsid))
    output.append("Major version: {0}".format(cfb.ver_major))
    output.append("Minor version: {0}".format(cfb.ver_minor))
    output.append("Transaction signature #: {0}".format(header.trans_num))
    output.append("Byte order: 0x{0:X}".format(header.byte_order))
    output.append("Sector size: {0} bytes".format(cfb.sect_size))
    output.append("Mini sector size: {0} bytes".format(cfb.mini_sect_size))
    output.append("Mini stream cutoff: {0} bytes".format(
        cfb.mini_stream_cutoff
    ))
    output.append("Number of dir. sectors: {0}".format(header.dir_sect_count))
    output.append("Dir. sector offset: {0}".format(header.dir_sect_offset))
    output.append("Reserved value: {0}".format(header.rsvd))
    output.append("")

    output.append("FATs:")
    output.append("DI FAT sector offset: {0}".format(header.di_fat_sect_offset))
    output.append("Number of DI FAT sectors: {0}".format(
        header.di_fat_sect_count
    ))
    output.append("Number of FAT sectors: {0}".format(header.fat_sect_count))
    output.append("Mini FAT sector offset: {0}".format(
        header.mini_fat_sect_offset
    ))
    output.append("Number of Mini FAT sectors: {0}".format(
        header.mini_fat_sect_count
    ))

    return output
# end def format_header

def format_di_fat(cfb):
    """Outputs the DI FAT"""

    output = list()

    output.append("Double Indirect FAT:")
    output.append("")

    for (index, value) in enumerate(cfb.di_fat):
        if value != FAT_UNALLOC:
            output.append("{0}: {1}".format(index, value))
        # end if
    # end for

    return output
# end def format_di_fat

def format_fat(cfb):
    """Outputs the FAT"""

    output = list()
    fat = cfb.fat
    seen = list()
    last_fat = len(fat)

    output.append("FAT:")
    output.append("")

    start_index = None
    current_index = 0
    next_index = 1

    while next_index < last_fat:
        current_value = fat[current_index]
        next_value = fat[next_index]

        if start_index is None:  # Starting a new run
            if current_value == FAT_EOC:
                output.append("{0}-{0} (1) -> EOC".format(current_index))
                current_index = next_index
                next_index += 1
                continue
            elif current_value == FAT_UNALLOC:
                current_index = next_index
                next_index += 1
                continue
            elif current_value == FAT_FAT_SECT:
                output.append("{0}: 0x{1:X} (FAT sector)".format(
                    current_index, current_value
                ))
                current_index = next_index
                next_index += 1
                continue
            elif current_value == FAT_DIF_SECT:
                output.append("{0}: 0x{1:X} (DIFAT sector)".format(
                    current_value
                ))
                current_index = next_index
                next_index += 1
                continue
            # end if

            start_index = current_index
        # end if

        if current_value == next_index:
            current_index = next_index
            next_index += 1
            continue
        # end if

        # If we get this far, it means we've reached the end of a run
        delta = current_index - start_index + 1
        if current_value == FAT_EOC:
            output.append("{0}-{1} ({2}) -> EOC".format(
                start_index, current_index, delta
            ))
        elif current_value == FAT_DIF_SECT:
            delta -= 1
            prev_index = current_index - 1
            output.append("{0}-{1} ({2}) -> {3}".format(
                start_index, prev_index, delta, fat[prev_index]
            ))

            output.append("{0}: 0x{1:X} (DIFAT sector".format(
                current_index, current_value
            ))
        elif current_value == FAT_FAT_SECT:
            delta -= 1
            prev_index = current_index - 1
            output.append("{0}-{1} ({2}) -> {3}".format(
                start_index, prev_index, delta, fat[prev_index]
            ))

            output.append("{0}: 0x{1:X} (FAT sector)".format(
                current_index, current_value
            ))
        else:
            output.append("{0}-{1} ({2}) -> {3}".format(
                start_index, current_index, delta, current_value
            ))
        # end if

        start_index = None
        current_index = next_index
        next_index += 1
    else:
        current_value = fat[current_index]

        if start_index is None:
            if current_value == FAT_FAT_SECT:
                output.append("{0}: 0x{1:X} (FAT sector)".format(
                    current_value
                ))
            elif current_value == FAT_DIF_SECT:
                output.append("{0}: 0x{1:X} (DIFAT sector)".format(
                    current_value
                ))
            elif current_value == FAT_EOC:
                output.append("{0}-{0} (1) -> EOC".format(current_index))
            # end if
        else:
            delta = current_index - start_index + 1
            if current_value == FAT_EOC:
                output.append("{0}-{1} ({2}) -> EOC".format(
                    start_index, current_index, delta
                ))
            elif current_value == FAT_FAT_SECT:
                prev_index = current_index - 1
                delta -= 1

                output.append("{0}-{1} ({2}) -> {3}".format(
                    start_index, prev_index, delta, current_index
                ))

                output.append("{0}-{0} (1) -> 0x{1:X} (FAT sector)".format(
                    start_index, current_value
                ))
            elif current_value == FAT_DIF_SECT:
                prev_index = current_index - 1
                delta -= 1

                output.append("{0}-{1} ({2}) -> {3}".format(
                    start_index, prev_index, delta, current_index
                ))

                output.append("{0}-{0} (1) -> 0x{1:X} (DIFAT sector)".format(
                    start_index, current_value
                ))
            else:
                output.append("{0}-{1} ({2}) -> {3}".format(
                    start_index, current_index, delta, current_value
                ))
            # end if
        # end if
    # end while

    return output
# end def format_fat

def format_mini_fat(cfb):
    """Outputs the Mini FAT"""

    output = list()
    fat = cfb.mini_fat
    seen = list()
    last_fat = len(fat)

    output.append("Mini FAT:")
    output.append("")

    start_index = None
    current_index = 0
    next_index = 1

    while next_index < last_fat:
        current_value = fat[current_index]
        next_value = fat[next_index]

        if start_index is None:  # Starting a new run
            if current_value == FAT_EOC:
                output.append("{0}-{0} (1) -> EOC".format(current_index))
                current_index = next_index
                next_index += 1
                continue
            elif current_value == FAT_UNALLOC:
                current_index = next_index
                next_index += 1
                continue
            # end if

            start_index = current_index
        # end if

        if current_value == next_index:
            current_index = next_index
            next_index += 1
            continue
        # end if

        # If we get this far, it means we've reached the end of a run
        delta = current_index - start_index + 1
        if current_value == FAT_EOC:
            output.append("{0}-{1} ({2}) -> EOC".format(
                start_index, current_index, delta
            ))
        else:
            output.append("{0}-{1} ({2}) -> {3}".format(
                start_index, current_index, delta, current_value
            ))
        # end if

        start_index = None
        current_index = next_index
        next_index += 1
    else:
        current_value = fat[current_index]

        if start_index is None:
            if current_value == FAT_EOC:
                output.append("{0}-{0} (1) -> EOC".format(current_index))
            elif current_value != FAT_UNALLOC:
                output.append("{0}-{0} (1) -> {1}".format(
                    current_index, current_value
                ))
            # end if
        else:
            delta = current_index - start_index + 1
            if current_value == FAT_EOC:
                output.append("{0}-{1} ({2}) -> EOC".format(
                    start_index, current_index, delta
                ))
            else:
                output.append("{0}-{1} ({2}) -> {3}".format(
                    start_index, current_index, delta, current_value
                ))
            # end if
        # end if
    # end while

    return output
# end def mini_format_fat

def main():
    usage = "%prog olefile sid"
    description = "\n".join([
        "Displays statistics about entries in an OLE compound file.",
        "",
        "If file is '-' then stdin is read."
        ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("Must specify both a file and stream identifier")
    # end if

    if args[0] == "-":
        cfb = CompoundFile(ByteIStream(sys.stdin.buffer.read()))
    else:
        cfb = CompoundFile(RawIStream(args[0]))
    # end if

    sid = int(args[1])

    last_sid = len(cfb.dir_entries)
    header_sid = last_sid + 0
    difat_sid = last_sid + 1
    fat_sid = last_sid + 2
    mini_fat_sid = last_sid + 3

    if sid in cfb.dir_entries:
        entry = cfb.dir_entries[sid]
        if cfb.is_valid_dir_entry(entry):
            output = format_entry(cfb, sid)
        else:
            print("Invalid sid {0}".format(sid), file=sys.stderr)
            sys.exit(-2)
        # end if
    elif sid == header_sid:
        output = format_header(cfb)
    elif sid == difat_sid:
        output = format_di_fat(cfb)
    elif sid == fat_sid:
        output = format_fat(cfb)
    elif sid == mini_fat_sid:
        output = format_mini_fat(cfb)
    else:
        print("Invalid sid {0}".format(sid), file=sys.stderr)
        sys.exit(-3)
    # end if

    print ("\n".join(output))
# end def main()

if __name__ == "__main__":
    main()
# end if
