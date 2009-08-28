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
Objects for working with shell link (.lnk) files

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "ShellLink", "ShellLinkHeader", "LinkInfo", "VolumeID", "CNRL",
    "ConsoleProps", "ConsoleFEProps", "DarwinProps", "EnvironmentProps",
    "IconEnvironmentProps", "KnownFolderProps", "PropertyStoreProps",
    "ShimProps", "SpecialFolderProps", "TrackerProps",
    "VistaAndAboveIDListProps", "TerminalBlock", "ExtraDataBlockFactory",
    "ExtraDataBlock"
]

from lf.io.consts import SEEK_SET
from lf.datatype.extractors import uint16_le, uint32_le
from lf.windows.time import filetime_to_datetime
from lf.windows.guid import guid_to_uuid

from lf.windows.shell.link import extractors
from lf.windows.shell.link.consts import (
    CONSOLE_PROPS_SIG, CONSOLE_FE_PROPS_SIG, DARWIN_PROPS_SIG,
    ENVIRONMENT_PROPS_SIG, ICON_ENVIRONMENT_PROPS_SIG, KNOWN_FOLDER_PROPS_SIG,
    PROPERTY_STORE_PROPS_SIG, SHIM_PROPS_SIG, SPECIAL_FOLDER_PROPS_SIG,
    TRACKER_PROPS_SIG, VISTA_AND_ABOVE_IDLIST_PROPS_SIG
)

