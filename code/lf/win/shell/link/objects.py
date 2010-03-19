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

"""Objects for working with shell link files"""

# stdlib imports
from codecs import utf_16_le_decode as _utf16_le_decoder

# local imports
from lf.dec import SEEK_SET
from lf.dtypes import (
    LITTLE_ENDIAN, ActiveStructuple, CtypesWrapper, Structuple
)
from lf.dtypes.ctypes import uint32_le, uint16_le
from lf.time import FILETIMETodatetime
from lf.win.objects import GUIDToUUID, CLSIDToUUID, LCID
from lf.win.con.objects import COORD

from lf.win.shell.objects import ITEMIDLIST
from lf.win.shell.link.ctypes import (
    shell_link_header, link_info_header, volume_id_header, cnrl_header,
    console_data_block, known_folder_data_block, special_folder_data_block,
    tracker_data_block, tracker_data_block_footer, data_block_header,
    file_attributes, link_flags, console_fe_data_block, darwin_data_block,
    expandable_strings_data_block
)
from lf.win.shell.link.consts import (
    CONSOLE_PROPS_SIG, CONSOLE_FE_PROPS_SIG, DARWIN_PROPS_SIG,
    ENVIRONMENT_PROPS_SIG, ICON_ENVIRONMENT_PROPS_SIG, KNOWN_FOLDER_PROPS_SIG,
    PROPERTY_STORE_PROPS_SIG, SHIM_PROPS_SIG, SPECIAL_FOLDER_PROPS_SIG,
    TRACKER_PROPS_SIG, VISTA_AND_ABOVE_IDLIST_PROPS_SIG
)

__docformat__ = "restructuredtext en"
__all__ = [
    "ShellLink", "FileAttributes", "LinkFlags", "ShellLinkHeader",
    "StringData", "LinkInfo", "VolumeID", "CNRL", "ExtraDataBlock",
    "ConsoleProps", "ConsoleFEProps", "DarwinProps",
    "ExpandableStringsDataBlock", "EnvironmentProps", "IconEnvironmentProps",
    "KnownFolderProps", "PropertyStoreProps", "ShimProps",
    "SpecialFolderProps", "DomainRelativeObjId", "TrackerProps",
    "VistaAndAboveIDListProps", "TerminalBlock", "ExtraDataBlockFactory",
    "StringDataSet"
]

class ShellLink():
    """Represents a shell link (.lnk) file.

    .. attribute:: header

        A :class:`ShellLinkHeader` object.

    .. attribute:: idlist

        An :class:`~lf.win.shell.objects.ITEMIDLIST` describing the target (or
        None if not present).

    .. attribute:: link_info

        A :class:`LinkInfo` object (or None if not present).

    .. attribute:: string_data

        An instance of a :class:`StringDataSet` object.

    .. attribute:: extra_data

        A list of :class:`ExtraDataBlock` objects.

    """

    def __init__(self, stream, offset=None):
        """Initializes a ShellLink object.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the link file.

        :type offset: ``int``
        :param offset: The start of the link file, in :attr:`stream`.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        header = ShellLinkHeader.from_stream(stream, offset)
        offset += header.size
        flags = header.flags

        is_unicode = flags.is_unicode

        if flags.has_idlist:
            stream.seek(offset, SEEK_SET)
            id_list_size = uint16_le.from_buffer_copy(stream.read(2)).value
            offset += 2
            id_list = ITEMIDLIST.from_stream(stream, offset, id_list_size)
            offset += id_list_size
        else:
            id_list = None
        # end if

        if flags.has_link_info:
            link_info = LinkInfo.from_stream(stream, offset)
            offset += link_info.size
        else:
            link_info = None
        # end if

        if flags.has_name:
            name_str = StringData.from_stream(stream, offset, is_unicode)
            offset += name_str.size
        else:
            name_str = None
        # end if

        if flags.has_relative_path:
            rel_path  = StringData.from_stream(stream, offset, is_unicode)
            offset += rel_path.size
        else:
            rel_path = None
        # end if

        if flags.has_working_dir:
            working_dir = StringData.from_stream(stream, offset, is_unicode)
            offset += working_dir.size
        else:
            working_dir = None
        # end if

        if flags.has_args:
            cmd_args = StringData.from_stream(stream, offset, is_unicode)
            offset += cmd_args.size
        else:
            cmd_args = None
        # end if

        if flags.has_icon_location:
            icon_location = StringData.from_stream(stream, offset, is_unicode)
            offset += icon_location.size
        else:
            icon_location = None
        # end if

        string_data = StringDataSet((
            name_str, rel_path, working_dir, cmd_args, icon_location
        ))

        extra_data = list(ExtraDataBlockFactory.make_blocks(stream, offset))

        self.header = header
        self.idlist = id_list
        self.link_info = link_info
        self.string_data = string_data
        self.extra_data = extra_data
    # end def __init__
# end class ShellLink

class StringDataSet(Structuple):
    """Represents a collection of :class:`StringData` objects.

    .. attribute:: name_str

        A :class:`StringData` object describing the shortcut (or ``None`` if
        not present).

    .. attribute:: rel_path

        A :class:`StringData` object describing the path to the target,
        relative to the file that contains the link (or ``None`` if not
        present).

    .. attribute:: working_dir

        A :class:`StringData` object describing the working directory to use
        when activating/running the target (or ``None`` if not present).

    .. attribute:: cmd_args

        A :class:`StringData` object describing the command line arguments to
        use when activating/running the target (or ``None`` if not present).

    .. attribute:: icon_location

        A :class:`StringData` object describing the location of the icon to
        display for the link file (or ``None`` if not present).

    """
    _fields_ = (
        "name_str", "rel_path", "working_dir", "cmd_args", "icon_location"
    )
    __slots__ = ()
# end class StringDataSet

class StringData(ActiveStructuple):
    """Represents a StringData structure.

    .. attribute:: size

        The size of the :class:`StringData` structure in bytes.

    .. attribute:: char_count

        The number of characters in the string.

    .. attribute:: string

        The string associated with the structure.

    """
    _fields_ = (
        "size", "char_count", "string"
    )
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None, is_unicode=True):
        """Creates a :class:`StringData` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :type is_unicode: ``bool``
        :param is_unicode: If the string is in unicode (utf16-le)

        :rtype: :class:`StringData`
        :returns: The corresponding :class:`StringData` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        char_count = uint16_le.from_buffer_copy(stream.read(2)).value
        offset += 2

        if is_unicode:
            read_size = char_count * 2
        else:
            read_size = char_count
        # end if

        string = stream.read(read_size)

        if is_unicode:
            new_string = _utf16_le_decoder(string, "ignore")[0]

            if new_string:
                string = new_string
            # end if
        # end if

        return cls((read_size + 2, char_count, string))
    # end def from_stream
