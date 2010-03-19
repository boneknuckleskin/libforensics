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

"""Displays information about shell link (.lnk) files"""

# stdlib imports
import sys
from optparse import OptionParser
from datetime import datetime

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.shell.link import (
    ShellLink, ConsoleProps, ConsoleFEProps, DarwinProps, EnvironmentProps,
    IconEnvironmentProps, KnownFolderProps, PropertyStoreProps, ShimProps,
    SpecialFolderProps, TrackerProps, VistaAndAboveIDListProps
)
from lf.win.consts.vkcode import virtual_key_code_names
from lf.win.consts.hotkey import (
    HOTKEYF_SHIFT, HOTKEYF_CONTROL, HOTKEYF_ALT, HOTKEYF_EXT
)
from lf.win.consts.fs import (
    DRIVE_NO_ROOT_DIR, DRIVE_REMOVABLE, DRIVE_FIXED, DRIVE_REMOTE, DRIVE_CDROM,
    DRIVE_RAMDISK
)
from lf.win.consts.npt import wnnc_net_names
from lf.win.shell.link.consts import (
    CONSOLE_PROPS_SIG, CONSOLE_FE_PROPS_SIG, DARWIN_PROPS_SIG,
    ENVIRONMENT_PROPS_SIG, ICON_ENVIRONMENT_PROPS_SIG, KNOWN_FOLDER_PROPS_SIG,
    PROPERTY_STORE_PROPS_SIG, SHIM_PROPS_SIG, TRACKER_PROPS_SIG,
    VISTA_AND_ABOVE_IDLIST_PROPS_SIG, SPECIAL_FOLDER_PROPS_SIG
)
from lf.win.consts.font import (
    FF_DONTCARE, FF_ROMAN, FF_SWISS, FF_MODERN, FF_SCRIPT, FF_DECORATIVE
)
from lf.win.shell.consts.csidl import csidl_names, csidl_display_names
from lf.win.con.consts import (
    FOREGROUND_BLUE, FOREGROUND_RED, FOREGROUND_GREEN, FOREGROUND_INTENSITY,
    BACKGROUND_BLUE, BACKGROUND_RED, BACKGROUND_GREEN, BACKGROUND_INTENSITY
)

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)

__docformat__ = "restructuredtext en"
__all__ = [
]

def format_timestamp(timestamp):
    if isinstance(timestamp, datetime):
        new_timestamp = timestamp.isoformat(" ")
    else:
        new_timestamp = timestamp
    # end if

    return new_timestamp
# end def format_timestamp

