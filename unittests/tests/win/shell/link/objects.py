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

"""Unit tests for the lf.win.shell.link.objects module."""


# stdlib imports
from io import BytesIO
from uuid import UUID
from unittest import TestCase
from os.path import join

# local imports
from lf.dec import ByteIStream, RawIStream
from lf.time import FILETIMETodatetime
from lf.win.objects import LCID, GUIDToUUID
from lf.win.con.objects import COORD
from lf.win.shell.objects import SHITEMID, ITEMIDLIST
from lf.win.shell.link.ctypes import (
    file_attributes, link_flags, shell_link_header, domain_relative_obj_id
)
from lf.win.shell.link.objects import (
    ShellLink, FileAttributes, LinkFlags, ShellLinkHeader, StringData,
    LinkInfo, VolumeID, CNRL, ExtraDataBlock, ConsoleProps, ConsoleFEProps,
    DarwinProps, ExpandableStringsDataBlock, EnvironmentProps,
    IconEnvironmentProps, KnownFolderProps, PropertyStoreProps, ShimProps,
    SpecialFolderProps, DomainRelativeObjId, TrackerProps,
    VistaAndAboveIDListProps, TerminalBlock, ExtraDataBlockFactory,
    StringDataSet
)

__docformat__ = "restructuredtext en"
__all__ = [
    "ShellLinkHeaderTestCase", "FileAttributesTestCase", "LinkFlagsTestCase",
    "LinkInfoTestCase", "VolumeIDTestCase", "CNRLTestCase",
    "StringDataTestCase", "ExtraDataBlockTestCase", "ConsolePropsTestCase",
    "ConsoleFEPropsTestCase", "DarwinPropsTestCase",
    "ExpandableStringsDataBlockTestCase", "EnvironmentPropsTestCase",
    "IconEnvironmentPropsTestCase", "KnownFolderPropsTestCase",
    "PropertyStorePropsTestCase", "ShimPropsTestCase",
    "SpecialFolderPropsTestCase", "DomainRelativeObjIdTestCase",
    "TrackerPropsTestCase", "VistaAndAboveIDListPropsTestCase",
    "TerminalBlockTestCase", "ExtraDataBlockFactoryTestCase"
]

class StringDataTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        # good size, good data format, is_unicode = True
        stream = ByteIStream(b"\x04\x00a\x00b\x00c\x00d\x00")
        sd1 = StringData.from_stream(stream, is_unicode=True)
        sd2 = StringData.from_stream(stream, 0, True)

        ae(sd1.size, 10)
        ae(sd2.size, 10)
        ae(sd1.char_count, 4)
        ae(sd1.string, "abcd")
        ae(sd2.char_count, 4)
        ae(sd2.string, "abcd")


        # good size, good data format, is_unicode = False
        stream = ByteIStream(b"\x04\x00a\x01cd")
        sd1 = StringData.from_stream(stream, is_unicode=False)
        sd2 = StringData.from_stream(stream, 0, False)

        ae(sd1.size, 6)
        ae(sd2.size, 6)
        ae(sd1.char_count, 4)
        ae(sd1.string, b"a\x01cd")
        ae(sd2.char_count, 4)
        ae(sd2.string, b"a\x01cd")


        # good size, bad data format, is_unicode = True
        stream = ByteIStream(b"\x02\x00\x00\xD8\x00\xD8")
        sd1 = StringData.from_stream(stream, is_unicode=True)
        sd2 = StringData.from_stream(stream, 0, True)

        ae(sd1.size, 6)
        ae(sd2.size, 6)
        ae(sd1.char_count, 2)
        ae(sd1.string, "\x00")
        ae(sd2.char_count, 2)
        ae(sd2.string, "\x00")


        # good size, bad data format, is_unicode = False
        stream = ByteIStream(b"\x02\x00\x00\xD8\x00\xD8")
        sd1 = StringData.from_stream(stream, is_unicode=False)
        sd2 = StringData.from_stream(stream, 0, is_unicode=False)

        ae(sd1.size, 4)
        ae(sd2.size, 4)
        ae(sd1.char_count, 2)
        ae(sd1.string, b"\x00\xD8")
        ae(sd2.char_count, 2)
        ae(sd2.string, b"\x00\xD8")


        # bad size, good data format, is_unicode = True
        stream = ByteIStream(b"\x04\x00a\x01")
        sd1 = StringData.from_stream(stream, is_unicode=True)
        sd2 = StringData.from_stream(stream, 0, True)

        ae(sd1.size, 10)
        ae(sd2.size, 10)
        ae(sd1.char_count, 4)
        ae(sd1.string, "\u0161")
        ae(sd2.char_count, 4)
        ae(sd2.string, "\u0161")


        # bad size, good data format, is_unicode = False
        stream = ByteIStream(b"\x04\x00a\x01")
        sd1 = StringData.from_stream(stream, is_unicode=False)
        sd2 = StringData.from_stream(stream, 0, False)

        ae(sd1.size, 6)
        ae(sd2.size, 6)
        ae(sd1.char_count, 4)
        ae(sd1.string, b"a\x01")
        ae(sd2.char_count, 4)
        ae(sd2.string, b"a\x01")


        # bad size, bad data format, is_unicode = True
        stream = ByteIStream(b"\x04\x00\x00\xD8")
        sd1 = StringData.from_stream(stream, is_unicode=True)
        sd2 = StringData.from_stream(stream, 0, True)

        ae(sd1.size, 10)
        ae(sd2.size, 10)
        ae(sd1.char_count, 4)
        ae(sd1.string, b"\x00\xD8")
        ae(sd2.char_count, 4)
        ae(sd2.string, b"\x00\xD8")


        # bad size, bad data format, is_unicode = False
        stream = ByteIStream(b"\x04\x00\x00\xD8")
        sd1 = StringData.from_stream(stream, is_unicode=False)
        sd2 = StringData.from_stream(stream, 0, False)

        ae(sd1.size, 6)
        ae(sd2.size, 6)
        ae(sd1.char_count, 4)
        ae(sd1.string, b"\x00\xD8")
        ae(sd2.char_count, 4)
        ae(sd2.string, b"\x00\xD8")
    # end def test_from_stream
# end class StringDataTestCase

class FileAttributesTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        attrs = FileAttributes.from_stream(ByteIStream(b"\x55\x55\x55\x55"))
        ae(attrs.read_only, 1)
        ae(attrs.hidden, 0)
        ae(attrs.system, 1)
        ae(attrs.directory, 1)
        ae(attrs.archive, 0)
        ae(attrs.normal, 0)
        ae(attrs.temp, 1)
        ae(attrs.sparse, 0)
        ae(attrs.reparse_point, 1)
        ae(attrs.compressed, 0)
        ae(attrs.offline, 1)
        ae(attrs.not_content_indexed, 0)
        ae(attrs.encrypted, 1)

        attrs = FileAttributes.from_stream(ByteIStream(b"\xAA\xAA\xAA\xAA"))
        ae(attrs.read_only, 0)
        ae(attrs.hidden, 1)
        ae(attrs.system, 0)
        ae(attrs.directory, 0)
        ae(attrs.archive, 1)
        ae(attrs.normal, 1)
        ae(attrs.temp, 0)
        ae(attrs.sparse, 1)
        ae(attrs.reparse_point, 0)
        ae(attrs.compressed, 1)
        ae(attrs.offline, 0)
        ae(attrs.not_content_indexed, 1)
        ae(attrs.encrypted, 0)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        ctype = file_attributes.from_buffer_copy(b"\x55\x55\x55\x55")
        attrs = FileAttributes.from_ctype(ctype)
        ae(attrs.read_only, 1)
        ae(attrs.hidden, 0)
        ae(attrs.system, 1)
        ae(attrs.directory, 1)
        ae(attrs.archive, 0)
        ae(attrs.normal, 0)
        ae(attrs.temp, 1)
        ae(attrs.sparse, 0)
        ae(attrs.reparse_point, 1)
        ae(attrs.compressed, 0)
        ae(attrs.offline, 1)
        ae(attrs.not_content_indexed, 0)
        ae(attrs.encrypted, 1)

        ctype = file_attributes.from_buffer_copy(b"\xAA\xAA\xAA\xAA")
        attrs = FileAttributes.from_ctype(ctype)
        ae(attrs.read_only, 0)
        ae(attrs.hidden, 1)
        ae(attrs.system, 0)
        ae(attrs.directory, 0)
        ae(attrs.archive, 1)
        ae(attrs.normal, 1)
        ae(attrs.temp, 0)
        ae(attrs.sparse, 1)
        ae(attrs.reparse_point, 0)
        ae(attrs.compressed, 1)
        ae(attrs.offline, 0)
        ae(attrs.not_content_indexed, 1)
        ae(attrs.encrypted, 0)
    # end def test_from_ctype
# end class FileAttributesTestCase

class LinkFlagsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(b"\x55\x55\x55\x55")
        flags = LinkFlags.from_stream(stream)
        ae(flags.has_idlist, 1)
        ae(flags.has_link_info, 0)
        ae(flags.has_name, 1)
        ae(flags.has_relative_path, 0)
        ae(flags.has_working_dir, 1)
        ae(flags.has_args, 0)
        ae(flags.has_icon_location, 1)
        ae(flags.is_unicode, 0)
        ae(flags.force_no_link_info, 1)
        ae(flags.has_exp_string, 0)
        ae(flags.run_in_separate_proc, 1)
        ae(flags.has_logo3_id, 0)
        ae(flags.has_darwin_id, 1)
        ae(flags.run_as_user, 0)
        ae(flags.has_exp_icon, 1)
        ae(flags.no_pidl_alias, 0)
        ae(flags.force_unc_name, 1)
        ae(flags.run_with_shim_layer, 0)
        ae(flags.force_no_link_track, 1)
        ae(flags.enable_target_metadata, 0)
        ae(flags.disable_link_path_tracking, 1)
        ae(flags.disable_known_folder_rel_tracking, 0)
        ae(flags.no_kf_alias, 1)
        ae(flags.allow_link_to_link, 0)
        ae(flags.unalias_on_save, 1)
        ae(flags.prefer_environment_path, 0)
        ae(flags.keep_local_idlist_for_unc_target, 1)

        stream = ByteIStream(b"\xAA\xAA\xAA\xAA")
        flags = LinkFlags.from_stream(stream)
        ae(flags.has_idlist, 0)
        ae(flags.has_link_info, 1)
        ae(flags.has_name, 0)
        ae(flags.has_relative_path, 1)
        ae(flags.has_working_dir, 0)
        ae(flags.has_args, 1)
        ae(flags.has_icon_location, 0)
        ae(flags.is_unicode, 1)
        ae(flags.force_no_link_info, 0)
        ae(flags.has_exp_string, 1)
        ae(flags.run_in_separate_proc, 0)
        ae(flags.has_logo3_id, 1)
        ae(flags.has_darwin_id, 0)
        ae(flags.run_as_user, 1)
        ae(flags.has_exp_icon, 0)
        ae(flags.no_pidl_alias, 1)
        ae(flags.force_unc_name, 0)
        ae(flags.run_with_shim_layer, 1)
        ae(flags.force_no_link_track, 0)
        ae(flags.enable_target_metadata, 1)
        ae(flags.disable_link_path_tracking, 0)
        ae(flags.disable_known_folder_rel_tracking, 1)
        ae(flags.no_kf_alias, 0)
        ae(flags.allow_link_to_link, 1)
        ae(flags.unalias_on_save, 0)
        ae(flags.prefer_environment_path, 1)
        ae(flags.keep_local_idlist_for_unc_target, 0)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        ctype = link_flags.from_buffer_copy(b"\x55\x55\x55\x55")
        flags = LinkFlags.from_ctype(ctype)
        ae(flags.has_idlist, 1)
        ae(flags.has_link_info, 0)
        ae(flags.has_name, 1)
        ae(flags.has_relative_path, 0)
        ae(flags.has_working_dir, 1)
        ae(flags.has_args, 0)
        ae(flags.has_icon_location, 1)
        ae(flags.is_unicode, 0)
        ae(flags.force_no_link_info, 1)
        ae(flags.has_exp_string, 0)
        ae(flags.run_in_separate_proc, 1)
        ae(flags.has_logo3_id, 0)
        ae(flags.has_darwin_id, 1)
        ae(flags.run_as_user, 0)
        ae(flags.has_exp_icon, 1)
        ae(flags.no_pidl_alias, 0)
        ae(flags.force_unc_name, 1)
        ae(flags.run_with_shim_layer, 0)
        ae(flags.force_no_link_track, 1)
        ae(flags.enable_target_metadata, 0)
        ae(flags.disable_link_path_tracking, 1)
        ae(flags.disable_known_folder_rel_tracking, 0)
        ae(flags.no_kf_alias, 1)
        ae(flags.allow_link_to_link, 0)
        ae(flags.unalias_on_save, 1)
        ae(flags.prefer_environment_path, 0)
        ae(flags.keep_local_idlist_for_unc_target, 1)

        ctype = link_flags.from_buffer_copy(b"\xAA\xAA\xAA\xAA")
        flags = LinkFlags.from_ctype(ctype)
        ae(flags.has_idlist, 0)
        ae(flags.has_link_info, 1)
        ae(flags.has_name, 0)
        ae(flags.has_relative_path, 1)
        ae(flags.has_working_dir, 0)
        ae(flags.has_args, 1)
        ae(flags.has_icon_location, 0)
        ae(flags.is_unicode, 1)
        ae(flags.force_no_link_info, 0)
        ae(flags.has_exp_string, 1)
        ae(flags.run_in_separate_proc, 0)
        ae(flags.has_logo3_id, 1)
        ae(flags.has_darwin_id, 0)
        ae(flags.run_as_user, 1)
        ae(flags.has_exp_icon, 0)
        ae(flags.no_pidl_alias, 1)
        ae(flags.force_unc_name, 0)
        ae(flags.run_with_shim_layer, 1)
        ae(flags.force_no_link_track, 0)
        ae(flags.enable_target_metadata, 1)
        ae(flags.disable_link_path_tracking, 0)
        ae(flags.disable_known_folder_rel_tracking, 1)
        ae(flags.no_kf_alias, 0)
        ae(flags.allow_link_to_link, 1)
        ae(flags.unalias_on_save, 0)
        ae(flags.prefer_environment_path, 1)
        ae(flags.keep_local_idlist_for_unc_target, 0)
    # end def test_from_ctype
