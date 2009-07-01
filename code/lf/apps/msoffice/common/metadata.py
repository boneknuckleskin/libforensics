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
Common metadata for Microsoft Office documents

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "SummaryInfo", "DocSummaryInfo"
]

import pdb

from datetime import datetime

from lf.windows.ole.propertyset.objects import PropertySetStream
from lf.windows.ole.propertyset.consts import (
    FMTID_SummaryInformation, FMTID_DocSummaryInformation
)

from lf.apps.msoffice.common.consts import (
    SUMMARY_INFORMATION_NAME, DOC_SUMMARY_INFORMATION_NAME,

    PIDSI_CODEPAGE, PIDSI_TITLE, PIDSI_SUBJECT, PIDSI_AUTHOR, PIDSI_KEYWORDS,
    PIDSI_COMMENTS, PIDSI_TEMPLATE, PIDSI_LAST_AUTHOR, PIDSI_REV_NUMBER,
    PIDSI_EDIT_TIME, PIDSI_LAST_PRINTED_TIME, PIDSI_CREATE_TIME,
    PIDSI_SAVE_TIME, PIDSI_PAGE_COUNT, PIDSI_WORD_COUNT, PIDSI_CHAR_COUNT,
    PIDSI_THUMBNAIL, PIDSI_APP_NAME, PIDSI_DOC_SECURITY,

    PIDDSI_CODEPAGE, PIDDSI_CATEGORY, PIDDSI_PRESFORMAT, PIDDSI_SLIDECOUNT,
    PIDDSI_MANAGER, PIDDSI_COMPANY, PIDDSI_VERSION, PIDDSI_CONTENTTYPE,
    PIDDSI_CONTENTSTATUS, PIDDSI_LANGUAGE, PIDDSI_DOCVERSION
)

# Map of PIDSI_* values and the corresponding attribute in SummaryInfo
_pidsi_attr_name_map = {
    PIDSI_CODEPAGE: "cp", PIDSI_TITLE: "title",
    PIDSI_SUBJECT: "subject", PIDSI_AUTHOR: "author",
    PIDSI_KEYWORDS: "keywords", PIDSI_COMMENTS: "comments",
    PIDSI_TEMPLATE: "template", PIDSI_LAST_AUTHOR: "last_mod_author",
    PIDSI_REV_NUMBER: "rev", PIDSI_EDIT_TIME: "edit_time_tot",
    PIDSI_LAST_PRINTED_TIME: "print_time", PIDSI_CREATE_TIME: "btime",
    PIDSI_SAVE_TIME: "mtime", PIDSI_PAGE_COUNT: "page_count",
    PIDSI_WORD_COUNT: "word_count", PIDSI_CHAR_COUNT: "char_count",
    PIDSI_THUMBNAIL: "thumbnail", PIDSI_APP_NAME: "app_name",
    PIDSI_DOC_SECURITY: "security"
}

_piddsi_attr_name_map = {
    PIDDSI_CODEPAGE: "cp", PIDDSI_CATEGORY: "category",
    PIDDSI_PRESFORMAT: "pres_format", PIDDSI_SLIDECOUNT: "slide_count",
    PIDDSI_MANAGER: "manager", PIDDSI_COMPANY: "company",
    # We do this one on our own
    # PIDDSI_VERSION: "version",
    PIDDSI_CONTENTTYPE: "content_type", PIDDSI_CONTENTSTATUS: "content_status",
    PIDDSI_LANGUAGE: "language", PIDDSI_DOCVERSION: "doc_version"
}

