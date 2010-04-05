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

"""Unit tests for the lf.apps.msoffice.shared.metadata module."""

# stdlib imports
import codecs
from os.path import join
from itertools import chain
from uuid import UUID
from unittest import TestCase

# local imports
from lf.dec import ByteIStream, RawIStream, SEEK_SET
from lf.time import FILETIMETodatetime
from lf.win.ole.cfb import CompoundFile
from lf.win.ole.ps import (
    VT_I2, VT_FILETIME, VT_I4, VT_BOOL, VT_VECTOR, CodePageString, VT_EMPTY,
    Dictionary, VT_BLOB, VT_CF, VT_LPSTR
)

from lf.apps.msoffice.shared import (
    PropertySetSystemIdentifier, VtThumbnailValue, VtThumbnail, Lpstr,
    UnalignedLpstr, VtVecUnalignedLpstrValue, VtVecUnalignedLpstr,
    Lpwstr, VtVecLpwstrValue, VtVecLpwstr, VtString, VtUnalignedString,
    VtHeadingPair, VtVecHeadingPairValue, VtVecHeadingPair, VtDigSigValue,
    VtDigSig, VtHyperlink, VecVtHyperlink, VtHyperlinkValue, VtHyperlinks,
    Builder,

    SummaryInfo, DocSummaryInfo, UserDefinedProperties
)

__docformat__ = "restructuredtext en"
__all__ = [
    "SummaryInfoTestCase", "DocSummaryInfoTestCase",
    "UserDefinedPropertiesTestCase"
]

class CommonSetup():
    def setUp(self):
        blair_path = join("data", "doc", "blair.doc")
        sample_path = join("data", "doc", "sample.doc")

        blair_cfb = CompoundFile(RawIStream(blair_path))
        sample_cfb = CompoundFile(RawIStream(sample_path))

        self.blair_si_stream = blair_cfb.get_stream(3)
        self.sample_si_stream = sample_cfb.get_stream(39)

        self.blair_dsi_stream = blair_cfb.get_stream(4)
        self.sample_dsi_stream = sample_cfb.get_stream(40)
    # end def setUp
# end class CommonSetup

class SummaryInfoTestCase(CommonSetup, TestCase):
    def test_from_properties(self):
        ae = self.assertEqual

        blair_si_stream = self.blair_si_stream
        sample_si_stream = self.sample_si_stream

        blair_props = list()
        sample_props = list()

        control_metadata = SummaryInfo((
            0x4E4,
            None,
            None,
            None,
            set([
                "code_page",
                "title",
                "subject",
                "author",
                "keywords",
                "comments",
                "template",
                "last_author",
                "rev",
                "edit_time_tot",
                "print_time",
                "btime",
                "mtime",
                "page_count",
                "word_count",
                "char_count",
                "app_name",
                "security"
            ]),
            "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND "
            "INTIMIDATION",
            "",
            "default",
            "",
            "",
            "Normal.dot",
            "MKhan",
            "4",
            FILETIMETodatetime.from_int(0x6B49D200),
            FILETIMETodatetime.from_int(0x01C2C8A7296E8E00),
            FILETIMETodatetime.from_int(0x01C2CB66F65A2200),
            FILETIMETodatetime.from_int(0x01C2CB75E8F86400),
            1,
            0xF23,
            0x564A,
            None,
            "Microsoft Word 8.0",
            0,
        ))

        property_set_stream = Builder.build(blair_si_stream)
        blair_properties = property_set_stream.property_set_0.properties
        metadata = SummaryInfo.from_properties(blair_properties)
        ae(metadata, control_metadata)


        sample_si_stream.seek(0x1F8, SEEK_SET)
        cf_data = sample_si_stream.read(0x254A6)
        control_metadata = SummaryInfo((
            0x4E4,
            None,
            None,
            None,
            set([
                "code_page",
                "title",
                "subject",
                "author",
                "keywords",
                "comments",
                "template",
                "last_author",
                "rev",
                "edit_time_tot",
                "btime",
                "mtime",
                "page_count",
                "word_count",
                "char_count",
                "thumbnail",
                "app_name",
                "security"
            ]),
            "title_value",
            "subject_value",
            "author_value",
            "keyword0 keyword1",
            "Comments in the comments box",
            "Normal",
            "lftest2",
            "24",
            FILETIMETodatetime.from_int(0x1176592E00),
            None,
            FILETIMETodatetime.from_int(0x01CAA3C0F0A6EC00),
            FILETIMETodatetime.from_int(0x01CAA3D361570400),
            7,
            0xAA,
            0x0550,
            VtThumbnailValue((
                0x0254B4,
                cf_data,
                0xFFFFFFFF,
                3
            )),
            "Microsoft Office Word",
            8,
        ))

        property_set_stream = Builder.build(sample_si_stream, 0)
        sample_properties = property_set_stream.property_set_0.properties
        metadata = SummaryInfo.from_properties(sample_properties)
        ae(metadata, control_metadata)
    # end def test_from_properties