# end class LinkFlagsTestCase

class ExtraDataBlockTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(b"\x0A\x00\x00\x00\x01\x02\x03\x04\x64\x53")
        edb1 = ExtraDataBlock.from_stream(stream)
        edb2 = ExtraDataBlock.from_stream(stream, 0)

        ae(edb1.size, 0xA)
        ae(edb2.size, 0xA)
        ae(edb1.sig, 0x04030201)
        ae(edb2.sig, 0x04030201)
        ae(edb1.data, b"\x64\x53")
        ae(edb2.data, b"\x64\x53")


        stream = ByteIStream(b"\xFF\x00\x00\x00\x01\x02\x03\x04\x64\x53")
        edb1 = ExtraDataBlock.from_stream(stream)
        edb2 = ExtraDataBlock.from_stream(stream, 0)

        ae(edb1.size, 0xFF)
        ae(edb2.size, 0xFF)
        ae(edb1.sig, 0x04030201)
        ae(edb2.sig, 0x04030201)
        ae(edb1.data, b"\x64\x53")
        ae(edb2.data, b"\x64\x53")
    # end def test_from_stream
# end class ExtraDataBlockTestCase

class ConsolePropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(204)]))
        cp1 = ConsoleProps.from_stream(stream)
        cp2 = ConsoleProps.from_stream(stream, 0)

        for cp in (cp1, cp2):
            ae(cp.size, 0x03020100)
            ae(cp.sig, 0x07060504)
            ae(cp.fill_attributes, 0x0908)
            ae(cp.popup_fill_attributes, 0x0B0A)

            coord_data = b"\x0C\x0D\x0E\x0F"
            coord = COORD.from_stream(ByteIStream(coord_data))
            ae(cp2.screen_buffer_size, coord)

            coord_data = b"\x10\x11\x12\x13"
            coord = COORD.from_stream(ByteIStream(coord_data))
            ae(cp.window_size, coord)

            coord_data = b"\x14\x15\x16\x17"
            coord = COORD.from_stream(ByteIStream(coord_data))
            ae(cp.window_origin, coord)

            ae(cp.font, 0x1B1A1918)
            ae(cp.input_buf_size, 0x1F1E1D1C)
            ae(cp.font_size, 0x23222120)
            ae(cp.font_family, 0x27262524)
            ae(cp.font_weight, 0x2B2A2928)

            face_name = bytes([x for x in range(0x2C, 0x6C)])
            face_name = face_name.decode("utf_16_le")
            ae(cp.face_name, face_name)

            ae(cp.cursor_size, 0x6F6E6D6C)
            ae(cp.full_screen, 0x73727170)
            ae(cp.quick_edit, 0x77767574)
            ae(cp.insert_mode, 0x7B7A7978)
            ae(cp.auto_position, 0x7F7E7D7C)
            ae(cp.history_buf_size, 0x83828180)
            ae(cp.history_buf_count, 0x87868584)
            ae(cp.history_no_dup, 0x8B8A8988)

            color_table = [
                0x8F8E8D8C, 0x93929190, 0x97969594, 0x9B9A9998,
                0x9F9E9D9C, 0xA3A2A1A0, 0xA7A6A5A4, 0xABAAA9A8,
                0xAFAEADAC, 0xB3B2B1B0, 0xB7B6B5B4, 0xBBBAB9B8,
                0xBFBEBDBC, 0xC3C2C1C0, 0xC7C6C5C4, 0xCBCAC9C8,
            ]
            ae(cp.color_table, color_table)
        # end for
    # end def test_from_stream
# end class ConsolePropsTestCase

class ConsoleFEPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(12)]))
        cfep1 = ConsoleFEProps.from_stream(stream)
        cfep2 = ConsoleFEProps.from_stream(stream, 0)

        ae(cfep1.size, 0x03020100)
        ae(cfep2.size, 0x03020100)

        ae(cfep1.sig, 0x07060504)
        ae(cfep2.sig, 0x07060504)

        lcid = LCID.from_stream(ByteIStream(b"\x08\x09\x0A\x0B"))
        ae(cfep1.code_page, lcid)
        ae(cfep2.code_page, lcid)
    # end def test_from_stream
# end class ConsoleFEPropsTestCase

class DarwinPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # block size
        data.extend(b"\x04\x05\x06\x07")  # blog sig
        data.extend([0x41] * 260)  # darwin_data_ansi
        data.extend([0xEB, 0xFE] * 260)  # darwin_data_uni
        stream = ByteIStream(data)

        dp1 = DarwinProps.from_stream(stream)
        dp2 = DarwinProps.from_stream(stream, 0)

        ae(dp1.size, 0x03020100)
        ae(dp2.size, 0x03020100)

        ae(dp1.sig, 0x07060504)
        ae(dp2.sig, 0x07060504)

        ae(dp1.darwin_data_ansi, b"\x41" * 260)
        ae(dp2.darwin_data_ansi, b"\x41" * 260)

        darwin_data_uni = bytes([0xEB, 0xFE] * 260)
        darwin_data_uni = darwin_data_uni.decode("utf_16_le", "ignore")
        darwin_data_uni = darwin_data_uni.split("\x00", 1)[0]
        ae(dp1.darwin_data_uni, darwin_data_uni)
        ae(dp2.darwin_data_uni, darwin_data_uni)
    # end def test_from_stream
# end class DarwinPropsTestCase

class ExpandableStringsDataBlockTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # block size
        data.extend(b"\x04\x05\x06\x07")  # blog sig
        data.extend([0x41] * 260)  # target_ansi
        data.extend([0xEB, 0xFE] * 260)  # target_uni
        stream = ByteIStream(data)

        esdb1 = ExpandableStringsDataBlock.from_stream(stream)
        esdb2 = ExpandableStringsDataBlock.from_stream(stream, 0)

        ae(esdb1.size, 0x03020100)
        ae(esdb2.size, 0x03020100)

        ae(esdb1.sig, 0x07060504)
        ae(esdb2.sig, 0x07060504)

        ae(esdb1.target_ansi, b"\x41" * 260)
        ae(esdb2.target_ansi, b"\x41" * 260)

        target_uni = bytes([0xEB, 0xFE] * 260)
        target_uni = target_uni.decode("utf_16_le", "ignore")
        target_uni = target_uni.split("\x00", 1)[0]
        ae(esdb1.target_uni, target_uni)
        ae(esdb2.target_uni, target_uni)
    # end def test_from_stream
# end class ExpandableStringsDataBlockTestCase

class EnvironmentPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # block size
        data.extend(b"\x04\x05\x06\x07")  # blog sig
        data.extend([0x41] * 260)  # target_ansi
        data.extend([0xEB, 0xFE] * 260)  # target_uni
        stream = ByteIStream(data)

        ep1 = EnvironmentProps.from_stream(stream)
        ep2 = EnvironmentProps.from_stream(stream, 0)

        ae(ep1.size, 0x03020100)
        ae(ep2.size, 0x03020100)

        ae(ep1.sig, 0x07060504)
        ae(ep2.sig, 0x07060504)

        ae(ep1.target_ansi, b"\x41" * 260)
        ae(ep2.target_ansi, b"\x41" * 260)

        target_uni = bytes([0xEB, 0xFE] * 260)
        target_uni = target_uni.decode("utf_16_le", "ignore")
        target_uni = target_uni.split("\x00", 1)[0]
        ae(ep1.target_uni, target_uni)
        ae(ep2.target_uni, target_uni)
    # end def test_from_stream
# end class EnvironmentPropsTestCase

class IconEnvironmentPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # block size
        data.extend(b"\x04\x05\x06\x07")  # blog sig
        data.extend([0x41] * 260)  # target_ansi
        data.extend([0xEB, 0xFE] * 260)  # target_uni
        stream = ByteIStream(data)

        iep1 = IconEnvironmentProps.from_stream(stream)
        iep2 = IconEnvironmentProps.from_stream(stream, 0)

        ae(iep1.size, 0x03020100)
        ae(iep2.size, 0x03020100)

        ae(iep1.sig, 0x07060504)
        ae(iep2.sig, 0x07060504)

        ae(iep1.target_ansi, b"\x41" * 260)
        ae(iep2.target_ansi, b"\x41" * 260)

        target_uni = bytes([0xEB, 0xFE] * 260)
        target_uni = target_uni.decode("utf_16_le", "ignore")
        target_uni = target_uni.split("\x00", 1)[0]
        ae(iep1.target_uni, target_uni)
        ae(iep2.target_uni, target_uni)
    # end def test_from_stream
# end class IconEnvironmentPropsTestCase

class KnownFolderPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytes([x for x in range(28)])
        stream = ByteIStream(data)
        kfp1 = KnownFolderProps.from_stream(stream)
        kfp2 = KnownFolderProps.from_stream(stream, 0)

        ae(kfp1.size, 0x03020100)
        ae(kfp2.size, 0x03020100)

        ae(kfp1.sig, 0x07060504)
        ae(kfp2.sig, 0x07060504)

        kf_id = GUIDToUUID.from_stream(ByteIStream(data[8:24]))
        ae(kfp1.kf_id, kf_id)
        ae(kfp2.kf_id, kf_id)

        ae(kfp1.offset, 0x1B1A1918)
        ae(kfp2.offset, 0x1B1A1918)
    # end def test_from_stream
# end class KnownFolderPropsTestCase

class PropertyStorePropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x10\x00\x00\x00")  # block size
        data.extend(b"\x00\x01\x02\x03")  # block sig
        data.extend(b"\x04\x05\x06\x07\x08\x09\x0A\x0B")  # data
        stream = ByteIStream(data)

        psp1 = PropertyStoreProps.from_stream(stream)
        psp2 = PropertyStoreProps.from_stream(stream, 0)

        ae(psp1.size, 0x10)
        ae(psp2.size, 0x10)

        ae(psp1.sig, 0x03020100)
        ae(psp2.sig, 0x03020100)

        ae(psp1.property_store, b"\x04\x05\x06\x07\x08\x09\x0A\x0B")
        ae(psp2.property_store, b"\x04\x05\x06\x07\x08\x09\x0A\x0B")
    # end def test_from_stream
# end class PropertyStorePropsTestCase

class ShimPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(b"\x0A\x00\x00\x00\x01\x02\x03\x04\x64\x53")
        sp1 = ShimProps.from_stream(stream)
        sp2 = ShimProps.from_stream(stream, 0)

        ae(sp1.size, 0xA)
        ae(sp2.size, 0xA)
        ae(sp1.sig, 0x04030201)
        ae(sp2.sig, 0x04030201)
        ae(sp1.layer_name, "\u5364")
        ae(sp2.layer_name, "\u5364")


        stream = ByteIStream(b"\xFF\x00\x00\x00\x01\x02\x03\x04\x64\x53")
        sp1 = ShimProps.from_stream(stream)
        sp2 = ShimProps.from_stream(stream, 0)

        ae(sp1.size, 0xFF)
        ae(sp2.size, 0xFF)
        ae(sp1.sig, 0x04030201)
        ae(sp2.sig, 0x04030201)
        ae(sp1.layer_name, "\u5364")
        ae(sp2.layer_name, "\u5364")
    # end def test_from_stream
# end class ShimPropsTestCase

class SpecialFolderPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(bytes([x for x in range(16)]))
        sfp1 = SpecialFolderProps.from_stream(stream)
        sfp2 = SpecialFolderProps.from_stream(stream, 0)

        ae(sfp1.size, 0x03020100)
        ae(sfp2.size, 0x03020100)

        ae(sfp1.sig, 0x07060504)
        ae(sfp2.sig, 0x07060504)

        ae(sfp1.sf_id, 0x0B0A0908)
        ae(sfp2.sf_id, 0x0B0A0908)

        ae(sfp1.offset, 0x0F0E0D0C)
        ae(sfp2.offset, 0x0F0E0D0C)
    # end def test_from_stream
