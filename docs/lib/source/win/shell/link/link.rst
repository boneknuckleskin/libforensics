:mod:`lf.win.shell.link` --- Shell link (.lnk) files
====================================================

.. module:: lf.win.shell.link
   :synopsis: Shell link (.lnk) files
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module defines classes to work with Microsoft Windows shell link (.lnk,
shortcut) files.

Inheritance Diagram
-------------------

.. graphviz::

	digraph shell_link_property_classes {
		fontname = "Courier New"
		fontsize = 10

		node [
			fontname = "Courier New"
			fontsize = 10
			shape = "record"
		]

		edge [
			arrowhead = "none"
			arrowtail = "empty"
			fontsize = 8
		]

		ExtraDataBlock [
			label = "{ExtraDataBlock\l|size\lsig\l\l|}"
		]

		ConsoleProps [
			label = "{ConsoleProps\l|\l|}"
		]

		ConsoleFEProps [
			label = "{ConsoleFEProps\l|\l|}"
		]

		DarwinProps [
			label = "{DarwinProps\l|\l|}"
		]

		ExpandableStringsDataBlock [
			label = "{ExpandableStringsDataBlock\l|\l|}"
		]

		EnvironmentProps [
			label = "{EnvironmentProps\l|\l|}"
		]

		IconEnvironmentProps [
			label = "{IconEnvironmentProps\l|\l|}"
		]

		KnownFolderProps [
			label = "{KnownFolderProps\l|\l|}"
		]

		PropertyStoreProps [
			label = "{PropertyStoreProps\l|\l|}"
		]

		ShimProps [
			label = "{ShimProps\l|\l|}"
		]

		SpecialFolderProps [
			label = "{SpecialFolderProps\l|\l|}"
		]

		TrackerProps [
			label = "{TrackerProps\l|\l|}"
		]

		VistaAndAboveIDListProps [
			label = "{VistaAndAboveIDListProps\l|\l|}"
		]

		TerminalBlock [
			label = "{TerminalBlock\l|\l|}"
		]

		ExtraDataBlock -> ConsoleProps;
		ExtraDataBlock -> ConsoleFEProps;
		ExtraDataBlock -> DarwinProps;
		ExtraDataBlock -> ExpandableStringsDataBlock;
		ExpandableStringsDataBlock -> EnvironmentProps;
		ExpandableStringsDataBlock -> IconEnvironmentProps;
		ExtraDataBlock -> KnownFolderProps;
		ExtraDataBlock -> PropertyStoreProps;
		ExtraDataBlock -> ShimProps;
		ExtraDataBlock -> SpecialFolderProps;
		ExtraDataBlock -> TrackerProps;
		ExtraDataBlock -> VistaAndAboveIDListProps
		ExtraDataBlock -> TerminalBlock
	}

SHELL_LINK structures
---------------------

.. class:: ShellLink(stream, offset=None)

	Represents a shell link (.lnk) file.

	:type stream: :class:`~lf.dec.IStream`
	:param stream: A stream that contains the link file.

	:type offset: ``int``
	:param offset: The start of the link file, in :attr:`stream`.

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

SHELL_LINK_HEADER structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: ShellLinkHeader

	Represents a header from a shell link (.lnk) file.

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

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`ShellLinkHeader` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`ShellLinkHeader`
		:returns: The corresponding :class:`ShellLinkHeader` object.

	.. classmethod:: from_ctype(ctype)

		Creates a :class:`ShellLinkHeader` object from a ctype.

		:type ctype: :class:`lf.win.shell.dtypes.ShellLinkHeader`
		:param ctype: An instance of a ShellLinkHeader ctype.

		:rtype: :class:`ShellLinkHeader`
		:returns: The corresponding :class:`ShellLinkHeader` object.

.. class:: FileAttributes

	Represents the file system attributes of a link target.

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

.. class:: LinkFlags

	Represents the LinkFlags structure from :class:`ShellLinkHeader`.

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

LINKINFO structures
^^^^^^^^^^^^^^^^^^^

.. class:: LinkInfo

	Represents a LinkInfo structure.

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

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`LinkInfo` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`LinkInfo`
		:returns: The corresponding :class:`LinkInfo` object.

.. class:: VolumeID

	Represents a VolumeID structure.

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

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`VolumeID` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`VolumeID`
		:returns: The corresponding :class:`VolumeID` object.

.. class:: CNRL

	Represents a Common Network Relative Link structure.

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

	.. attribute:: net_type

		Describes the type of network provider.  See :mod:`lf.win.consts.npt`
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

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`CNRL` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`CNRL`
		:returns: The corresponding :class:`CNRL` object.

STRING_DATA structures
^^^^^^^^^^^^^^^^^^^^^^

.. class:: StringDataSet

	Represents a collection of :class:`StringData` objects.

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

.. class:: StringData

	Represents a StringData structure.

	.. attribute:: size

		The size of the :class:`StringData` structure in bytes.

	.. attribute:: char_count

		The number of characters in the string.

	.. attribute:: string

		The string associated with the structure.

	.. classmethod:: from_stream(stream, offset=None, is_unicode=True)

		Creates a :class:`StringData` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:type is_unicode: ``bool``
		:param is_unicode: If the string is in unicode (utf16-le)

		:rtype: :class:`StringData`
		:returns: The corresponding :class:`StringData` object.

EXTRA_DATA structures
^^^^^^^^^^^^^^^^^^^^^