def format_header_info(lnk):
    output = list()
    header = lnk.header
    flags = header.flags
    attrs = header.attrs
    vkmod = header.vkmod
    vkcode = header.vkcode

    has_idlist = bool(flags.has_idlist)
    has_link_info = bool(flags.has_link_info)
    has_name = bool(flags.has_name)
    has_rel_path = bool(flags.has_relative_path)
    has_working_dir = bool(flags.has_working_dir)
    has_args = bool(flags.has_args)
    has_icon_loc = bool(flags.has_icon_location)
    is_unicode = bool(flags.is_unicode)
    force_no_link_info = bool(flags.force_no_link_info)
    has_exp_str = bool(flags.has_exp_string)
    run_in_sep_proc = bool(flags.run_in_separate_proc)
    has_logo3_id = bool(flags.has_logo3_id)
    has_darwin_id = bool(flags.has_darwin_id)
    run_as_user = bool(flags.run_as_user)
    has_exp_icon = bool(flags.has_exp_icon)
    no_pidl_alias = bool(flags.no_pidl_alias)
    force_unc_name = bool(flags.force_unc_name)
    shim_layer = bool(flags.run_with_shim_layer)
    force_no_link_track = bool(flags.force_no_link_track)
    target_metadata = bool(flags.enable_target_metadata)
    link_path_track = bool(flags.disable_link_path_tracking)
    kf_track = bool(flags.disable_known_folder_rel_tracking)
    no_kf_alias = bool(flags.no_kf_alias)
    allow_link_to_link = bool(flags.allow_link_to_link)
    unalias_on_save = bool(flags.unalias_on_save)
    prefer_env_path = bool(flags.prefer_environment_path)
    keep_local = bool(flags.keep_local_idlist_for_unc_target)

    read_only = bool(attrs.read_only)
    hidden = bool(attrs.hidden)
    system = bool(attrs.system)
    directory = bool(attrs.directory)
    archive = bool(attrs.archive)
    normal = bool(attrs.normal)
    temp = bool(attrs.temp)
    sparse = bool(attrs.sparse)
    reparse_point = bool(attrs.reparse_point)
    compressed = bool(attrs.compressed)
    offline = bool(attrs.offline)
    not_content_indexed = bool(attrs.not_content_indexed)
    encrypted = bool(attrs.encrypted)

    btime = format_timestamp(header.btime)
    atime = format_timestamp(header.atime)
    mtime = format_timestamp(header.mtime)

    if header.show_cmd == 3:
        show_cmd = "SW_SHOWMAXIMIZED (0x3)"
    elif header.show_cmd == 7:
        show_cmd = "SW_SHOWMINNOACTIVE (0x7)"
    else:
        show_cmd = "SW_SHOWNORMAL (0x{0:X})".format(header.show_cmd)
    # end if

    hotkey_output = list()
    if vkmod & HOTKEYF_CONTROL:
        hotkey_output.append("CTRL")
    # end if

    if vkmod & HOTKEYF_SHIFT:
        hotkey_output.append("SHIFT")
    # end if

    if vkmod & HOTKEYF_ALT:
        hotkey_output.append("ALT")
    # end if

    if vkmod & HOTKEYF_EXT:
        hotkey_output.append("EXT")
    # end if

    hotkey_output = " + ".join(hotkey_output)

    if vkcode in virtual_key_code_names:
        name = virtual_key_code_names[vkcode]
        vkcode_output = "{0}".format(name)
    elif chr(vkcode) in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        vkcode_output = "{0}".format(chr(vkcode))
    elif vkcode != 0:
        vkcode_output = "Unknown"
    else:
        vkcode_output = ""
    # end if

    if vkcode_output:
        if hotkey_output:
            hotkey_output = " + ".join([hotkey_output, vkcode_output])
        else:
            hotkey_output = vkcode_output
        # end if
    # end if


    if hotkey_output:
        hotkey_output = "({0})".format(hotkey_output)
    # end if

    output.append(" Header size: {0}".format(header.size))
    output.append(" CLSID: {0}".format(header.clsid))
    output.append(" Creation time: {0}".format(btime))
    output.append(" Access time: {0}".format(atime))
    output.append(" Modification time: {0}".format(mtime))
    output.append(" Target size: {0}".format(header.target_size))
    output.append(" Icon index: {0}".format(header.icon_index))
    output.append(" Show command: {0}".format(show_cmd))
    output.append(" Hotkey: {0:X}:{1:X} {2}".format(
        vkmod, vkcode, hotkey_output
    ))

    output.append("")
    output.append(" Link Flags:")
    output.append(" -----------")
    output.append("  Has link target idlist: {0}".format(has_idlist))
    output.append("  Has link info: {0}".format(has_link_info))
    output.append("  Has name: {0}".format(has_name))
    output.append("  Has relative path: {0}".format(has_rel_path))
    output.append("  Has working directory: {0}".format(has_working_dir))
    output.append("  Has arguments: {0}".format(has_args))
    output.append("  Has icon location: {0}".format(has_icon_loc))
    output.append("  Is unicode: {0}".format(is_unicode))
    output.append("  Force no link info: {0}".format(force_no_link_info))
    output.append("  Has exp. string: {0}".format(has_exp_str))
    output.append("  Run in separate process: {0}".format(run_in_sep_proc))
    output.append("  Has logo3 id: {0}".format(has_logo3_id))
    output.append("  Has darwin id: {0}".format(has_darwin_id))
    output.append("  Run as user: {0}".format(run_as_user))
    output.append("  Has exp. icon: {0}".format(has_exp_icon))
    output.append("  No pidl alias: {0}".format(no_pidl_alias))
    output.append("  Force UNC name: {0}".format(force_unc_name))
    output.append("  Run with shim layer: {0}".format(shim_layer))
    output.append("  Force no link track: {0}".format(force_no_link_track))
    output.append("  Enable target metadata: {0}".format(target_metadata))
    output.append("  Disable link path tracking: {0}".format(link_path_track))
    output.append("  Disable known folder tracking: {0}".format(kf_track))
    output.append("  Disable known folder alias: {0}".format(no_kf_alias))
    output.append("  Allow link to link: {0}".format(allow_link_to_link))
    output.append("  Prefer environment path: {0}".format(prefer_env_path))
    output.append("  Keep local idlist for UNC target: {0}".format(keep_local))

    output.append("")
    output.append(" File Attributes:")
    output.append(" ----------------")
    output.append("  Read only: {0}".format(read_only))
    output.append("  Hidden: {0}".format(hidden))
    output.append("  System: {0}".format(system))
    output.append("  Directory: {0}".format(directory))
    output.append("  Archive: {0}".format(archive))
    output.append("  Normal: {0}".format(normal))
    output.append("  Temp: {0}".format(temp))
    output.append("  Sparse: {0}".format(sparse))
    output.append("  Reparse point: {0}".format(reparse_point))
    output.append("  Compressed: {0}".format(compressed))
    output.append("  Offline: {0}".format(offline))
    output.append("  Not content indexed: {0}".format(not_content_indexed))
    output.append("  Encrypted: {0}".format(encrypted))

    return output
