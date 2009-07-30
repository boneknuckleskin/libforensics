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
Dumps information from shell link (.lnk) files

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

import sys
from datetime import datetime
from optparse import OptionParser
from lf.io import byte, raw
from lf.windows.consts.vkcode import virtual_key_code_names
from lf.windows.consts.hotkey import (
    HOTKEYF_SHIFT, HOTKEYF_CONTROL, HOTKEYF_ALT, HOTKEYF_EXT
)
from lf.windows.consts.lcid import lang_id_names
from lf.windows.shell.link.consts import (
    DRIVE_UNKNOWN, DRIVE_NO_ROOT_DIR, DRIVE_REMOVABLE, DRIVE_FIXED,
    DRIVE_REMOTE, DRIVE_CDROM, DRIVE_RAMDISK, wnnc_net_names,

    FF_DONTCARE, FF_ROMAN, FF_SWISS, FF_MODERN, FF_SCRIPT, FF_DECORATIVE,

    CONSOLE_PROPS_SIG, CONSOLE_FE_PROPS_SIG, DARWIN_PROPS_SIG,
    ENVIRONMENT_PROPS_SIG, ICON_ENVIRONMENT_PROPS_SIG, KNOWN_FOLDER_PROPS_SIG,
    PROPERTY_STORE_PROPS_SIG, SHIM_PROPS_SIG, SPECIAL_FOLDER_PROPS_SIG,
    TRACKER_PROPS_SIG, VISTA_AND_ABOVE_IDLIST_PROPS_SIG
)
from lf.windows.shell.consts.showwin import sw_names
from lf.windows.shell.consts.csidl import csidl_names, csidl_display_names
from lf.windows.shell.consts.knownfolders import kfid_names, kfid_display_names
from lf.windows.shell.link.objects import ShellLink, TerminalBlock

def format_time(datetime_obj):
    """Formats a date/time object"""

    if not isinstance(datetime_obj, datetime):
        return str(datetime_obj)
    # end if

    dto = datetime_obj
    formatted = "{0:02}/{1:02}/{2:02} {3:02}:{4:02}:{5:02}".format(
        dto.month, dto.day, dto.year, dto.hour, dto.minute, dto.second
    )

    return formatted
# end def format_time

