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
Data structures to work with shell link (.lnk) files.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "HotKey", "Header", "LinkInfoHeader", "VolumeIDHeader", "CNRLHeader",
    "DataBlockNeader", "ConsoleDataBlock", "ConsoleDataBockFull",
    "DarwinDataBlock", "DarwinDataBlockFull", "EnvironmentVariableDataBlock",
    "EnvironmentVariableDataBlockFull", "IconEnvironmentDataBlock",
    "IconEnvironmentDataBlockFull", "KnownFolderDataBlock",
    "KnownFolderDataBlockFull", "SpecialFolderDataBlock",
    "SpecialFolderDataBlockFull", "TrackerDataBlockHeader",
    "TrackerDataBlockHeaderFull", "TrackerDataBlockFooter"
]

from lf.datastruct import bit, UBits32, DataStruct_LE, array, raw
from lf.windows.types import FILETIME, COLORREF, DWORD, WORD, BYTE
from lf.windows.structs import CLSID, GUID, COORD

class LinkFlagsBits(UBits32):
    bits = [
        bit("has_id_list", 1),
        bit("has_link_info", 1),
        bit("has_name", 1),
        bit("has_relative_path", 1),
        bit("has_working_dir", 1),
        bit("has_args", 1),
        bit("has_icon_location", 1),
        bit("is_unicode", 1),
        bit("force_no_link_info", 1),
        bit("has_exp_string", 1),
        bit("run_in_separate_proc", 1),
        bit("has_logo3_id", 1),
        bit("has_darwin_id", 1),
        bit("run_as_user", 1),
        bit("has_exp_icon", 1),
        bit("no_pidl_alias", 1),
        bit("force_unc_name", 1),
        bit("run_with_shim_layer", 1),
        bit("force_no_link_track", 1),
        bit("enable_target_metadata", 1),
        bit("disable_link_path_tracking", 1),
        bit("disable_known_folder_rel_tracking", 1),
        bit("no_kf_alias", 1),
        bit("allow_link_to_link", 1),
        bit("unalias_on_save", 1),
        bit("prefer_environment_path", 1),
        bit("keep_local_idlist_for_unc_target", 1)
    ]
# end class LinkFlagsBits

class LinkFlags(DataStruct_LE):
    fields = [
        LinkFlagsBits()
    ]
# end class LinkFlags

class FileAttributesBits(UBits32):
    bits = [
        bit("read_only", 1),
        bit("hidden", 1),
        bit("system", 1),
        bit("reserved1", 1),
        bit("directory", 1),
        bit("archive", 1),
        bit("reserved2", 1),
        bit("normal", 1),
        bit("temp", 1),
        bit("sparse", 1),
        bit("reparse_point", 1),
        bit("compressed", 1),
        bit("offline", 1),
        bit("not_content_indexed", 1),
        bit("encrypted", 1)
    ]
# end class FileAttributesBits

class FileAttributes(DataStruct_LE):
    fields = [
        FileAttributesBits()
    ]
# end class FileAttributes

class HotKey(DataStruct_LE):
    fields = [
        BYTE("vkcode"),
        BYTE("vkmod"),
    ]
# end class HotKey

class Header(DataStruct_LE):
    fields = [
        DWORD("size"),
        CLSID("clsid"),
        LinkFlags("flags"),
        FileAttributes("attrs"),
        FILETIME("btime"),
        FILETIME("atime"),
        FILETIME("mtime"),
        DWORD("target_size"),
        DWORD("icon_index"),
        DWORD("show_cmd"),
        HotKey("hotkey"),
        raw("reserved1", 2),
        raw("reserved2", 4),
        raw("reserved3", 4)
    ]
# end class Header

class LinkInfoFlags(UBits32):
    bits = [
        bit("has_vol_id_and_local_base_path", 1),
        bit("has_cnrl_and_path_suffix", 1)
    ]
# end class LinkInfoFlags

class LinkInfoHeader(DataStruct_LE):
    fields = [
        DWORD("size"),
        DWORD("header_size"),
        LinkInfoFlags(),
        DWORD("vol_id_offset"),
        DWORD("local_base_path_offset"),
        DWORD("cnrl_offset"),
        DWORD("path_suffix_offset"),
        DWORD("local_base_path_uni_offset"),
        DWORD("path_suffix_uni_offset"),
    ]
# end class LinkInfoHeader

class VolumeIDHeader(DataStruct_LE):
    fields = [
        DWORD("size"),
        DWORD("type"),
        DWORD("serial_num"),
        DWORD("vol_label_offset"),
    ]
# end class VolumeIDHeader