# end def format_header_info

def format_idlist(lnk, full_output):
    output = list()

    if lnk.idlist is not None:
        for shitemid in lnk.idlist.mkid:
            output.append(" Byte count: {0}".format(shitemid.cb))

            if shitemid.abID is not None:
                if full_output:
                    output.append(" Data:")
                    output.append("{0}".format(shitemid.abID))
                else:
                    output.append(" Data: {0}".format(shitemid.abID[:15]))
                # end if
            else:
                output.append(" Data: Not in file")
            # end if

            output.append("")
        else:
            if output[-1] == "":
                output = output[:-1]
            # end if
        # end for
    else:
        output.append(" Not in file")
    # end if

    return output
# end def format_idlist

def format_link_info(lnk):
    output = list()
    li = lnk.link_info
    volidlbp = bool(li.vol_id_and_local_base_path)
    cnrlaps = bool(li.cnrl_and_path_suffix)

    if li is not None:
        output.append(" Size: {0}".format(li.size))
        output.append(" Header size: {0}".format(li.header_size))
        output.append(" Volume ID and local base path: {0}".format(volidlbp))
        output.append(" CNRL and path suffix: {0}".format(cnrlaps))
        output.append(" Volume ID offset: {0}".format(li.vol_id_offset))
        output.append(" Local base path offset: {0}".format(
            li.local_base_path_offset
        ))
        output.append(" CNRL offset: {0}".format(li.cnrl_offset))
        output.append(" Common path suffix offset: {0}".format(
            li.path_suffix_offset
        ))
        output.append(" Local base path offset (unicode): {0}".format(
            li.local_base_path_offset_uni
        ))
        output.append(" Common path suffix offset (unicode): {0}".format(
            li.path_suffix_offset_uni
        ))

        if li.local_base_path is not None:
            output.append(" Local base path: {0}".format(li.local_base_path))
        else:
            output.append(" Local base path: Not in file")
        # end if

        if li.local_base_path_uni is not None:
            output.append(" Local base path (unicode): {0}".format(
                li.local_base_path_uni
            ))
        else:
            output.append(" Local base path (unicode): Not in file")
        # end if

        if li.path_suffix:
            output.append(" Common path suffix: {0}".format(li.path_suffix))
        else:
            output.append(" Common path suffix: Not in file")
        # end if

        if li.path_suffix_uni:
            output.append(" Common path suffix (unicode): {0}".format(
                li.path_suffix_uni
            ))
        else:
            output.append(" Common path suffix (unicode): Not in file")
        # end if

        output.append("")
        output.append(" Volume ID:")
        output.append(" ----------")

        if li.vol_id is not None:
            volid = li.vol_id

            if volid.drive_type == DRIVE_NO_ROOT_DIR:
                drive_type = "Invalid root path (0x1)"
            elif volid.drive_type == DRIVE_REMOVABLE:
                drive_type = "Removable (0x2)"
            elif volid.drive_type == DRIVE_FIXED:
                drive_type = "Fixed (0x3)"
            elif volid.drive_type == DRIVE_REMOTE:
                drive_type = "Network (0x4)"
            elif volid.drive_type == DRIVE_CDROM:
                drive_type = "CDROM (0x5)"
            elif volid.drive_type == DRIVE_RAMDISK:
                drive_type = "RAM disk (0x6)"
            else:
                drive_type = "Unknown (0x{0:X})".format(volid.drive_type)
            # end if

            output.append("  Size: {0}".format(volid.size))
            output.append("  Drive type: {0}".format(drive_type))
            output.append("  Drive serial number: 0x{0:X}".format(
                volid.drive_serial_num
            ))
            output.append("  Volume label offset: {0}".format(
                volid.volume_label_offset
            ))
            output.append("  Volume label offset (unicode): {0}".format(
                volid.volume_label_offset_uni
            ))
            output.append("  Volume label: {0}".format(volid.volume_label))
        else:
            output.append("  Not in file")
        # end if
    else:
        output.append("  Not in file")
    # end if

    output.append("")
    output.append(" Common Network Relative Link:")
    output.append(" -----------------------------")

    if li.cnrl is not None:
        cnrl = li.cnrl
        valid_device = bool(cnrl.valid_device)
        valid_net_type = bool(cnrl.valid_net_type)

        if cnrl.valid_net_type and (cnrl.net_type in wnnc_net_names):
            net_type = "{0} (0x{1:X})".format(
                wnnc_net_names[cnrl.net_type], cnrl.net_type
            )
        else:
            net_type = "Unknown (0x{0:X})".format(cnrl.net_type)
        # end if

        output.append("  Size: {0}".format(cnrl.size))
        output.append("  Valid device: {0}".format(valid_device))
        output.append("  Valid net type: {0}".format(valid_net_type))
        output.append("  Net name offset: {0}".format(cnrl.net_name_offset))
        output.append("  Device name offset: {0}".format(
            cnrl.device_name_offset
        ))
        output.append("  Network provider type: {0}".format(net_type))
        output.append("  Net name offset (unicode): {0}".format(
            cnrl.net_name_offset_uni
        ))
        output.append("  Device name offset (unicode): {0}".format(
            cnrl.device_name_offset_uni
        ))

        if cnrl.net_name is not None:
            output.append("  Net name: {0}".format(cnrl.net_name))
        else:
            output.append("  Net name: Not in file")
        # end if

        if cnrl.device_name is not None:
            output.append("  Device name: {0}".format(cnrl.device_name))
        else:
            output.append("  Device name: Not in file")
        # end if

        if cnrl.net_name_uni is not None:
            output.append("  Net name (unicode): {0}".format(
                cnrl.net_name_uni
            ))
        else:
            output.append("  Net name (unicode): Not in file")
        # end if

        if cnrl.device_name_uni is not None:
            output.append("  Device name (unicode): {0}".format(
                cnrl.device_name_uni
            ))
        else:
            output.append("  Device name (unicode): Not in file")
        # end if

    else:
        output.append("  Not in file")
    # end if

    return output