# end class StringData

class FileAttributes(CtypesWrapper):
    """ Represents the file system attributes of a link target.

    .. attribute:: read_only

        True if the target is read only.

    .. attribute:: hidden

        True if the target is hidden.

    .. attribute:: system

        True if the target has the system attribute set.

    .. attribute:: directory

        True if the target is a directory.

    .. attribute:: archive

        True if the target has the archive attribute set.

    .. attribute:: normal

        True if this is the only bit set.

    .. attribute:: temp

        True if the target is a temp file.

    .. attribute:: sparse

        True if the target is a sparse file.

    .. attribute:: reparse_point

        True if the target is a reparse_point.

    .. attribute:: compressed

        True if the target is compressed.

    .. attribute:: offline

        True if the content of the target is not immediately available.

    .. attribute:: not_content_indexed

        True if the content of the target needs indexing.

    .. attribute:: encrypted

        True if the target is encrypted.

    """

    _fields_ = (
        "read_only", "hidden", "system", "reserved1", "directory", "archive",
        "reserved2", "normal", "temp", "sparse", "reparse_point", "compressed",
        "offline", "not_content_indexed", "encrypted"
    )
    _ctype_ = file_attributes
    __slots__ = tuple()
# end def FileAttributes

class LinkFlags(CtypesWrapper):
    """Represents the LinkFlags structure from :class:`ShellLinkHeader`.

    .. attribute:: has_idlist

        True if the link has an :class:`~lf.win.shell.objects.ITEMIDLIST` for
        the target.

    .. attribute:: has_link_info

        True if the link has a LinkInfo structure.

    .. attribute:: has_name

        True if the link has a NAME_STRING StringData structure.

    .. attribute:: has_relative_path

        True if the link has a RELATIVE_PATH StringData structure.

    .. attribute:: has_working_dir

        True if the link has a WORKING_DIR StringData structure.

    .. attribute:: has_args

        True if the link has a COMMAND_LINE_ARGUMENTS StringData structure.

    .. attribute:: has_icon_location

        True if the link has an ICON_LOCATION StringData structure.

    .. attribute:: is_unicode

        True if the link has unicode encoded strings.

    .. attribute:: force_no_link_info

        True if the LinkInfo structure should be ignored.

    .. attribute:: has_exp_string

        True if the link has an EnvironmentVariableDataBlock structure.

    .. attribute:: run_in_separate_proc

        True if the target is run in a separate VM.

    .. attribute:: has_logo3_id

        Undefined.

    .. attribute:: has_darwin_id

        True if the link has a DarwinDataBlock structure.

    .. attribute:: run_as_user

        True if the target is run as a different user.

    .. attribute:: has_exp_icon

        True if the link has an IconEnvironmentDataBlock structure.

    .. attribute:: no_pidl_alias

        True if the file system locations is represented in the shell
        namespace.

    .. attribute:: force_unc_name

        True if UNC naming is required.

    .. attribute:: run_with_shim_layer

        True if the link has a ShimDataBlock structure.

    .. attribute:: force_no_link_track

        True if the TrackerDataBlock structure should be ignored.

    .. attribute:: enable_target_metadata

        True if the link has metadata about the target.

    .. attribute:: disable_link_path_tracking

        True if the EnvironmentVariableDataBlock structure should be ignored.

    .. attribute:: disable_known_folder_rel_tracking

        True if the SpecialFolderDataBlock and the KnownFolderDataBlock
        structures should be ignored.

    .. attribute:: no_kf_alias

        True if the unaliased form of the known folder ID list should be used.

    .. attribute:: allow_link_to_link

        True if the target can be another link.

    .. attribute:: unalias_on_save

        True if unaliased form should be used when saving a link.

    .. attribute:: prefer_environment_path

        True if path specified in the EnvironmentVariableDataBlock should be
        used to refer to the target.

    .. attribute:: keep_local_idlist_for_unc_target

        True if the local path IDlist should be stored.

    """
    _fields_ = (
        "has_idlist", "has_link_info", "has_name", "has_relative_path",
        "has_working_dir", "has_args", "has_icon_location", "is_unicode",
        "force_no_link_info", "has_exp_string", "run_in_separate_proc",
        "has_logo3_id", "has_darwin_id", "run_as_user", "has_exp_icon",
        "no_pidl_alias", "force_unc_name", "run_with_shim_layer",
        "force_no_link_track", "enable_target_metadata",
        "disable_link_path_tracking", "disable_known_folder_rel_tracking",
        "no_kf_alias", "allow_link_to_link", "unalias_on_save",
        "prefer_environment_path", "keep_local_idlist_for_unc_target"
    )
    _ctype_ = link_flags
    __slots__ = tuple()