class ShellLink():
    """
    Represents a shell link (.lnk) file.

    .. attribute:: header

        A ShellLinkHeader object.

    .. attribute:: id_list

        A list of ItemID objects describing the target (or None if not present).

    .. attribute:: link_info

        A LinkInfo object (or None if not present).

    .. attribute:: name_str

        Description of the shortcut (or None if not present).

    .. attribute:: relative_path

        Specifies the location of the shortcut (or None if not present).

    .. attribute:: working_dir

        Specifies the file system path of the shortcut (or None if not
        present).

    .. attribute:: args

        Command line arguments when activating the target (or None if not
        present).

    .. attribute:: icon_location

        The location of the link icon (or None if not present).

    .. attribute:: extra_data

        A list of ExtraDataBlock objects.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a ShellLink object.

        :parameters:
            stream
                A stream that contains the shell link (.lnk) file.

            offset
                The start of the shell link, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = ShellLinkHeader(stream, offset)
        offset += header.size
        flags = header.flags

        is_unicode = flags.is_unicode
        char_width = 1 + is_unicode

        id_list = list()
        if flags.has_id_list:
            id_list_size = uint16_le.extract(stream.read(2))[0]
            offset += 2

            bytes_read = 0
            while bytes_read < id_list_size:
                item_id_size = uint16_le.extract(stream.read(2))[0]
                bytes_read += 2

                if not item_id_size:
                    break
                # end if

                item_id_size -= 2

                id_list.append(stream.read(item_id_size))
                bytes_read += item_id_size
            # end while
            if bytes_read < id_list_size:
                bytes_read = id_list_size
            # end if

            offset += bytes_read
        # end if

        if flags.has_link_info:
            link_info = LinkInfo(stream, offset)
            offset += link_info.size
        else:
            link_info = None
        # end if
        stream.seek(offset, SEEK_SET)  # Because LinkInfo may move the pointer

        if flags.has_name:
            char_count = uint16_le.extract(stream.read(2))[0] * char_width

            name_str = stream.read(char_count)
            offset += (char_count + 2)

            if is_unicode:
                try:
                    name_str = name_str.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            # end if
        else:
            name_str = None
        # end if

        if flags.has_relative_path:
            char_count = uint16_le.extract(stream.read(2))[0] * char_width

            relative_path = stream.read(char_count)
            offset += (char_count + 2)

            if is_unicode:
                try:
                    relative_path = relative_path.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            # end if
        else:
            relative_path = None
        # end if

        if flags.has_working_dir:
            char_count = uint16_le.extract(stream.read(2))[0] * char_width

            working_dir = stream.read(char_count)
            offset += (char_count + 2)

            if is_unicode:
                try:
                    working_dir = working_dir.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            # end if
        else:
            working_dir = None
        # end if

        if flags.has_args:
            char_count = uint16_le.extract(stream.read(2))[0] * char_width

            args = stream.read(char_count)
            offset += (char_count + 2)

            if is_unicode:
                try:
                    args = args.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            # end if
        else:
            args = None
        # end if

        if flags.has_icon_location:
            char_count = uint16_le.extract(stream.read(2))[0] * char_width

            icon_location = stream.read(char_count)
            offset += (char_count + 2)

            if is_unicode:
                try:
                    icon_location = icon_location.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            # end if
        else:
            icon_location = None
        # end if

        extra_data = list(ExtraDataBlockFactory.make_blocks(stream, offset))


        self.header = header
        self.id_list = id_list
        self.link_info = link_info
        self.name_str = name_str
        self.relative_path = relative_path
        self.working_dir = working_dir
        self.args = args
        self.icon_location = icon_location
        self.extra_data = extra_data
    # end def __init__
# end class ShellLink

class ShellLinkHeader():
    """
    Represents a header from a shell link (.lnk) file.

    .. attribute:: size

        The size of the header structure

    .. attribute:: clsid

        The CLSID of the link.

    .. attribute:: flags

        The flags for the shell link header.  See LinkFlags() struct for a list
        of the individual fields.

    .. attribute:: attrs

        The file attributes for the target.  See FileAttributes() struct for a
        list of the individual fields.

    .. attribute:: btime

        The creation time of the target.

    .. attribute:: atime

        The last access time of the target.

    .. attribute:: mtime

        The last modification time of the target.

    .. attribute:: target_size

        The size of the target.

    .. attribute:: icon_index

        The index of an icon.

    .. attribute:: show_cmd

        The state of the window, if one is launched.

    .. attribute:: vkcode

        The virtual keycode of the hotkey, used to activate the link.

    .. attribute:: vkmod

        The modifiers to vkcode.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a ShellLinkHeader object.

        :parameters:
            stream
                A stream that contains the ShellLinkHeader.

            offset
                The start of the ShellLinkHeader, in the stream.
        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = extractors.header.extract(stream.read(76))

        clsid = header.clsid
        clsid = guid_to_uuid(
            clsid.data1, clsid.data2, clsid.data3, clsid.data4
        )

        try:
            btime = filetime_to_datetime(header.btime)
        except (ValueError, TypeError):
            btime = header.btime
        # end try

        try:
            atime = filetime_to_datetime(header.atime)
        except (ValueError, TypeError):
            atime = header.atime
        # end try

        try:
            mtime = filetime_to_datetime(header.mtime)
        except (ValueError, TypeError):
            mtime = header.mtime
        # end try

        self.size = header.size
        self.clsid = clsid
        self.flags = header.flags
        self.attrs = header.attrs
        self.btime = btime
        self.atime = atime
        self.mtime = mtime
        self.target_size = header.target_size
        self.icon_index = header.icon_index
        self.show_cmd = header.show_cmd
        self.vkcode = header.hotkey.vkcode
        self.vkmod = header.hotkey.vkmod
    # end def __init__
# end class ShellLinkHeader