class SummaryInfo():
    """
    Summary information from a Microsoft Office document.

    .. attribute:: cp

        The code page used to encode strings.

    .. attribute:: title

        The title of the document.

    .. attribute:: subject

        The subject of the document.

    .. attribute:: author

        The document's author.

    .. attribute:: keywords

        Keywords for the document.

    .. attribute:: comments

        The document's comments.

    .. attribute:: template

        The template used for the document.

    .. attribute:: last_mod_author

        The last author who modified the document.

    .. attribute:: rev

        The revision number.

    .. attribute:: edit_time_tot

        The total time spent editing the document.

    .. attribute:: print_time

        The last time the document was printed.

    .. attribute:: btime

        The creation time of the document.

    .. attribute:: mtime

        The last time the document was saved.

    .. attribute:: page_count

        The number of pages in the document.

    .. attribute:: word_count

        The number of words in the document.

    .. attribute:: char_count

        The number of characters in the document.

    .. attribute:: thumbnail

        An image used for the thumbnail of the document.

    .. attribute:: app_name

        The name of the application that created the document.

    .. attribute:: security

        The document's security.

    .. attribute:: in_file

        A list of properties that were actually found in the document.
    """

    def __init__(self, cfb):
        """
        Initializes a SummaryInfo object.

        :parameters:
            cfb
                A CompoundFile object.
        """

        for entry in cfb.dir_entries.values():
            if entry.name == SUMMARY_INFORMATION_NAME:
                stream_id = entry.sid
                break
            # end if
        else:
            self.in_file = list()
            for attr_name in _pidsi_attr_name_map.values():
                setattr(self, attr_name, None)
            # end for

            return
        # end for

        stream = cfb.get_stream(stream_id, ignore_size=True)
        properties = PropertySetStream(stream).property_sets[0].properties

        in_file = list()

        if PIDSI_EDIT_TIME in properties:
            etime = properties[PIDSI_EDIT_TIME].value
            properties[PIDSI_EDIT_TIME].value = etime - datetime(1601, 1, 1)
        # end if

        for (pid, attr_name) in _pidsi_attr_name_map.items():
            if pid in properties:
                in_file.append(attr_name)
                setattr(self, attr_name, properties[pid].value)
            else:
                setattr(self, attr_name, None)
            # end if
        # end for

        self.in_file = in_file
    # end def __init__
# end class SummaryInfo

class DocSummaryInfo():
    """
    Document summary information from a Microsoft Office document.

    .. attribute:: cp

        The code page used to encode strings.

    .. attribute:: category

        The document category.

    .. attribute:: pres_format

        The presentation format for the document.

    .. attribute:: slide_count

        The number of slides in the document (for PPT only).

    .. attribute:: manager

        The manager associated with the document.

    .. attribute:: company

        The company associated with the document.

    .. attribute:: ver_major

        The major version of the application that wrote the document.

    .. attribute:: ver_minor

        The minor version of the application that wrote the document.

    .. attribute:: content_type

        The document's content type.

    .. attribute:: content_status

        The document's content status.

    .. attribute:: language

        The language associated with the document.

    .. attribute:: doc_version

        The version of the document.

    .. attribute:: os_ver_major

        The major version number of the OS that wrote the file.

    .. attribute:: os_ver_minor

        The minor version number of the OS that wrote the file.

    .. attribute:: in_file

        A list of the properties that actually appeared in the stream.

    .. attribute:: user_defined

        A dictionary of user defined properties (if any)

    .. attribute:: user_defined_cp

        The code page for user defined properties (if any)
    """

    def __init__(self, cfb):
        """
        Initializes a DocSummaryInfo object.

        :parameters:
            cfb
                A CompoundFile object.
        """

        for entry in cfb.dir_entries.values():
            if entry.name == DOC_SUMMARY_INFORMATION_NAME:
                stream_id = entry.sid
                break
            # end if
        else:
            self.os_ver_major = None
            self.os_ver_minor = None
            self.ver_major = None
            self.ver_minor = None
            self.in_file = list()

            for attr_name in _piddsi_attr_name_map.values():
                setattr(self, attr_name, None)
            # end for

            return
        # end if

        stream = cfb.get_stream(stream_id)
        pss = PropertySetStream(stream)
        properties = pss.property_sets[0].properties
        self.os_ver_major = pss.sys_id >> 24
        self.os_ver_minor = (pss.sys_id >> 16) & 0x0F

        in_file = ["os_ver_major", "os_ver_minor"]

        for (pid, attr_name) in _piddsi_attr_name_map.items():
            if pid in properties:
                in_file.append(attr_name)
                setattr(self, attr_name, properties[pid].value)
            else:
                setattr(self, attr_name, None)
            # end if
        # end for

        if PIDDSI_VERSION in properties:
            in_file.extend(["ver_major", "ver_minor"])
            version = properties[PIDDSI_VERSION].value
            self.ver_major = version >> 16
            self.ver_minor = version & 0x00FF
        else:
            self.ver_major = None
            self.ver_minor = None
        # end if

        user_defined = dict()
        user_defined_cp = None

        if len(pss.property_sets) == 2:
            properties = pss.property_sets[1].properties
            user_defined_cp = properties[1].value
            dictionary = properties[0]
            for (pid, name) in dictionary.items():
                user_defined[name] = properties[pid].value
            # end for
        # end if

        self.user_defined = user_defined
        self.user_defined_cp = user_defined_cp
        self.in_file = in_file
    # end def __init__
# end class DocSummaryInfo
