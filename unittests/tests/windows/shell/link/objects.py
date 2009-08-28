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
Unit tests for the lf.windows.shell.link.structs module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

from uuid import UUID
from unittest import TestCase
from os.path import join

from lf.io import raw
from lf.utils.time import filetime_to_datetime
from lf.windows.shell.link.objects import (
    ShellLink, EnvironmentProps, IconEnvironmentProps, SpecialFolderProps,
    SpecialFolderProps, TrackerProps, VistaAndAboveIDListProps,
    KnownFolderProps, TerminalBlock
)

class CommonMethodsMixin():
    def setUp(self):
        path = ["tests", "windows", "shell", "link", "data"]
        filenames = [
            "shortcut_to_local_executable.lnk",
            "shortcut_to_local_envr_var.lnk",
            "shortcut_to_mapped_file.lnk",
            "shortcut_to_network_file.lnk"
        ]

        name_map = dict()

        for filename in filenames:
            full_path = list(path)
            full_path.append(filename)
            fqfn = join(*full_path)

            stream = raw.open(fqfn)
            shell_link = ShellLink(stream)
            name_map[filename] = shell_link
        # end for

        self.name_map = name_map
        self.filenames = filenames
    # end def setUp

    def check_attribute(self, struct_name, attr_name, attr_values):
        ae = self.assertEqual

        for (index, name) in enumerate(self.filenames):
            if struct_name is None:
                test_struct = self.name_map[name]
            else:
                pieces = struct_name.split(".")
                test_struct = getattr(self.name_map[name], pieces[0])

                for piece_name in pieces[1:]:
                    test_struct = getattr(test_struct, piece_name)
                # end for
            # end if
            test_attr_value = getattr(test_struct, attr_name)

            ae(test_attr_value, attr_values[index])
        # end for
    # end def check_attribute
# end class CommonMethodsMixin