def create_header(lnk, filename):
    """Creates basic header information"""

    output = list()

    flags_info = [
        ("has_id_list", "Has item id list"),
        ("has_link_info", "Has link information"),
        ("has_name", "Has NAME_STRING"),
        ("has_relative_path", "Has RELATIVE_PATH"),
        ("has_working_dir", "Has WORKING_DIR"),
        ("has_args", "Has COMMAND_LINE_ARGUMENTS"),
        ("has_icon_location", "Has ICON_LOCATION"),
        ("is_unicode", "Has Unicode encoded strings"),
        ("force_no_link_info", "Ignore LinkInfo structure"),
        ("has_exp_string", "Has EnvironmentVariableDataBlock structure"),
        ("run_in_separate_proc", "Run in separate vm"),
        ("has_logo3_id", "Has logo3 id (unused)"),
        ("has_darwin_id", "Has DarwinDataBlock structure"),
        ("run_as_user", "Run as a different user"),
        ("has_exp_icon", "Has IconEnvironmentDataBlock structure"),
        ("no_pidl_alias", "In shell namespace"),
        ("force_unc_name", "Force UNC name"),
        ("run_with_shim_layer", "Run with shim layer"),
        ("force_no_link_track", "Object ID distributed tracking disabled"),
        ("enable_target_metadata", "Cache target metadata"),
        ("disable_link_path_tracking", "Shell link tracking disabled"),
        ("disable_known_folder_rel_tracking", "Known folder tracking disabled"),
        ("no_kf_alias", "Known folder alias mapping disabled"),
        ("allow_link_to_link", "Can point to other shell link files"),
        ("unalias_on_save", "Remove alias when saving item id list"),
        ("prefer_environment_path", "Recalculate item id list from path"),
        (
            "keep_local_idlist_for_unc_target",
            "Keep local copy of item id list (if on UNC)"
        )
    ]

    attrs_info = [
        ("read_only", "Read only"),
        ("hidden", "Hidden"),
        ("system", "System"),
        ("directory", "Directory"),
        ("archive", "Archive"),
        ("normal", "Normal"),
        ("temp", "Temporary"),
        ("sparse", "Sparse"),
        ("reparse_point", "Reparse point"),
        ("compressed", "Compressed"),
        ("offline", "Offline"),
        ("not_content_indexed", "Contents need indexing"),
        ("encrypted", "Encrypted")
    ]

    header = lnk.header

    output.append("Header Information")
    output.append("------------------")
    output.append("Filename: {0}".format(filename))
    output.append("CLSID: {0}".format(header.clsid))

    if header.show_cmd in sw_names:
        show_str = "0x{0:X} ({1})".format(
            header.show_cmd, sw_names[header.show_cmd]
        )
    else:
        show_str = "0x{0:X}".format(header.show_cmd)
    # end if
    output.append("Show command: {0}".format(show_str))

    vkcode = header.vkcode
    vkmod = header.vkmod
    hk_str = "{0:02X}:{1:02X}".format(vkcode, vkmod)
    hk_name_str = list()

    if vkmod:
        if vkmod & HOTKEYF_SHIFT:
            hk_name_str.append("Shift")
        # end if

        if vkmod & HOTKEYF_CONTROL:
            hk_name_str.append("Ctrl")
        # end if

        if vkmod & HOTKEYF_ALT:
            hk_name_str.append("Alt")
        # end if

        if vkmod & HOTKEYF_EXT:
            hk_name_str.append("Extended")
        # end if
    # end if

    if vkcode:
        if vkcode in virtual_key_code_names:
            hk_name_str.append(virtual_key_code_names[vkcode])
        else:
            hk_name_str.append(chr(vkcode))
        # end if
    # end if

    if hk_name_str:
        hk_name_str = " + ".join(hk_name_str)
        hk_name_str = "({0})".format(hk_name_str)
    # end if

    output.append("Hotkey: {0} {1}".format(hk_str, hk_name_str))

    output.append("")
    output.append(" Flags")
    output.append(" -----")

    for (attr_name, text) in flags_info:
        value = getattr(header.flags, attr_name)

        if value:
            value = "Yes"
        else:
            value = "No"
        # end if

        output.append(" {0}: {1}".format(text, value))
    # end for

    output.append("")
    output.append(" Target Metadata")
    output.append(" ---------------")
    output.append(" Creation time: {0}".format(format_time(header.btime)))
    output.append(" Access time: {0}".format(format_time(header.atime)))
    output.append(" Modification time: {0}".format(format_time(header.mtime)))
    output.append(" File size: {0}".format(header.target_size))
    output.append(" Icon index: {0}".format(header.icon_index))

    output.append("")
    output.append("  Attributes")
    output.append("  ----------")

    for (attr_name, text) in attrs_info:
        value = getattr(header.attrs, attr_name)

        if value:
            value = "Yes"
        else:
            value = "No"
        # end if

        output.append("  {0}: {1}".format(text, value))
    # end for

    output.append("")
    return output
# end def create_header

def create_item_id_list(lnk):
    """Creates information about the item id list"""

    output = list()

    output.append("Item ID List")
    output.append("------------")

    if not lnk.header.flags.has_id_list:
        output.append("Not in file")
        output.append("")
        return output
    # end if

    for (index, item_id) in enumerate(lnk.id_list):
        output.append("{0}: {1}".format(index, item_id))
    # end for

    output.append("")
    return output
# end def create_item_id_list

def create_volume_id(lnk):
    """Creates information about the volume id structure"""

    output = list()

    drive_type_names = {
        DRIVE_UNKNOWN: "Unknown",
        DRIVE_NO_ROOT_DIR: "No root path",
        DRIVE_REMOVABLE: "Removable",
        DRIVE_FIXED: "Fixed",
        DRIVE_REMOTE: "Remote (network)",
        DRIVE_CDROM: "CD-ROM",
        DRIVE_RAMDISK: "RAM disk"
    }

    output.append(" Volume ID")
    output.append(" ---------")

    if not lnk.link_info.vol_id:
        output.append(" Not in file")
        output.append("")
        return output
    # end if

    vol_id = lnk.link_info.vol_id

    if vol_id.type in drive_type_names:
        type_str = "{0} ({1})".format(
            vol_id.type, drive_type_names[vol_id.type]
        )
    else:
        type_str = "{0}".format(vol_id.type)
    # end if

    output.append(" Drive type: {0}".format(type_str))
    output.append(" Drive serial num: 0x{0:X}".format(vol_id.serial_num))
    output.append(" Volume label: {0}".format(vol_id.volume_label))

    output.append("")
    return output
# end def create_volume_id

