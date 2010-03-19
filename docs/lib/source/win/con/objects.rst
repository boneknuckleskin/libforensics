:mod:`lf.win.con.objects` --- Windows console objects
=====================================================

.. module:: lf.win.con.objects
   :synopsis: Windows console objects
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module defines classes to work with Microsoft Windows console functions.

.. class:: COORD

	Represents coordinates.

	.. attribute:: x

		The x coordinate.

	.. attribute:: y

		The y coordinate.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a :class:`COORD` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:rtype: :class:`COORD`
		:returns: The corresponding :class:`COORD` object.

	.. classmethod:: from_ctype(ctype)

		Creates a :class:`COORD` object from a ctype.

		:type ctype: :class:`~lf.win.con.ctypes.coord_le` or
					 :class:`~lf.win.con.ctypes.coord_be`
		:param ctype: An instance of a coord ctype.

		:rtype: :class:`COORD`
		:returns: The corresponding :class:`COORD` object.