# end class SpecialFolderPropsTestCase

class DomainRelativeObjIdTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(bytes([x for x in range(16)]))  # volume
        data.extend(bytes([x for x in range(15, -1, -1)]))  # object
        stream = ByteIStream(data)

        droid1 = DomainRelativeObjId.from_stream(stream)
        droid2 = DomainRelativeObjId.from_stream(stream, 0)

        ae(droid1.volume, UUID(bytes_le=data[:16]))
        ae(droid2.volume, UUID(bytes_le=data[:16]))

        ae(droid1.object, UUID(bytes_le=data[16:]))
        ae(droid2.object, UUID(bytes_le=data[16:]))
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(bytes([x for x in range(16)]))
        data.extend(bytes([x for x in range(15, -1, -1)]))
        droid = domain_relative_obj_id.from_buffer_copy(data)
        droid = DomainRelativeObjId.from_ctype(droid)

        ae(droid.volume, UUID(bytes_le=data[:16]))
        ae(droid.object, UUID(bytes_le=data[16:]))
    # end def test_from_ctype
# end class DomainRelativeObjIdTestCase

class TrackerPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # block size
        data.extend(b"\x04\x05\x06\x07")  # block sig
        data.extend(b"\x50\x00\x00\x00")  # length
        data.extend(b"\x0B\x0A\x09\x08")  # version
        data.extend(b"abcdefgh")  # machine_id
        data.extend(bytes([x for x in range(32)]))
        data.extend(bytes([x for x in range(31, -1, -1)]))
        stream = ByteIStream(data)

        tp1 = TrackerProps.from_stream(stream)
        tp2 = TrackerProps.from_stream(stream, 0)

        ae(tp1.size, 0x03020100)
        ae(tp2.size, 0x03020100)

        ae(tp1.sig, 0x07060504)
        ae(tp2.sig, 0x07060504)

        ae(tp1.length, 0x50)
        ae(tp2.length, 0x50)

        ae(tp1.machine_id, b"abcdefgh")
        ae(tp2.machine_id, b"abcdefgh")

        droid_stream = ByteIStream(data[24:56])
        droid = DomainRelativeObjId.from_stream(droid_stream)
        ae(tp1.droid, droid)
        ae(tp2.droid, droid)

        droid_stream = ByteIStream(data[56:])
        droid = DomainRelativeObjId.from_stream(droid_stream)
        ae(tp1.droid_birth, droid)
        ae(tp2.droid_birth, droid)
    # end def test_from_stream
# end class TrackerPropsTestCase

class VistaAndAboveIDListPropsTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        item1 = b"\x06\x00\x01\x02\x03\x04"
        item2 = b"\x05\x00\x05\x06\x07"
        item3 = b"\x04\x00\x08\x09"
        little_item = b"\x01\x00"
        big_item = b"\xFF\x00\x64\x53"
        null_item = b"\x00\x00"

        itemid1 = SHITEMID((6, 6, b"\x01\x02\x03\x04"))
        itemid2 = SHITEMID((5, 5, b"\x05\x06\x07"))
        itemid3 = SHITEMID((4, 4, b"\x08\x09"))
        little_itemid = SHITEMID((2, 1, None))
        big_itemid = SHITEMID((2, 0xFF, b"\x64\x53"))
        null_itemid = SHITEMID((2, 0, None))


        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # block size
        data.extend(b"\x04\x05\x06\x07")  # block signature
        data.extend(b"".join([item1, item2, item3, null_item]))
        stream = ByteIStream(data)

        vaaidlp1 = VistaAndAboveIDListProps.from_stream(stream)
        vaaidlp2 = VistaAndAboveIDListProps.from_stream(stream, 0)

        ae(vaaidlp1.size, 0x03020100)
        ae(vaaidlp2.size, 0x03020100)

        ae(vaaidlp1.sig, 0x07060504)
        ae(vaaidlp2.sig, 0x07060504)

        id_list = [itemid1, itemid2, itemid3, null_itemid]
        ae(vaaidlp1.idlist.mkid, id_list)
        ae(vaaidlp2.idlist.mkid, id_list)
    # end def test_from_stream
# end class VistaAndAboveIDLisPropsTestCase

class TerminalBlockTestCase(TestCase):
    def test__init__(self):
        ae = self.assertEqual

        tb = TerminalBlock((0, None))
        ae(tb.size, 0)
        ae(tb.sig, None)
    # end def test__init__
# end class TerminalBlockTestCase