class LinkInfo():
    """
    Represents a LinkInfo structure.

    .. attribute:: size

        The size of the LinkInfo structure.

    .. attribute:: header_size

        The size of the LinkInfo header.

    .. attribute:: vol_id

        The VolumeID structure (or None if not present).

    .. attribute:: cnrl

        The CommonNetworkRelativeLink structure (or None if not present).

    .. attribute:: local_base_path

        The local path prefix (or None if not present).

    .. attribute:: local_base_path_uni

        The unicode version of local_base_path (or None if not present).

    .. attribute:: path_suffix

        The field appended to local_base_path (or None if not present).

    .. attribute:: path_suffix_uni

        The unicode version of path_suffix (or None if not present).
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a LinkInfo structure.

        :parameters:
            stream
                A stream that contains the LinkInfo structure.

            offset
                The start of the LinkInfo structure, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = extractors.link_info_header.extract(stream.read(36))

        size = header.size

        if header.header_size >= 0x24:
            if header.has_vol_id_and_local_base_path:
                local_base_path_uni_offset = \
                    uint32_le.extract(stream.read(4))[0]
            else:
                local_base_path_uni_offset = None
            # end if

            path_suffix_uni_offset = uint32_le.extract(stream.read(4))[0]

            if local_base_path_uni_offset:
                local_base_path_uni_offset += offset
                stream.seek(local_base_path_uni_offset, SEEK_SET)
                local_base_path_uni = stream.read(
                    size - local_base_path_uni_offset
                )

                for offset in range(0, len(local_base_path_uni), 2):
                    if local_base_path_uni[offset:offset+2] == b"\x00\x00":
                        local_base_path_uni = local_base_path_uni[:offset]
                        break
                    # end if
                # end for

                try:
                    local_base_path_uni = \
                        local_base_path_uni.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            else:
                local_base_path_uni = None
            # end if

            if path_suffix_uni_offset:
                path_suffix_uni_offset += offset
                stream.seek(path_suffix_uni_offset, SEEK_SET)
                path_suffix_uni = stream.read(size - path_suffix_uni_offset)

                for offset in range(0, len(path_suffix_uni), 2):
                    if path_suffix_uni[offset:offset+2] == b"\x00\x00":
                        path_suffix_uni = path_suffix_uni[:offset]
                        break
                    # end if
                # end for

                try:
                    path_suffix_uni = path_suffix_uni.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            else:
                path_suffix_uni = None
            # end if
        else:
            path_suffix_uni = None
            local_base_path_uni = None
        # end if

        if header.has_vol_id_and_local_base_path:
            if header.vol_id_offset:
                vol_id = VolumeID(stream, offset + header.vol_id_offset)
            else:
                vol_id = None
            # end if

            if header.local_base_path_offset:
                new_offset = header.local_base_path_offset + offset

                stream.seek(new_offset, SEEK_SET)
                local_base_path = stream.read(size - new_offset)
                local_base_path = local_base_path.split(b"\x00", 1)[0]
            else:
                local_base_path = None
            # end if
        else:
            vol_id = None
            local_base_path = None
        # end if

        if header.has_cnrl_and_path_suffix:
            cnrl = CNRL(stream, offset + header.cnrl_offset)
        else:
            cnrl = None
        # end if

        if header.path_suffix_offset:
            new_offset = header.path_suffix_offset + offset
            stream.seek(new_offset, SEEK_SET)
            path_suffix = stream.read(size - new_offset)
            path_suffix = path_suffix.split(b"\x00", 1)[0]
        # end if

        self.size = header.size
        self.header_size = header.header_size
        self.vol_id = vol_id
        self.local_base_path = local_base_path
        self.local_base_path_uni = local_base_path_uni
        self.cnrl = cnrl
        self.path_suffix = path_suffix
        self.path_suffix_uni = path_suffix_uni
    # end def __init__
# end class LinkInfo

class VolumeID():
    """
    Represents a VolumeID structure.

    .. attribute:: size

        The size of the volume id structure.

    .. attribute:: type

        The type of drive the target is stored on.

    .. attribute:: serial_num

        The serial number of the drive the target is on.

    .. attribute:: volume_label

        The volume label of the drive the target is on.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a VolumeID object.

        :parameters:
            stream
                A stream that contains the volume id structure.

            offset
                The start of the volume id structure, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = extractors.volume_id_header.extract(stream.read(16))

        if header.size == 0x14:
            # Volume label is unicode
            vol_label_uni_offset = uint32_le.extract(stream.read(4))[0]

            if vol_label_uni_offset:
                new_offset = vol_label_uni_offset + offset
                stream.seek(new_offset, SEEK_SET)
                volume_label = stream.read(header.size - new_offset)

                for offset in range(0, len(volume_label), 2):
                    if volume_label[offset:offset+2] == b"\x00\x00":
                        volume_label = volume_label[:offset]
                    # end if
                # end for

                try:
                    volume_label = volume_label.decode("utf_16_le")
                except UnicodeError:
                    pass
                # end try
            # end if
        else:
            new_offset = header.vol_label_offset + offset
            stream.seek(new_offset, SEEK_SET)
            volume_label = stream.read(header.size - new_offset)
            volume_label = volume_label.split(b"\x00", 1)[0]
        # end if

        self.size = header.size
        self.type = header.type
        self.serial_num = header.serial_num
        self.volume_label = volume_label
    # end def __init__
