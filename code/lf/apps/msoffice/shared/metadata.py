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

"""Shared metadata for Microsoft Office documents."""

# stdlib imports
from codecs import getdecoder
from uuid import UUID

# local imports
from lf.dec import ByteIStream
from lf.dtypes import Structuple
from lf.win.codepage.consts import code_page_names

from lf.win.ole.ps.consts import (
    CODEPAGE_PROPERTY_IDENTIFIER, DICTIONARY_PROPERTY_IDENTIFIER,
    LOCALE_PROPERTY_IDENTIFIER, BEHAVIOR_PROPERTY_IDENTIFIER, PropertyType,

    FMTID_SummaryInformation, FMTID_DocSummaryInformation
)
from lf.win.ole.ps import PropertiesMetadata

from lf.apps.msoffice.shared.objects import VecVtHyperlink
from lf.apps.msoffice.shared.consts import (
    PIDSI, PIDDSI
)

# module globals

# Map of PIDSI_* values and the corresponding attribute in SummaryInfo
_pidsi_attr_name_map = {
    CODEPAGE_PROPERTY_IDENTIFIER: "code_page",
    DICTIONARY_PROPERTY_IDENTIFIER: "dictionary",
    LOCALE_PROPERTY_IDENTIFIER: "locale",
    BEHAVIOR_PROPERTY_IDENTIFIER: "behavior",

    PIDSI.TITLE: "title", PIDSI.SUBJECT: "subject", PIDSI.AUTHOR: "author",
    PIDSI.KEYWORDS: "keywords", PIDSI.COMMENTS: "comments",
    PIDSI.TEMPLATE: "template", PIDSI.LAST_AUTHOR: "last_author",
    PIDSI.REVNUMBER: "rev", PIDSI.EDIT_TIME: "edit_time_tot",
    PIDSI.LAST_PRINTED_TIME: "print_time", PIDSI.CREATE_TIME: "btime",
    PIDSI.SAVE_TIME: "mtime", PIDSI.PAGE_COUNT: "page_count",
    PIDSI.WORD_COUNT: "word_count", PIDSI.CHAR_COUNT: "char_count",
    PIDSI.THUMBNAIL: "thumbnail", PIDSI.APPNAME: "app_name",
    PIDSI.DOC_SECURITY: "security"
}

_piddsi_attr_name_map = {
    CODEPAGE_PROPERTY_IDENTIFIER: "code_page",
    DICTIONARY_PROPERTY_IDENTIFIER: "dictionary",
    LOCALE_PROPERTY_IDENTIFIER: "locale",
    BEHAVIOR_PROPERTY_IDENTIFIER: "behavior",

    PIDDSI.CATEGORY: "category", PIDDSI.PRESFORMAT: "pres_format",
    PIDDSI.BYTECOUNT: "byte_count", PIDDSI.LINECOUNT: "line_count",
    PIDDSI.PARACOUNT: "para_count", PIDDSI.SLIDECOUNT: "slide_count",
    PIDDSI.NOTECOUNT: "note_count", PIDDSI.HIDDENCOUNT: "hidden_count",
    PIDDSI.MMCLIPCOUNT: "mm_clip_count", PIDDSI.SCALE: "scale",
    PIDDSI.HEADINGPAIR: "heading_pair", PIDDSI.DOCPARTS: "doc_parts",
    PIDDSI.MANAGER: "manager", PIDDSI.COMPANY: "company",
    PIDDSI.LINKSDIRTY: "links_dirty", PIDDSI.CCHWITHSPACES: "char_count_full",
    PIDDSI.SHAREDDOC: "shared_doc", PIDDSI.LINKBASE: "link_base",
    PIDDSI.HLINKS: "hlinks", PIDDSI.HYPERLINKSCHANGED: "hyperlinks_changed",

    # We do this one on our own
    # PIDDSI.VERSION: "version",

    PIDDSI.DIGSIG: "dig_sig",  PIDDSI.CONTENTTYPE: "content_type",
    PIDDSI.CONTENTSTATUS: "content_status", PIDDSI.LANGUAGE: "language",
    PIDDSI.DOCVERSION: "doc_version"
}

_pidus_attr_name_map = {
    CODEPAGE_PROPERTY_IDENTIFIER: "code_page",
    DICTIONARY_PROPERTY_IDENTIFIER: "dictionary",
    LOCALE_PROPERTY_IDENTIFIER: "locale",
    BEHAVIOR_PROPERTY_IDENTIFIER: "behavior",
}

# Used by UserDefinedProperties
_utf_16_le_decoder = getdecoder("utf_16_le")


__docformat__ = "restructuredtext en"
__all__ = [
    "SummaryInfo", "DocSummaryInfo", "UserDefinedProperties"
]