class ExtraDataBlockFactoryTestCase(TestCase):
    def test_make_blocks(self):
        ae = self.assertEqual

        # This will hold the entire stream of blocks.
        data = bytearray()


        # Make the ConsoleProps
        console_props_data = bytearray()

        # block size
        console_props_data.extend(b"\xCC\x00\x00\x00")

        # block signature
        console_props_data.extend(b"\x02\x00\x00\xA0")

        # fill attributes (bright green on black)
        console_props_data.extend(b"\x0A\x00")

        # popup fill attributes (bright red on bright green)
        console_props_data.extend(b"\xB4\x00")

        # screen buffer size (x,y)
        console_props_data.extend(b"\x64\x53\xEB\xFE")

        # window size (x,y)
        console_props_data.extend(b"\x41\x41\x42\x42")

        # window origin (x, y)
        console_props_data.extend(b"\xAD\xBA\x0D\xF0")

        # font
        console_props_data.extend(b"\xAA\xBB\xCC\xDD")

        # input_buf_size
        console_props_data.extend(b"\xFF\xFF\x00\x00")

        # Font size
        console_props_data.extend(b"\x10\x00\x00\x00")

        # Font family (modern)
        console_props_data.extend(b"\x30\x00\x00\x00")

        # Font weight (bold)
        console_props_data.extend(b"\x35\x19\x00\x00")

        # Face name
        face_name = "thisisnotthedatayouarelookingfor"
        console_props_data.extend(face_name.encode("utf_16_le"))

        # Cursor size (medium)
        console_props_data.extend(b"\x1A\x00\x00\x00")

        # Full screen (yes)
        console_props_data.extend(b"\x01\x00\x00\x00")

        # Quick edit (yes)
        console_props_data.extend(b"\x08\x00\x00\x00")

        # Insert mode (yes)
        console_props_data.extend(b"\x98\xBA\xDC\xFE")

        # Auto position (yes)
        console_props_data.extend(b"\x02\x00\x00\x00")

        # History buffer size
        console_props_data.extend(b"\xFF\x00\x00\x00")

        # Number of history buffers
        console_props_data.extend(b"\x04\x00\x00\x00")

        # HistoryNoDup (duplicates allowed)
        console_props_data.extend(b"\x03\x00\x00\x00")

        # Color table
        console_props_data.extend([(x % 256) for x in range(1000, 1064)])

        console_props = \
            ConsoleProps.from_stream(ByteIStream(console_props_data))


        # Make the ConsoleFEProps
        console_fe_props_data = bytearray()
        console_fe_props_data.extend(b"\x0C\x00\x00\x00")  # block size
        console_fe_props_data.extend(b"\x04\x00\x00\xA0")  # block signature
        console_fe_props_data.extend(b"\x04\x04\x04\x00")  # LCID (zh-TW_radstr)
        console_fe_props = \
            ConsoleFEProps.from_stream(ByteIStream(console_fe_props_data))


        # Make the DarwinProps
        darwin_props_data = bytearray()

        # block size
        darwin_props_data.extend(b"\x14\x03\x00\x00")

        # block signature
        darwin_props_data.extend(b"\x06\x00\x00\xA0")

        # Darwin data ANSI
        darwin_props_data.extend(b"".join([b"\x41" * 259, b"\x00"]))

        # Darwin data unicode
        darwin_props_data.extend(b"".join([b"\x41\x00" * 259, b"\x00\x00"]))

        darwin_props = DarwinProps.from_stream(ByteIStream(darwin_props_data))


        # Make the EnvironmentProps
        environment_props_data = bytearray()

        # block size
        environment_props_data.extend(b"\x14\x03\x00\x00")

        # block signature
        environment_props_data.extend(b"\x01\x00\x00\xA0")

        # Target ANSI
        environment_props_data.extend(b"".join([b"\x41" * 259, b"\x00"]))

        # Target unicode
        environment_props_data.extend(b"\x41\x00" * 260)
        environment_props = EnvironmentProps.from_stream(ByteIStream(
            environment_props_data
        ))


        # Make the IconEnvironmentProps
        icon_environment_props_data = bytearray()

        # block size
        icon_environment_props_data.extend(b"\x14\x03\x00\x00")

        # block signature
        icon_environment_props_data.extend(b"\x07\x00\x00\xA0")

        # Target ANSI
        icon_environment_props_data.extend(b"".join([b"\x41" * 259, b"\x00"]))

        # Target unicode
        icon_environment_props_data.extend(b"\x41\x00" * 260)

        icon_environment_props = IconEnvironmentProps.from_stream(
            ByteIStream(icon_environment_props_data)
        )


        # Make the KnownFolderProps
        known_folder_props_data = bytearray()
        known_folder_props_data.extend(b"\x1C\x00\x00\x00")  # block size
        known_folder_props_data.extend(b"\x0B\x00\x00\xA0")  # block signature
        known_folder_props_data.extend([x for x in range(16)])  # kf_id
        known_folder_props_data.extend(b"\x01\x02\x03\x04")  # offset
        known_folder_props = \
            KnownFolderProps.from_stream(ByteIStream(known_folder_props_data))


        # Make the PropertyStoreProps
        property_store_props_data = bytearray()

        # block size
        property_store_props_data.extend(b"\x10\x00\x00\x00")

        # block signature
        property_store_props_data.extend(b"\x09\x00\x00\xA0")

        # property store
        property_store_props_data.extend([x for x in range(32, 40)])

        property_store_props = PropertyStoreProps.from_stream(
            ByteIStream(property_store_props_data)
        )


        # Make the ShimProps
        shim_props_data = bytearray()
        shim_props_data.extend(b"\x90\x00\x00\x00")  # block size
        shim_props_data.extend(b"\x08\x00\x00\xA0")  # block signature
        shim_props_data.extend(b"a\x00b\x00c\x00d\x00" * 17)  # layer name
        shim_props = ShimProps.from_stream(ByteIStream(shim_props_data))


        # Make the SpecialFolderProps
        special_folder_props_data = bytearray()
        special_folder_props_data.extend(b"\x10\x00\x00\x00")  # block size
        special_folder_props_data.extend(b"\x05\x00\x00\xA0")  # block signature
        special_folder_props_data.extend(b"\x53\x64\x53\x64")  # sf_id
        special_folder_props_data.extend(b"\x32\x54\x76\x98")  # offset
        special_folder_props = SpecialFolderProps.from_stream(
            ByteIStream(special_folder_props_data)
        )


        # Make the TrackerProps
        tracker_props_data = bytearray()
        tracker_props_data.extend(b"\x60\x00\x00\x00")  # block size
        tracker_props_data.extend(b"\x03\x00\x00\xA0")  # block signature
        tracker_props_data.extend(b"\x58\x00\x00\x00")  # length
        tracker_props_data.extend(b"\x00\x00\x00\x00")  # version
        tracker_props_data.extend(b"0123456789012345")  # machine id
        tracker_props_data.extend([x for x in range(128, 160)])  # droid
        tracker_props_data.extend([x for x in range(160, 192)])  # droid birth
        tracker_props = \
            TrackerProps.from_stream(ByteIStream(tracker_props_data))


        # Make the VistaAndAboveIDListProps
        item1 = b"\x05\x00\x0A\x0B\x0C"
        item2 = b"\x03\x00\xFF"
        null_item = b"\x00\x00"
        id_list = b"".join([item1, item2, null_item])

        vista_and_above_id_list_props_data = bytearray()

        # block size
        vista_and_above_id_list_props_data.extend(b"\x12\x00\x00\x00")

        # block signature
        vista_and_above_id_list_props_data.extend(b"\x0C\x00\x00\xA0")

        # id list
        vista_and_above_id_list_props_data.extend(id_list)

        vista_and_above_id_list_props = VistaAndAboveIDListProps.from_stream(
            ByteIStream(vista_and_above_id_list_props_data)
        )


        data = bytearray()
        data.extend(b"".join([
            console_props_data,
            console_fe_props_data,
            darwin_props_data,
            environment_props_data,
            icon_environment_props_data,
            known_folder_props_data,
            property_store_props_data,
            shim_props_data,
            special_folder_props_data,
            tracker_props_data,
            vista_and_above_id_list_props_data
        ]))

        stream = ByteIStream(data)

        ref_properties = [
            console_props,
            console_fe_props,
            darwin_props,
            environment_props,
            icon_environment_props,
            known_folder_props,
            property_store_props,
            shim_props,
            special_folder_props,
            tracker_props,
            vista_and_above_id_list_props
        ]
        test_properties = list(ExtraDataBlockFactory.make_blocks(stream))
        ae(test_properties, ref_properties)
    # end def test_make_blocks
# end class ExtraDataBlockFactoryTestCase