# end class LinkFlags

class ShellLinkHeader(ActiveStructuple):
    """Represents a header from a shell link (.lnk) file.

    .. attribute:: size

        The size of the header structure

    .. attribute:: clsid

        The CLSID of the link.

    .. attribute:: flags

        An instance of :class:`LinkFlags` describing the flags for the shell
        link header.

    .. attribute:: attrs

        An instance of :class:`FileAttributes` describing the file attributes
        for the target.

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
    _fields_ = (
        "size", "clsid", "flags", "attrs", "btime", "atime", "mtime",
        "target_size", "icon_index", "show_cmd", "vkcode", "vkmod"
    )
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`ShellLinkHeader` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`ShellLinkHeader`
        :returns: The corresponding :class:`ShellLinkHeader` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        data = stream.read(76)
        return cls.from_ctype((shell_link_header.from_buffer_copy(data)))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a :class:`ShellLinkHeader` object from a ctype.

        :type ctype: :class:`lf.win.shell.dtypes.ShellLinkHeader`
        :param ctype: An instance of a ShellLinkHeader ctype.

        :rtype: :class:`ShellLinkHeader`
        :returns: The corresponding :class:`ShellLinkHeader` object.

        """
        clsid = CLSIDToUUID.from_ctype(ctype.clsid)

        try:
            btime = FILETIMETodatetime.from_ctype(ctype.btime)
        except (ValueError, TypeError):
            btime = ctype.btime
        # end try

        try:
            atime = FILETIMETodatetime.from_ctype(ctype.atime)
        except (ValueError, TypeError):
            atime = ctype.atime
        # end try

        try:
            mtime = FILETIMETodatetime.from_ctype(ctype.mtime)
        except (ValueError, TypeError):
            mtime = ctype.mtime
        # end try

        attrs = FileAttributes.from_ctype(ctype.attrs)
        flags = LinkFlags.from_ctype(ctype.flags)

        return cls((
            ctype.size, clsid, flags, attrs, btime, atime, mtime,
            ctype.target_size, ctype.icon_index, ctype.show_cmd,
            ctype.hotkey.vkcode, ctype.hotkey.vkmod
        ))
    # end def from_ctype
# end class ShellLinkHeader

