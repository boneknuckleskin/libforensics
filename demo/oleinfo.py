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

import sys
from optparse import OptionParser

from lf.io import raw
from lf.io.consts import SEEK_SET

from lf.windows.ole.compoundfile.objects import CompoundFile
from lf.windows.ole.compoundfile.extractors import header
from lf.windows.ole.compoundfile.consts import (
    STREAM_ID_NONE, FAT_EOC
)

from lf.apps.msoffice.common.metadata import SummaryInfo, DocSummaryInfo

def format_sid(sid):
    """Gives a nice string representation of the SID"""

    if sid == STREAM_ID_NONE:
        return "(none)"
    else:
        return "{0}".format(sid)
    # end if
# end def format_sid

def format_fat(entry):
    """Gives a nice string representation of the FAT entry"""

    if entry == FAT_EOC:
        return "(none)"
    else:
        return "{0}".format(entry)
    # end if
# end def format_fat

def create_header(stream):
    """Creates header information"""

    stream.seek(0, SEEK_SET)
    values = header.extract(stream.read(512))
    cfb = CompoundFile(stream, 0)
    output = list()

    output.append("Header Information")
    output.append("------------------")
    output.append("File name: {0}".format(sys.argv[1]))
    output.append("Signature: {0}".format(values.sig))
    output.append("CLSID: {0}".format(cfb.clsid))
    output.append("Version: {0}.{1}".format(values.ver_major, values.ver_minor))
    output.append("Byte order: {0:X}".format(values.byte_order))
    output.append("Sector size: {0}".format(cfb.sect_size))
    output.append("Mini sector size: {0}".format(cfb.mini_sect_size))
    output.append("Transaction number: {0}".format(cfb.trans_num))
    output.append("Mini stream cutoff: {0}".format(values.mini_stream_cutoff))
    output.append("Number of DI FAT entries: {0}".format(values.di_fat_count))
    output.append("First sector of DI FAT: {0}".format(
        format_fat(values.di_fat_sect)))
    output.append("Number of Mini FAT entries: {0}".format(
        values.mini_fat_count))
    output.append("First sector of Mini FAT: {0}".format(
        format_fat(values.mini_fat_sect)))
    output.append("Number of FAT entries: {0}".format(values.fat_count))
    output.append("Number of sectors in directory: {0}".format(
        values.dir_count))
    output.append("First sector of directory: {0}".format(values.dir_sect))
    output.append("Size of root directory: {0}".format(cfb.dir_stream.size))
    output.append("")

    return output
# end def create_header

def create_summary_info(cfb):
    """Creates summary information"""

    output = list()
    output.append("Summary Information")
    output.append("-------------------")

    summary_info = SummaryInfo(cfb)
    in_file = summary_info.in_file

    if not len(in_file):
        output.append("(not in file)")
        output.append("")
        return output
    # end if

    prop_info = [
        ("title", "Title"), ("subject", "Subject"), ("author", "Author"),
        ("cp", "Code page"),
        ("keywords", "Keywords"), ("comments", "Comments"),
        ("template", "Template used"),
        ("last_mod_author", "Last author"), ("rev", "Revision"),
        ("app_name", "Creator")
    ]

    for (attr_name, desc) in prop_info:
        if attr_name in in_file:
            value = getattr(summary_info, attr_name)
        else:
            value = "(not in file)"
        # end if

        output.append("{0}: {1}".format(desc, value))
    # end for

    prop_info = [
        ("print_time", "Last printed"), ("btime", "Creation time"),
        ("mtime", "Last saved")
    ]

    for (attr_name, desc) in prop_info:
        if attr_name in in_file:
            value = getattr(summary_info, attr_name).ctime()
        else:
            value = "(not in file)"
        # end if

        output.append("{0}: {1}".format(desc, value))
    # end for

    etime = summary_info.edit_time_tot
    days = etime.days
    secs = etime.seconds
    hours = secs // 3600
    secs -= (hours * 3600)
    mins = secs // 60
    secs -= (mins * 60)

    output.append(
        "Total edit time: {0} days, {1} hours, {2} mins, {3} secs".format(
            days, hours, mins, secs
        )
    )

    output.append("")
    return output
