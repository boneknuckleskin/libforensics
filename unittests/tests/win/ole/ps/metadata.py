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

"""Unit tests for the lf.win.ole.ps.metadata module."""

# stdlib imports
import os.path
from unittest import TestCase
from uuid import UUID

# local imports
from lf.dec import RawIStream
from lf.win.ole.cfb import CompoundFile
from lf.win.ole.ps.objects import Builder
from lf.win.ole.ps.metadata import (
    PropertySetMetadata, PropertiesMetadata
)

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertySetMetadataTestCase", "PropertiesMetadataTestCase"
]

class PropertySetMetadataTestCase(TestCase):
    def test_from_property_set(self):
        ae = self.assertEqual

        blair_path = os.path.join("data", "doc", "blair.doc")
        sample_path = os.path.join("data", "doc", "sample.doc")

        blair_cfb = CompoundFile(RawIStream(blair_path))
        sample_cfb = CompoundFile(RawIStream(sample_path))

        blair_si = Builder.build(blair_cfb.get_stream(3))
        blair_dsi = Builder.build(blair_cfb.get_stream(4))

        sample_si = Builder.build(sample_cfb.get_stream(39))
        sample_dsi = Builder.build(sample_cfb.get_stream(40))

        blair_si_metadata = PropertySetMetadata.from_property_set(blair_si)
        blair_dsi_metadata = PropertySetMetadata.from_property_set(blair_dsi)

        sample_si_metadata = PropertySetMetadata.from_property_set(sample_si)
        sample_dsi_metadata = PropertySetMetadata.from_property_set(sample_dsi)

        ae(blair_si_metadata.byte_order, blair_si.byte_order)
        ae(blair_si_metadata.version, blair_si.version)
        ae(blair_si_metadata.sys_id, blair_si.sys_id)
        ae(blair_si_metadata.clsid, blair_si.clsid)
        ae(
            blair_si_metadata.fmtid0,
            UUID("f29f85e0-4ff9-1068-ab91-08002b27b3d9")
        )
        ae(blair_si_metadata.fmtid1, None)

        ae(blair_dsi_metadata.byte_order, blair_dsi.byte_order)
        ae(blair_dsi_metadata.version, blair_dsi.version)
        ae(blair_dsi_metadata.sys_id, blair_dsi.sys_id)
        ae(blair_dsi_metadata.clsid, blair_dsi.clsid)
        ae(
            blair_dsi_metadata.fmtid0,
            UUID("d5cdd502-2e9c-101b-9397-08002b2cf9ae")
        )
        ae(
            blair_dsi_metadata.fmtid1,
            UUID("d5cdd505-2e9c-101b-9397-08002b2cf9ae")
        )

        ae(sample_si_metadata.byte_order, sample_si.byte_order)
        ae(sample_si_metadata.version, sample_si.version)
        ae(sample_si_metadata.sys_id, sample_si.sys_id)
        ae(sample_si_metadata.clsid, sample_si.clsid)
        ae(
            sample_si_metadata.fmtid0,
            UUID("f29f85e0-4ff9-1068-ab91-08002b27b3d9")
        )
        ae(sample_si_metadata.fmtid1, None)


        ae(sample_dsi_metadata.byte_order, sample_dsi.byte_order)
        ae(sample_dsi_metadata.version, sample_dsi.version)
        ae(sample_dsi_metadata.sys_id, sample_dsi.sys_id)
        ae(sample_dsi_metadata.clsid, sample_dsi.clsid)
        ae(
            sample_dsi_metadata.fmtid0,
            UUID("d5cdd502-2e9c-101b-9397-08002b2cf9ae")
        )
        ae(
            sample_dsi_metadata.fmtid1,
            UUID("d5cdd505-2e9c-101b-9397-08002b2cf9ae")
        )
    # end def test_from_property_set
# end class PropertySetMetadataTestCase

class PropertiesMetadataTestCase(TestCase):
    def test_from_properties(self):
        ae = self.assertEqual

        blair_path = os.path.join("data", "doc", "blair.doc")
        sample_path = os.path.join("data", "doc", "sample.doc")

        blair_cfb = CompoundFile(RawIStream(blair_path))
        sample_cfb = CompoundFile(RawIStream(sample_path))

        blair_si = Builder.build(blair_cfb.get_stream(3))
        blair_dsi = Builder.build(blair_cfb.get_stream(4))

        sample_si = Builder.build(sample_cfb.get_stream(39))
        sample_dsi = Builder.build(sample_cfb.get_stream(40))


        blair_si_metadata = PropertiesMetadata.from_properties(
            blair_si.property_set_0.properties
        )
        blair_dsi_metadata_0 = PropertiesMetadata.from_properties(
            blair_dsi.property_set_0.properties
        )
        blair_dsi_metadata_1 = PropertiesMetadata.from_properties(
            blair_dsi.property_set_1.properties
        )

        sample_si_metadata = PropertiesMetadata.from_properties(
            sample_si.property_set_0.properties
        )
        sample_dsi_metadata_0 = PropertiesMetadata.from_properties(
            sample_dsi.property_set_0.properties
        )
        sample_dsi_metadata_1 = PropertiesMetadata.from_properties(
            sample_dsi.property_set_1.properties
        )


        ae(blair_si_metadata.code_page, 0x4E4)
        ae(blair_si_metadata.dictionary, None)
        ae(blair_si_metadata.locale, None)
        ae(blair_si_metadata.behavior, None)
        ae(blair_si_metadata.attr_exists, set(["code_page"]))

        ae(blair_dsi_metadata_0.code_page, 0x4E4)
        ae(blair_dsi_metadata_0.dictionary, None)
        ae(blair_dsi_metadata_0.locale, None)
        ae(blair_dsi_metadata_0.behavior, None)
        ae(blair_dsi_metadata_0.attr_exists, set(["code_page"]))

        ae(blair_dsi_metadata_1.code_page, 0x4E4)
        ae(blair_dsi_metadata_1.dictionary, { 2: "_PID_GUID" })
        ae(blair_dsi_metadata_1.locale, None)
        ae(blair_dsi_metadata_1.behavior, None)
        ae(blair_dsi_metadata_1.attr_exists, set(["dictionary", "code_page"]))


        ae(sample_si_metadata.code_page, 0x4E4)
        ae(sample_si_metadata.dictionary, None)
        ae(sample_si_metadata.locale, None)
        ae(sample_si_metadata.behavior, None)
        ae(sample_si_metadata.attr_exists, set(["code_page"]))

        ae(sample_dsi_metadata_0.code_page, 0x4E4)
        ae(sample_dsi_metadata_0.dictionary, None)
        ae(sample_dsi_metadata_0.locale, None)
        ae(sample_dsi_metadata_0.behavior, None)
        ae(sample_dsi_metadata_0.attr_exists, set(["code_page"]))

        ae(sample_dsi_metadata_1.code_page, 0x4E4)
        ae(sample_dsi_metadata_1.dictionary,
            {
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
            }
        )
        ae(sample_dsi_metadata_1.locale, None)
        ae(sample_dsi_metadata_1.behavior, None)
        ae(sample_dsi_metadata_1.attr_exists, set(["dictionary", "code_page"]))
    # end def test_from_properties
# end class PropertiesMetadataTestCase