# end class VolumeID

class CNRL():
    """
    Represents a Common Network Relative Link structure.

    .. attribute:: size

        The size of the CNRL structure.

    .. attribute:: net_name

        The server share (or None if not present).

    .. attribute:: net_name_uni

        The unicode version of net_name (or None if not present).

    .. attribute:: device_name

        The drive letter (or None if not present).

    .. attribute:: device_name_uni

        The unicode version of device_name (or None if not present).

    .. attribute:: device_name_valid

        Whether or not the device_name attribute should be set.

    .. attribute:: net_type

        The type of network (or None if not present.

    .. attribute:: net_type_valid

        Whether or not the net_type attribute should be set.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a CNRL structure.

        :parameters:
            stream
                A stream that contains the CNRL structure.

            offset
                The start of the CNRL structure, in the stream.
        """

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = extractors.cnrl_header.extract(stream.read(20))
        size = header.size

        if header.net_name_offset > 0x14:
            net_name_uni_offset = uint32_le.extract(stream.read(4))[0]
        else:
            net_name_uni_offset = None
        # end if

        if header.valid_device:
            if header.net_name_offset > 0x14:
                device_name_uni_offset = uint32_le.extract(stream.read(4))[0]
            else:
                device_name_uni_offset = None
            # end if
        else:
            device_name_uni_offset = None
        # end if

        if net_name_uni_offset:
            net_name_uni_offset += offset
            stream.seek(net_name_uni_offset, SEEK_SET)
            net_name_uni = stream.read(size - net_name_uni_offset)

            for offset in range(0, len(net_name_uni), 2):
                if net_name_uni[offset:offset+2] == b"\x00\x00":
                    net_name_uni = net_name_uni[:offset]
                    break
                # end if
            # end for

            try:
                net_name_uni = net_name_uni.decode("utf_16_le")
            except UnicodeError:
                pass
            # end try
        else:
            net_name_uni = None
        # end if

        if device_name_uni_offset:
            device_name_uni_offset += offset
            stream.seek(device_name_uni_offset, SEEK_SET)
            device_name_uni = stream.read(size - device_name_uni_offset)

            for offset in range(0, len(device_name_uni), 2):
                if device_name_uni[offset:offset+2] == b"\x00\x00":
                    device_name_uni = device_name_uni[:offset]
                    break
                # end if
            # end for

            try:
                device_name_uni = device_name_uni.decode("utf_16_le")
            except UnicodeError:
                pass
            # end try
        else:
            device_name_uni = None
        # end if

        if header.valid_device and header.device_name_offset:
            new_offset = header.device_name_offset + offset
            stream.seek(new_offset, SEEK_SET)
            device_name = stream.read(size - new_offset)
            device_name = device_name.split(b"\x00", 1)[0]
        else:
            device_name = None
        # end if

        if header.net_name_offset:
            new_offset = header.net_name_offset + offset
            stream.seek(new_offset, SEEK_SET)
            net_name = stream.read(size - new_offset)
            net_name = net_name.split(b"\x00", 1)[0]
        else:
            net_name = None
        # end if

        if header.valid_net_type:
            net_type = header.net_type
        else:
            net_type = None
        # end if

        self.size = size
        self.net_name = net_name
        self.net_name_uni = net_name_uni
        self.device_name = device_name
        self.device_name_uni = device_name_uni
        self.device_name_valid = header.valid_device
        self.net_type = net_type
        self.net_type_valid = header.valid_net_type
    # end def __init__
