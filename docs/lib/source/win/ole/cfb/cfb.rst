:mod:`lf.win.ole.cfb` --- OLE structured storage (compound file binary)
=======================================================================

.. module:: lf.win.ole.cfb
   :synopsis: OLE structured storage support (compound file binaries)
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This package provides support to work with OLE structured storage files.  More
information about this file format can be found at:
http://msdn.microsoft.com/en-us/library/dd942138(PROT.10).aspx

.. class:: CompoundFile(stream, offset=None)

	Represents an OLE structured storage file (compound file binary).

	:type stream: :class:`~lf.dec.IStream`
	:param stream: A stream covering the contents of the compound file.

	:type offset: ``int``
	:param offset: The start of the compound file in the stream.

	.. attribute:: header

		A :class:`Header` object containing information from the compound file
		header.

	.. attribute:: sect_size

		The number of bytes in a sector.

	.. attribute:: mini_sect_size

		The number of bytes in a mini sector.

	.. attribute:: mini_stream_cutoff

		The maximum size of a file (in bytes) in the mini stream.

	.. attribute:: ver_major

		The major version number. (from the header)

	.. attribute:: ver_minor

		The minor version number. (from the header)

	.. attribute:: di_fat

		A list of entries from the double indirect FAT.

	.. attribute:: fat

		A list of entries from the FAT.

	.. attribute:: mini_fat

		A list of entries from the mini FAT.

	.. attribute:: mini_stream

		A stream covering the contents of the mini stream.  None if there is no
		mini stream.

	.. attribute:: dir_stream

		A stream covering the contents of the directory stream.  None if there
		is no directory stream.

	.. attribute:: root_dir_entry

		A DirEntry object for the root directory entry.  None if there is no
		root directory.

	.. attribute:: dir_entries

		A dictionary of directory entries, found by traversing the RB tree.

	.. attribute:: cfb_stream

		A stream covering the contents of the file.

	.. method:: byte_offset(sect_num)

		Calculates the byte offset of a sector number.

		:type sect_num: ``int``
		:param sect_num: The sector number.

		:rtype: ``int``
		:returns: The byte offset in the file of the sector.

	.. method:: mini_byte_offset(mini_sect_num)

		Calculates the byte offset of a mini sector number.

		:type mini_sect_num: ``int``
		:param mini_sect_num: The mini sector number.

		:rtype: ``int``
		:returns: The byte offset in the mini stream of the mini sector number.

	.. method:: get_fat_chain(first_sect)

		Retrieves a chain from the FAT.

		:type first_sect: ``int``
		:param first_sect: The sector number of the first sector in the chain.

		:raises IndexError: If :attr:`first_sect` is beyond the size of the
							file.

		:rtype: list
		:returns: The sector chain from the FAT.

	.. method:: get_mini_fat_chain(first_mini_sect)

		Retrieves a chain from the mini FAT.

		:type first_mini_sect: ``int``
		:param first_mini_sect: The sector number of the first sector in the
								chain.

		:raises IndexError: If :attr:`first_mini_sect` is beyond the size of
							the mini FAT.

		:rtype: list
		:returns: The sector chain from the mini FAT.

	.. method:: get_dir_entry(sid)

		Retrieves a directory entry

		:type sid: ``int``
		:param sid: The stream identifier of the directory entry.

		:raises IndexError: If :attr:`sid` is out of range.

		:rtype: :class:`DirEntry`
		:returns: The directory entry.

	.. classmethod:: is_valid_dir_entry(entry)

		Determines if a :class:`DirEntry` object is valid.

		If :attr:`entry` matches any of the following tests, it is
		considered invalid:

			* if :attr:`entry.name` is empty
			* if :attr:`entry.name` contains invalid characters
			* if :attr:`entry.type` is not 0x0, 0x1, 0x2, or 0x5
			* if :attr:`entry.color` is not 0x0 or 0x1
			* if :attr:`entry.left_sid`, :attr:`entry.right_sid`, or
			  :attr:`entry.child_sid` is not between :const:`STREAM_ID_MIN`
			  and :const:`STREAM_ID_MAX`, and is not :const:`STREAM_ID_NONE`

		:type entry: :class:`DirEntry`
		:param entry: The :class:`DirEntry` object to examine

		:rtype: ``bool``
		:returns: ``True`` if :attr:`entry` is a valid directory entry.

	.. method:: get_stream(sid, slack=False)

		Retrieves the contents of a stream.

		:type sid: ``int``
		:param sid: The stream identifier for the directory entry associated
					with the stream.

		:type slack: ``bool``
		:param slack: If ``True``, the contents of the entire stream are
					  returned.  Otherwise the stream is truncated at the size
					  specified by the associated directory entry.

		:raises IndexError: If :attr:`sid` is out of range.

		:rtype: :class:`~lf.dec.IStream`
		:returns: An :class:`~lf.dec.IStream` covering the contents of the
				  stream.