# end def format_link_info

def format_string_data(lnk):
    output = list()
    sd = lnk.string_data

    output.append("")
    output.append(" Name String:")
    output.append(" ------------")
    if sd.name_str is not None:
        output.append("  Character count: {0}".format(sd.name_str.char_count))
        output.append("  String: {0}".format(sd.name_str.string))
    else:
        output.append("  Not in file")
    # end if

    output.append("")
    output.append(" Relative Path:")
    output.append(" --------------")
    if sd.rel_path is not None:
        output.append("  Character count: {0}".format(sd.rel_path.char_count))
        output.append("  String: {0}".format(sd.rel_path.string))
    else:
        output.append("  Not in file")
    # end if

    output.append("")
    output.append(" Working Directory:")
    output.append(" ------------------")
    if sd.working_dir is not None:
        output.append("  Character count: {0}".format(
            sd.working_dir.char_count
        ))
        output.append("  String: {0}".format(sd.working_dir.string))
    else:
        output.append("  Not in file")
    # end if

    output.append("")
    output.append(" Command Line Arguments:")
    output.append(" -----------------------")
    if sd.cmd_args is not None:
        output.append("  Character count: {0}".format(sd.cmd_args.char_count))
        output.append("  String: {0}".format(sd.cmd_args.string))
    else:
        output.append("  Not in file")
    # end if

    output.append("")
    output.append(" Icon Location:")
    output.append(" --------------")
    if sd.icon_location is not None:
        output.append("  Character count: {0}".format(
            sd.icon_location.char_count
        ))
        output.append("  String: {0}".format(sd.icon_location.string))
    else:
        output.append("  Not in file")
    # end if

    return output