class ShellLinkTestCase(TestCase):
    def test__init__(self):
        ae = self.assertEqual

        filename0 = join("data", "lnk", "shortcut_to_local_exe.lnk")
        filename1 = join("data", "lnk", "shortcut_to_mapped_exe.lnk")

        stream0 = RawIStream(filename0)
        stream1 = RawIStream(filename1)

        sl0 = ShellLink(stream0)
        sl1 = ShellLink(stream0, 0)

        sl2 = ShellLink(stream1)
        sl3 = ShellLink(stream1, 0)

        header0 = ShellLinkHeader.from_stream(stream0, 0)
        header1 = ShellLinkHeader.from_stream(stream1, 0)
        ae(sl0.header, header0)
        ae(sl1.header, header0)
        ae(sl2.header, header1)
        ae(sl3.header, header1)

        idlist0 = ITEMIDLIST.from_stream(stream0, 78)
        ae(sl0.idlist, idlist0)
        ae(sl1.idlist, idlist0)
        ae(sl2.idlist, None)
        ae(sl3.idlist, None)

        li0 = LinkInfo.from_stream(stream0, 285)
        li1 = LinkInfo.from_stream(stream1, 76)
        ae(sl0.link_info, li0)
        ae(sl1.link_info, li0)
        ae(sl2.link_info, li1)
        ae(sl3.link_info, li1)

        sds0 = StringDataSet((
            StringData((16, 7, "comment")),
            StringData((52, 25, "..\\..\\..\\Windows\PING.EXE")),
            StringData((32, 15, "c:\\start-in-dir")),
            StringData((30, 14, "arg1 arg2 arg3")),
            StringData((68, 33, "%SystemRoot%\\system32\\SHELL32.dll"))
        ))

        sds1 = StringDataSet((
            None,
            None,
            StringData((40, 19, "X:\\windows\\system32")),
            None,
            None
        ))

        ae(sl0.string_data, sds0)
        ae(sl1.string_data, sds0)
        ae(sl2.string_data, sds1)
        ae(sl3.string_data, sds1)

        edbs0 = list(ExtraDataBlockFactory.make_blocks(stream0, 549))
        edbs1 = list(ExtraDataBlockFactory.make_blocks(stream1, 217))
        ae(sl0.extra_data, edbs0)
        ae(sl1.extra_data, edbs0)
        ae(sl2.extra_data, edbs1)
        ae(sl3.extra_data, edbs1)
    # end def test__init__
# end class ShellLinkTestCase

class LinkInfoTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        ain = self.assertIsNone
        ainn = self.assertIsNotNone

        data0 = bytearray()

        # link info header
        data0.extend(b"\x78\x00\x00\x00")  # link info size
        data0.extend(b"\x24\x00\x00\x00")  # link info header size
        data0.extend(b"\x13\x00\x00\x00")  # link info flags
        data0.extend(b"\x24\x00\x00\x00")  # volume id offset
        data0.extend(b"\x3C\x00\x00\x00")  # local base path offset
        data0.extend(b"\x40\x00\x00\x00")  # cnrl offset
        data0.extend(b"\x6C\x00\x00\x00")  # common path suffix offset
        data0.extend(b"\x70\x00\x00\x00")  # local base path offset unicode
        data0.extend(b"\x74\x00\x00\x00")  # comon path suffix offset unicode

        # volume id
        data0.extend(b"\x18\x00\x00\x00")  # volume id size
        data0.extend(b"\x01\x02\x03\x04")  # drive type
        data0.extend(b"\x05\x06\x07\x08")  # drive serial number
        data0.extend(b"\x14\x00\x00\x00")  # volume label offset
        data0.extend(b"\x14\x00\x00\x00")
        data0.extend(b"d\x00\x00\x00")  # data

        # local base path
        data0.extend(b"ijk\x00")

        # cnrl
        data0.extend(b"\x2C\x00\x00\x00")  # cnrl size
        data0.extend(b"\x03\x00\x00\x00")  # cnrl flags
        data0.extend(b"\x1C\x00\x00\x00")  # net name offset
        data0.extend(b"\x20\x00\x00\x00")  # device name offset
        data0.extend(b"\x64\x53\x64\x53")  # network provider type
        data0.extend(b"\x24\x00\x00\x00")  # net name offset unicode
        data0.extend(b"\x28\x00\x00\x00")  # device name offset unicode
        data0.extend(b"abc\x00")  # net name
        data0.extend(b"def\x00")  # device name
        data0.extend(b"g\x00\x00\x00")  # net name unicode
        data0.extend(b"h\x00\x00\x00")  # device name unicode

        # common path suffix
        data0.extend(b"lmn\x00")

        # local base path unicode
        data0.extend(b"o\x00\x00\x00")

        # common path suffix unicode
        data0.extend(b"p\x00\x00\x00")

        stream0 = ByteIStream(data0)
        stream1 = ByteIStream(b"".join([b"\x64\x53", data0]))

        li0 = LinkInfo.from_stream(stream0)
        li1 = LinkInfo.from_stream(stream1, 2)

        volid = VolumeID((0x18, 0x04030201, 0x08070605, 0x14, 0x14, "d"))
        cnrl = CNRL((
            0x2C,
            1,
            1,
            0x1C,
            0x20,
            0x53645364,
            0x24,
            0x28,
            b"abc",
            b"def",
            "g",
            "h"
        ))


        ae(li0.size, 0x78)
        ae(li1.size, 0x78)

        ae(li0.header_size, 0x24)
        ae(li1.header_size, 0x24)

        ae(li0.vol_id_and_local_base_path, 1)
        ae(li1.vol_id_and_local_base_path, 1)

        ae(li0.cnrl_and_path_suffix, 1)
        ae(li1.cnrl_and_path_suffix, 1)

        ae(li0.vol_id_offset, 0x24)
        ae(li1.vol_id_offset, 0x24)

        ae(li0.local_base_path_offset, 0x3C)
        ae(li1.local_base_path_offset, 0x3C)

        ae(li0.cnrl_offset, 0x40)
        ae(li1.cnrl_offset, 0x40)

        ae(li0.path_suffix_offset, 0x6C)
        ae(li1.path_suffix_offset, 0x6C)

        ae(li0.local_base_path_offset_uni, 0x70)
        ae(li1.local_base_path_offset_uni, 0x70)

        ae(li0.path_suffix_offset_uni, 0x74)
        ae(li1.path_suffix_offset_uni, 0x74)

        ae(li0.vol_id, volid)
        ae(li1.vol_id, volid)

        ae(li0.cnrl, cnrl)
        ae(li1.cnrl, cnrl)
    # end def test_from_stream
# end class LinkInfoTestCase

class VolumeIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data0 = bytearray()
        data0.extend(b"\x14\x00\x00\x00")  # volume id size
        data0.extend(b"\x01\x02\x03\x04")  # drive type
        data0.extend(b"\x05\x06\x07\x08")  # drive serial number
        data0.extend(b"\x10\x00\x00\x00")  # volume label offset
        data0.extend(b"abc\x00")  # data

        data1 = bytearray()
        data1.extend(b"\x18\x00\x00\x00")  # volume id size
        data1.extend(b"\x01\x02\x03\x04")  # drive type
        data1.extend(b"\x05\x06\x07\x08")  # drive serial number
        data1.extend(b"\x14\x00\x00\x00")  # volume label offset
        data1.extend(b"\x14\x00\x00\x00")
        data1.extend(b"d\x00\x00\x00")  # data

        stream0 = ByteIStream(data0)
        stream1 = ByteIStream(b"".join([b"\x64\x53", data0]))
        stream2 = ByteIStream(data1)
        stream3 = ByteIStream(b"".join([b"\x64\x53", data1]))

        volid0 = VolumeID.from_stream(stream0)
        volid1 = VolumeID.from_stream(stream1, 2)
        volid2 = VolumeID.from_stream(stream2)
        volid3 = VolumeID.from_stream(stream3, 2)


        ae(volid0.size, 0x14)
        ae(volid1.size, 0x14)
        ae(volid2.size, 0x18)
        ae(volid3.size, 0x18)

        ae(volid0.drive_type, 0x04030201)
        ae(volid1.drive_type, 0x04030201)
        ae(volid2.drive_type, 0x04030201)
        ae(volid3.drive_type, 0x04030201)

        ae(volid0.drive_serial_num, 0x08070605)
        ae(volid1.drive_serial_num, 0x08070605)
        ae(volid2.drive_serial_num, 0x08070605)
        ae(volid3.drive_serial_num, 0x08070605)

        ae(volid0.volume_label_offset, 0x10)
        ae(volid1.volume_label_offset, 0x10)
        ae(volid2.volume_label_offset, 0x14)
        ae(volid2.volume_label_offset, 0x14)

        ae(volid0.volume_label_offset_uni, None)
        ae(volid1.volume_label_offset_uni, None)
        ae(volid2.volume_label_offset_uni, 0x14)
        ae(volid3.volume_label_offset_uni, 0x14)

        ae(volid0.volume_label, b"abc")
        ae(volid1.volume_label, b"abc")
        ae(volid2.volume_label, "d")
        ae(volid3.volume_label, "d")
    # end def test_from_stream
# end class VolumeIDTestCase

class CNRLTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data0 = bytearray()
        data0.extend(b"\x2C\x00\x00\x00")  # cnrl size
        data0.extend(b"\x03\x00\x00\x00")  # cnrl flags
        data0.extend(b"\x1C\x00\x00\x00")  # net name offset
        data0.extend(b"\x20\x00\x00\x00")  # device name offset
        data0.extend(b"\x64\x53\x64\x53")  # network provider type
        data0.extend(b"\x24\x00\x00\x00")  # net name offset unicode
        data0.extend(b"\x28\x00\x00\x00")  # device name offset unicode
        data0.extend(b"abc\x00")  # net name
        data0.extend(b"def\x00")  # device name
        data0.extend(b"g\x00\x00\x00")  # net name unicode
        data0.extend(b"h\x00\x00\x00")  # device name unicode

        data1 = bytearray()
        data1.extend(b"\x1C\x00\x00\x00")  # cnrl size
        data1.extend(b"\x03\x00\x00\x00")  # cnrl flags
        data1.extend(b"\x14\x00\x00\x00")  # net name offset
        data1.extend(b"\x18\x00\x00\x00")  # device name offset
        data1.extend(b"\x64\x53\x64\x53")  # network provider type
        data1.extend(b"abc\x00")  # net name
        data1.extend(b"def\x00")  # device name

        stream0 = ByteIStream(data0)
        stream1 = ByteIStream(b"".join([b"\x64\x53", data0]))
        stream2 = ByteIStream(data1)
        stream3 = ByteIStream(b"".join([b"\x64\x53", data1]))

        cnrl0 = CNRL.from_stream(stream0)
        cnrl1 = CNRL.from_stream(stream1, 2)
        cnrl2 = CNRL.from_stream(stream2)
        cnrl3 = CNRL.from_stream(stream3, 2)

        ae(cnrl0.size, 0x2C)
        ae(cnrl1.size, 0x2C)
        ae(cnrl2.size, 0x1C)
        ae(cnrl3.size, 0x1C)

        ae(cnrl0.valid_device, 1)
        ae(cnrl1.valid_device, 1)
        ae(cnrl2.valid_device, 1)
        ae(cnrl3.valid_device, 1)

        ae(cnrl0.valid_net_type, 1)
        ae(cnrl1.valid_net_type, 1)
        ae(cnrl2.valid_net_type, 1)
        ae(cnrl3.valid_net_type, 1)

        ae(cnrl0.net_name_offset, 0x1C)
        ae(cnrl1.net_name_offset, 0x1C)
        ae(cnrl2.net_name_offset, 0x14)
        ae(cnrl3.net_name_offset, 0x14)

        ae(cnrl0.device_name_offset, 0x20)
        ae(cnrl1.device_name_offset, 0x20)
        ae(cnrl2.device_name_offset, 0x18)
        ae(cnrl3.device_name_offset, 0x18)

        ae(cnrl0.net_type, 0x53645364)
        ae(cnrl1.net_type, 0x53645364)
        ae(cnrl2.net_type, 0x53645364)
        ae(cnrl3.net_type, 0x53645364)

        ae(cnrl0.net_name_offset_uni, 0x24)
        ae(cnrl1.net_name_offset_uni, 0x24)
        ae(cnrl2.net_name_offset_uni, None)
        ae(cnrl3.net_name_offset_uni, None)

        ae(cnrl0.net_name, b"abc")
        ae(cnrl1.net_name, b"abc")
        ae(cnrl2.net_name, b"abc")
        ae(cnrl3.net_name, b"abc")

        ae(cnrl0.device_name, b"def")
        ae(cnrl1.device_name, b"def")
        ae(cnrl2.device_name, b"def")
        ae(cnrl3.device_name, b"def")

        ae(cnrl0.net_name_uni, "g")
        ae(cnrl1.net_name_uni, "g")
        ae(cnrl2.net_name_uni, None)
        ae(cnrl3.net_name_uni, None)

        ae(cnrl0.device_name_uni, "h")
        ae(cnrl1.device_name_uni, "h")
        ae(cnrl2.device_name_uni, None)
        ae(cnrl3.device_name_uni, None)
    # end def test_from_stream
# end class CNRLTestCase