# end class SummaryInfoTestCase

class DocSummaryInfoTestCase(CommonSetup, TestCase):
    def test_from_properties(self):
        ae = self.assertEqual

        blair_dsi_stream = self.blair_dsi_stream
        sample_dsi_stream = self.sample_dsi_stream

        control_metadata_dict = {
            "code_page": 0x4E4,
            "dictionary": None,
            "locale": None,
            "behavior": None,
            "attr_exists": set([
                "code_page",
                "line_count",
                "para_count",
                "scale",
                "heading_pair",
                "doc_parts",
                "company",
                "links_dirty",
                "char_count_full",
                "shared_doc",
                "hyperlinks_changed",
                "ver_major",
                "ver_minor",
            ]),
            "category": None,
            "pres_format": None,
            "byte_count": None,
            "line_count": 0xB8,
            "para_count": 0x2C,
            "slide_count": None,
            "note_count": None,
            "hidden_count": None,
            "mm_clip_count": None,
            "scale": 0,
            "heading_pair": [("Title", 1)],
            "doc_parts": [
                "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND "
                "INTIMIDATION"
            ],
            "manager": None,
            "company": "default",
            "links_dirty": 0,
            "char_count_full": 0x69F8,
            "shared_doc": 0,
            "link_base": None,
            "hlinks": None,
            "hyperlinks_changed": 0,
            "ver_major": 0x8,
            "ver_minor": 0x1531,
            "dig_sig": None,
            "content_type": None,
            "content_status": None,
            "language": None,
            "doc_version": None
        }
        control_metadata_list = [
            control_metadata_dict.get(name) for name in DocSummaryInfo._fields_
        ]
        control_metadata = DocSummaryInfo(control_metadata_list)

        pss = Builder.build(blair_dsi_stream, 0)
        blair_properties = pss.property_set_0.properties

        metadata = DocSummaryInfo.from_properties(blair_properties)
        ae(metadata, control_metadata)


        sample_dsi_stream.seek(0x445, SEEK_SET)
        blob_data0 = sample_dsi_stream.read(0x2A)

        sample_dsi_stream.seek(0x479, SEEK_SET)
        blob_data1 = sample_dsi_stream.read(0x4A4)

        control_metadata_dict = {
            "code_page": 1252,
            "dictionary": None,
            "behavior": None,
            "locale": None,
            "attr_exists": set([
                "code_page",
                "category",
                "line_count",
                "para_count",
                "scale",
                "heading_pair",
                "doc_parts",
                "manager",
                "company",
                "links_dirty",
                "char_count_full",
                "shared_doc",
                "hyperlinks_changed",
                "ver_major",
                "ver_minor",
                "content_status"
            ]),
            "category": "category_value",
            "pres_format": None,
            "byte_count": None,
            "line_count": 0x55,
            "para_count": 0x1D,
            "slide_count": None,
            "note_count": None,
            "hidden_count": None,
            "mm_clip_count": None,
            "scale": 0,
            "heading_pair": [("Title", 1), ("Headings", 4)],
            "doc_parts": [
                "title_value",
                "",
                "TOC Entry 1",
                "    TOC Entry 1.1",
                "TOC Entry 2"
            ],
            "manager": "manager_value",
            "company": "company_value",
            "links_dirty": 0,
            "char_count_full": 0x5DD,
            "shared_doc": 0,
            "link_base": None,
            "hlinks": None,
            "hyperlinks_changed": 0,
            "ver_major": 0x0C,
            "ver_minor": 0,
            "dig_sig": None,
            "content_type": None,
            "content_status": "status_value",
            "language": None,
            "doc_version": None
        }
        control_metadata_list = [
            control_metadata_dict.get(field) for field in metadata._fields_
        ]
        control_metadata = DocSummaryInfo(control_metadata_list)

        pss = Builder.build(sample_dsi_stream, 0)
        sample_properties = pss.property_set_0.properties
        metadata = DocSummaryInfo.from_properties(sample_properties)

        ae(metadata, control_metadata)
    # end def test_from_properties