# end def format_string_data

def format_extra_data(lnk, full_output):
    output = list()

    for block in lnk.extra_data:
        sig = block.sig

        if sig == CONSOLE_PROPS_SIG:
            sig_str = "CONSOLE_PROPS"
        elif sig == CONSOLE_FE_PROPS_SIG:
            sig_str = "CONSOLE_FE_PROPS"
        elif sig == DARWIN_PROPS_SIG:
            sig_str = "DARWIN_PROPS"
        elif sig == ENVIRONMENT_PROPS_SIG:
            sig_str = "ENVIRONMENT_PROPS"
        elif sig == ICON_ENVIRONMENT_PROPS_SIG:
            sig_str = "ICON_ENVIRONMENT_PROPS"
        elif sig == KNOWN_FOLDER_PROPS_SIG:
            sig_str = "KNOWN_FOLDER_PROPS"
        elif sig == PROPERTY_STORE_PROPS_SIG:
            sig_str = "PROPERTY_STORE_PROPS"
        elif sig == SHIM_PROPS_SIG:
            sig_str = "SHIM_PROPS"
        elif sig == SPECIAL_FOLDER_PROPS_SIG:
            sig_str = "SPECIAL_FOLDER_PROPS"
        elif sig == TRACKER_PROPS_SIG:
            sig_str = "TRACKER_PROPS"
        elif sig == VISTA_AND_ABOVE_IDLIST_PROPS_SIG:
            sig_str = "VISTA_AND_ABOVE_IDLIST_PROPS"
        else:
            sig_str = "Unknown"
        # end if

        sig_output = "{0} (0x{1:X})".format(sig_str, sig)

        if isinstance(block, ConsoleProps):
            if block.font_family == FF_DONTCARE:
                font_family = "Don't care"
            elif block.font_family == FF_ROMAN:
                font_family = "Roman"
            elif block.font_family == FF_SWISS:
                font_family = "Swiss"
            elif block.font_family == FF_MODERN:
                font_family = "Modern"
            elif block.font_family == FF_SCRIPT:
                font_family = "Script"
            elif block.font_family == FF_DECORATIVE:
                font_family = "Decorative"
            else:
                font_family = "Unknown"
            # end if
            font_family = "{0} (0x{1:X})".format(
                font_family, block.font_family
            )

            if block.font_weight >= 700:
                font_weight = "Bold ({0})".format(block.font_weight)
            else:
                font_weight = "Regular ({0})".format(block.font_weight)
            # end if

            if block.cursor_size <= 25:
                cursor_size = "Small ({0})".format(block.cursor_size)
            elif block.cursor_size <= 50:
                cursor_size = "Medium ({0})".format(block.cursor_size)
            else:
                cursor_size = "Large ({0})".format(block.cursor_size)
            # end if

            if block.full_screen:
                full_screen = "True ({0})".format(block.full_screen)
            else:
                full_screen = "False (0)"
            # end if

            if block.insert_mode:
                insert_mode = "True ({0})".format(block.insert_mode)
            else:
                insert_mode = "False (0)"
            # end if

            if block.auto_position:
                auto_position = "True ({0})".format(block.auto_position)
            else:
                auto_position = "False (0)"
            # end if

            if block.history_no_dup:
                history_no_dup = "True ({0})".format(block.history_no_dup)
            else:
                history_no_dup = "False (0)"
            # end if

            fore_blue = bool(block.fill_attributes & FOREGROUND_BLUE)
            fore_green = bool(block.fill_attributes & FOREGROUND_GREEN)
            fore_red = bool(block.fill_attributes & FOREGROUND_RED)
            fore_intense = bool(block.fill_attributes & FOREGROUND_INTENSITY)
            back_blue = bool(block.fill_attributes & BACKGROUND_BLUE)
            back_green = bool(block.fill_attributes & BACKGROUND_GREEN)
            back_red = bool(block.fill_attributes & BACKGROUND_RED)
            back_intense = bool(block.fill_attributes & BACKGROUND_INTENSITY)

            pop_fore_blue = bool(block.popup_fill_attributes & FOREGROUND_BLUE)
            pop_fore_green = \
                bool(block.popup_fill_attributes & FOREGROUND_GREEN)
            pop_fore_red = bool(block.popup_fill_attributes & FOREGROUND_RED)
            pop_fore_intense = \
                bool(block.popup_fill_attributes & FOREGROUND_INTENSITY)
            pop_back_blue = bool(block.popup_fill_attributes & BACKGROUND_BLUE)
            pop_back_green = \
                bool(block.popup_fill_attributes & BACKGROUND_GREEN)
            pop_back_red = bool(block.fill_attributes & BACKGROUND_RED)
            pop_back_intense = \
                bool(block.popup_fill_attributes & BACKGROUND_INTENSITY)


            output.append(" ConsoleDataBlock:")
            output.append(" -----------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Screen buffer size (horizontal): {0}".format(
                block.screen_buffer_size.x
            ))
            output.append("  Screen buffer size (vertical): {0}".format(
                block.screen_buffer_size.y
            ))
            output.append("  Window size (horizontal): {0}".format(
                block.window_size.x
            ))
            output.append("  Window size (vertical): {0}".format(
                block.window_size.y
            ))
            output.append("  Window origin: ({0}, {1})".format(
                block.window_origin.x, block.window_origin.y
            ))
            output.append("  Font: {0}".format(block.font))
            output.append("  Input buffer size: {0}".format(
                block.input_buf_size
            ))
            output.append("  Font size: {0}".format(block.font_size))
            output.append("  Font family: {0}".format(font_family))
            output.append("  Font weight: {0}".format(font_weight))
            output.append("  Face name: {0}".format(block.face_name))
            output.append("  Cursor size: {0}".format(cursor_size))
            output.append("  Full screen: {0}".format(full_screen))
            output.append("  Insert mode: {0}".format(insert_mode))
            output.append("  Auto position window: {0}".format(auto_position))
            output.append("  History buffer size: {0}".format(
                block.history_buf_size
            ))
            output.append("  Number of history buffers: {0}".format(
                block.history_buf_count
            ))
            output.append("  Remove history duplicates: {0}".format(
                history_no_dup
            ))

            output.append("")
            output.append("  Fill Attributes:")
            output.append("  ----------------")
            output.append("   Blue (foreground): {0}".format(fore_blue))
            output.append("   Green (foreground): {0}".format(fore_green))
            output.append("   Red (foreground): {0}".format(fore_red))
            output.append("   Intensity (foreground): {0}".format(
                fore_intense
            ))
            output.append("   Blue (background): {0}".format(back_blue))
            output.append("   Green (background): {0}".format(back_green))
            output.append("   Red (background): {0}".format(back_red))
            output.append("   Intensity (background): {0}".format(
                back_intense
            ))

            output.append("")
            output.append("  Popup Fill Attributes:")
            output.append("  ----------------------")
            output.append("   Blue (foreground): {0}".format(pop_fore_blue))
            output.append("   Green (foreground): {0}".format(pop_fore_green))
            output.append("   Red (foreground): {0}".format(pop_fore_red))
            output.append("   Intensity (foreground): {0}".format(
                pop_fore_intense
            ))
            output.append("   Blue (background): {0}".format(pop_back_blue))
            output.append("   Green (background): {0}".format(pop_back_green))
            output.append("   Red (background): {0}".format(pop_back_red))
            output.append("   Intensity (background): {0}".format(
                pop_back_intense
            ))


            output.append("")
            output.append("  Color Table:")
            output.append("  ------------")

            output_str = (
                "   "
                "0x{0:0>8X}, "
                "0x{1:0>8X}, "
                "0x{2:0>8X}, "
                "0x{3:0>8X}"
            )

            for counter in range(4):
                value0 = block.color_table[(counter * 4)]
                value1 = block.color_table[((counter * 4) + 1)]
                value2 = block.color_table[((counter * 4) + 2)]
                value3 = block.color_table[((counter * 4) + 3)]

                output.append(output_str.format(
                    value0, value1, value2, value3
                ))
            # end for

        elif isinstance(block, ConsoleFEProps):
            output.append(" ConsoleFEDataBlock:")
            output.append(" -------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Code Page: {0}".format(block.code_page))

        elif isinstance(block, DarwinProps):
            output.append(" DarwinDataBlock:")
            output.append(" ----------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Darwin data ANSI: {0}".format(
                block.darwin_data_ansi
            ))
            output.append("  Darwin data unicode: {0}".format(
                block.darwin_data_uni
            ))

        elif isinstance(block, EnvironmentProps):
            output.append(" EnvironmentVariableDataBlock:")
            output.append(" ------------------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Target ANSI: {0}".format(block.target_ansi))
            output.append("  Target unicode: {0}".format(block.target_uni))

        elif isinstance(block, IconEnvironmentProps):
            output.append(" IconEnvironmentDataBlock:")
            output.append(" -------------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Target ANSI: {0}".format(block.target_ansi))
            output.append("  Target unicode: {0}".format(block.target_uni))

        elif isinstance(block, KnownFolderProps):
            output.append(" KnownFolderDataBlock:")
            output.append(" ---------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Known folder ID: {0}".format(block.kf_id))
            output.append("  Offset: {0}".format(block.offset))

        elif isinstance(block, PropertyStoreProps):
            output.append(" PropertyStoreDataBlock:")
            output.append(" -----------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))

            if full_output:
                output.append("  Property store:")
                output.append("{0}".format(block.property_store))
            else:
                output.append("  Property store: {0}".format(
                    block.property_store[:15]
                ))
            # end if

        elif isinstance(block, ShimProps):
            output.append(" ShimDataBlock:")
            output.append(" --------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Layer name: {0}".format(block.layer_name))

        elif isinstance(block, SpecialFolderProps):
            if block.sf_id in csidl_names:
                name = csidl_names[block.sf_id]
                if block.sf_id in csidl_display_names:
                    disp_name = csidl_display_names[block.sf_id]

                    sf_id = "{0} (0x{1:X}) ({2})".format(
                        disp_name, block.sf_id, name
                    )
                else:
                    sf_id = "{0} (0x{1:X})".format(name, block.sf_id)
                # end if
            else:
                sf_id = "0x{0:X}".format(block.sf_id)
            # end if

            output.append(" SpecialFolderDataBlock:")
            output.append(" -----------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Special folder id: {0}".format(sf_id))
            output.append("  Offset: {0}".format(block.offset))

        elif isinstance(block, TrackerProps):
            output.append(" TrackerDataBlock:")
            output.append(" -----------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("  Length: {0}".format(block.length))
            output.append("  Version: {0}".format(block.version))
            output.append("  Machine ID: {0}".format(block.machine_id))
            output.append("")
            output.append("  DROID:")
            output.append("  ------")
            output.append("   Volume: {0}".format(block.droid.volume))
            output.append("   Object: {0}".format(block.droid.object))
            output.append("")
            output.append("  DROID Birth:")
            output.append("  ------------")
            output.append("   Volume: {0}".format(block.droid_birth.volume))
            output.append("   Object: {0}".format(block.droid_birth.object))

        elif isinstance(block, VistaAndAboveIDListProps):
            output.append(" VistaAndAboveIDListDataBlock:")
            output.append(" -----------------------------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))
            output.append("")

            output.append("  Item ID List:")
            output.append("  -------------")

            temp_output = list()
            for shitemid in block.idlist.mkid:
                temp_output.append("   Byte count: {0}".format(shitemid.cb))

                if shitemid.abID is not None:
                    if full_output:
                        temp_output.append("   Data:")
                        temp_output.append("{0}".format(shitemid.abID))
                    else:
                        temp_output.append("   Data: {0}".format(
                            shitemid.abID[:15]
                        ))
                    # end if
                else:
                    temp_output.append("   Data: Not in file")
                # end if

                temp_output.append("")
            else:
                if temp_output[-1] == "":
                    temp_output = temp_output[:-1]
                # end if
            # end for

            output.extend(temp_output)

        else:
            output.append(" DataBlock:")
            output.append(" ----------")
            output.append("  Size: {0}".format(block.size))
            output.append("  Signature: {0}".format(sig_output))

            if full_output:
                output.append("  Data:")
                output.append(block.data)
            else:
                output.append("  Data: {0}".format(block.data[:15]))
            # end if
        # end if

        output.append("")
    # end for

    return output
# end def format_extra_data

def format_output(lnk, full_output):
    output = list()

    output.append("Shell Link Header")
    output.append("=================")
    output.extend(format_header_info(lnk))
    output.append("")
    output.append("")

    output.append("Link Target IDList")
    output.append("==================")
    output.extend(format_idlist(lnk, full_output))
    output.append("")
    output.append("")

    output.append("Link Info")
    output.append("=========")
    output.extend(format_link_info(lnk))
    output.append("")
    output.append("")

    output.append("String Data")
    output.append("===========")
    output.extend(format_string_data(lnk))
    output.append("")
    output.append("")

    output.append("Extra Data")
    output.append("==========")
    output.extend(format_extra_data(lnk, full_output))
    output.append("")

    return output
# end def format_output


def main():
    usage = "%prog [options] lnkfile"
    description = "\n".join([
        "Displays information from shell link (.lnk) files.",
        "",
        "If file is '-' then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-f",
        dest="full_output",
        action="store_true",
        help="Display full output for binary attributes",
        default=False
    )

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("You must supply a file name or '-'")
    # end if

    if args[0] == "-":
        lnk = ShellLink(ByteIStream(sys.stdin.buffer.read()))
        filename = "-stdin-"
    else:
        lnk = ShellLink(RawIStream(args[0]))
        filename = args[0]
    # end if

    output = ["File: {0}".format(filename)]
    output.append("")
    output.extend(format_output(lnk, options.full_output))
    print("\n".join(output))
# end def main()

if __name__ == "__main__":
    main()
# end if
