:mod:`lf.win.objects` --- Common Microsoft Windows objects and converters
==========================================================================

.. module:: lf.win.objects
   :synopsis: Common Microsoft Windows objects and converters
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>



Converters
----------
These classes convert from a :mod:`lf.win.ctypes` object to an object from the
Python standard library.

.. class:: GUIDToUUID

	Converts a GUID to a ``UUID``.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``UUID`` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the GUID structure.

		:type offset: ``int`` or ``None``
		:param offset: The start of the GUID structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:rtype: ``UUID``
		:returns: The corresponding ``UUID`` object.

	.. classmethod:: from_ctype(ctype)

		Creates a ``UUID`` object from a ctype.

		:type ctype: :class:`~lf.win.ctypes.guid_le` or
					 :class:`~lf.win.ctypes.guid_be`
		:param ctype: A GUID object.

		:rtype: ``UUID``
		:returns: The corresponding ``UUID`` object.

	.. classmethod:: from_guid(data1, data2, data3, data4)

		Creates a ``UUID`` object from individual GUID fields.

		:type data1: ``int``
		:param data1: The first 8 hexadecimal digits (32 bits).

		:type data2: ``int``
		:param data2: The first group of 4 hexadecimal digits (16 bits).

		:type data3: ``int``
		:param data3: The second group of 4 hexadecimal digits (16 bits).

		:type data4: ``bytes`` or ``bytearray``
		:param data4: The last 8 bytes.

		:rtype: ``UUID``
		:returns: The corresponding ``UUID`` object.

.. class:: CLSIDToUUID

	Converts a CLSID to a ``UUID``.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``UUID`` object from a stream.
		
		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the CLSID structure.
		
		:type offset: ``int`` or ``None``
		:param offset: The start of the CLSID structure in the stream.
		
		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)
		
		:rtype: ``UUID``
		:returns: The corresponding ``UUID`` object.

	.. classmethod:: from_ctype(ctype)

		Creates a ``UUID`` object from a ctype.

		:type ctype: :class:`~lf.win.ctypes.clsid_le` or
					 :class:`~lf.win.ctypes.clsid_be`
		:param ctype: A CLSID object.

		:rtype: ``UUID``
		:returns: The corresponding ``UUID`` object.

.. class:: DECIMALToDecimal

	Converts a DECIMAL to a ``Decimal``.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``Decimal`` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the DECIMAL structure.

		:type offset: ``int`` or ``None``
		:param offset: The start of the DECIMAL structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:rtype: ``Decimal``
		:returns: The corresponding ``Decimal`` object.

	.. classmethod:: from_ctype(ctype)

		Creates a ``Decimal`` object from a ctype.

		:type ctype: :class:`~lf.win.ctypes.decimal_le` or
					 :class:`~lf.win.ctypes.decimal_be`
		:param ctype: A DECIMAL object.

		:raises ValueError: If the DECIMAL object is invalid.

		:rtype: ``Decmial``
		:returns: The corresponding ``Decimal`` object.

.. class:: CURRENCYToDecimal

	Converts a CURRENCY data type to a ``Decimal``.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``Decimal`` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the CURRENCY structure.

		:type offset: ``int`` or ``None``
		:param offset: The start of the CURRENCY structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:rtype: ``Decimal``
		:returns: The corresponding ``Decmial`` object.

	.. classmethod:: from_int(integer)

		Creates a ``Decimal`` object from an ``int``.

		:type integer: ``int``
		:param integer: The value of the CURRENCY object.

		:rtype: ``Decimal``
		:returns: The corresponding ``Decimal`` object.


Value Objects
-------------
The following classes subclass :class:`lf.dtypes.ActiveStructuple` to provide a
Python data type not found in the standard library.

.. class:: LCID

	Represents a Locale ID data type.

	.. attribute:: rsvd

		The reserved field.

	.. attribute:: sort_id

		The sort ID field.

	.. attribute:: lang_id

		The language ID field.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a :class:`LCID` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the LCID structure.

		:type offset: ``int`` or ``None``
		:param offset: The start of the LCID structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:rtype: :class:`LCID`
		:returns: The extracted :class:`LCID` object.

	.. classmethod:: from_ctype(ctype)

		Creates a :class:`LCID` object from a ctype.

		:type ctype: :class:`~lf.win.ctypes.lcid_le` or
					 :class:`~lf.win.ctypes.lcid_be`
		:param ctype: An instance of an lcid ctype.

		:rtype: :class:`LCID`
		:returns: The corresponding :class:`LCID` object.

.. class:: HRESULT

	Represents and HRESULT data type.

	.. attribute:: s

		The severity bit.

	.. attribute:: r

		The reserved bit.

	.. attribute:: c

		The customer bit.

	.. attribute:: n

		The NTSTATUS bit.

	.. attribute:: x

		The x field.

	.. attribute:: facility

		Indicates the source of the error.

	.. attribute:: code

		The remaining part of the error code.

	.. classmethod:: from_stream(stream, offset=None, byte_order=LITTLE_ENDIAN)

		Creates a ``HRESULT`` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the HRESULT structure.

		:type offset: ``int`` or ``None``
		:param offset: The start of the HRESULT structure in the stream.

		:type byte_order: constant
		:param byte_order: The byte order to use (from :mod:`lf.dtypes`)

		:rtype: :class:`HRESULT`
		:returns: The extracted :class:`HRESULT` object.

	.. classmethod:: from_ctype(ctype)

		Creates a ``HRESULT`` object from a ctype.

		:type ctype: :class:`~lf.win.ctypes.hresult_le` or
					 :class:`~lf.win.ctypes.hresult_be`
		:param ctype: A hresult object.

		:rtype: :class:`HRESULT`
		:returns: The corresponding :class:`HRESULT` object.

	.. classmethod:: from_int(hresult)

		Creates a ``HRESULT`` object from an ``int``.

		:type hresult: ``int``
		:param hresult: The value of the HRESULT.

		:rtype: :class:`HRESULT`
		:returns: The corresponding :class:`HRESULT` object.