# end class DocSummaryInfoTestCase

class UserDefinedPropertiesTestCase(CommonSetup, TestCase):
    def test_from_properties(self):
        ae = self.assertEqual
        blair_dsi_stream = self.blair_dsi_stream
        sample_dsi_stream = self.sample_dsi_stream

        control_metadata_dict = {
            "code_page": 0x4E4,
            "dictionary": {2: "_PID_GUID"},
            "locale": None,
            "behavior": None,
            "attr_exists": set([
                "code_page",
                "dictionary",
                "guid"
            ]),
            "linked": None,
            "guid": UUID("{5E2C2E6C-8A16-46F3-8843-7F739FA12901}"),
            "link_base": None,
            "hlinks": None
        }
        fields = UserDefinedProperties._fields_
        control_metadata_list = [
            control_metadata_dict.get(field) for field in fields
        ]
        control_metadata = UserDefinedProperties(control_metadata_list)

        pss = Builder.build(blair_dsi_stream, 0)
        blair_properties = pss.property_set_1.properties
        metadata = UserDefinedProperties.from_properties(blair_properties)
        ae(metadata, control_metadata)


        sample_dsi_stream.seek(0x2C1, SEEK_SET)
        link_base_data = sample_dsi_stream.read(0x38)

        sample_dsi_stream.seek(0x301, SEEK_SET)
        hlinks_data = sample_dsi_stream.read(0x3B4)
        hlinks_value = VecVtHyperlink.from_stream(ByteIStream(hlinks_data))

        control_metadata_dict = {
            "code_page": 1252,
            "dictionary": {
                2: "_PID_LINKBASE",
                3: "_PID_HLINKS",
                4: "text_name",
                5: "date_name",
                6: "number_name_0",
                7: "number_name_1",
                8: "number_name_2",
                9: "number_name_3",
                0xA: "number_name_4",
                0xB: "number_name_5",
                0xC: "number_name_6",
                0xD: "number_name_7",
                0xE: "yes_name_yes",
                0xF: "yes_name_no",
                0x10: "link_to_bookmark_name1",
                0x11: "link_to_bookmark_name2",
                0x12: "link_to__1326562448"
            },
            "behavior": None,
            "locale": None,
            "attr_exists": set([
                "code_page",
                "dictionary",
                "linked",
                "link_base",
                "hlinks"
            ]),
            "linked": [
                ("bookmark_name1", 0x10),
                ("bookmark_name2", 0x11),
                ("_1326562448", 0x12)
            ],
            "guid": None,
            "link_base": "hyperlink_base_value",
            "hlinks": [
                (
                    0x70003D,
                    42,
                    0,
                    5,
                    "http://www.adigitaldreamer.com/gallery/displayimage.php"
                    "?album=13&pos=9\x00",
                    "\x00"
                ),
                (
                    0x380071,
                    33,
                    0,
                    5,
                    "http://www.adigitaldreamer.com/gallery/displayimage.php"
                    "?album=3&pos=95\00",
                    "\x00"
                ),
                (
                    0x3F0079,
                    30,
                    0,
                    5,
                    "http://www.adigitaldreamer.com/gallery/displayimage.php"
                    "?album=3&pos=122\00",
                    "\x00",
                ),
                (
                    0x340077,
                    27,
                    0,
                    5,
                    "http://commons.wikimedia.org/wiki/"
                    "File:Makari_the_Tiger.jpg\x00",
                    "\x00"
                ),
                (
                    0x28006B,
                    21,
                    0,
                    5,
                    "http://commons.wikimedia.org/wiki/"
                    "File:Kookaburra_at_Marwell.jpg\x00",
                    "\x00"
                ),
                (
                    0x1D003A,
                    14,
                    0,
                    5,
                    "\x00",
                    "_Toc252820870\00"
                ),
                (
                    0x1C003A,
                    8,
                    0,
                    5,
                    "\x00",
                    "_Toc252820869\00"
                ),
                (
                    0x1C003A,
                    2,
                    0,
                    5,
                    "\x00",
                    "_Toc252820868\00"
                )
            ]
        }
        control_metadata_list = [
            control_metadata_dict.get(field) for field in fields
        ]
        control_metadata = UserDefinedProperties(control_metadata_list)

        pss = Builder.build(sample_dsi_stream, 0)
        sample_properties = pss.property_set_1.properties
        metadata = UserDefinedProperties.from_properties(sample_properties)
        ae(metadata, control_metadata)
    # end def test_from_properties
# end class UserDefinedPropertiesTestCase