def create_cnrl(lnk):
    """Creates information about the CNRL structure"""

    output = list()

    output.append(" Common Network Relative Link")
    output.append(" ----------------------------")

    if not lnk.link_info.cnrl:
        output.append(" Not in file")
        output.append("")
        return output
    # end if

    cnrl = lnk.link_info.cnrl

    if cnrl.device_name_valid:
        device_name_valid = "Yes"
    else:
        device_name_valid = "No"
    # end if

    output.append(" Device name valid: {0}".format(device_name_valid))

    if cnrl.device_name is not None:
        device_name = cnrl.device_name
    else:
        device_name = "Not in file"
    # end if
    output.append(" Device name: {0}".format(device_name))

    if cnrl.device_name_uni is not None:
        device_name_uni = cnrl.device_name_uni
    else:
        device_name_uni = "Not in file"
    # end if
    output.append(" Device name (unicode): {0}".format(device_name_uni))

    if cnrl.net_name is not None:
        net_name = cnrl.net_name
    else:
        net_name = "Not in file"
    # end if
    output.append(" Net name: {0}".format(net_name))

    if cnrl.net_name_uni is not None:
        net_name_uni = cnrl.net_name_uni
    else:
        net_name_uni = "Not in file"
    # end if
    output.append(" Net name (unicode): {0}".format(net_name_uni))

    if cnrl.net_type_valid:
        net_type_valid = "Yes"
    else:
        net_type_valid = "No"
    # end if
    output.append(" Net type valid: {0}".format(net_type_valid))

    if cnrl.net_type in wnnc_net_names:
        net_type_str = "0x{0:X} ({1})".format(
            cnrl.net_type, wnnc_net_names[cnrl.net_type]
        )
    else:
        net_type_str = "0x{0:X}".format(cnrl.net_type)
    # end if
    output.append(" Net type: {0}".format(net_type_str))

    output.append("")
    return output
# end def create_cnrl

def create_link_info(lnk):
    """Creates information about the link_info structure"""

    output = list()

    output.append("Link Info")
    output.append("---------")

    if not lnk.header.flags.has_link_info:
        output.append("Not in file")
        output.append("")
        return output
    # end if

    info = lnk.link_info

    if info.local_base_path is not None:
        local_base_path = info.local_base_path
    else:
        local_base_path = "Not in file"
    # end if
    output.append("Local base path: {0}".format(local_base_path))

    if info.local_base_path_uni is not None:
        local_base_path_uni = info.local_base_path_uni
    else:
        local_base_path_uni = "Not in file"
    # end if
    output.append("Local base path (unicode): {0}".format(local_base_path_uni))

    if info.path_suffix is not None:
        path_suffix = info.path_suffix
    else:
        path_suffix = "Not in file"
    # end if
    output.append("Path suffix: {0}".format(path_suffix))

    if info.path_suffix_uni is not None:
        path_suffix_uni = info.path_suffix_uni
    else:
        path_suffix_uni = "Not in file"
    # end if
    output.append("Path suffix (unicode): {0}".format(path_suffix_uni))
    output.append("")

    output.extend(create_volume_id(lnk))
    output.extend(create_cnrl(lnk))
    return output
# end def create_link_info

def create_string_data(lnk):
    """Creates information about the strings"""

    output = list()

    output.append("String Data")
    output.append("-----------")

    if lnk.name_str is not None:
        data = lnk.name_str
    else:
        data = "Not in file"
    # end if
    output.append("NAME_STRING: {0}".format(data))

    if lnk.relative_path is not None:
        data = lnk.relative_path
    else:
        data = "Not in file"
    # end if
    output.append("RELATIVE_PATH: {0}".format(data))

    if lnk.working_dir is not None:
        data = lnk.working_dir
    else:
        data = "Not in file"
    # end if
    output.append("WORKING_DIR: {0}".format(data))

    if lnk.args is not None:
        data = lnk.args
    else:
        data = "Not in file"
    # end if
    output.append("COMMAND_LINE_ARGS: {0}".format(data))

    if lnk.icon_location is not None:
        data = lnk.icon_location
    else:
        data = "Not in file"
    # end if
    output.append("ICON_LOCATION: {0}".format(data))

    output.append("")
    return output
# end def create_string_data