class LinkInfo(ActiveStructuple):
    """Represents a LinkInfo structure.

    .. attribute:: size

        The size of the structure.

    .. attribute:: header_size

        The size of the :class:`LinkInfo` header.

    .. attribute:: vol_id_and_local_base_path

        Describes if the volume id and local base path are present.

    .. attribute:: cnrl_and_path_suffix

        Describes if the Common Network Relative Link field is present.

    .. attribute:: vol_id_offset

        The relative offset of the :class:`VolumeID` structure.

    .. attribute:: local_base_path_offset

        The relative offset of the local base path.

    .. attribute:: cnrl_offset

        The relative offset of the CNRL.

    .. attribute:: path_suffix_offset

        The relative offset of the common path suffix.

    .. attribute:: local_base_path_offset_uni

        The unicode version of :attr:`local_base_path_offset` (or ``None`` if
        not present).

    .. attribute:: path_suffix_offset_uni

        The unicode version of :attr:`path_suffix_offset` (or ``None`` if not
        present).

    .. attribute:: vol_id

        The :class:`VolumeID` structure (or ``None`` if not present).

    .. attribute:: cnrl

        The :class:`CNRL` structure (or ``None`` if not present).

    .. attribute:: local_base_path

        The local path prefix (or ``None`` if not present).

    .. attribute:: local_base_path_uni

        The unicode version of :attr:`local_base_path` (or ``None`` if not
        present).

    .. attribute:: path_suffix

        The field appended to :attr:`local_base_path` (or ``None`` if not
        present).

    .. attribute:: path_suffix_uni

        The unicode version of :attr:`path_suffix` (or ``None`` if not
        present).


    """
    _fields_ = (
        "size", "header_size", "vol_id_and_local_base_path",
        "cnrl_and_path_suffix", "vol_id_offset", "local_base_path_offset",
        "cnrl_offset", "path_suffix_offset", "local_base_path_offset_uni",
        "path_suffix_offset_uni", "vol_id", "cnrl", "local_base_path",
        "local_base_path_uni", "path_suffix", "path_suffix_uni"
    )
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`LinkInfo` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`LinkInfo`
        :returns: The corresponding :class:`LinkInfo` object.

        """
        decoder = _utf16_le_decoder

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = link_info_header.from_buffer_copy(stream.read(28))

        size = header.size
        vol_id_offset = header.vol_id_offset
        local_base_path_offset = header.local_base_path_offset
        cnrl_offset = header.cnrl_offset
        path_suffix_offset = header.path_suffix_offset

        if header.header_size >= 0x24:
            local_base_path_offset_uni = \
                uint32_le.from_buffer_copy(stream.read(4)).value
            path_suffix_offset_uni = \
                uint32_le.from_buffer_copy(stream.read(4)).value
        else:
            local_base_path_offset_uni = None
            path_suffix_offset_uni = None
        # end if

        if header.has_vol_id_and_local_base_path:
            vol_id = VolumeID.from_stream(stream, offset + vol_id_offset)

            if local_base_path_offset:
                new_offset = offset + local_base_path_offset
                stream.seek(new_offset, SEEK_SET)
                local_base_path = stream.read(size - local_base_path_offset)
                local_base_path = local_base_path.split(b"\x00", 1)[0]
            else:
                local_base_path = None
            # end if

            if local_base_path_offset_uni:
                new_offset = offset + local_base_path_offset_uni
                read_size = size - local_base_path_offset_uni

                stream.seek(offset, SEEK_SET)
                local_base_path_uni = stream.read(read_size)

                new_local_base_path_uni = \
                    decoder(local_base_path_uni, "ignore")[0]

                if new_local_base_path_uni:
                    local_base_path_uni = \
                        new_local_base_path_uni.split("\x00", 1)[0]
                # end if
            else:
                local_base_path_uni = None
            # end if
        else:
            vol_id = None
            local_base_path = None
            local_base_path_uni = None
        # end if

        if header.has_cnrl_and_path_suffix:
            cnrl = CNRL.from_stream(stream, offset + cnrl_offset)
        else:
            cnrl = None
        # end if

        if path_suffix_offset:
            new_offset = offset + path_suffix_offset
            stream.seek(new_offset)
            path_suffix = stream.read(size - path_suffix_offset)
            path_suffix = path_suffix.split(b"\x00", 1)[0]
        else:
            path_suffix = None
        # end if

        if path_suffix_offset_uni:
            new_offset = offset + path_suffix_offset_uni
            stream.seek(new_offset)
            path_suffix_uni = stream.read(size - path_suffix_offset_uni)

            new_path_suffix_uni = decoder(path_suffix_uni, "ignore")[0]
            if new_path_suffix_uni:
                path_suffix_uni = new_path_suffix_uni.split("\x00", 1)[0]
            # end if
        else:
            path_suffix_uni = None
        # end if


        return cls((
            header.size, header.header_size,
            header.has_vol_id_and_local_base_path,
            header.has_cnrl_and_path_suffix, vol_id_offset,
            local_base_path_offset, cnrl_offset, path_suffix_offset,
            local_base_path_offset_uni, path_suffix_offset_uni, vol_id, cnrl,
            local_base_path, local_base_path_uni, path_suffix, path_suffix_uni
        ))
    # end def from_stream
# end class LinkInfo

class VolumeID(ActiveStructuple):
    """ Represents a VolumeID structure.

    .. attribute:: size

        The size of the volume id structure.

    .. attribute:: drive_type

        The type of drive the target is stored on.

    .. attribute:: drive_serial_num

        The serial number of the drive the target is on.

    .. attribute:: volume_label_offset

        The relative offset of the volume label.

    .. attribute:: volume_label_offset_uni

        The unicode version of :attr:`volume_label_offset` (or ``None`` if not
        present).

    .. attribute:: volume_label

        The volume label of the drive the target is on.

    """
    _fields_ = (
        "size", "drive_type", "drive_serial_num", "volume_label_offset",
        "volume_label_offset_uni", "volume_label"
    )
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`VolumeID` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`VolumeID`
        :returns: The corresponding :class:`VolumeID` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = volume_id_header.from_buffer_copy(stream.read(16))
        size = header.size
        volume_label = None

        if header.vol_label_offset == 0x14:
            # Volume label is unicode
            vol_label_offset_uni = \
                uint32_le.from_buffer_copy(stream.read(4)).value

            if vol_label_offset_uni:
                new_offset = vol_label_offset_uni + offset
                stream.seek(new_offset, SEEK_SET)
                volume_label = stream.read(header.size - vol_label_offset_uni)

                new_volume_label = _utf16_le_decoder(volume_label, "ignore")[0]
                if new_volume_label:
                    volume_label = new_volume_label.split("\x00", 1)[0]
                # end if
            # end if
        else:
            vol_label_offset_uni = None
            new_offset = header.vol_label_offset + offset
            stream.seek(new_offset, SEEK_SET)
            volume_label = stream.read(size - 16)
            volume_label = volume_label.split(b"\x00", 1)[0]
        # end if

        return cls((
            header.size, header.type, header.serial_num,
            header.vol_label_offset, vol_label_offset_uni, volume_label
        ))
    # end def from_stream
# end class VolumeID

class CNRL(ActiveStructuple):
    """Represents a Common Network Relative Link structure.

    .. attribute:: size

        The size of the CNRL structure.

    .. attribute:: valid_device

        True if :attr:`device_name_offset` is valid.

    .. attribute:: valid_net_type

        True if :attr:`net_provider_type` is valid.

    .. attribute:: net_name_offset

        The relative offset of the :attr:`net_name` field.

    .. attribute:: device_name_offset

        The relative offset of the :attr:`device_name` field.

    .. attribute: net_type

        Describes the type of network provider.  See :mod:`lf.win.consts.net`
        for a list of valid network provider type constants.

    .. attribute:: net_name_offset_uni

        The unicode version of :attr:`net_name_offset`.

    .. attribute:: device_name_offset_uni

        The unicode version of :attr:`device_name_offset`.

    .. attribute:: net_name

        Specifies the server path.

    .. attribute:: device_name

        Specifies the device.

    .. attribute:: net_name_uni

        The unicode version of :attr:`net_name`.

    .. attribute:: device_name_uni

        The unicode version of :attr:`device_name`.

    """
    _fields_ = (
        "size", "valid_device", "valid_net_type", "net_name_offset",
        "device_name_offset", "net_type", "net_name_offset_uni",
        "device_name_offset_uni", "net_name", "device_name", "net_name_uni",
        "device_name_uni"
    )
    takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`CNRL` object from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`CNRL`
        :returns: The corresponding :class:`CNRL` object.

        """

        decoder = _utf16_le_decoder

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = cnrl_header.from_buffer_copy(stream.read(20))
        size = header.size
        net_name_offset = header.net_name_offset
        device_name_offset = header.device_name_offset
        valid_device = header.valid_device

        if net_name_offset > 0x14:
            net_name_offset_uni = \
                uint32_le.from_buffer_copy(stream.read(4)).value

            if valid_device:
                device_name_offset_uni = \
                    uint32_le.from_buffer_copy(stream.read(4)).value
            else:
                device_name_offset_uni = None
            # end if
        else:
            net_name_offset_uni = None
            device_name_offset_uni = None
        # end if

        if net_name_offset_uni:
            new_offset = offset + net_name_offset_uni
            stream.seek(new_offset, SEEK_SET)
            net_name_uni = stream.read(size - net_name_offset_uni)

            new_net_name_uni = decoder(net_name_uni, "ignore")[0]
            if new_net_name_uni:
                net_name_uni = new_net_name_uni.split("\x00", 1)[0]
            # end if
        else:
            net_name_uni = None
        # end if

        if device_name_offset_uni:
            new_offset = offset + device_name_offset_uni
            stream.seek(new_offset, SEEK_SET)
            device_name_uni = stream.read(size - device_name_offset_uni)

            new_device_name_uni = decoder(device_name_uni, "ignore")[0]
            if new_device_name_uni:
                device_name_uni = new_device_name_uni.split("\x00", 1)[0]
            # end if
        else:
            device_name_uni = None
        # end if

        if valid_device and device_name_offset:
            new_offset = device_name_offset + offset
            stream.seek(new_offset, SEEK_SET)
            device_name = stream.read(size - device_name_offset)
            device_name = device_name.split(b"\x00", 1)[0]
        else:
            device_name = None
        # end if

        if net_name_offset:
            new_offset = header.net_name_offset + offset
            stream.seek(new_offset, SEEK_SET)
            net_name = stream.read(size - net_name_offset)
            net_name = net_name.split(b"\x00", 1)[0]
        else:
            net_name = None
        # end if

        return cls((
            size, valid_device, header.valid_net_type, net_name_offset,
            device_name_offset, header.net_type, net_name_offset_uni,
            device_name_offset_uni, net_name, device_name, net_name_uni,
            device_name_uni
        ))
    # end def from_stream