class ShellLinkTestCase(CommonMethodsMixin, TestCase):
    def test_header(self):
        ae = self.assertEqual
        link_flags = [
            ("has_id_list", 1),
            ("has_link_info", 1),
            ("has_name", 1),
            ("has_relative_path", 1),
            ("has_working_dir", 1),
            ("has_args", 1),
            ("has_icon_location", 1),
            ("is_unicode", 1),
            ("force_no_link_info", 0),
            ("has_exp_string", 0),
            ("run_in_separate_proc", 0),
            ("has_logo3_id", 0),
            ("has_darwin_id", 0),
            ("run_as_user", 1),
            ("has_exp_icon", 1),
            ("no_pidl_alias", 0),
            ("force_unc_name", 0),
            ("run_with_shim_layer", 0),
            ("force_no_link_track", 0),
            ("enable_target_metadata", 1),
            ("disable_link_path_tracking", 0),
            ("disable_known_folder_rel_tracking", 0),
            ("no_kf_alias", 0),
            ("allow_link_to_link", 0),
            ("unalias_on_save", 0),
            ("prefer_environment_path", 0),
            ("keep_local_idlist_for_unc_target", 0)
        ]

        file_attributes = [
            ("read_only", 0),
            ("hidden", 0),
            ("system", 0),
            ("reserved1", 0),
            ("directory", 0),
            ("archive", 1),
            ("reserved2", 0),
            ("normal", 0),
            ("temp", 0),
            ("sparse", 0),
            ("reparse_point", 0),
            ("compressed", 0),
            ("offline", 0),
            ("not_content_indexed", 0),
            ("encrypted", 0),
        ]

        header = self.name_map["shortcut_to_local_executable.lnk"].header

        ae(header.size, 0x4C)
        ae(header.clsid, UUID("{00021401-0000-0000-C000-000000000046}"))

        for (flag_name, flag_value) in link_flags:
            flag_attr_value = getattr(header.flags, flag_name)
            ae(flag_attr_value, flag_value)
        # end for

        for (file_attr_name, file_attr_value) in file_attributes:
            attr_value = getattr(header.attrs, file_attr_name)
            ae(attr_value, file_attr_value)
        # end for

        ae(header.btime, filetime_to_datetime(0x01C6FE7B50C695B8))
        ae(header.atime, filetime_to_datetime(0x01C6FE7B50C695B8))
        ae(header.mtime, filetime_to_datetime(0x01C6FE7B50C695B8))
        ae(header.target_size, 0x024E00)
        ae(header.icon_index, 0)
        ae(header.show_cmd, 3)
        ae(header.vkcode, ord("S"))
        ae(header.vkmod, 6)
    # end def test_header

    def test_id_list(self):
        ae = self.assertEqual
        id_list = [
            b"\x1F\x50\xE0\x4F\xD0\x20\xEA\x3A\x69\x10\xA2\xD8\x08\x00\x2B"
            b"\x30\x30\x9D",

            b"\x2F\x43\x3A\x5C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00",

            b"\x31\x00\x00\x00\x00\x00\xFB\x3A\x54\xBA\x10\x00\x57\x69\x6E"
            b"\x64\x6F\x77\x73\x00\x38\x00\x07\x00\x04\x00\xEF\xBE\x62\x35"
            b"\x52\x5A\xFB\x3A\x54\xBA\x26\x00\x00\x00\xC5\x01\x00\x00\x00"
            b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x57\x00"
            b"\x69\x00\x6E\x00\x64\x00\x6F\x00\x77\x00\x73\x00\x00\x00\x16"
            b"\x00",

            b"\x32\x00\x00\x4E\x02\x00\x62\x35\x61\x64\x20\x00\x6E\x6F\x74"
            b"\x65\x70\x61\x64\x2E\x65\x78\x65\x00\x40\x00\x07\x00\x04\x00"
            b"\xEF\xBE\x62\x35\x61\x64\x62\x35\x61\x64\x26\x00\x00\x00\x4C"
            b"\x21\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x6E\x00\x6F\x00\x74\x00\x65\x00\x70\x00\x61\x00\x64"
            b"\x00\x2E\x00\x65\x00\x78\x00\x65\x00\x00\x00\x1A\x00",
        ]

        test_id_list = \
            self.name_map["shortcut_to_local_executable.lnk"].id_list

        ae(test_id_list, id_list)
    # end def test_id_list

    def test_link_info(self):
        ainn = self.assertIsNotNone

        for name in self.filenames:
            shell_link = self.name_map[name]
            ainn(shell_link.link_info)
        # end for
    # end def test_link_info

    def test_name_str(self):
        values = [
            "this is a comment",
            None,
            None,
            None
        ]

        self.check_attribute(None, "name_str", values)
    # end def test_name_str

    def test_relative_path(self):
        values = [
            "..\\..\\..\\Windows\\notepad.exe",
            "..\\..\\..\\WINDOWS",
            None,
            None
        ]

        self.check_attribute(None, "relative_path", values)
    # end def test_relative_path

    def test_working_dir(self):
        values = [
            "C:\\Windows",
            None,
            "W:\\WINDOWS",
            None
        ]

        self.check_attribute(None, "working_dir", values)
    # end def test_working_dir

    def test_args(self):
        values = [
            "c:\\arg1.txt",
            None,
            None,
            None
        ]

        self.check_attribute(None, "args", values)
    # end def test_args

    def test_icon_location(self):
        values = [
            "C:\\Windows\\twunk_32.exe",
            None,
            None,
            None
        ]

        self.check_attribute(None, "icon_location", values)
    # end def test_icon_location

    def test_extra_data(self):
        ae = self.assertEqual
        at = self.assertTrue

        values_list = [
            [
                SpecialFolderProps, KnownFolderProps, TrackerProps,
                IconEnvironmentProps, TerminalBlock
            ],

            [
                EnvironmentProps, SpecialFolderProps, TrackerProps,
                TerminalBlock
            ],

            [
                VistaAndAboveIDListProps, EnvironmentProps, TrackerProps,
                TerminalBlock
            ],

            [
                VistaAndAboveIDListProps, EnvironmentProps, TrackerProps,
                TerminalBlock
            ]
        ]

        for (index, name) in enumerate(self.filenames):
            shell_link = self.name_map[name]
            values = values_list[index]
            ae(len(shell_link.extra_data), len(values))

            for (value_index, value) in enumerate(values):
                at(isinstance(shell_link.extra_data[value_index], value))
            # end for
        # end for
    # end def test_extra_data