# end class CNRL

class ExtraDataBlock():
    """
    Represents an ExtraDataBlock structure.

    .. attribute:: size

        The size of the ExtraDataBlock structure.

    .. attribute:: sig

        The signature of the ExtraDataBlock structure.
    """

    def __init__(self, size, sig):
        """
        Initializes an ExtraDataBlock object.

        :parameters:
            size
                The size of the ExtraDataBlock structure.

            sig
                The signature of th ExtraDataBlock structure.
        """

        self.size = size
        self.sig = sig
    # end def __init__
# end class ExtraDataBlock

class ConsoleProps(ExtraDataBlock):
    """
    Represents a ConsoleProps structure.

    .. attribute:: fill_attributes

        The foreground and background text colors for the console window.

    .. attribute:: popup_fill_attributes

        The foreground and background text colors for the console window popup.

    .. attribute:: screen_buffer_size

        A tuple (x,y) of the dimensions of the console window buffer.

    .. attribute:: window_size

        A tuple (x,y) of the dimensions of the console window.

    .. attribute:: window_origin

        A tuple (x,y) of the console window origin.

    .. attribute:: font_size

        The size (in pixels) of the font to use in the console window.

    .. attribute:: font_family

        The family of the font to use in the console window.

    .. attribute:: font_weight

        The stroke weight of the font to use in the console window.

    .. attribute:: face_name

        The face name of the font to use in the console window.

    .. attribute:: cursor_size

        The size of the cursor (in pixels) to use in the console window.

    .. attribute:: full_screen

        Whether or not to open the console window in full screen mode.

    .. attribute:: insert_mode

        Whether or not to enable insert mode in the console window.

    .. attribute: auto_position

        Whether or not to automatically position the console window.

    .. attribute:: history_buff_size

        The number of characters to store in the history of the console window.

    .. attribute:: history_buff_count

        The number of history buffers.

    .. attribute:: history_no_dup

        Whether or not duplicates are stored in the history buffers.

    .. attribute:: color_table

        A tuple of the RGB colors used for text in the console window.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a ConsoleProps object.

        :parameters:
            size
                The size of the ConsoleProps.

            sig
                The signature of the ConsoleProps.

            stream
                A stream that contains the ConsoleProps.

            offset
                The start of the ConsoleProps (after the header), in the
                stream.
        """

        super(ConsoleProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        cdb = extractors.console_data_block.extract(stream.read(188))
        face_name = cdb.face_name

        for offset in range(0, len(face_name), 2):
            if face_name[offset:offset+2] == b"\x00\x00":
                face_name = face_name[:offset]
                break
            # end if
        # end for

        try:
            face_name = face_name.decode("utf_16_le")
        except UnicodeError:
            pass
        # end try

        self.fill_attributes = cdb.fill_attributes
        self.popup_fill_attributes = cdb.popup_fill_attributes
        self.screen_buffer_size = cdb.screen_buffer_size
        self.window_size = cdb.window_size
        self.window_origin = cdb.window_origin
        self.font_size = cdb.font_size
        self.font_family = cdb.font_family
        self.font_weight = cdb.font_weight
        self.face_name = face_name
        self.cursor_size = cdb.cursor_size
        self.full_screen = cdb.full_screen
        self.insert_mode = cdb.insert_mode
        self.auto_position = cdb.auto_position
        self.history_buff_size = cdb.history_buff_size
        self.history_buff_count = cdb.history_buff_count
        self.history_no_dup = cdb.history_no_dup
        self.color_table = cdb.color_table
    # end def __init__
# end class ConsoleProps

class ConsoleFEProps(ExtraDataBlock):
    """
    Represents a ConsoleFEProps structure.

    .. attribute:: lcid

        The code page LCID used to display text.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a ConsoleFEProps object.

        :parameters:
            size
                The size of the ConsoleFEProps structure.

            sig
                The signature for the ConsoleFEProps structure.

            stream
                A stream that contains the ConsoleFEProps structure.

            offset
                The start of the ConsoleFEProps structure (after the
                header), in the stream.
        """

        super(ConsoleFEProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        self.lcid = lcid_le.extract(stream.read(4))
    # end def __init__
# end class ConsoleFEProps

class DarwinProps(ExtraDataBlock):
    """
    Represents a DarwinProps structure.

    .. attribute:: darwin_data_ansi

        An application identifier.

    .. attribute:: darwin_data_uni

        A unicode version of darwin_data_ansi.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a DarwinProps object.

        :parameters:
            size
                The size of the DarwinProps structure.

            sig
                The signature for the DarwinProps structure.

            stream
                A stream that contains the DarwinProps structure.

            offset
                The start of the DarwinDatablock structure (after the header),
                in the stream.
        """

        super(DarwinProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        darwin_data_ansi = stream.read(260).split(b"\x00", 1)[0]
        darwin_data_uni = stream.read(520)

        for offset in range(0,len(darwin_data_uni), 2):
            if darwin_data_uni[offset:offset+2] == b"\x00\x00":
                darwin_data_uni = darwin_data_uni[:offset]
                break
            # end if
        # end for

        try:
            darwin_data_uni = darwin_data_uni.decode("utf_16_le")
        except UnicodeError:
            pass
        # end try

        self.darwin_data_ansi = darwin_data_ansi
        self.darwin_data_uni = darwin_data_uni
    # end def __init__
# end class DarwinProps

class ExpandableStringsDataBlock(ExtraDataBlock):
    """
    Represents an EnvironmentDataBlock (or IconEnvironmentProps) structure.

    :parameters:
        target_ansi
            The path that is constructed with environment variables.

        target_uni
            The unicode version of target_ansi.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes an ExpandableStringsDataBlock object.

        :parameters:
            size
                The size of the ExpandableStringDataBlock structure.

            sig
                The signature of the ExpandableStringDataBlock structure.

            stream
                A stream that contains the ExpandableStringDataBlock structure.

            offset
                The start of the ExpandableStringDataBlock structure (after the
                header), in the stream.
        """

        super(ExpandableStringsDataBlock, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        target_ansi = stream.read(260).split(b"\x00", 1)[0]
        target_uni = stream.read(520)

        for offset in range(0, len(target_uni), 2):
            if target_uni[offset:offset+2] == b"\x00\x00":
                target_uni = target_uni[:offset]
                break
            # end if
        # end for

        try:
            target_uni = target_uni.decode("utf_16_le")
        except UnicodeError:
            pass
        # end try

        self.target_ansi = target_ansi
        self.target_uni = target_uni
    # end def __init__
# end class ExpandableStringsDataBlock

class EnvironmentProps(ExpandableStringsDataBlock):
    pass
# end class EnvironmentProps

class IconEnvironmentProps(ExpandableStringsDataBlock):
    pass
# end class IconEnvironmentProps

class KnownFolderProps(ExtraDataBlock):
    """
    Represents a KnownFolderProps structure.

    .. attribute:: kfid

        A GUID for the folder.

    .. attribute:: offset

        The index in the item id list of the known folder.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a KnownFolderProps object.

        :parameters:
            size
                The size of the KnownFolderProps structure.

            sig
                The signature for the KnownFolderProps structure.

            stream
                A stream that contains the KnownFolderProps structure.

            offset
                The start of the KnownFolderProps structure (after the
                header), in the stream.
        """

        super(KnownFolderProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        (kfid, offset) = \
            extractors.known_folder_data_block.extract(stream.read(20))

        kfid = \
            guid_to_uuid(kfid.data1, kfid.data2, kfid.data3, kfid.data4)

        self.kfid = kfid
        self.offset = offset
    # end class __init__
# end class KnownFolderProps

class PropertyStoreProps(ExtraDataBlock):
    """
    Represents a PropertyStoreProps structure.

    .. attribute:: property_store

        A serialized property storage structure (currently not implemented)
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a PropertyStoreProps object.

        :parameters:
            size
                The size of the PropertyStoreProps structure.

            sig
                The signature of the PropertyStoreProps structure.

            stream
                A stream that contains the PropertyStoreProps structure.

            offset
                The start of the PropertyStoreProps structure (after the
                header), in the stream.
        """

        super(PropertyStoreProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        self.property_store = stream.read(size - 8)
    # end class __init__
# end class PropertyStoreProps

class ShimProps(ExtraDataBlock):
    """
    Represents a ShimProps structure.

    .. attribute:: layer_name

        A unicode name of the shim layer to use when running the target.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a ShimProps object.

        :parameters:
            size
                The size of the ShimProps structure.

            sig
                The signature of the ShimProps structure.

            stream
                A stream that contains the ShimProps structure.

            offset
                The start of the ShimProps structure (after the header), in
                the stream.
        """

        super(ShimProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        layer_name = stream.read(size - 8)
        for offset in range(0, len(layer_name), 2):
            if layer_name[offset:offset+2] == b"\x00\x00":
                layer_name = layer_name[:offset]
                break
            # end if
        # end for

        try:
            layer_name = layer_name.decode("utf_16_le")
        except UnicodeError:
            pass
        # end try

        self.layer_name = layer_name
    # end def __init__
# end class ShimProps

class SpecialFolderProps(ExtraDataBlock):
    """
    Represents a SpecialFolderProps structure.

    .. attribute:: special_folder_id

        The folder identifier.

    .. attribute:: offset

        The index in the item id list of the special folder.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a SpecialFolderProps object.

        :parameters:
            size
                The size of the SpecialFolderProps structure.

            sig
                The signature of the SpecialFolderProps structure.

            stream
                A stream that contains the SpecialFolderProps structure.

            offset
                The start of the SpecialFolderProps structure (after the
                header), in the stream.
        """

        super(SpecialFolderProps, self).__init__(size, sig)
        (self.special_folder_id, self.offset) = \
            extractors.special_folder_data_block.extract(stream.read(8))
    # end def __init__
# end class SpecialFolderProps

class DomainRelativeObjId():
    """
    Represents a DomainRelativeObjId structure.

    .. attribute:: volume

        The volume field for a DomainRelativeObjId.

    .. attribute:: object

        The object field for a DomainRelativeObjId.
    """

    def __init__(self, volume, object_):
        """
        Initializes a DomainRelativeObjId object.

        :parameters:
            volume
                The volume field for a DomainRelativeObjId.

            object_
                The object field for a DomainRelativeObjId.
        """

        self.volume = volume
        self.object = object_
    # end def __init__
# end class DomainRelativeObjId

class TrackerProps(ExtraDataBlock):
    """
    Represents a TrackerProps structure.

    .. attribute:: version

        The version field from the TrackerProps structure.

    .. attribute:: machine_id

        The NetBIOS name of the machine the target was last known to reside.

    .. attribute:: droid

        A DomainRelativeObjId structure used to find the target.

    .. attribute:: droid_birth
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a TrackerProps object.

        :parameters:
            size
                The size of the TrackerProps structure.

            sig
                The signature of the TrackerProps structure.

            stream
                A stream that contains the TrackerProps structure.

            offset
                The start of the TrackerProps structure (after the
                header), in the stream.
        """

        super(TrackerProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        (length, version) = \
            extractors.tracker_data_block.extract(stream.read(8))

        self.version = version

        self.machine_id = stream.read(length - 72).split(b"\x00", 1)[0]
        (droid, droid_birth) = \
            extractors.tracker_data_block_footer.extract(stream.read(64))

        volume = guid_to_uuid(
            droid.volume.data1,
            droid.volume.data2,
            droid.volume.data3,
            droid.volume.data4
        )

        object_ = guid_to_uuid(
            droid.object.data1,
            droid.object.data2,
            droid.object.data3,
            droid.object.data4
        )

        self.droid = DomainRelativeObjId(volume, object_)

        volume = guid_to_uuid(
            droid_birth.volume.data1,
            droid_birth.volume.data2,
            droid_birth.volume.data3,
            droid_birth.volume.data4
        )

        object_ = guid_to_uuid(
            droid_birth.object.data1,
            droid_birth.object.data2,
            droid_birth.object.data3,
            droid_birth.object.data4,
        )

        self.droid_birth = DomainRelativeObjId(volume, object_)
    # end def __init__
# end class TrackerProps

class VistaAndAboveIDListProps(ExtraDataBlock):
    """
    Represents a VistaAndAboveIDListProps structure.

    .. attribute:: id_list

        An alternate item id list.
    """

    def __init__(self, size, sig, stream, offset=None):
        """
        Initializes a VistaAndAboveIDListProps object.

        :parameters:
            size
                The size of the VistaAndAboveIDListProps structure.

            sig
                The signature of the VistaAndAboveIDListProps structure.

            stream
                A stream that contains the VistaAndAboveIDListProps
                structure.

            offset
                The start of the VistaAndAboveIDListProps structure
                (after the header), in the stream.
        """

        super(VistaAndAboveIDListProps, self).__init__(size, sig)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        id_list = list()
        id_list_size = size - 8

        bytes_read = 0
        while bytes_read < id_list_size:
            item_id_size = uint16_le.extract(stream.read(2))[0]
            bytes_read += 2

            if not item_id_size:
                break
            # end if

            item_id_size -= 2

            id_list.append(stream.read(item_id_size))
            bytes_read += item_id_size
        # end while

        self.id_list = id_list
    # end def __init__
# end class VistaAndAboveIDListProps

class TerminalBlock(ExtraDataBlock):
    """Represents a Terminal block"""

    def __init__(self, size):
        """
        Initializes a TerminalBlock object.

        :parameters:
            size
                The size of the terminal block
        """

        super(TerminalBlock, self).__init__(size, 0)
    # end def __init__
# end class TerminalBlock

class ExtraDataBlockFactory():
    """
    Makes ExtraDataBlock objects.

    .. attribute:: props_class_map

        A mapping of *_PROPS_SIG values to their corresponding class object.
    """

    props_class_map = {
        CONSOLE_PROPS_SIG: ConsoleProps,
        CONSOLE_FE_PROPS_SIG: ConsoleFEProps,
        DARWIN_PROPS_SIG: DarwinProps,
        ENVIRONMENT_PROPS_SIG: EnvironmentProps,
        ICON_ENVIRONMENT_PROPS_SIG: IconEnvironmentProps,
        KNOWN_FOLDER_PROPS_SIG: KnownFolderProps,
        PROPERTY_STORE_PROPS_SIG: PropertyStoreProps,
        SHIM_PROPS_SIG: ShimProps,
        SPECIAL_FOLDER_PROPS_SIG: SpecialFolderProps,
        TRACKER_PROPS_SIG: TrackerProps,
        VISTA_AND_ABOVE_IDLIST_PROPS_SIG: VistaAndAboveIDListProps
    }

    @staticmethod
    def make_blocks(stream, offset=None):
        """
        Creates a series of ExtraDataBlock objects.

        :parameters:
            stream
                A stream that contains the ExtraDataBlock structure.

            offset
                The start of the ExtraDataBlock structure, in the stream.

        :rtype: iterator
        :returns: An iterator that produces each ExtraDataBlock object.
        """

        if offset is None:
            offset = stream.tell()
        # end if

        max_bytes_left = stream.size - offset

        while max_bytes_left >= 0x8:
            stream.seek(offset, SEEK_SET)
            header = extractors.data_block.extract(stream.read(8))

            size = header.size
            sig = header.sig

            if size < 4:
                yield TerminalDataBlock()
            # end if

            if sig in ExtraDataBlockFactory.props_class_map:
                block = ExtraDataBlockFactory.props_class_map[sig](
                    size, sig, stream
                )
                yield block
            # end if

            offset += size
            max_bytes_left -= size
        else:
            if max_bytes_left >= 4:
                last_value = uint32_le.extract(stream.read(4))[0]
                if last_value < 4:
                    yield TerminalBlock(last_value)
                # end if
        # end while
    # end def make_blocks
# end class ExtraDataBlockFactory
