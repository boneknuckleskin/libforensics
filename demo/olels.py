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
import calendar
from collections import deque
from datetime import datetime
from optparse import OptionParser

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.ole.cfb import CompoundFile, DirEntry
from lf.win.ole.cfb.consts import (
    STGTY_STORAGE, STGTY_ROOT, STGTY_STREAM, STREAM_ID_NONE, STREAM_ID_MAX
)

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)
DEFAULT_START_SID = 0

__docformat__ = "restructuredtext en"
__all__ = [
    "enumerate_entries", "format_output", "main", "format_timestamp"
]

def format_timestamp(timestamp, options):
    """Formats a DirEntry's timestamp according to output format"""

    if options.mactime_filename:
        if isinstance(timestamp, datetime):
            new_timestamp = calendar.timegm(timestamp.timetuple())
            if new_timestamp < 0:
                new_timestamp = 0
            # end if
        else:
            try:
                new_timestamp = int(timestamp)
            except (ValueError, TypeError):
                new_timestamp = 0
            # end try
        # end if
    elif options.long_output:
        if isinstance(timestamp, datetime):
            new_timestamp = timestamp.isoformat(" ")
        else:
            new_timestamp = timestamp
        # end try
    else:
        new_timestamp = timestamp
    # end if

    return new_timestamp
# end def format_timestamp

def enumerate_entries(cfb, start_sid, options):
    """Enumerates directory entries, recursing as specified by options"""

    # Keeps track of all info needed to traverse the tree(s)
    # List of tuples of (parent_sid, parent_siblings, next_sids, siblings)
    stack_of_stacks = list()

    # To avoid looping
    seen_sids = [start_sid]

    dir_entries = cfb.dir_entries
    is_valid_dir_entry = cfb.is_valid_dir_entry

    if start_sid not in dir_entries:
        return [(start_sid, list())]
    # end if

    start_entry = dir_entries[start_sid]
    child_sid = start_entry.child_sid

    if (child_sid not in dir_entries) or (child_sid in seen_sids):
        return [(start_sid, list())]
    # end if

    stack_of_stacks.append((start_sid, [], [child_sid], []))
    while stack_of_stacks:
        (parent_sid, parent_sibs, sids, sibs) = stack_of_stacks.pop()

        while sids:
            sid = sids.pop()

            if (sid not in dir_entries) or (sid in seen_sids):
                continue
            # end if

            entry = dir_entries[sid]
            sids.append(entry.right_sid)
            sids.append(entry.left_sid)

            child_sid = entry.child_sid
            if (child_sid not in dir_entries) or (child_sid in seen_sids):
                # Don't need to process a subdirectory
                sibs.append((sid, []))
                seen_sids.append(sid)
            elif not options.recurse:
                # Valid subdirectory, but we aren't recursing...
                sibs.append((sid, []))
                seen_sids.append(sid)
            else:
                # We have a subdirectory so process it
                # First save our current position
                stack_of_stacks.append((parent_sid, parent_sibs, sids, sibs))

                # Create a new stack_of_stacks entry for the subdirectory
                stack_of_stacks.append((sid, sibs, [child_sid], []))

                # Restart outer while loop
                break
            # end if
        else:
            # When we've finished the inner while loop, it means we've finished
            # processing an entire directory (and any subdirectories)
            parent_sibs.append((parent_sid, sibs))
            seen_sids.append(parent_sid)
        # end while
    # end while

    return parent_sibs
# end def enumerate_entries