# end class CNRL

class ExtraDataBlock(ActiveStructuple):
    """Base class for :class:`ExtraDataBlock` subclasses.

    .. attribute:: size

        The size of the structure in bytes.

    .. attribute:: sig

        The signature field.

    .. attribute:: data

        An optional field that describes the data in the structure.

        .. note::

            Subclasses set this to ``None``

    """
    _fields_ = (
        "size", "sig", "data"
    )
    _takes_stream = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`ExtraDataBlock` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`ExtraDataBlock`
        :returns: The corresponding :class:`ExtraDataBlock` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = data_block_header.from_buffer_copy(stream.read(8))
        offset += 8

        if header.size >= 8:
            data_size = header.size - 8
            data = stream.read(data_size)
        else:
            data = None
        # end if

        return cls((header.size, header.sig, data))
    # end def from_stream
# end class ExtraDataBlock

class ConsoleProps(ExtraDataBlock):
    """Represents a ConsoleProps structure.

    .. attribute:: fill_attributes

        The foreground and background text colors for the console window.

    .. attribute:: popup_fill_attributes

        The foreground and background text colors for the console window popup.

    .. attribute:: screen_buffer_size

        A :class:`~lf.win.con.objects.COORD` object describing the dimensions
        of the console window buffer.

    .. attribute:: window_size

        A :class:`~lf.win.con.objects.COORD` object describing the dimensions
        of the console window.

    .. attribute:: window_origin

        A :class:`~lf.win.con.objects.COORD` object describing the console
        window origin.

    .. attribute:: font

        The font.

    .. attribute:: input_buf_size

        The size of the input buffer.

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

    .. attribute:: quick_edit

        True if the console window should be in quick edit mode.

    .. attribute:: insert_mode

        Whether or not to enable insert mode in the console window.

    .. attribute: auto_position

        Whether or not to automatically position the console window.

    .. attribute:: history_buf_size

        The number of characters to store in the history of the console window.

    .. attribute:: history_buf_count

        The number of characters to store in the history of the console window.

    .. attribute:: history_buf_count

        The number of characters to store in the history of the console window.

    .. attribute:: history_no_dup

        Whether or not duplicates are stored in the history buffers.

    .. attribute:: color_table

        A tuple of the RGB colors used for text in the console window.

    """
    _fields_ = (
        "fill_attributes", "popup_fill_attributes", "screen_buffer_size",
        "window_size", "window_origin", "font", "input_buf_size", "font_size",
        "font_family", "font_weight", "face_name", "cursor_size",
        "full_screen", "quick_edit", "insert_mode", "auto_position",
        "history_buf_size", "history_buf_count", "history_no_dup",
        "color_table", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`ConsoleProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`ConsoleProps`
        :returns: The corresponding :class:`ConsoleProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        cdb = console_data_block.from_buffer_copy(stream.read(204))
        face_name = bytes(cdb.face_name)

        new_face_name = _utf16_le_decoder(face_name, "ignore")[0]
        if new_face_name:
            face_name = new_face_name.split("\x00", 1)[0]
        # end if

        screen_buffer_size = COORD.from_ctype(cdb.screen_buffer_size)
        window_size = COORD.from_ctype(cdb.window_size)
        window_origin = COORD.from_ctype(cdb.window_origin)

        return cls((
            cdb.size, cdb.sig, cdb.fill_attributes, cdb.popup_fill_attributes,
            screen_buffer_size, window_size, window_origin, cdb.font,
            cdb.input_buf_size, cdb.font_size, cdb.font_family,
            cdb.font_weight, face_name, cdb.cursor_size, cdb.full_screen,
            cdb.quick_edit, cdb.insert_mode, cdb.auto_position,
            cdb.history_buf_size, cdb.history_buf_count, cdb.history_no_dup,
            list(cdb.color_table), None
        ))
    # end def from_stream
# end class ConsoleProps

class ConsoleFEProps(ExtraDataBlock):
    """Represents a ConsoleFEProps structure.

    .. attribute:: code_page

        The code page LCID used to display text.

    """
    _fields_ = (
        "code_page", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`ConsoleFEProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`ConsoleFEProps`
        :returns: The corresponding :class:`ConsoleFEProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        blk = console_fe_data_block.from_buffer_copy(stream.read(12))

        return cls((blk.size, blk.sig, LCID.from_ctype(blk.code_page), None))
    # end def from_stream
# end class ConsoleFEProps

class DarwinProps(ExtraDataBlock):
    """Represents a DarwinProps structure.

    .. attribute:: darwin_data_ansi

        An application identifier.

    .. attribute:: darwin_data_uni

        A unicode version of :attr:`darwin_data_ansi`.

    """
    _fields_ = (
        "darwin_data_ansi", "darwin_data_uni", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`DarwinProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`DarwinProps`
        :returns: The corresponding :class:`DarwinProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        ddb = darwin_data_block.from_buffer_copy(stream.read(788))
        darwin_data_ansi = bytes(ddb.darwin_data_ansi)
        darwin_data_ansi = darwin_data_ansi.split(b"\x00", 1)[0]

        darwin_data_uni = bytes(ddb.darwin_data_uni)

        new_darwin_data_uni = _utf16_le_decoder(darwin_data_uni, "ignore")[0]
        if new_darwin_data_uni:
            darwin_data_uni = new_darwin_data_uni.split("\x00", 1)[0]
        # end if

        return cls((
            ddb.size, ddb.sig, darwin_data_ansi, darwin_data_uni, None
        ))
    # end def from_stream
# end class DarwinProps

class ExpandableStringsDataBlock(ExtraDataBlock):
    """Base class for blocks that use environment variables.

    .. attribute:: target_ansi

        A path that is constructed with environment variables.

    .. attribute:: target_uni

        A unicode version of :attr:`target_ansi`

    """
    _fields_ = (
        "target_ansi", "target_uni", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`ExpandableStringsDataBlock` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`ExpandableStringsDataBlock`
        :returns: The corresponding :class:`ExpandableStringsDataBlock` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        edb = expandable_strings_data_block.from_buffer_copy(stream.read(788))
        target_ansi = bytes(edb.target_ansi)
        target_ansi = target_ansi.split(b"\x00", 1)[0]

        target_uni = bytes(edb.target_uni)
        new_target_uni = _utf16_le_decoder(target_uni, "ignore")[0]
        if new_target_uni:
            target_uni = new_target_uni.split("\x00", 1)[0]
        # end if

        return cls((edb.size, edb.sig, target_ansi, target_uni, None))
    # end def from_stream
# end class ExpandableStringsDataBlock

class EnvironmentProps(ExpandableStringsDataBlock):
    """Path to environment variable information."""

    pass
# end class EnvironmentProps

class IconEnvironmentProps(ExpandableStringsDataBlock):
    """Path to an icon encoded with environment variables."""

    pass
# end class IconEnvironmentProps

class KnownFolderProps(ExtraDataBlock):
    """Represents a KnownFolderProps structure.

    .. attribute:: kf_id

        A GUID for the folder.

    .. attribute:: offset

        The index in the item id list of the known folder.

    """
    _fields_ = (
        "kf_id", "offset", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`KnownFolderProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`KnownFolderProps`
        :returns: The corresponding :class:`KnownFolderProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        kfb = known_folder_data_block.from_buffer_copy(stream.read(28))
        kf_id = GUIDToUUID.from_ctype(kfb.kf_id)

        return cls((kfb.size, kfb.sig, kf_id, kfb.offset, None))
    # end class from_stream
# end class KnownFolderProps

class PropertyStoreProps(ExtraDataBlock):
    """Represents serialized property storage values.

    .. attribute:: property_store

        A serialized property storage structure (currently not implemented).

    """
    _fields_ = (
        "property_store", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`PropertyStoreProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`PropertyStoreProps`
        :returns: The corresponding :class:`PropertyStoreProps` object.

        """
        edb = ExtraDataBlock.from_stream(stream, offset)

        return cls((edb.size, edb.sig, edb.data, None))
    # end class from_stream
# end class PropertyStoreProps

class ShimProps(ExtraDataBlock):
    """Specifies the name of a shim to use when activating/running the target.

    .. attribute:: layer_name

        A unicode name of the shim layer.

    """
    _fields_ = (
        "layer_name", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`ShimProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`ShimProps`
        :returns: The corresponding :class:`ShimProps` object.

        """
        edb = ExtraDataBlock.from_stream(stream, offset)
        layer_name = edb.data

        new_layer_name = _utf16_le_decoder(layer_name, "ignore")[0]
        if new_layer_name:
            layer_name = new_layer_name.split("\x00", 1)[0]
        # end if

        return cls((edb.size, edb.sig, layer_name, None))
    # end def from_stream
# end class ShimProps

class SpecialFolderProps(ExtraDataBlock):
    """Specifies the location of special folders in an item id list.

    .. attribute:: sf_id

        The special folder identifier.

    .. attribute:: offset

        The index in the item id list of the special folder.

    """

    _fields_ = (
        "sf_id", "offset", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`SpecialFolderProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`SpecialFolderProps`
        :returns: The corresponding :class:`SpecialFolderProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        sfdb = special_folder_data_block.from_buffer_copy(stream.read(16))

        return cls((sfdb.size, sfdb.sig, sfdb.sf_id, sfdb.offset, None))
    # end def from_stream
# end class SpecialFolderProps

class DomainRelativeObjId(ActiveStructuple):
    """Represents a domain relative object identifier (DROID).

    .. attribute:: volume

        The volume field.

    .. attribute:: object

        The object field.

    """
    _fields_ = ("volume", "object")
    _takes_stream = True
    _takes_ctype = True

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`DomainRelativeObjId` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`DomainRelativeObjId`
        :returns: The corresponding :class:`DomainRelativeObjId` object.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        volume = GUIDToUUID.from_stream(stream, offset, LITTLE_ENDIAN)
        object = GUIDToUUID.from_stream(stream, offset + 16, LITTLE_ENDIAN)

        return DomainRelativeObjId((volume, object))
    # end def from_stream

    @classmethod
    def from_ctype(cls, ctype):
        """Creates a :class:`DomainRelativeObjId` object from a ctype.

        :type ctype: :class:`lf.win.shell.dtypes.DomainRelativeObjId`
        :param ctype: An instance of a DomainRelativeObjId ctype.

        :rtype: :class:`DomainRelativeObjId`
        :returns: The corresponding :class:`DomainRelativeObjId` object.

        """
        return DomainRelativeObjId((
            GUIDToUUID.from_ctype(ctype.volume),
            GUIDToUUID.from_ctype(ctype.object)
        ))
    # end def from_ctype
# end class DomainRelativeObjId

class TrackerProps(ExtraDataBlock):
    """ Data used to resolve a link target with the Link Tracking Service.

    .. attribute:: length

        The length of the structure (excluding the size and signature).

    .. attribute:: version

        The version field.

    .. attribute:: machine_id

        The NetBIOS name of the machine the target was last known to reside on.

    .. attribute:: droid

        A :class:`DomainRelativeObjId` structure used to find the target.

    .. attribute:: droid_birth

        A :class:`DomainRelativeObjId` structure used to find the target.

    """
    _fields_ = (
        "length", "version", "machine_id", "droid", "droid_birth", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`TrackerProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`TrackerProps`
        :returns: The corresponding :class:`TrackerProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if

        tdb = tracker_data_block.from_buffer_copy(stream.read(16))
        length = tdb.length

        machine_id = stream.read(length - 72).split(b"\x00", 1)[0]

        tdbf = tracker_data_block_footer.from_buffer_copy(stream.read(64))
        droid = DomainRelativeObjId.from_ctype(tdbf.droid)
        droid_birth = DomainRelativeObjId.from_ctype(tdbf.droid_birth)

        return cls((
            tdb.size, tdb.sig, length, tdb.version, machine_id, droid,
            droid_birth, None
        ))
    # end def from_stream
# end class TrackerProps

class VistaAndAboveIDListProps(ExtraDataBlock):
    """An alternative to an item id list.

    .. attribute:: idlist

        An alternate item id list.

    """
    _fields_ = (
        "idlist", "data"
    )

    @classmethod
    def from_stream(cls, stream, offset=None):
        """Creates a :class:`VistaAndAboveIDListProps` from a stream.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structure.

        :type offset: ``int``
        :param offset: The start of the structure in the stream.

        :rtype: :class:`VistaAndAboveIDListProps`
        :returns: The corresponding :class:`VistaAndAboveIDListProps` object.

        """
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        header = data_block_header.from_buffer_copy(stream.read(8))
        offset += 8

        list_size = header.size - 8
        idlist = ITEMIDLIST.from_stream(stream, offset, list_size)

        return cls((header.size, header.sig, idlist, None))
    # end def from_stream
# end class VistaAndAboveIDListProps

class TerminalBlock(ExtraDataBlock):
    """Represents a Terminal block."""

    pass
# end class TerminalBlock

class ExtraDataBlockFactory():
    """Makes :class:`ExtraDataBlock` (and subclass) objects.

    .. attribute:: props_map

        A dictionary mapping variosu signature values to their corresponding
        object factories.  Used by :meth:`make_blocks`.

    """

    props_map = {
        CONSOLE_PROPS_SIG: ConsoleProps.from_stream,
        CONSOLE_FE_PROPS_SIG: ConsoleFEProps.from_stream,
        DARWIN_PROPS_SIG: DarwinProps.from_stream,
        ENVIRONMENT_PROPS_SIG: EnvironmentProps.from_stream,
        ICON_ENVIRONMENT_PROPS_SIG: IconEnvironmentProps.from_stream,
        KNOWN_FOLDER_PROPS_SIG: KnownFolderProps.from_stream,
        PROPERTY_STORE_PROPS_SIG: PropertyStoreProps.from_stream,
        SHIM_PROPS_SIG: ShimProps.from_stream,
        SPECIAL_FOLDER_PROPS_SIG: SpecialFolderProps.from_stream,
        TRACKER_PROPS_SIG: TrackerProps.from_stream,
        VISTA_AND_ABOVE_IDLIST_PROPS_SIG: VistaAndAboveIDListProps.from_stream
    }

    @classmethod
    def make_blocks(cls, stream, offset=None):
        """reates a series of :class:`ExtraDataBlock` (or subclass) objects.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the structures.

        :type offset: ``int``
        :param offset: The start of the structures in the stream.

        :rtype: ``iterator``
        :returns: An iterator of the corresponding objects.

        """
        if offset is None:
            offset = stream.tell()
        # end if

        props_map = ExtraDataBlockFactory.props_map

        stream.seek(offset, SEEK_SET)
        data = stream.read(4)
        if len(data) != 4:
            return
        # end if

        size = uint32_le.from_buffer_copy(data).value
        if size < 4:
            return
        # end if

        data = stream.read(4)
        if len(data) != 4:
            return
        # end if

        sig = uint32_le.from_buffer_copy(data).value
        if sig == 0:
            return
        # end if

        if sig in props_map:
            block = props_map[sig](stream, offset)
        else:
            block = ExtraDataBlock.from_stream
        # end if

        yield block
        offset += size

        while block.sig != 0:
            stream.seek(offset, SEEK_SET)

            data = stream.read(4)
            if len(data) != 4:
                break
            # end if

            size = uint32_le.from_buffer_copy(data).value
            if size < 4:
                break
            # end if

            data = stream.read(4)
            if len(data) != 4:
                break
            # end if

            sig = uint32_le.from_buffer_copy(data).value
            if sig in props_map:
                block = props_map[sig](stream, offset)
            else:
                block = ExtraDataBlock.from_stream(stream, offset)
            # end if

            yield block
            offset += size
        # end while
    # end def make_blocks
# end class ExtraDataBlockFactory
