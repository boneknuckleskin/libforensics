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

"""Data structures to work with shell link files"""

# local imports
from lf.dtypes import LERecord, BitTypeU32, bit, raw
from lf.win.dtypes import (
    FILETIME_LE, COLORREF, DWORD, WORD, BYTE, CLSID_LE, GUID_LE,
    LCID_LE
)
from lf.win.con.dtypes import COORD_LE

__docformat__ = "restructuredtext en"
__all__ = [
    "HotKey", "ShellLinkHeader", "LinkInfoHeader", "VolumeIDHeader",
    "CNRLHeader", "DataBlockHeader", "ConsoleDataBlock", "ConsoleFEDataBlock",
    "DarwinDataBlock", "EnvironmentVariableDataBlock",
    "IconEnvironmentDataBlock", "KnownFolderDataBlock",
    "SpecialFolderDataBlock", "TrackerDataBlock", "TrackerDataBlockFooter",
    "DomainRelativeObjId"
]

class LinkFlagsBits(BitTypeU32):
    has_idlist = bit
    has_link_info = bit
    has_name = bit
    has_relative_path = bit
    has_working_dir = bit
    has_args = bit
    has_icon_location = bit
    is_unicode = bit
    force_no_link_info = bit
    has_exp_string = bit
    run_in_separate_proc = bit
    has_logo3_id = bit
    has_darwin_id = bit
    run_as_user = bit
    has_exp_icon = bit
    no_pidl_alias = bit
    force_unc_name = bit
    run_with_shim_layer = bit
    force_no_link_track = bit
    enable_target_metadata = bit
    disable_link_path_tracking = bit
    disable_known_folder_rel_tracking = bit
    no_kf_alias = bit
    allow_link_to_link = bit
    unalias_on_save = bit
    prefer_environment_path = bit
    keep_local_idlist_for_unc_target = bit
# end class LinkFlagsBits

class LinkFlags(LERecord):
    field = LinkFlagsBits
# end class LinkFlags

class FileAttributesBits(BitTypeU32):
    read_only = bit
    hidden = bit
    system = bit
    reserved1 = bit
    directory = bit
    archive = bit
    reserved2 = bit
    normal = bit
    temp = bit
    sparse = bit
    reparse_point = bit
    compressed = bit
    offline = bit
    not_content_indexed = bit
    encrypted = bit
# end class FileAttributesBits

class FileAttributes(LERecord):
    field = FileAttributesBits
# end class FileAttributes

class HotKey(LERecord):
    vkcode = BYTE
    vkmod = BYTE
# end class HotKey

class ShellLinkHeader(LERecord):
    size = DWORD
    clsid = CLSID_LE
    flags = LinkFlags
    attrs = FileAttributes
    btime = FILETIME_LE
    atime = FILETIME_LE
    mtime = FILETIME_LE
    target_size = DWORD
    icon_index = DWORD
    show_cmd = DWORD
    hotkey = HotKey
    reserved1 = raw(2)
    reserved2 = raw(4)
    reserved3 = raw(4)
# end class ShellLinkHeader

class LinkInfoFlags(BitTypeU32):
    has_vol_id_and_local_base_path = bit
    has_cnrl_and_path_suffix = bit
# end class LinkInfoFlags

class LinkInfoHeader(LERecord):
    size = DWORD
    header_size = DWORD
    flags = LinkInfoFlags
    vol_id_offset = DWORD
    local_base_path_offset = DWORD
    cnrl_offset = DWORD
    path_suffix_offset = DWORD
# end class LinkInfoHeader

class VolumeIDHeader(LERecord):
    size = DWORD
    type = DWORD
    serial_num = DWORD
    vol_label_offset = DWORD
# end class VolumeIDHeader

class CNRLFlags(BitTypeU32):
    valid_device = bit
    valid_net_type = bit
# end class CNRLFlags

class CNRLHeader(LERecord):
    size = DWORD
    flags = CNRLFlags
    net_name_offset = DWORD
    device_name_offset = DWORD
    net_type = DWORD
# end class CNRLHeader

class DataBlockHeader(LERecord):
    size = DWORD
    sig = DWORD
# end class DataBlockHeader

class ConsoleDataBlock(DataBlockHeader):
    fill_attributes = WORD
    popup_fill_attributes = WORD
    screen_buffer_size = COORD_LE
    window_size = COORD_LE
    window_origin = COORD_LE
    font = DWORD
    input_buf_size = DWORD
    font_size = DWORD
    font_family = DWORD
    font_weight = DWORD
    face_name = raw(64)
    cursor_size = DWORD
    full_screen = DWORD
    quick_edit = DWORD
    insert_mode = DWORD
    auto_position = DWORD
    history_buf_size = DWORD
    history_buf_count = DWORD
    history_no_dup = DWORD
    color_table = [COLORREF] * 16
# end class ConsoleDataBlock

class ConsoleFEDataBlock(DataBlockHeader):
    code_page = LCID_LE
# end class ConsoleFEDataBlock

class DarwinDataBlock(DataBlockHeader):
    darwin_data_ansi = raw(260)
    darwin_data_uni = raw(520)
# end class DarwinDataBlock

class ExpandableStringsDataBlock(DataBlockHeader):
    target_ansi = raw(260)
    target_uni = raw(520)
# end class ExpandableStringsDataBlock

class EnvironmentVariableDataBlock(ExpandableStringsDataBlock):
    pass
# end class EnvironmentVariableDataBlock

class IconEnvironmentDataBlock(ExpandableStringsDataBlock):
    pass
# end class IconEnvironmentDataBlock

class KnownFolderDataBlock(DataBlockHeader):
    kf_id = GUID_LE
    offset = DWORD
# end class KnownFolderDataBlock

class SpecialFolderDataBlock(DataBlockHeader):
    sf_id = DWORD
    offset = DWORD
# end class SpecialFolderDataBlock

class DomainRelativeObjId(LERecord):
    volume = GUID_LE
    object = GUID_LE
# end class DomainRelativeObjId

class TrackerDataBlock(DataBlockHeader):
    length = DWORD
    version = DWORD
# end class TrackerDataBlock

class TrackerDataBlockFooter(LERecord):
    droid = DomainRelativeObjId
    droid_birth = DomainRelativeObjId
# end class TrackerDataBlockFooter