def format_output(cfb, entries, options, path=""):
    """Formats the output according to options"""

    output = list()
    dir_entries = cfb.dir_entries

    if options.mactime_filename:
        format_str = "|".join([
            "0",  # MD5
            "{path}{name}",  # Name (w/path)
            "{sid}",  # inode (sid)
            "{mode}",  # Mode (as a string)
            "0",  # UID
            "0",  # GID
            "{entry.stream_size}",  # Size
            "0",  # atime (n/a)
            "{mtime}",  # mtime
            "0",  # ctime (n/a)
            "{btime}"  # btime
        ])
    elif options.long_output:
        format_str = "\t".join([
            "{mode} {sid}:",
            "{path}{name}",
            "{mtime}",
            "{btime}",
            "{entry.stream_size}"
        ])
    else:
        format_str = "{mode} {sid} {path}{name}"
    # end if

    (root_sid, kid_sids) = entries[0]

    # Display the root entry for mactime output
    if (root_sid == 0) and options.mactime_filename:
        entry = dir_entries[0]

        output_line = False
        if options.only_dirs:
            output_line = True
        elif options.only_files:
            output_line = False
        else:
            output_line = True
        # end if

        name = repr(entry.name)[1:-1]

        if output_line:
            mtime = format_timestamp(entry.mtime, options)
            btime = format_timestamp(entry.btime, options)

            output_str = format_str.format(
                mode="d/d",
                sid=0,
                entry=entry,
                path="",
                name=name,
                mtime=mtime,
                btime=btime
            )

            output.append(output_str)
        # end if
    # end if

    for (sid, kids) in kid_sids:
        entry = dir_entries[sid]

        output_line = False
        if options.only_dirs:
            if entry.type == STGTY_STORAGE:
                output_line = True
            # end if
        elif options.only_files:
            if entry.type != STGTY_STORAGE:
                output_line = True
            # end if
        else:
            output_line = True
        # end if

        name = repr(entry.name)[1:-1]

        if output_line:
            if (entry.type == STGTY_STORAGE) or (entry.type == STGTY_ROOT):
                mode = "d/d"  # directory
            elif entry.type == STGTY_STREAM:
                mode = "r/r"  # file
            else:
                mode = "-/-"  # unknown
            # end if

            mtime = format_timestamp(entry.mtime, options)
            btime = format_timestamp(entry.btime, options)

            output_str = format_str.format(
                mode=mode,
                sid=sid,
                entry=entry,
                path=path,
                name=name,
                mtime=mtime,
                btime=btime
            )

            output.append(output_str)
        # end if


        if kids and options.recurse:
            old_path = path
            if options.display_full_path or options.mactime_filename:
                path = "".join([path, name, "/"])
            else:
                path = "".join([path, "+"])
            # end if

            output.extend(format_output(cfb, ((sid, kids),), options, path))
            path = old_path
        # end if
    # end for

    # Add virtual entries if root dir. and not mactime output
    include_virtual_entries = (
        (root_sid == 0) and
        (not options.mactime_filename) and
        (not options.only_files) and
        (not options.only_dirs)
    )

    if include_virtual_entries:
        sid = len(dir_entries)
        mode = "v/v"

        for name in ("$Header", "$DIFAT", "$FAT", "$MiniFAT"):
            entry = DirEntry([0] * 13)
            output.append(format_str.format(
                sid=sid,
                mode=mode,
                name=name,
                entry=entry,
                path="",
                mtime=0,
                btime=0
            ))

            sid = sid + 1
        # end for
    # end if

    return output
# end def format_output

def main():
    usage = "%prog [options] olefile [dir. entry #]"
    description = "\n".join([
        "Lists entries in an OLE compound file.",
        "",
        "If file is '-', then stdin is read.",
        "If a directory entry number is not specified, root is assumed."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-D",
        dest="only_dirs",
        action="store_true",
        help="Display only directories (storages)",
        default=False
    )

    parser.add_option(
        "-F",
        dest="only_files",
        action="store_true",
        help="Display only files (streams)",
        default=False
    )

    parser.add_option(
        "-l",
        dest="long_output",
        action="store_true",
        help="Display details in long format",
        default=False
    )

    parser.add_option(
        "-m",
        metavar="PATH",
        dest="mactime_filename",
        action="store",
        help="Display details in mactime format (prefixed by PATH)"
    )

    parser.add_option(
        "-p",
        dest="display_full_path",
        action="store_true",
        help="Display full path when recursing",
        default=False
    )

    parser.add_option(
        "-r",
        dest="recurse",
        action="store_true",
        help="Recurse into sub-directories",
        default=False
    )

    (options, args) = parser.parse_args()

    if options.only_dirs and options.only_files:
        parser.error("Can't specify both -D and -F")
    elif options.long_output and options.mactime_filename:
        parser.error("Can't specify both -l and -m")
    # end if

    if (len(args) < 1) or (len(args) > 2):
        parser.error("Invalid number of arguments")
        sys.exit(-1)
    # end if

    if args[0] == "-":
        cfb = CompoundFile(ByteIStream(sys.stdin.buffer.read()))
    else:
        cfb = CompoundFile(RawIStream(args[0]))
    # end if

    if len(args) == 1:
        start_sid = DEFAULT_START_SID
    else:
        start_sid = int(args[1])
    # end if

    if start_sid in cfb.dir_entries:
        entry = cfb.dir_entries[start_sid]
        if cfb.is_valid_dir_entry(entry):
            entries = enumerate_entries(cfb, start_sid, options)

            if options.mactime_filename:
                path = "".join([options.mactime_filename, "/"])
            else:
                path = ""
            # end if

            output = format_output(cfb, entries, options, path)
        else:
            print("Invalid directory {0}".format(start_sid), file=sys.stderr)
            sys.exit(-2)
        # end if
    else:
        print("Invalid directory {0}".format(start_sid), file=sys.stderr)
        sys.exit(-3)
    # end if

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