def create_data_block(block):
    """Creates information about an individual ExtraDataBlock"""

    output = list()

    sig = block.sig

    if sig == CONSOLE_PROPS_SIG:
        output.append(" Console Data Block")
        output.append(" ------------------")
        output.append(" Fill attributes: {0}".format(block.fill_attributes))
        output.append(" Popup fill attributes: {0}".format(
            block.popup_fill_attributes
            )
        )
        output.append(" Screen buffer size: {0}".format(
            block.screen_buffer_size
            )
        )
        output.append(" Window size: {0}".format(block.window_size))
        output.append(" Window origin: {0}".format(block.window_origin))
        output.append(" Font size: {0} px".format(block.font_size))

        font_family = block.font_family
        if font_family == FF_DONTCARE:
            ff_str = "0x{0:X} (Don't Care)".format(font_family)
        elif font_family == FF_ROMAN:
            ff_str = "0x{0:X} (Roman)".format(font_family)
        elif font_family == FF_SWISS:
            ff_str = "0x{0:X} (Swiss)".format(font_family)
        elif font_family == FF_MODERN:
            ff_str = "0x{0:X} (Modern)".format(font_family)
        elif font_family == FF_SCRIPT:
            ff_str = "0x{0:X} (Script)".format(font_family)
        elif font_family == FF_DECORATIVE:
            ff_str = "0x{0:X} (Decorative)".format(font_family)
        else:
            ff_str = "0x{0:X}".format(font_family)
        # end if
        output.append(" Font family: {0}".format(ff_str))

        font_weight = block.font_weight
        if font_weight >= 700:
            output.append(" Font weight: {0} (bold)".format(font_weight))
        else:
            output.append(" Font weight: {0} (regular)".format(font_weight))
        # end if

        output.append(" Face name: {0}".format(block.face_name))

        cursor_size = block.cursor_size
        if cursor_size <= 25:
            cursor_str = "0x{0:X} (small)".format(cursor_size)
        elif cursor_size <= 50:
            cursor_str = "0x{0:X} (medium)".format(cursor_size)
        else:
            cursor_str = "0x{0:X} (large)".format(cursor_size)
        # end if
        output.append(" Cursor size: {0}".format(cursor_str))

        full_screen = block.full_screen
        if full_screen:
            full_screen_str = "0x{0:X} (Yes)".format(full_screen)
        else:
            full_screen_str = "0x{0:X} (No)".format(full_screen)
        # end if
        output.append(" Full screen: {0}".format(full_screen_str))

        insert_mode = block.insert_mode
        if insert_mode:
            insert_str = "0x:{0:X} (Yes)".format(insert_mode)
        else:
            insert_str = "0x:{0:X} (No)".format(insert_mode)
        # end if
        output.append(" Insert mode: {0}".format(insert_str))

        auto_pos = block.auto_position
        if auto_pos:
            auto_str = "0x:{0:X} (Yes)".format(auto_pos)
        else:
            auto_str = "0x:{0:X} (No)".format(auto_pos)
        # end if
        output.append(" Auto position: {0}".format(auto_str))

        output.append(" History buffer size: {0}".format(
            block.history_buff_size
            )
        )

        output.append(" Number of history buffers: {0}".format(
            block.history_buff_count
            )
        )

        history_no_dup = block.history_no_dup
        if history_no_dup:
            hist_str = "0x{0X:} (Yes)".format(history_no_dup)
        else:
            hist_str = "0x{0:X} (No)".format(history_no_dup)
        # endif
        output.append(" Allow duplicates in history {0}".format(hist_str))

        output.append("  Color Table")
        output.append("  -----------")

        for (index, entry) in enumreate(block.color_table):
            output.append("  {0}: 0x{0:X}".format(index, entry))
        # end for

    elif sig == CONSOLE_FE_PROPS_SIG:
        output.append(" Console FE Data Block")
        output.append(" ---------------------")

        if block.lcid.lang_id in lang_id_names:
            lang_id_str = "0x{0:X} ({1})".format(
                block.lcid.lang_id, lang_id_names[block.lcid.lang_id]
            )
        else:
            lang_id_str = "0x{0:X}".format(block.lcid.lang_id)
        # end if
        output.append(" Lang ID: {0}".format(lang_id_str))

    elif sig == DARWIN_PROPS_SIG:
        output.append(" Darwin Data Block")
        output.append(" -----------------")
        output.append(" Darwin data (ansi): {0}".format(
            block.darwin_data_ansi
            )
        )
        output.append(" Darwin data (unicode): {0}".format(
            block.darwin_data_uni
            )
        )

    elif sig == ENVIRONMENT_PROPS_SIG:
        output.append(" Environment Variable Data Block")
        output.append(" -------------------------------")
        output.append(" Target (ansi): {0}".format(block.target_ansi))
        output.append(" Target (unicode): {0}".format(block.target_uni))

    elif sig == ICON_ENVIRONMENT_PROPS_SIG:
        output.append(" Icon Environment Data Block")
        output.append(" ---------------------------")
        output.append(" Target (ansi): {0}".format(block.target_ansi))
        output.append(" Target (unicode): {0}".format(block.target_uni))

    elif sig == KNOWN_FOLDER_PROPS_SIG:
        output.append(" Known Folder Data Block")
        output.append(" -----------------------")

        kfid = block.kfid
        if kfid in kfid_names:
            if kfid in kfid_display_names:
                kfid_str = "{0} ({1}, \"{2}\")".format(
                    kfid, kfid_names[kfid], kfid_display_names[kfid]
                )
            else:
                kfid_str = "{0} ({1})".format(kfid, kfid_names[kfid])
            # end if
        else:
            kfid_str = "{0}".format(kfid)
        # end if

        output.append(" Known folder ID: {0}".format(kfid_str))
        output.append(" Offset: 0x{0:X}".format(block.offset))

    elif sig == PROPERTY_STORE_PROPS_SIG:
        output.append(" Property Store Data Block")
        output.append(" -------------------------")
        output.append(" Property store: {0}".format(block.property_store))

    elif sig == SHIM_PROPS_SIG:
        output.append(" Shim Data Block")
        output.append(" ---------------")
        output.append(" Layer name: {0}".format(block.layer_name))

    elif sig == SPECIAL_FOLDER_PROPS_SIG:
        output.append(" Special Folder Data Block")
        output.append(" -------------------------")

        fs_id = block.special_folder_id
        if fs_id in csidl_names:
            if fs_id in csidl_display_names:
                sf_str = "0x{0:X} ({1}, \"{2}\")".format(
                    fs_id, csidl_names[fs_id], csidl_display_names[fs_id]
                )
            else:
                sf_str = "0x{0:X} ({1})".format(fs_id, csidl_names[fs_id])
            # end if
        else:
            sf_str = "0x{0:X}".format(fs_id)
        # end if
        output.append(" Special folder ID: {0}".format(sf_str))
        output.append(" Offset: 0x{0:X}".format(block.offset))

    elif sig == TRACKER_PROPS_SIG:
        output.append(" Tracker Data Block")
        output.append(" ------------------")
        output.append(" Version: 0x{0:X}".format(block.version))
        output.append(" Machine ID: {0}".format(block.machine_id))
        output.append(" Droid (volume): {0}".format(block.droid.volume))
        output.append(" Droid (object): {0}".format(block.droid.object))
        output.append(" Droid birth (volume): {0}".format(
            block.droid_birth.volume
            )
        )
        output.append(" Droid birth (object): {0}".format(
            block.droid_birth.object
            )
        )

    elif sig == VISTA_AND_ABOVE_IDLIST_PROPS_SIG:
        output.append(" Vista and Above ID List Data Block")
        output.append(" ----------------------------------")

        for (index, entry) in enumerate(block.id_list):
            output.append(" {0}: {1}".format(index, entry))
        # end for

    elif isinstance(block, TerminalBlock):
        output.append(" Terminal Data Block")
        output.append(" -------------------")
        output.append(" Size: {0}".format(block.size))

    else:
        output.append(" Unknown Data Block")
        output.append(" ------------------")
        output.append(" Size: 0x{0:X}".format(block.size))
        output.append(" Sig: 0x{0:X}".format(block.sig))
    # end if

    output.append("")
    return output
# end def create_data_block

def create_extra_data(lnk):
    """Creates information about the extra data blocks"""

    output = list()
    extra_data = lnk.extra_data

    output.append("Extra Data")
    output.append("----------")

    if not extra_data:
        output.append("Not in file")
        output.append("")
        return output
    # end if

    for block in extra_data:
        output.extend(create_data_block(block))
    # end for

    output.append("")
    return output
# end def create_extra_data

parser = OptionParser()
parser.set_usage("%prog [lnk file]")

(options, args) = parser.parse_args()

if not args:
    filename = "--stdin--"
    lnk = ShellLink(byte.open(sys.stdin.buffer.read()))
else:
    filename = args[0]
    lnk = ShellLink(raw.open(filename))
# end if

output = list()
output.extend(create_header(lnk, filename))
output.extend(create_item_id_list(lnk))
output.extend(create_link_info(lnk))
output.extend(create_string_data(lnk))
output.extend(create_extra_data(lnk))

print("\n".join(output))
