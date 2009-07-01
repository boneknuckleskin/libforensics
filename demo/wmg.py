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
Extracts metadata from a Microsoft Word document.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

import sys

from lf.io import raw
from lf.windows.ole.compoundfile.objects import CompoundFile
from lf.windows.lcid.consts import lcid_names
from lf.apps.msoffice.common.metadata import SummaryInfo, DocSummaryInfo
from lf.apps.msoffice.word.metadata import WordMetadata

from lf.apps.msoffice.word.consts import (
    magic_names, ENVR_WINDOWS,
    ASSOC_DOT, ASSOC_TITLE, ASSOC_SUBJECT, ASSOC_KEYWORDS, ASSOC_COMMENTS,
    ASSOC_AUTHOR, ASSOC_LAST_REV_BY,
    ROLE_NONE, ROLE_OWNER, ROLE_EDITOR
)

VERSION = "1.0"

def create_header(cfb, file_name):
    """Creates header information from a compound file"""

    output = list()

    output.append("Compound File Information")
    output.append("-------------------------")
    output.append("File: {0}".format(file_name))

    btime = cfb.dir_entries[0].btime.ctime()
    mtime = cfb.dir_entries[0].mtime.ctime()

    str = "Root directory creation time: {0} UTC".format(btime)
    output.append(str)

    str = "Root directory modification time: {0} UTC".format(mtime)
    output.append(str)

    output.append("")

    return output
# end def create_header

def create_summary_information(cfb):
    """Creates summary information from a compound file"""


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
# end def create_summary_information

def create_doc_summary_information(cfb):
    """Creates metadata for the DocumentSummaryInformation stream"""

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
# end def create_doc_summary_information

def create_word_metadata(cfb):
    """Creates Word metadata"""

    def yes_no(val):
        if val:
            return "yes"
        else:
            return "no"
    # end def yes_no

    output = list()
    output.append("Word Information")
    output.append("----------------")

    wmd = WordMetadata(cfb)

    if wmd.magic in magic_names:
        str = magic_names[wmd.magic]
    else:
        str = "Unknown"
    # end if

    output.append("Magic: {0} (0x{1:X})".format(str, wmd.magic))
    output.append("Version: 0x{0:X}".format(wmd.version))

    if wmd.lang_id in lcid_names:
        str = lcid_names[wmd.lang_id]
    else:
        str = "Unknown (0x{0:X})".format(wmd.lang_id)
    # end if

    output.append("Language: {0}".format(str))
    output.append("Encryption key: {0}".format(wmd.encryption_key))

    if wmd.created_environment == ENVR_WINDOWS:
        str = "Windows"
    else:
        str = "Mac"
    # end if
    output.append("Created in: {0}".format(str))

    if wmd.magic_created_by in magic_names:
        str = magic_names[wmd.magic_created_by]
    else:
        str = "Unknown (0x{0:X})".format(wmd.magic_created_by)
    # end if
    output.append(
        "Created by: {0} (Build date: {1})".format(
            str, wmd.created_build_date.strftime("%a %b %d %Y")
        )
    )

    if wmd.magic_revised_by in magic_names:
        str = magic_names[wmd.magic_revised_by]
    else:
        str = "Unknown (0x{0:X})".format(wmd.magic_revised_by)
    # end if
    output.append(
        "Last revised by: {0} (Build date: {1})".format(
            str, wmd.revised_build_date.strftime("%a %b %d %Y")
        )
    )

    output.append("")
    output.append(" Miscellaneous Properties")
    output.append(" ------------------------")
    output.append(" Is a template: {0}".format(yes_no(wmd.is_template)))
    output.append(" Is a glossary: {0}".format(yes_no(wmd.is_glossary)))
    output.append(" Is in complex format: {0}".format(yes_no(wmd.is_complex)))
    output.append(" Has pictures: {0}".format(yes_no(wmd.has_pictures)))
    output.append(" Is encrypted: {0}".format(yes_no(wmd.is_encrypted)))
    output.append(
        " Is Far East encoded: {0}".format(yes_no(wmd.is_far_east_encoded))
    )
    output.append(" Last saved on a Mac: {0}".format(yes_no(wmd.saved_mac)))

    output.append("")
    output.append(" Last Authors / Locations")
    output.append(" ------------------------")
    author_location = list(zip(wmd.last_saved_by, wmd.last_saved_locations))
    list_len = len(author_location)

    for index, (author, location) in enumerate(author_location[::-1]):
        output.append(
            " {0}: {1}: {2}".format(list_len - index, author, location)
        )
    # end for

    output.append("")
    output.append(" Associated Strings")
    output.append(" ------------------")

    strs = wmd.associated_strings
    output.append(" Template used: {0}".format(strs[ASSOC_DOT]))
    output.append(" Title: {0}".format(strs[ASSOC_TITLE]))
    output.append(" Subject: {0}".format(strs[ASSOC_SUBJECT]))
    output.append(" Keywords: {0}".format(strs[ASSOC_KEYWORDS]))
    output.append(" Comments: {0}".format(strs[ASSOC_COMMENTS]))
    output.append(" Author: {0}".format(strs[ASSOC_AUTHOR]))
    output.append(" Last revised by: {0}".format(strs[ASSOC_LAST_REV_BY]))

    output.append("")
    output.append(" Users / Roles")
    output.append(" -------------")

    if wmd.users_roles:
        for (user, role) in wmd.users_roles:
            if role == ROLE_NONE:
                str = "No role"
            elif role == ROLE_OWNER:
                str = "Owner"
            elif role == ROLE_EDITOR:
                str = "Editor"
            else:
                str = "Unknown role"
            # end if

            output.append(" {0}: {1}".format(user, str))
        # end for
    else:
        output.append(" No users / roles in document")
    # end if

    output.append("")
    return output
# end def create_word_metadata

output = list()

if len(sys.argv) < 2:
    print("Word Metadata Grabber {0}".format(VERSION))
    print("Usage: {0} <word file>".format(sys.argv[0]))
    sys.exit(-1)
# end if

output = list()
cfb = CompoundFile(raw.open(sys.argv[1]))

output.extend(create_header(cfb, sys.argv[1]))
output.extend(create_summary_information(cfb))
output.extend(create_doc_summary_information(cfb))
output.extend(create_word_metadata(cfb))
output.append("")

print("\n".join(output))