# end class ShellLinkTestCase

class LinkInfoTestCase(CommonMethodsMixin, TestCase):
    def test_size(self):
        sizes = [
            0x6C, 0x39, 0x61, 0x55
        ]

        self.check_attribute("link_info", "size", sizes)
    # end def test_size

    def test_header_size(self):
        header_sizes = [
            0x1C, 0x1C, 0x1C, 0x1C
        ]

        self.check_attribute("link_info", "header_size", header_sizes)
    # end def test_header_size

    def test_vol_id(self):
        ain = self.assertIsNone
        ainn = self.assertIsNotNone

        vol_ids = [
            ainn, ainn, ain, ain, ain
        ]

        for (index, name) in enumerate(self.filenames):
            vol_id_test_func = vol_ids[index]
            vol_id_test_func(self.name_map[name].link_info.vol_id)
        # end for
    # end def test_vol_id

    def test_cnrl(self):
        ain = self.assertIsNone
        ainn = self.assertIsNotNone

        cnrls = [
            ainn, ain, ainn, ainn
        ]

        for (index, name) in enumerate(self.filenames):
            cnrl_test_func = cnrls[index]
            cnrl_test_func(self.name_map[name].link_info.cnrl)
        # end for
    # end def test_cnrl

    def test_local_base_path(self):
        values = [
            b"C:\\",
            b"C:\\WINDOWS",
            None,
            None
        ]

        self.check_attribute("link_info", "local_base_path", values)
    # end def test_local_base_path

    def test_local_base_path_uni(self):
        values = [
            None,
            None,
            None,
            None
        ]

        self.check_attribute("link_info", "local_base_path_uni", values)
    # end def test_local_base_path_uni

    def test_path_suffix(self):
        values = [
            b"Windows\\notepad.exe",
            b"",
            b"WINDOWS\\NOTEPAD.EXE",
            b"CONFIG.SYS",
        ]

        self.check_attribute("link_info", "path_suffix", values)
    # end def test_path_suffix

    def test_path_suffix_uni(self):
        values = [None, None, None, None]
        self.check_attribute("link_info", "path_suffix_uni", values)
    # end def test_path_sufix_uni
# end class LinkInfoTestCase

class VolumeIDTestCase(CommonMethodsMixin, TestCase):
    def setUp(self):
        super(VolumeIDTestCase, self).setUp()

        self.filenames = [
            "shortcut_to_local_executable.lnk",
            "shortcut_to_local_envr_var.lnk"
        ]
    # end def setUp

    def test_size(self):
        values = [0x11, 0x11]
        self.check_attribute("link_info.vol_id", "size", values)
    # end def test_size

    def test_type(self):
        values = [3, 3]
        self.check_attribute("link_info.vol_id", "type", values)
    # end def test_type

    def test_serial_num(self):
        values = [0x900FF081, 0x3C051378]
        self.check_attribute("link_info.vol_id", "serial_num", values)
    # end def test_serial_num

    def test_volume_label(self):
        values = [b"", b""]
        self.check_attribute("link_info.vol_id", "volume_label", values)
    # end def test_volume_label
# end class VolumeIDTestCase