class CNRLFlags(UBits32):
    bits = [
        bit("valid_device", 1),
        bit("valid_net_type", 1)
    ]
# end class CNRLFlags

class CNRLHeader(DataStruct_LE):
    fields = [
        DWORD("size"),
        CNRLFlags(),
        DWORD("net_name_offset"),
        DWORD("device_name_offset"),
        DWORD("net_type")
    ]
# end class CNRLHeader

class DataBlockHeader(DataStruct_LE):
    fields = [
        DWORD("size"),
        DWORD("sig")
    ]
# end class DataBlockHeader

class ConsoleDataBlock(DataStruct_LE):
    fields = [
        WORD("fill_attributes"),
        WORD("popup_fill_attributes"),
        COORD("screen_buffer_size"),
        COORD("window_size"),
        COORD("window_origin"),
        raw("unused1", 4),
        raw("unsed2", 4),
        DWORD("font_size"),
        DWORD("font_family"),
        DWORD("font_weight"),
        raw("face_name", 64),
        DWORD("cursor_size"),
        DWORD("full_screen"),
        DWORD("insert_mode"),
        DWORD("auto_position"),
        DWORD("history_buff_size"),
        DWORD("history_buff_count"),
        DWORD("history_no_dup"),
        array("color_table", DWORD("entry"), 16)
    ]
# end class ConsoleDataBlock

class ConsoleDataBlockFull(DataStruct_LE):
    fields = [
        DataBlockHeader("header")
    ]

    fields.extend(ConsoleDataBlock.fields)
# end class ConsoleDataBlockFull

class DarwinDataBlock(DataStruct_LE):
    fields = [
        raw("darwin_data_ansi", 260),
        raw("darwin_data_uni", 520)
    ]
# end class DarwinDataBlock

class DarwinDataBlockFull(DataStruct_LE):
    fields = [
        DataBlockHeader("header"),
        raw("darwin_data_ansi", 260),
        raw("darwin_data_uni", 520)
    ]
# end class DarwinDataBlockFull

class ExpandableStringsDataBlock(DataStruct_LE):
    fields = [
        raw("target_ansi", 260),
        raw("target_uni", 520)
    ]
# end class ExpandableStringsDataBlock

class ExpandableStringsDataBlockFull(DataStruct_LE):
    fields = [
        DataBlockHeader("header"),
        raw("target_ansi", 260),
        raw("target_uni", 520)
    ]
# en class ExpandableStringsDataBlockFull

class EnvironmentVariableDataBlock(ExpandableStringsDataBlock):
    pass
# end class EnvironmentVariableDataBlock

class EnvironmentVariableDataBlockFull(ExpandableStringsDataBlockFull):
    pass
# end class EnvironmentVariableDataBlockFull

class IconEnvironmentDataBlock(ExpandableStringsDataBlock):
    pass
# end class IconEnvironmentDataBlock

class IconEnvironmentDataBlockFull(ExpandableStringsDataBlockFull):
    pass
# end class IconEnvironmentDataBlockFull

class KnownFolderDataBlock(DataStruct_LE):
    fields = [
        GUID("kf_id"),
        DWORD("offset")
    ]
# end class KnownFolderDataBlock

class KnownFolderDataBlockFull(DataStruct_LE):
    fields = [
        DataBlockHeader("header"),
        GUID("kf_id"),
        DWORD("offset")
    ]
# end class KnownFolderDataBlockFull

class SpecialFolderDataBlock(DataStruct_LE):
    fields = [
        DWORD("special_folder_id"),
        DWORD("offset")
    ]
# end class SpecialFolderDataBlock

class SpecialFolderDataBlockFull(DataStruct_LE):
    fields = [
        DataBlockHeader("header"),
        DWORD("special_folder_id"),
        DWORD("offset")
    ]
# end class SpecialFolderDataBlockFull

class DomainRelativeObjId(DataStruct_LE):
    fields = [
        GUID("volume"),
        GUID("object")
    ]
# end class DomainRelativeObjId

class TrackerDataBlockHeader(DataStruct_LE):
    fields = [
        DWORD("length"),
        DWORD("version"),
    ]
# end class TrackerDataBlockHeader

class TrackerDataBlockHeaderFull(DataStruct_LE):
    fields = [
        DataBlockHeader("header"),
        DWORD("length"),
        DWORD("version")
    ]
# end class TrackerDataBlockHeaderFull

class TrackerDataBlockFooter(DataStruct_LE):
    fields = [
        DomainRelativeObjId("droid"),
        DomainRelativeObjId("droid_birth")
    ]
# end class TrackerDataBlockFooter
