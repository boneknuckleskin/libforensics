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

"""Tool to demonstrate some of the capabilities in lf.win.shell.thumbsdb"""

# stdlib imports
import sys
from optparse import OptionParser
from datetime import datetime

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.ole.cfb import CompoundFile
from lf.win.shell.thumbsdb import ThumbsDb

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)


__docformat__ = "restructuredtext en"
__all__ = [
    "format_timestamp", "format_entry", "main"
]

def format_timestamp(timestamp):
    if isinstance(timestamp, datetime):
        new_timestamp = timestamp.replace(microsecond=0)
        new_timestamp = new_timestamp.isoformat(" ")
    else:
        new_timestamp = timestamp
    # end if

    return new_timestamp
# end def format_timestamp

def format_catalog(tdb):
    output = list()
    catalog = tdb.catalog

    output.append("Thumbnail width: {0}".format(catalog.width))
    output.append("Thumbnail height: {0}".format(catalog.height))
    output.append("Thumbnail count: {0}".format(catalog.item_count))

    return output
# end def format_catalog

def format_entry(tdb, entry):
    output = list()

    thumbnail = tdb.thumbnails[entry.id]
    mtime = format_timestamp(entry.mtime)

    output.append("ID: {0}".format(entry.id))
    output.append("Catalog entry size: {0}".format(entry.size))
    output.append("File name: {0}".format(entry.file_name))
    output.append("File size: {0}".format(thumbnail.size))
    output.append("Stream name: {0}".format(entry.stream_name))
    output.append("Modification time: {0}".format(mtime))

    return output
# end def format_entry

def main():
    usage = "%prog thumbsdb id"
    description = "\n".join([
        "Displays statistics about a specific entry in a thumbs.db file."
        "",
        "If thumbsdb is '-', then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-c",
        dest="catalog_name",
        action="store",
        help="The name of the catalog stream (def: %default)",
        default="Catalog"
    )

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("You must specify both an thumbs.db file and an id")
    # end fi


    if args[0] == "-":
        cfb = CompoundFile(ByteIStream(sys.stdin.buffer.read()))
    else:
        cfb = CompoundFile(RawIStream(args[0]))
    # end if
    tdb = ThumbsDb(cfb, options.catalog_name)

    entry_id = int(args[1])

    entries = tdb.catalog.entries
    key_values = dict([(getattr(entry, "id"), entry) for entry in entries])
    ids = list(key_values.keys())
    ids.append(ids[-1] + 1)  # $Catalog

    if entry_id not in ids:
        parser.error("Unknown id {0}".format(entry_id))
    # end if

    if entry_id == ids[-1]:
        output = format_catalog(tdb)
    else:
        output = format_entry(tdb, key_values[entry_id])
    # end if

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