class SummaryInfo(PropertiesMetadata):
    """Parsed properties from a Summary Information stream.

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

    .. attribute:: last_author

        The last author who modified the document.

    .. attribute:: rev

        The revision number.

    .. attribute:: edit_time_tot

        The total time spent modifying (editing) the document.

    .. attribute:: print_time

        The time the document was last printed.

    .. attribute:: btime

        The creation time of the document.

    .. attribute:: mtime

        The time the document was last saved.

    .. attribute:: page_count

        The number of pages in the document.

    .. attribute:: word_count

        The number of words in the document.

    .. attribute:: char_count

        The number of characters in the document.

    .. attribute:: thumbnail

        An image used as a thumbnail of the document.

    .. attribute:: app_name

        The name of the application that created the document.

    .. attribute:: security

        The document's security

    """
    _fields_ = (
        "title", "subject", "author", "keywords", "comments", "template",
        "last_author", "rev", "edit_time_tot", "print_time", "btime", "mtime",
        "page_count", "word_count", "char_count", "thumbnail", "app_name",
        "security"
    )

    @classmethod
    def from_properties(cls, properties):
        """Creates a :class:`SummaryInfo` from properties.

        :type properties: ``dict``
        :param properties: A dictionary of property identifiers (keys) and the
                           corresponding :class:`~lf.win.ole.ps.PropertyPacket`
                           objects.

        :rtype: :class:`SummaryInfo`
        :returns: The corresponding :class:`SummaryInfo` object.

        """
        attr_exists = set()
        properties_dict = dict()

        for (pid, property) in properties.items():
            if pid in _pidsi_attr_name_map:
                name = _pidsi_attr_name_map[pid]
                properties_dict[name] = property.value
                attr_exists.add(name)
            # end if
        # end for

        if "code_page" in properties_dict:
            if properties_dict["code_page"] < 0:
                properties_dict["code_page"] += 0x10000
            # end if
        # end if

        properties_dict["attr_exists"] = attr_exists
        values = [properties_dict.get(name) for name in cls._fields_]

        return cls(values)
    # end def from_properties
# end class SummaryInfo

class DocSummaryInfo(PropertiesMetadata):
    """Parsed properties from a Document Summary Information stream.
    .. attribute:: category

        The document category.

    .. attribute:: pres_format

        The presentation format.

    .. attribute:: byte_count

        The size of the document in bytes.

    .. attribute:: para_count

        The number of paragraphs in the document.

    .. attribute:: slide_count

        The number of slides in the document.

    .. attribute:: note_count

        The number of notes in the document.

    .. attribute:: hidden_count

        The number of hidden slides.

    .. attribute:: mm_clip_count

        The number of multimedia clips in the document.

    .. attribute:: scale

        The value of GKPIDDSI_SCALE.

    .. attribute:: heading_pair

         A list of (heading string, document part count) tuples.

    .. attribute:: doc_parts

        A list of strings of the document parts, in the same order as the
        elements of :attr:`heading_pair`.

    .. attribute:: manager

        The manager associated with the document.

    .. attribute:: company

        The company associated with the document.

    .. attribute:: links_dirty

        True if any linked properties in a User Defined Property Set have
        changed outside of the application.

    .. attribute:: char_count_full

        The number of characters in the document, including whitespace.

    .. attribute:: shared_doc

        The value of GKPIDDSI_SHAREDDOC.

    .. attribute:: link_base

        The base URL for converting relative links.

    .. attribute:: hlinks

        A list of hyperlinks.

    .. attribute:: hyperlinks_changed

        True if the "_PID_HLINKS" property in a User Defined Property set has
        changed outside of the application.

    .. attribute:: ver_major

        The major version of the application that wrote the document.

    .. attribute:: ver_minor

        The minor version of the application that wrote the document.

    .. attribute:: dig_sig

        A VBA digital signature.

    .. attribute:: content_type

        The document's content type.

    .. attribute:: content_status

        The document's content status.

    .. attribute:: language

        The language associated with the document.

    .. attribute:: doc_version

        The version of the document.

    """
    _fields_ = (
        "category", "pres_format", "byte_count", "para_count", "slide_count",
        "note_count", "hidden_count", "mm_clip_count", "scale", "heading_pair",
        "doc_parts", "manager", "company", "links_dirty", "char_count_full",
        "shared_doc", "link_base", "hlinks", "hyperlinks_changed", "ver_major",
        "ver_minor", "dig_sig", "content_type", "content_status", "language",
        "doc_version"
    )

    @classmethod
    def from_properties(cls, properties):
        """Creates a :class:`DocSummaryInfo` from properties.

        :type properties: ``dict``
        :param properties: A dictionary of property identifiers (keys) and the
                           corresponding :class:`~lf.win.ole.ps.PropertyPacket`
                           objects.

        :rtype: :class:`DocSummaryInfo`
        :returns: The corresponding :class:`DocSummaryInfo` object.

        """
        attr_exists = set()
        properties_dict = dict()
        PIDDSI_VERSION = PIDDSI.VERSION

        for (pid, property) in properties.items():
            if pid == PIDDSI_VERSION:
                version = property.value
                properties_dict["ver_major"] = (version >> 16)
                properties_dict["ver_minor"] = (version & 0xFFFF)
                attr_exists.add("ver_major")
                attr_exists.add("ver_minor")
            else:
                if pid in _piddsi_attr_name_map:
                    name = _piddsi_attr_name_map[pid]

                    properties_dict[name] = property.value
                    attr_exists.add(name)
                # end if
            # end if
        # end for

        if "code_page" in properties_dict:
            if properties_dict["code_page"] < 0:
                properties_dict["code_page"] += 0x10000
            # end if
        # end if

        if "heading_pair" in properties_dict:
            properties_dict["heading_pair"] = [
                (pair.heading_str.value, pair.header_parts.value)
                for pair in properties_dict["heading_pair"].value
            ]
        # end if

        if "doc_parts" in properties_dict:
            properties_dict["doc_parts"] = [
                string.value for string in properties_dict["doc_parts"].value
            ]
        # end if

        properties_dict["attr_exists"] = attr_exists
        values = [properties_dict.get(name) for name in cls._fields_]

        return cls((values))
    # end def from_properties
