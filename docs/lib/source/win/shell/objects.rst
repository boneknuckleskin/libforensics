:mod:`lf.win.shell.objects` --- Objects for Windows shell artifacts
===================================================================

.. module:: lf.win.shell.objects
   :synopsis: Objects for Windows shell artifacts
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module provides support for common Windows shell artifacts.


.. class:: SHITEMID

	Represents a SHITEMID structure.

	.. attribute:: size

		The size of the SHITEMID structure. (calculated)

	.. attribute:: cb

		The count of bytes of the structure. (extracted)

	.. attribute:: abID

		An application defined BLOB of data.

	.. attribute:: id

		An alias for the :attr:`abID` attribute.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`SHITEMID` from a stream.

		:type stream: :class:`lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`

		:rtype: :class:`SHITEMID`
		:returns: The corresponding :class:`SHITEMID` object.

.. class:: ITEMIDLIST

	Represents an ITEMIDLIST structure.

	.. attribute:: mkid

		A list of :class:`SHITEMID` structures.

	.. classmethod:: from_stream(stream, offset=None, max_bytes=None)

		Creates an :class:`ITEMIDLIST` from a stream.

		:type stream: :class:`lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`

		:type max_bytes: ``int``
		:param max_bytes: The maximum number of bytes to read from the stream.
						  If this is ``None`` then it is ignored.

		:rtype: :class:`ITEMIDLIST`
		:returns: The corresponding :class:`ITEMIDLIST` object.