class CNRLTestCase(CommonMethodsMixin, TestCase):
    def setUp(self):
        super(CNRLTestCase, self).setUp()

        self.filenames = [
            "shortcut_to_local_executable.lnk",
            "shortcut_to_mapped_file.lnk",
            "shortcut_to_network_file.lnk"
        ]
    # end def setUp

    def test_size(self):
        values = [0x24, 0x31, 0x2E]
        self.check_attribute("link_info.cnrl", "size", values)
    # end def test_size

    def test_net_name(self):
        values = [
            b"\\\\TESTUSER-PC\\C",
            b"\\\\ANALYST-2B6A5KE\\c_drive",
            b"\\\\ANALYST-2B6A5KE\\C_DRIVE"
        ]

        self.check_attribute("link_info.cnrl", "net_name", values)
    # end def test_net_name

    def test_net_name_uni(self):
        values = [None, None, None]
        self.check_attribute("link_info.cnrl", "net_name_uni", values)
    # end def test_net_name_uni

    def test_device_name(self):
        values = [None, b"W:", None]
        self.check_attribute("link_info.cnrl", "device_name", values)
    # end def test_device_name

    def test_device_name_uni(self):
        values = [None, None, None]
        self.check_attribute("link_info.cnrl", "device_name_uni", values)
    # end def test_device_name_uni

    def test_device_name_valid(self):
        values = [0, 1, 0]
        self.check_attribute("link_info.cnrl", "device_name_valid", values)
    # end def test_device_name_valid

    def test_net_type(self):
        values = [0x20000, 0x20000, 0x20000]
        self.check_attribute("link_info.cnrl", "net_type", values)
    # end def test_net_type

    def test_net_type_valid(self):
        values = [1, 1, 1]
        self.check_attribute("link_info.cnrl", "net_type_valid", values)
    # end def test_net_type_valid
# end class CNRLTestCase

class PropsCommonMethodsMixin(CommonMethodsMixin):
    def setUp(self):
        super(PropsCommonMethodsMixin, self).setUp()

        self.indices = list()

        self.sigs = list()
        self.sizes = list()
    # end def setUp

    def check_attribute(self, struct_name, attr_name, attr_values):
        ae = self.assertEqual

        for (index, name) in enumerate(self.filenames):
            extra_data = self.name_map[name].extra_data
            block = extra_data[self.indices[index]]

            if struct_name is None:
                test_attr_value = getattr(block, attr_name)
            else:
                pieces = struct_name.split(".")
                struct = getattr(block, pieces[0])

                for piece_name in pieces[1:]:
                    struct = getattr(struct, piece_name)
                # end for

                test_attr_value = getattr(struct, attr_name)
            # end if

            ae(test_attr_value, attr_values[index])
        # end for
    # end def check_attribute

    def test_size(self):
        self.check_attribute(None, "size", self.sizes)
    # end def test_size

    def test_sig(self):
        self.check_attribute(None, "sig", self.sigs)
    # end def test_sig
# end class PropsCommonMethodsMixin

class EnvironmentPropsTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(EnvironmentPropsTestCase, self).setUp()
        self.filenames = [
            "shortcut_to_local_envr_var.lnk",
            "shortcut_to_mapped_file.lnk",
            "shortcut_to_network_file.lnk"
        ]
        self.indices = [0, 1, 1]
        self.sigs = [
            0xA0000001,
            0xA0000001,
            0xA0000001
        ]
        self.sizes = [0x314, 0x314, 0x314]
    # end def setUp

    def test_target_ansi(self):
        values = [
            b"%SYSTEMROOT%",
            b"W:\\WINDOWS\\NOTEPAD.EXE",
            b"\\\\ANALYST-2B6A5KE\\c_drive\\CONFIG.SYS"
        ]

        self.check_attribute(None, "target_ansi", values)
    # end def test_target_ansi

    def test_target_uni(self):
        values = [
            "%SYSTEMROOT%",
            "W:\\WINDOWS\\NOTEPAD.EXE",
            "\\\\ANALYST-2B6A5KE\\c_drive\\CONFIG.SYS"
        ]

        self.check_attribute(None, "target_uni", values)
    # end def test_target_uni
# end class EnvironmentPropsTestCase

class IconEnvironmentPropsTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(IconEnvironmentPropsTestCase, self).setUp()

        self.filenames = ["shortcut_to_local_executable.lnk"]
        self.indices = [3]
        self.sigs = [0xA0000007]
        self.sizes = [0x314]
    # end def setUp

    def test_target_ansi(self):
        values = [b"%SystemRoot%\\twunk_32.exe"]
        self.check_attribute(None, "target_ansi", values)
    # end def test_target_ansi

    def test_target_uni(self):
        values = ["%SystemRoot%\\twunk_32.exe"]
        self.check_attribute(None, "target_uni", values)
    # end def test_target_uni
# end class IconEnvironmentPropsTestCase

class SpecialFolderPropsTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(SpecialFolderPropsTestCase, self).setUp()

        self.filenames = [
            "shortcut_to_local_executable.lnk",
            "shortcut_to_local_envr_var.lnk"
        ]

        self.indices = [0, 1]
        self.sigs = [0xA0000005, 0xA0000005]
        self.sizes = [0x10, 0x10]
    # end def setUp

    def test_special_folder_id(self):
        values = [0x24, 0x24]
        self.check_attribute(None, "special_folder_id", values)
    # end def test_special_folder_id

    def test_offset(self):
        values = [0x7B, 0x69]
        self.check_attribute(None, "offset", values)
    # end def test_offset
# end class SpecialFolderPropsTestCase

class TrackerPropsTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(TrackerPropsTestCase, self).setUp()
        self.indices = [2, 2, 2, 2]
        self.sizes = [0x60, 0x60, 0x60, 0x60]
        self.sigs = [0xA0000003, 0xA0000003, 0xA0000003, 0xA0000003]
    # end def setUp

    def test_version(self):
        values = [0, 0, 0, 0]
        self.check_attribute(None, "version", values)
    # end def test_version

    def test_machine_id(self):
        values = [b"testuser-pc"]
        values.extend([b"analyst-2b6a5ke"] * 3)
        self.check_attribute(None, "machine_id", values)
    # end def test_machine_id

    def test_droid_volume(self):
        values = [
            UUID("{e0d619cc-7a40-4399-b848-29fafe3bdbac}"),
            UUID("{c82c2600-df43-433c-b2cd-e21d78a543e0}"),
            UUID("{c82c2600-df43-433c-b2cd-e21d78a543e0}"),
            UUID("{c82c2600-df43-433c-b2cd-e21d78a543e0}")
        ]

        self.check_attribute("droid", "volume", values)
        self.check_attribute("droid_birth", "volume", values)
    # end def test_droid_volume

    def test_droid_object(self):
        values = [
            UUID("{c9b4b50f-7b03-11de-b10a-000c291b5cb3}"),
            UUID("{6a2ed50b-7b0e-11de-80b9-000c29a1e37a}"),
            UUID("{6a2ed50d-7b0e-11de-80b9-000c29a1e37a}"),
            UUID("{6a2ed50c-7b0e-11de-80b9-000c29a1e37a}")
        ]

        self.check_attribute("droid", "object", values)
        self.check_attribute("droid_birth", "object", values)
    # end def test_droid_object
# end class TrackerPropsTestCase

class VistaAndAboveIDListPropsTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(VistaAndAboveIDListPropsTestCase, self).setUp()

        self.filenames = [
            "shortcut_to_mapped_file.lnk",
            "shortcut_to_network_file.lnk"
        ]
        self.indices = [0, 0]
        self.sizes = [0xDF, 0x169]
        self.sigs = [0xA000000C, 0xA000000C]
    # end def setUp

    def test_id_list(self):
        values = [
            [
                b"\x1F\x50\xE0\x4F\xD0\x20\xEA\x3A\x69\x10\xA2\xD8\x08\x00\x2B"
                b"\x30\x30\x9D",

                b"\x2F\x57\x3A\x5C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00",

                b"\x31\x00\x00\x00\x00\x00\xFC\x3A\x5C\x04\x10\x00\x57\x49\x4E"
                b"\x44\x4F\x57\x53\x00\x38\x00\x07\x00\x04\x00\xEF\xBE\xFB\x3A"
                b"\x51\x88\xFC\x3A\x9A\x05\x26\x00\x00\x00\x1C\x00\x00\x00\x00"
                b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x57\x00"
                b"\x49\x00\x4E\x00\x44\x00\x4F\x00\x57\x00\x53\x00\x00\x00\x16"
                b"\x00",

                b"\x32\x00\x00\x0C\x01\x00\x79\x32\x00\x60\x20\x00\x4E\x4F\x54"
                b"\x45\x50\x41\x44\x2E\x45\x58\x45\x00\x40\x00\x07\x00\x04\x00"
                b"\xEF\xBE\xFB\x3A\xBC\x88\xFC\x3A\x09\x03\x26\x00\x00\x00\xC1"
                b"\x0E\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x4E\x00\x4F\x00\x54\x00\x45\x00\x50\x00\x41\x00\x44"
                b"\x00\x2E\x00\x45\x00\x58\x00\x45\x00\x00\x00\x1A\x00"
            ],

            [
                b"\x1F\x58\x0D\x1A\x2C\xF0\x21\xBE\x50\x43\x88\xB0\x73\x67\xFC"
                b"\x96\xEF\x3C",

                b"\x00\x00\xB9\x00\xBB\xAF\x93\x3B\xAB\x00\x04\x00\x00\x00\x00"
                b"\x00\x4D\x00\x00\x00\x31\x53\x50\x53\x30\xF1\x25\xB7\xEF\x47"
                b"\x1A\x10\xA5\xF1\x02\x60\x8C\x9E\xEB\xAC\x31\x00\x00\x00\x0A"
                b"\x00\x00\x00\x00\x1F\x00\x00\x00\x10\x00\x00\x00\x41\x00\x4E"
                b"\x00\x41\x00\x4C\x00\x59\x00\x53\x00\x54\x00\x2D\x00\x32\x00"
                b"\x42\x00\x36\x00\x41\x00\x35\x00\x4B\x00\x45\x00\x00\x00\x00"
                b"\x00\x00\x00\x2D\x00\x00\x00\x31\x53\x50\x53\x3A\xA4\xBD\xDE"
                b"\xB3\x37\x83\x43\x91\xE7\x44\x98\xDA\x29\x95\xAB\x11\x00\x00"
                b"\x00\x03\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x2D\x00\x00\x00\x31\x53\x50\x53\x73\x43\xE5\x0A"
                b"\xBE\x43\xAD\x4F\x85\xE4\x69\xDC\x86\x33\x98\x6E\x11\x00\x00"
                b"\x00\x0B\x00\x00\x00\x00\x0B\x00\x00\x00\xFF\xFF\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00",

                b"\xC3\x01\xC5\x5C\x5C\x41\x4E\x41\x4C\x59\x53\x54\x2D\x32\x42"
                b"\x36\x41\x35\x4B\x45\x5C\x63\x5F\x64\x72\x69\x76\x65\x00\x4D"
                b"\x69\x63\x72\x6F\x73\x6F\x66\x74\x20\x4E\x65\x74\x77\x6F\x72"
                b"\x6B\x00\x00\x02\x00",

                b"\x32\x00\x00\x00\x00\x00\xFC\x3A\x8A\x02\x20\x00\x43\x4F\x4E"
                b"\x46\x49\x47\x2E\x53\x59\x53\x00\x00\x3E\x00\x07\x00\x04\x00"
                b"\xEF\xBE\xFC\x3A\x8A\x02\xFC\x3A\x8A\x02\x26\x00\x00\x00\x60"
                b"\x1C\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x43\x00\x4F\x00\x4E\x00\x46\x00\x49\x00\x47\x00\x2E"
                b"\x00\x53\x00\x59\x00\x53\x00\x00\x00\x1A\x00"
            ]
        ]

        self.check_attribute(None, "id_list", values)
    # end def test_id_list
# end class VistaAndAboveIDListPropsTestCase

class KnownFolderPropsTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(KnownFolderPropsTestCase, self).setUp()

        self.filenames = ["shortcut_to_local_executable.lnk"]
        self.sizes = [0x1C]
        self.sigs = [0xA000000B]
        self.indices = [1]
    # end def setUp

    def test_kfid(self):
        values = [UUID("{f38bf404-1d43-42f2-9305-67de0b28fc23}")]
        self.check_attribute(None, "kfid", values)
    # end def test_kfid

    def test_offset(self):
        values = [0x7B]
        self.check_attribute(None, "offset", values)
    # end def test_offset
# end class KnownFolderPropsTestCase

class TerminalBlockTestCase(PropsCommonMethodsMixin, TestCase):
    def setUp(self):
        super(TerminalBlockTestCase, self).setUp()

        self.indices = [4, 3, 3, 3]
        self.sizes = [0, 0, 0, 0]
        self.sigs = [0, 0, 0, 0]
    # end def setUp
# end class TerminalBlockTestCase