.. class:: Header

	Represents the header from a compound file binary.

	.. attribute:: sig

		The signature value.

	.. attribute:: clsid

		The class ID value.

	.. attribute:: ver_minor

		The minor version number.

	.. attribute:: ver_major

		The major version number.

	.. attribute:: byte_order

		The byte order mark value.

	.. attribute:: sect_shift

		The size of a sector, as a power of 2.

	.. attribute:: mini_sect_shift

		The size of a sector in the mini stream, as a power of 2.

	.. attribute:: rsvd

		The reserved value.

	.. attribute:: dir_sect_count

		The number of sectors that contain directory entries.

	.. attribute:: fat_sect_count

		The number of sectors that contain FAT entries.

	.. attribute:: dir_sect_offset

		The sector offset of the first directory entry.

	.. attribute:: trans_num

		The transaction signature number.

	.. attribute:: mini_stream_cutoff

		The maximum size of a user-defined data stream that can be allocated in
		the mini FAT.

	.. attribute:: mini_fat_sect_offset

		The sector offset of the first mini FAT entry.

	.. attribute:: mini_fat_sect_count

		The number of sectors in the mini FAT.

	.. attribute:: di_fat_sect_offset

		The sector offset of the first DIFAT entry (beyond the header).

	.. attribute:: di_fat_sect_count

		The number of sectors in the DIFAT.

	.. attribute:: di_fat

		The first 109 DIFAT entries.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`Header` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the compound file header.

		:type offset: ``int``
		:param offset: The start of the header in :attr:`stream`.

		:rtype: :class:`Header`
		:returns: The corresponding :class:`Header` object.

.. class:: DirEntry

	Represents a directory entry in a compound file.

	.. attribute:: name

		The name of the directory entry.

	.. attribute:: name_size

		The length of the name field (in bytes).

	.. attribute:: type

		The type of directory entry.

	.. attribute:: color

		The color of the directory entry.

	.. attribute:: left_sid

		The stream identifier of the left sibling directory entry.

	.. attribute:: right_sid

		The stream identifier of the right sibling directory entry.

	.. attribute:: child_sid

		The stream identifier of the child directory entry.

	.. attribute:: clsid

		The CLSID of the directory entry.

	.. attribute:: state

		The user defined state bits.

	.. attribute:: btime

		The creation time of the directory entry.

	.. attribute:: mtime

		The last modification time of the directory entry.

	.. attribute:: stream_sect_offset

		The first sector of the stream.

	.. attribute:: stream_size

		The size in bytes of the stream.

		.. note::

			Per the spec. if ver_major is 0x3, the high 4 bytes of this value
			may be invalid, and must be ignored.  This is a responsibility of
			the calling function.


	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`DirEntry` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the directory entry.

		:type offset: ``int``
		:param offset: The start of the directory entry in :attr:`stream`.

		:rtype: :class:`DirEntry`
		:returns: The corresponding :class:`DirEntry` object.