# end class DocSummaryInfo

class UserDefinedProperties(PropertiesMetadata):
    """Parsed proeprties from a User Defined Proeprties property set.

    .. attribute:: linked

        A list of linked properties, in the form of (name, pid) tuples.

    .. attribute:: guid

        The _PID_GUID property (decoded if possible).

    .. attribute:: link_base

        The _PID_LINKBASE property (decoded if possible).

    .. attribute:: hlinks

        The _PID_HLINKS property.

    """
    _fields_ = ("linked", "guid", "link_base", "hlinks")

    @classmethod
    def from_properties(cls, properties, decoder=None):
        """Creates a :class:`UserDefinedProperties` from properties.

        :type properties: ``dict``
        :param properties: A dictionary of property identifiers (keys) and the
                           corresponding :class:`~lf.win.ole.ps.PropertyPacket`
                           objects.

        :rtype: :class:`UserDefinedProperties`
        :returns: The corresponding :class:`UserDefinedProperties` object.

        """
        attr_exists = set()
        properties_dict = dict()

        VT_BLOB = PropertyType.VT_BLOB

        if DICTIONARY_PROPERTY_IDENTIFIER not in properties:
            return super(UserDefinedProperties, cls).from_properties(
                properties
            )
        # end if

        dictionary = properties[DICTIONARY_PROPERTY_IDENTIFIER].value
        linked = list()

        for (pid, property) in properties.items():
            if pid in _pidus_attr_name_map:
                name = _pidus_attr_name_map[pid]
                properties_dict[name] = property.value
                attr_exists.add(name)
                continue
            # end if

            if pid & 0x1000000:  # Is it a linked property?
                associated_pid = pid & ~0x1000000
                linked.append((property.value, associated_pid))
            # end if

            if pid in dictionary:
                name = dictionary[pid]
            else:
                name = None
            # end if

            if (name == "_PID_GUID") and (property.type == VT_BLOB):
                guid = property.value
                new_guid = _utf_16_le_decoder(guid, "ignore")[0]

                if new_guid:
                    guid = new_guid.split("\x00", 1)[0]
                # end if

                try:
                    guid = UUID(guid)
                except (TypeError, ValueError):
                    pass
                # end try

                properties_dict["guid"] = guid
                attr_exists.add("guid")

            elif (name == "_PID_LINKBASE") and (property.type == VT_BLOB):
                link_base = property.value
                new_link_base = _utf_16_le_decoder(link_base, "ignore")[0]

                if new_link_base:
                    link_base = new_link_base.split("\x00", 1)[0]
                # end if
                properties_dict["link_base"] = link_base
                attr_exists.add("link_base")

            elif (name == "_PID_HLINKS") and (property.type == VT_BLOB):
                data = ByteIStream(property.value)
                hlinks = VecVtHyperlink.from_stream(data).value
                hlinks = [
                    (
                        hlink.hash.value,
                        hlink.app.value,
                        hlink.office_art.value,
                        hlink.info.value,
                        hlink.hlink1.value,
                        hlink.hlink2.value
                    )
                    for hlink in hlinks
                ]
                properties_dict["hlinks"] = hlinks
                attr_exists.add("hlinks")

            # end if
        # end for

        if "code_page" in properties_dict:
            if properties_dict["code_page"] < 0:
                properties_dict["code_page"] += 0xFFFF + 1
            # end if
        # end if

        if linked:
            properties_dict["linked"] = linked
            attr_exists.add("linked")
        else:
            properties_dict["linked"] = None
        # end if

        properties_dict["attr_exists"] = attr_exists
        values = [properties_dict.get(name) for name in cls._fields_]

        return cls(values)
    # end def from_properties
# end class UserDefinedProperties