.. class:: ExtraDataBlock

	Base class for :class:`ExtraDataBlock` subclasses.

	.. attribute:: size

		The size of the structure in bytes.

	.. attribute:: sig

		The signature field.

	.. attribute:: data

		An optional field that describes the data in the structure.

		.. note::

			Subclasses set this to ``None``

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`ExtraDataBlock` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`ExtraDataBlock`
		:returns: The corresponding :class:`ExtraDataBlock` object.

.. class:: ConsoleProps

	Represents a ConsoleProps structure.

	.. attribute:: fill_attributes

		The foreground and background text colors for the console window.

	.. attribute:: popup_fill_attributes

		The foreground and background text colors for the console window
		popup.

	.. attribute:: screen_buffer_size

		A :class:`~lf.win.con.objects.COORD` object describing the
		dimensions of the console window buffer.

	.. attribute:: window_size

		A :class:`~lf.win.con.objects.COORD` object describing the
		dimensions of the console window.

	.. attribute:: window_origin

		A :class:`~lf.win.con.objects.COORD` object describing the
		console window origin.

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

	.. attribute:: auto_position

		Whether or not to automatically position the console window.

	.. attribute:: history_buf_size

		The number of characters to store in the history of the console
		window.

	.. attribute:: history_buf_count

		The number of characters to store in the history of the console
		window.

	.. attribute:: history_no_dup

		Whether or not duplicates are stored in the history buffers.

	.. attribute:: color_table

		A tuple of the RGB colors used for text in the console window.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`ConsoleProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`ConsoleProps`
		:returns: The corresponding :class:`ConsoleProps` object.

.. class:: ConsoleFEProps

	Represents a ConsoleFEProps structure.

	.. attribute:: code_page

		The code page LCID used to display text.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`ConsoleFEProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`ConsoleFEProps`
		:returns: The corresponding :class:`ConsoleFEProps` object.

.. class:: DarwinProps

	Represents a DarwinProps structure.

	.. attribute:: darwin_data_ansi

		An application identifier.

	.. attribute:: darwin_data_uni

		A unicode version of :attr:`darwin_data_ansi`.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`DarwinProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`DarwinProps`
		:returns: The corresponding :class:`DarwinProps` object.

.. class:: ExpandableStringsDataBlock

	Base class for blocks that use environment variables.

	.. attribute:: target_ansi

		A path that is constructed with environment variables.

	.. attribute:: target_uni

		A unicode version of :attr:`target_ansi`

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`ExpandableStringsDataBlock` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`ExpandableStringsDataBlock`
		:returns: The corresponding :class:`ExpandableStringsDataBlock` object.

.. class:: EnvironmentProps

	Path to environment variable information.

.. class:: IconEnvironmentProps

	Path to an icon encoded with environment variables.

.. class:: KnownFolderProps

	Represents a KnownFolderProps structure.

	.. attribute:: kf_id

		A GUID for the folder.

	.. attribute:: offset

		The index in the item id list of the known folder.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`KnownFolderProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`KnownFolderProps`
		:returns: The corresponding :class:`KnownFolderProps` object.

.. class:: PropertyStoreProps

	Represents serialized property storage values.

	.. attribute:: property_store

		A serialized property storage structure (currently not implemented).

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`PropertyStoreProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`PropertyStoreProps`
		:returns: The corresponding :class:`PropertyStoreProps` object.

.. class:: ShimProps

	Specifies the name of a shim to use when activating/running the target.

	.. attribute:: layer_name

		A unicode name of the shim layer.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`ShimProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`ShimProps`
		:returns: The corresponding :class:`ShimProps` object.

.. class:: SpecialFolderProps

	Specifies the location of special folders in an item id list.

	.. attribute:: sf_id

		The special folder identifier.

	.. attribute:: offset

		The index in the item id list of the special folder.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`SpecialFolderProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`SpecialFolderProps`
		:returns: The corresponding :class:`SpecialFolderProps` object.

.. class:: DomainRelativeObjId

	Represents a domain relative object identifier (DROID).

	.. attribute:: volume

		The volume field.

	.. attribute:: object

		The object field.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`DomainRelativeObjId` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`DomainRelativeObjId`
		:returns: The corresponding :class:`DomainRelativeObjId` object.

	.. classmethod:: from_ctype(ctype)

		Creates a :class:`DomainRelativeObjId` object from a ctype.

		:type ctype: :class:`lf.win.shell.dtypes.DomainRelativeObjId`
		:param ctype: An instance of a DomainRelativeObjId ctype.

		:rtype: :class:`DomainRelativeObjId`
		:returns: The corresponding :class:`DomainRelativeObjId` object.

.. class:: TrackerProps

	Data used to resolve a link target with the Link Tracking Service.

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

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`TrackerProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`TrackerProps`
		:returns: The corresponding :class:`TrackerProps` object.

.. class:: VistaAndAboveIDListProps

	An alternative to an item id list.

	.. attribute:: idlist

		An alternate item id list.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`VistaAndAboveIDListProps` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:rtype: :class:`VistaAndAboveIDListProps`
		:returns: The corresponding :class:`VistaAndAboveIDListProps` object.

.. class:: TerminalBlock

	Represents a terminal block.

.. class:: ExtraDataBlockFactory

	Makes :class:`ExtraDataBlock` (and subclass) objects.

	.. attribute:: props_map

		A dictionary mapping variosu signature values to their corresponding
		object factories.  Used by :meth:`make_blocks`.

	.. classmethod:: make_blocks(stream, offset=None)

		Creates a series of :class:`ExtraDataBlock` (or subclass) objects.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structures.

		:type offset: ``int``
		:param offset: The start of the structures in the stream.

		:rtype: ``iterator``
		:returns: An iterator of the corresponding objects.