# end def create_summary_info

def create_doc_summary_info(cfb):
    """Creates document summary information"""

    output = list()

    output.append("Document Summary Information")
    output.append("----------------------------")

    doc_summary_info = DocSummaryInfo(cfb)

    if not len(doc_summary_info.in_file):
        output.append("(not found in file)")
        output.append("")
        output.append(" User Defined Properties")
        output.append(" -----------------------")
        output.append(" (not found in file)")
        output.append("")

        return(output)
    # end if

    prop_info = [
        ("category", "Category"), ("pres_format", "Presentation format"),
        ("slide_count", "Slide count"), ("manager", "Manager"),
        ("company", "Company"), ("ver_major", "Major version"),
        ("ver_minor", "Minor version"), ("content_type", "Content type"),
        ("content_status", "Content status"), ("language", "Language"),
        ("doc_version", "Document version")
    ]

    in_file = doc_summary_info.in_file

    for (attr_name, desc) in prop_info:
        if attr_name in in_file:
            value = getattr(doc_summary_info, attr_name)
        else:
            value = "(not in file)"
        # end if

        output.append("{0}: {1}".format(desc, value))
    # end for

    output.append("")
    output.append(" User Defined Properties")
    output.append(" -----------------------")

    user_defined = doc_summary_info.user_defined

    if not user_defined:
        output.append(" (not in file)")
        output.append("")
        return output
    # end if

    output.append(" Code page: {0}".format(doc_summary_info.user_defined_cp))

    if "_PID_HLINKS" in user_defined:
        output.append(" Hyperlinks:")

        for hyperlink in user_defined["_PID_HLINKS"]:
            output.append("".join(["  ", hyperlink[4], hyperlink[5]]))
        # end for

        del user_defined["_PID_HLINKS"]
    # end if

    for (key, value) in user_defined.items():
        output.append(" {0}: {1}".format(key, value))
    # end for

    output.append("")
    return output
# end def create_doc_summary_info

def create_dir_info(cfb):
    """Creates information about the directory entries"""
    output = list()
    entry_ids = list(cfb.dir_entries.keys())
    entry_ids.sort()

    output.append("Directory Entries")
    output.append("-----------------")
    for entry_id in entry_ids:
        de = cfb.dir_entries[entry_id]
        output.append("Directory entry: {0}".format(entry_id))
        output.append("Name: {0}".format(de.name))
        output.append("Type: {0}".format(de.type))
        output.append("Color: {0}".format(de.color))
        output.append("Left SID: {0}".format(format_sid(de.left_sid)))
        output.append("Right SID: {0}".format(format_sid(de.right_sid)))
        output.append("Child SID: {0}".format(format_sid(de.child_sid)))
        output.append("CLSID: {0}".format(de.clsid))
        output.append("State: {0}".format(de.state))
        output.append("Creation time: {0}".format(de.btime.ctime()))
        output.append("Modification time: {0}".format(de.mtime.ctime()))
        output.append("First sector: {0}".format(de.first_sect))
        output.append("Size: {0}".format(de.size))
        output.append("")
    # end for

    return output
# end def create_dir_info

parser = OptionParser()
parser.set_usage("%prog [options] <ole file>")

parser.add_option(
    "-s", "--summary-information", dest="show_summary_info",
    action="store_true", default=False,
    help="Show SummaryInformation stream (if it exists)"
)

parser.add_option(
    "-d", "--document-summary-information", dest="show_doc_summary_info",
    action="store_true", default=False,
    help="Show DocumentSummaryInformation stream (if it exists)"
)

(options, args) = parser.parse_args()

if len(args) < 1:
    parser.error("you must specify an OLE file")
# end if

stream = raw.open(args[0])
cfb = CompoundFile(stream, 0)
output = list()

output.extend(create_header(stream))

if options.show_summary_info:
    output.extend(create_summary_info(cfb))
# end if

if options.show_doc_summary_info:
    output.extend(create_doc_summary_info(cfb))
# end if

output.extend(create_dir_info(cfb))

print("\n".join(output))
