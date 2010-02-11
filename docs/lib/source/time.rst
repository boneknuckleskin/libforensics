:mod:`lf.time` --- Converters for various time formats
======================================================

.. module:: lf.time
   :synopsis: Converters for various time formats
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>


.. class:: FILETIMEToUnixTime

	Converts a FILETIME timestamp to a Unix timestamp.

	.. classmethod:: from_int(filetime)

		Converts a Microsoft Windows FILETIME timestamp to a Unix timestamp.

		:type filetime: ``int``
		:param filetime: The FILETIME timestamp.

		:rtype: ``int``
		:returns: The time as a Unix timestamp.

.. class:: UnixTimeToFILETIME

	Converts a Unix timestamp to a FILETIME timestamp.

	.. classmethod:: from_int(unix_time)

		Converts a Unix timestamp to a Microsoft Windows FILETIME timestamp.

		:type unix_time: ``int``
		:param unix_time: The Unix timestamp.

		:rtype: ``int``
		:returns: The time as a FILETIME timestamp.

.. class:: FILETIMETodatetime

	Converts a FILETIME to a ``datetime``.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``datetime`` object from a stream.

		:type stream: :class:`lf.dec.IStream`
		:param stream: A stream that contains the FILETIME structure.

		:type offset: ``int`` or ``None``
		:param offset: The start of the FILETIME structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:raises ValueError: If the FILETIME structure is invalid.

		:rtype: ``datetime``
		:returns: The corresponding ``datetime`` object.

	.. classmethod:: from_ctype(ctype)

		Creates a ``datetime`` object from a ctype.

		:type ctype: :class:`lf.win.ctypes.filetime_le` or
					 :class:`lf.win.ctypes.filetime_be`
		:param ctype: A FILETIME object.

		:raises ValueError: If the FILETIME object is invalid.

		:rtype: ``datetime``
		:returns: The corresponding ``datetime`` object.

	.. classmethod:: from_int(filetime)

		Converts a Microsoft FILETIME timestamp to a ``datetime`` object.

		:type filetime: ``int``
		:param filetime: The timestamp as a 64 bit integer.

		:raises ValueError: If :attr:`filetime` is an invalid value.

		:rtype: ``datetime``
		:returns: The corresponding ``datetime`` object.

.. class:: DOSDateTimeTodatetime

	Converts DOS date and times to a ``datetime``.

	.. classmethod:: from_ints(dos_date=None, dos_time=None)

		Converts DOS date and time values to a ``datetime``.

		:type dos_date: ``int``
		:param dos_date: An MS-DOS date.

		:type dos_time: ``int``
		:param dos_time: An MS-DOS time.

		:raises ValueError: if both :attr:`dos_date` and :attr:`dos_time` are
							``None``.

		:rtype: ``datetime``
		:returns: The corresponding ``datetime`` object.

.. class:: VariantTimeTodatetime

	Converts variant timestamp (OLE date) to a ``datetime``.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``datetime`` object from a stream.

		:type stream: :class:`lf.dec.IStream`
		:param stream: A stream that contains the Variant timestamp.

		:type offset: ``int`` or ``None``
		:param offset: The start of the Variant timestamp in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:raises ValueError: If the Variant timestamp is invalid.

		:rtype: ``datetime``
		:returns: The corresponding ``datetime`` object.

	.. classmethod:: from_float(vtime)

		Converts a Variant timestamp to a ``datetime``.

		:type vtime: float
		:param vtime: The Variant timestamp.

		:raises ValueError: If :attr:`vtime` is an invalid value.

		:rtype: ``datetime``
		:returns: The corresponding ``datetime`` object.
