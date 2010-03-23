:mod:`lf.win.shell.recyclebin` --- Recycle bin (INFO2)
======================================================

.. module:: lf.win.shell.recyclebin
   :synopsis: Recycle bin files (INFO2)
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module contains code to work with INFO2 files (found in the Recycle bin directory).


Classes
-------

.. class:: INFO2(stream, offset=None)

	Represents an INFO2 file.

	:type stream: :class:`~lf.dec.IStream`.
	:param stream: A stream that contains the INFO2 file.

	:type offset: ``int``
	:param offset: The start of the INFO2 file in :attr:`stream`.

	.. attribute:: header

		An instance of a :class:`INFO2Header`.

	.. attribute:: items

		A list of :class:`INFO2Item` objects.

.. class:: INFO2Header

	Represents the header from an INFO2 file.

	.. attribute:: version

		The version of the INFO2 file.

	.. attribute:: item_size

		The size of an :class:`INFO2Item`.

	.. attribute:: unknown1

		The first unknown value (bytes 4-7)

	.. attribute:: unknown2

		The second unknown value (bytes 8-11)

	.. attribute:: unknown3

		The third unknown value (bytes 16-19)

.. class:: INFO2Item

	Represents an item in an INFO2 file.

	.. attribute:: name_asc

		The name of the deleted file (ASCII).

	.. attribute:: index

		The index of the deleted file.

	.. attribute:: drive_num

		The drive number the file was deleted from.

	.. attribute:: dtime

		The time the file was deleted.

	.. attribute:: file_size

		The size of the deleted file.

	.. attribute:: name_uni

		The name of the deleted file (unicode), or ``None`` if not present.

	.. attribute:: exists

		``True`` if the corresponding file exists on disk.

	.. classmethod:: from_ctype(ctype)

		Creates a :class:`INFO2Item` object from a ctype.

		:type ctype: :class:`~lf.win.shell.recyclebin.ctypes.info2_item`
		:param ctype: An info2_item object.

		:rtype: :class:`INFO2Item`
		:returns: The corresponding :class:`INFO2Item` object.
