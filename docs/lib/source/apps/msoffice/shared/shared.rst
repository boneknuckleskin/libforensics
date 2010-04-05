:mod:`lf.apps.msoffice.shared` --- Shared Microsoft Office artifacts
====================================================================

.. module:: lf.apps.msoffice.shared
   :synopsis: Microsoft Office artifacts shared across multiple products
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>


This module defines classes to work with functionality shared across several
Microsoft Office products.  The classes are designed to extend/override some of
the classes in :mod:`lf.win.ole.ps`.


Inheritance Diagrams
--------------------

Common data types
^^^^^^^^^^^^^^^^^

.. graphviz::

	digraph mso_shared_common_data_types {
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

		ClipboardData [
			label = "{ClibpoardData\l|format\ldata\l|}"
		]

		CodePageString [
			label = "{CodePageString\l|\l|}"
		]

		ValuePacket [
			label = "{ValuePacket\l|size\lvalue\l|}"
		]

		Vector [
			label = "{Vector\l|\l|}"
		]

		UnicodeString [
			label = "{UnicodeString\l|\l|}"
		]

		Blob [
			label = "{Blob\l|\l|}"
		]

		VtThumbnailValue [
			label = "{VtThumbnailValue\l|tag\lformat_id\l|}"
		]

		Lpstr [
			label = "{Lpstr\l|\l|}"
		]

		Lpwstr [
			label = "{Lpwstr\l\l}"
		]

		UnalignedLpstr [
			label = "{UnalignedLpstr\l|\l|}"
		]

		VtVecUnalignedLpstrValue [
			label = "{VtVecUnalignedLpstrValue\l|\l|}"
		]

		VtHeadingPair [
			label = "{VtHeadingPair\l|heading_str\lheader_parts_count\l|}"
		]

		VtVecHeadingPairValue [
			label = "{VtVecHeadingPairValue\l|\l|}"
		]

		VtDigSigValue [
			label = "{VtDigSigValue\l|\l|}"
		]

		VtHyperlink [
			label = "{VtHyperlink\l|" +
					"hash\lapp\loffice_art\linfo\lhlink1\lhlink2\l|}"
		]

		VecVtHyperlink [
			label = "{VecVtHyperlink\l|hyperlinks\l|}"
		]

		VtHyperlinkValue [
			label = "{VtHyperlinkValue\l|vec_hyperlinks\l|}"
		]

		DigSigBlob [
			label = "{DigSigBlob\l|sig_info\lsig_info_offset\l|}"
		]

		DigSigInfoSerialized [
			label = "{DigSigInfoSerialized\l|" +
					"sig\ltimestamp\lsigning_cert_store\lproject_name\l" +
					"timestamp_buf\l|}"
		]

		ValuePacket -> ClipboardData;
		ValuePacket -> CodePageString;
		ValuePacket -> Vector;
		ValuePacket -> UnicodeString;
		ValuePacket -> Blob;
		ValuePacket -> VtHeadingPair;
		ValuePacket -> VtDigSigValue;
		ValuePacket -> VtHyperlink;
		ValuePacket -> DigSigBlob;
		ValuePacket -> DigSigInfoSerialized;

		ClipboardData -> VtThumbnailValue;
		CodePageString -> Lpstr;
		CodePageString -> UnalignedLpstr;
		Vector -> VtVecUnalignedLpstrValue;
		UnicodeString -> Lpwstr;
		Vector -> VtVecLpwstrValue;
		Vector -> VtVecHeadingPairValue;
		Vector -> VecVtHyperlink;
		Blob -> VtHyperlinkValue;
		
	}

Typed Property Value (TPV) classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. graphviz::

	digraph mso_shared_tpv_classes {
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

		TypedPropertyValue [
			label = "{TypedPropertyValue\l|size\lvalue\ltype\l_ctype\l|}"
		]

		VtVecUnalignedLpstr [
			label = "{VtVecUnalignedLpstr\l|\l|}"
		]

		VtVecLpwstr [
			label = "{VtVecLpwstr\l|\l|}"
		]

		VtString [
			label = "{VtString\l|\l|}"
		]

		VtUnalignedString [
			label = "{VtUnalignedString\l|\l|}"
		]

		VtVecHeadingPair [
			label = "{VtVecHeadingPair\l|\l|}"
		]

		VtDigSig [
			label = "{VtDigSig\l|\l|}"
		]

		VtHyperlinks [
			label = "{VtHyperlinks\l|\l|}"
		]

		TypedPropertyValue -> VtVecUnalignedLpstr;
		TypedPropertyValue -> VtVecLpwstr;
		TypedPropertyValue -> VtString;
		TypedPropertyValue -> VtUnalignedString;
		TypedPropertyValue -> VtVecHeadingPair;
		TypedPropertyValue -> VtDigSig;
		TypedPropertyValue -> VtHyperlinks;
	}

Metadata
^^^^^^^^
.. graphviz::

	digraph mso_shared_metadata {
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

		PropertiesMetadata [
			label = "{PropertiesMetadata\l|" +
					"code_page\ldictionary\llocale\lbehavior\lattr_exists\l|}"
		]

		SummaryInfo [
			label = "{SummaryInfo\l|" +
					"title\lsubject\lauthor\lkeywords\lcomments\ltemplate\l" +
					"last_author\lrev\ledit_time_tot\lprint_time\lbtime\l" +
					"mtime\lpage_count\lword_count\lchar_count\lthumbnail\l" +
					"app_name\lsecurity\l|}"
		]

		DocSummaryInfo [
			label = "{DocSummaryInfo\l|" +
					"category\lpres_format\lbyte_count\lpara_count\l" +
					"slide_count\lnote_count\lhidden_count\lmm_clip_count\l" +
					"scale\lheading_pair\ldoc_parts\lmanager\lcompany\l" +
					"links_dirty\lchar_count_full\lshared_doc\llink_base\l" +
					"hlinks\lhyperlinks_changed\lver_major\lver_minor\l" +
					"dig_sig\lcontent_type\lcontent_status\llanguage\l" +
					"doc_version\l|}"
			]

		UserDefinedProperties [
			label = "{UserDefinedProperties\l|" +
					"linked\lguid\llink_base\lhlinks\l|}"
		]

		PropertiesMetadata -> SummaryInfo;
		PropertiesMetadata -> DocSummaryInfo;
		PropertiesMetadata -> UserDefinedProperties;
	}


Headers
-------

.. class:: PropertySetSystemIdentifier

	Represents a PropertySetSystemIdentifier structure.

	.. attribute:: os_ver_major

		The major version number of the operating system that wrote the
		property set.

	.. attribute:: os_ver_minor

		The minor version number of the operating system that wrote the
		property set.

	.. attribute:: os_type

		The os type field.

	.. classmethod:: from_stream(stream, offset=None):

		Creates a :class:`PropertySetSystemIdentifier` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetSystemIdentifier`
		:returns: The corresponding :class:`PropertySetSystemIdentifier`
				  object.

	.. |pssid| replace::

		:class:`~lf.apps.msoffice.shared.ctypes.property_set_system_identifier`

	.. classmethod:: from_ctype(ctype):

		Creates a :class:`PropertySetSystemIdentifier` from a ctype.

		:type ctype: |pssid|
		:param ctype: An instance of a |pssid|
	

.. class:: PropertySetStreamHeader

	Subclasses :class:`lf.win.ole.ps.PropertySetStreamHeader`, replacing the
	:attr:`sys_id` attribute with an instance of a
	:class:`PropertySetSystemIdentifier`.

	.. attribute:: sys_id

		The system identifier field.

	.. classmethod:: from_stream(stream, offset=None):

		Creates a :class:`PropertySetStreamHeader` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetStreamHeader`
		:returns: The corresponding :class:`PropertySetStreamHeader` object.


Common data types
-----------------

.. class:: VtThumbnailValue

	Represents a VtThumbnailValue structure.

	.. attribute:: data

		The data for the thumbnail image.  If :attr:`tag` is 0, then this field
		will contain whatever data is between the :attr:`tag` field and the end
		of the packet.

	.. attribute:: tag

		The value of the cftag field. This is the format field from the
		:class:`~lf.win.ole.ps.VT_CF` type.  If this value is 0, then the
		:attr:`format_id` attribute is ``None``.

	.. attribute:: format_id

		The format of the data in :attr:`data`.

	.. attribute:: value

		An alias for the :attr:`data` attribute.

	.. attribute:: format

		An alias for the :attr:`tag` attribute.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`VtThumbnailValue` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`VtThumbnailValue`
		:returns: The corresponding :class:`VtThumbnailValue` object.


.. class:: Lpstr

	Represents an Lpstr structure (packet).

	.. note::

		This is essentially a :class:`~lf.win.ole.ps.CodePageString` that if
		properly decoded, is truncated at the first NULL character.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates an :class:`Lpstr` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`Lpstr`
		:returns: The corresponding :class:`Lpstr` object.


.. class:: UnalignedLpstr

	Represents an UnalignedLpstr structure (packet).

	.. note::

		This is similar to a :class:`~lf.win.ole.ps.CodePageString`, except
		that it is NULL terminated and does *not* have padding.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates an :class:`UnalignedLpstr` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`UnalignedLpstr`
		:returns: The corresponding :class:`UnalignedLpstr` object.


.. class:: VtVecUnalignedLpstrValue

	Represents a VtVecUnalignedLpstrValue structure (packet).

	.. note::

		This is effectively a
		(:class:`~lf.win.ole.ps.VT_VECTOR` | :class:`~lf.win.ole.ps.VT_LPSTR`)
		with :class:`UnalignedLpstr` strings.

	.. attribute:: scalar_count

		The number of strings in the data.

	.. attribute:: value

		A list of (unaligned) strings.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtVecUnalignedLpstrValue` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecUnalignedLpstrValue`
		:returns: The corresponding :class:`VtVecUnalignedLpstrValue` object.


.. class:: Lpwstr

	Represents a Lpwstr structure (packet).

	.. note::

		This class is essentially a :class:`~lf.win.ole.ps.UnicodeString`
		class, but was included for purposes of completeness.


.. class:: VtVecLpwstrValue

	Represents a VtVecLpwstrValue structure (packet).

	.. note::

		This class is essentially a :class:`~lf.win.ole.ps.Vector` class that
		has a hard coded scalar type of :class:`Lpwstr`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtVecLpwstrValue` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecLpwstrValue`
		:returns: The corresponding :class:`VtVecLpwstrValue` object.


.. class:: VtHeadingPair

	Represents a VtHeadingPair structure (packet).

	.. attribute:: heading_str

		The header string as a :class:`VtUnalignedString`.

	.. attribute:: header_parts

		A :class:`~lf.win.ole.ps.VT_I4` instance, where the
		:attr:`~lf.win.ole.ps.VT_I4.value` attribute is the number of document
		parts associated with the header.

	.. attribute:: value

		An alias for the :attr:`heading_str` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtHeadingPair` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtHeadingPair`
		:returns: The corresponding :class:`VtHeadingPair` object.


.. class:: VtVecHeadingPairValue

	Represents a VtVecHeadingPairValue structure (packet).

	.. note::

		This class is a :class:`~lf.win.ole.ps.Vector` class that has a hard
		coded scalar type of :class:`VtHeadingPair`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtVecHeadingPairValue` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecHeadingPairValue`
		:returns: The corresponding :class:`VtVecHeadingPairValue` object.


.. class:: VtDigSigValue

	Represents a VtDigSigValue structure (packet).

	.. attribute:: value

		An instance of :class:`DigSigBlob`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtDigSigValue` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtDigSigValue`
		:returns: The corresponding :class:`VtDigSigValue` object.


.. class:: VtHyperlink

	Represents a VtHyperlink structure (packet).

	.. attribute:: hash

		The value of the dwHash field (hash of :attr:`hlink1` and
		:attr:`hlink2`)

	.. attribute:: app

		The value of the dwApp field.

	.. attribute:: office_art

		The value of the dwOfficeArt field.

	.. attribute:: info

		The value of the dwInfo field.

	.. attribute:: hlink1

		The hyperlink target.

	.. attribute:: hlink2

		The hyperlink location.

	.. attribute:: value

		An alias for the :attr:`hlink2` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtHyperlink` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtHyperlink`
		:returns: The corresponding :class:`VtHyperlink` object.


.. class:: VecVtHyperlink

	Represents a VecVtHyperlink structure (packet).

	.. note::

		This class is a :class:`~lf.win.ole.ps.Vector` class with a scalar type
		hardcoded to :class:`VtHyperlink`.

	.. attribute:: hyperlinks

		A list of :class:`VtHyperlink` objects.

	.. attribute:: value

		An alias for the :attr:`hyperlinks` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VecVtHyperlink` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VecVtHyperlink`
		:returns: The corresponding :class:`VecVtHyperlink` object.


.. class:: VtHyperlinkValue

	Represents a VtHyperlinkValue structure (packet).

	.. attribute:: vec_hyperlinks

		An instance of :class:`VecVtHyperlink`.

	.. attribute:: value

		An alias for the :attr:`vec_hyperlinks` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtHyperlinkValue` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtHyperlinkValue`
		:returns: The corresponding :class:`VtHyperlinkValue` object.


.. class:: DigSigBlob

	Represents a DigSigBlob structure (packet).

	.. attribute:: sig_info_offset

		The offset of the :attr:`sig_info` attribute.

	.. attribute:: sig_info

		An instance of :class:`DigSigInfoSeralized`.

	.. attribute:: value

		An alias for the :attr:`sig_info` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`DigSigBlob` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`DigSigBlob`
		:returns: The corresponding :class:`DigSigBlob` object.


.. class:: DigSigInfoSerialized

	Represents a DigSigInfoSerialized structure (packet).

	.. attribute:: sig_size

		The size of the :attr:`sig_buf` attribute.

	.. attribute:: sig_offset

		The relative offset (from the parent structure) of the :attr:`sig_buf`
		attribute.  If the parent structure is a :class:`DigSigBlob` then the
		offset is relative to the start of the parent structure.  If the parent
		structure is a ``WordSigBlob`` Then the offset is relative to the
		:attr:`cbSigInfo` field of the parent structure.

	.. attribute:: cert_store_size

		The size of the :attr:`cert_store_buf` attribute.

	.. attribute:: cert_store_offset

		The relative offset (from the parent structure) of the
		:attr:`cert_store_buf` attribute.  If the parent structure is a
		:class:`DigSigBlob` then the offset is relative to the start of the
		parent structure.  If the parent structure is a ``WordSigBlob``
		Then the offset is relative to the :attr:`cbSigInfo` field of the
		parent structure.

	.. attribute:: proj_name_size

		The size of the :attr:`proj_name_buf` attribute.

	.. attribute:: proj_name_offset

		The relative offset (from the parent structure) of the
		:attr:`proj_name_buf` attribute.  If the parent structure is a
		:class:`DigSigBlob` then the offset is relative to the start of the
		parent structure.  If the parent structure is a ``WordSigBlob``
		Then the offset is relative to the :attr:`cbSigInfo` field of the
		parent structure.

	.. attribute:: timestamp

		The value of the fTimestamp field.

	.. attribute:: timestamp_buf_size

		The size of the :attr:`timestamp_buf` attribute.

	.. attribute:: timestamp_buf_offset

		The relative offset (from the parent structure) of the
		:attr:`timestamp_buf` attribute.  If the parent structure is a
		:class:`DigSigBlob` then the offset is relative to the start of the
		parent structure.  If the parent structure is a ``WordSigBlob``
		Then the offset is relative to the :attr:`cbSigInfo` field of the
		parent structure.

	.. attribute:: sig_buf

		The VBA digital signature.

	.. attribute:: cert_store_buf

		The digital certificate information of the certificate used to create
		the digital signature.

	.. attribute:: proj_name_buf

		The rchProjectNameBuffer field.

	.. attribute:: timestamp_buf

		The rchTimestampBuffer field.

	.. classmethod:: from_stream(stream, field_base, offset=None, decoder=None)

		Creates a :class:`DigSigInfoSerialized` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type field_base: ``int``
		:param field_base: A value to add to the various offset fields, to
						   determine where the corresponding fields start.  For
						   :class:`DigSigBlob` this is the start of the
						   :class:`DigSigBlob` structure.  For ``WordSigBlob``
						   this is the start of the :attr:`sig_info` field.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecHeadingPairValue`
		:returns: The corresponding :class:`VtVecHeadingPairValue` object.

Typed Property Value (TPV) classes
----------------------------------

.. class:: VtThumbnail

	Represents a VtThumbnail structure (packet).

	.. attribute:: value

		An instance of :class:`VtThumbnailValue`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtThumbnail` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`VtThumbnail`
		:returns: The corresponding :class:`VtThumbnail` object.


.. class:: VtVecUnalignedLpstr

	Represents a VtVecUnalignedLpstr structure (packet).

	.. attribute:: value

		An instance of :class:`VtVecUnalignedLpstrValue`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtVecUnalignedLpstr` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecUnalignedLpstr`
		:returns: The corresponding :class:`VtVecUnalignedLpstr` object.


.. class:: VtVecLpwstr

	Represents a VtVecLpwstr structure (packet).

	.. note::

		This is essentially a (:class:`~lf.win.ole.ps.VT_VECTOR` |
		:class:`~lf.win.ole.ps.VT_LPWSTR`) TPV type, except
		:class:`VtVecLpwstrValue` objects are used instead.

	.. attribute:: value

		A list of :class:`VtVecLpwstrValue` objects.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtVecLpwstr` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecLpwstr`
		:returns: The corresponding :class:`VtVecLpwstr` object.


.. class:: VtString

	Represents a VtString structure (packet).

	.. attribute:: value

		The value of either :class:`Lpstr` or :class:`Lpwstr` objects,
		depending on the :attr:`type` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtString` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtString`
		:returns: The corresponding :class:`VtString` object.


.. class:: VtUnalignedString

	Represents a VtUnalignedString structure (packet).

	.. attribute:: value

		The value of either :class:`UnalignedLpstr` or :class:`Lpwstr` objects,
		depending on the :attr:`type` attribute.

	.. attribute:: str_type

		An alias for the :attr:`type` field.

	.. attribute:: str_value

		An alias for the :attr:`value` field.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtUnalignedString` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtUnalignedString`
		:returns: The corresponding :class:`VtUnalignedString` object.


.. class:: VtVecHeadingPair

	Represents a VtVecHeadingPair structure (packet).

	.. attribute:: value

		An instance of a :class:`VtVecHeadingPairValue`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtVecHeadingPair` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtVecHeadingPair`
		:returns: The corresponding :class:`VtVecHeadingPair` object.


.. class:: VtDigSig

	Represents a VtDigSig structure (packet).

	.. attribute:: value

		An instance of :class:`VtDigSigValue`.
	
	.. classmethod:: 
		from_stream(stream, offset=None, decoder=_uft16_le_decoder)

		Creates a :class:`VtDigSig` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtDigSig`
		:returns: The corresponding :class:`VtDigSig` object.


.. class:: VtHyperlinks

	Represents a VtHyperlinks structure (packet).

	.. attribute:: value

		An instance of :class:`VtHyperlinkValue`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VtHyperlinks` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`VtHyperlinks`
		:returns: The corresponding :class:`VtHyperlinks` object.

Building properties
-------------------

.. class:: PropertyFactory

	Makes various property objects, using the classes from this module where
	appropriate.

	.. classmethod:: make(stream, offset=None, decoder=None)

		Makes a :class:`~lf.win.ole.ps.Packet` object.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`~lf.win.ole.ps.Packet`
		:returns: The corresponding :class:`~lf.win.ole.ps.Packet` (or
				  subclass) object.


.. class:: Builder

	Builds property set streams, property sets, and properties.

	.. classmethod:: build_property_set_stream_header(stream, offset=None)

		Builds a :class:`PropertySetStreamHeader` from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetStreamHeader`
		:returns: The corresponding :class:`PropertySetStreamHeader` object.

	.. classmethod::
		build_properties(stream, fmtid, property_set, offset=None, decoder=None)

		Builds a dictionary of :class:`~lf.win.ole.ps.PropertyPacket` objects.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the property structures.

		:type fmtid: :class:`UUID`
		:param fmtid: The FMTID of the property set.

		:type property_set: :class:`PropertySetHeader`
		:param property_set: A :class:`PropertySetHeader` object that describes
							 the properties in the property set.

		:type offset: ``int``
		:param offset: The start of the structures in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: A codec to decode string properties.

		:rtype: ``dict``
		:returns: A dictionary of property identifiers (keys) and the
				  corresponding :class:`~lf.win.ole.ps.PropertyPacket` objects
				  (values).

	.. classmethod::
		build_summary_info_properties(stream, fmtid, property_set, offset=None, decoder=None)

		Builds a dictionary of :class:`PropertyPacket` objects.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the property structures.

		:type fmtid: :class:`UUID`
		:param fmtid: The FMTID of the property set.

		:type property_set: :class:`PropertySetHeader`
		:param property_set: A :class:`PropertySetHeader` object that describes
							 the properties in the property set.

		:type offset: ``int``
		:param offset: The start of the structures in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: A codec to decode string properties.

		:rtype: ``dict``
		:returns: A dictionary of property identifiers (keys) and the
				  corresponding :class:`~lf.win.ole.ps.PropertyPacket` objects
				  (values).

	.. classmethod::
		build_doc_summary_info_properties(stream, fmtid, property_set, offset=None, decoder=None)

		Builds a dictionary of :class:`PropertyPacket` objects.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the property structures.

		:type fmtid: :class:`UUID`
		:param fmtid: The FMTID of the property set.

		:type property_set: :class:`PropertySetHeader`
		:param property_set: A :class:`PropertySetHeader` object that describes
							 the properties in the property set.

		:type offset: ``int``
		:param offset: The start of the structures in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: A codec to decode string properties.

		:rtype: ``dict``
		:returns: A dictionary of property identifiers (keys) and the
				  corresponding :class:`~lf.win.ole.ps.PropertyPacket` objects
				  (values).

Metadata
--------

.. class:: SummaryInfo

	Parsed properties from a Summary Information stream.

	.. attribute:: title

		The title of the document.

	.. attribute:: subject

		The subject of the document.

	.. attribute:: author

		The document's author.

	.. attribute:: keywords

		Keywords for the document.

	.. attribute:: comments

		The document's comments.

	.. attribute:: template

		The template used for the document.

	.. attribute:: last_author

		The last author who modified the document.

	.. attribute:: rev

		The revision number.

	.. attribute:: edit_time_tot

		The total time spent modifying (editing) the document.

	.. attribute:: print_time

		The time the document was last printed.

	.. attribute:: btime

		The creation time of the document.

	.. attribute:: mtime

		The time the document was last saved.

	.. attribute:: page_count

		The number of pages in the document.

	.. attribute:: word_count

		The number of words in the document.

	.. attribute:: char_count

		The number of characters in the document.

	.. attribute:: thumbnail

		An image used as a thumbnail of the document.

	.. attribute:: app_name

		The name of the application that created the document.

	.. attribute:: security

		The document's security

	.. classmethod:: from_properties(properties)

		Creates a :class:`SummaryInfo` from properties.

		:type properties: ``dict``
		:param properties: A dictionary of property identifiers (keys) and the
						   corresponding :class:`~lf.win.ole.ps.PropertyPacket`
						   objects.

		:rtype: :class:`SummaryInfo`
		:returns: The corresponding :class:`SummaryInfo` object.


.. class:: DocSummaryInfo

	Parsed properties from a Document Summary Information stream.

	.. attribute:: category

		The document category.

	.. attribute:: pres_format

		The presentation format.

	.. attribute:: byte_count

		The size of the document in bytes.

	.. attribute:: para_count

		The number of paragraphs in the document.

	.. attribute:: slide_count

		The number of slides in the document.

	.. attribute:: note_count

		The number of notes in the document.

	.. attribute:: hidden_count

		The number of hidden slides.

	.. attribute:: mm_clip_count

		The number of multimedia clips in the document.

	.. attribute:: scale

		The value of GKPIDDSI_SCALE.

	.. attribute:: heading_pair

		A list of (heading string, document part count) tuples.

	.. attribute:: doc_parts

		A list of strings of the document parts, in the same order as the
		elements of :attr:`heading_pair`.

	.. attribute:: manager

		The manager associated with the document.

	.. attribute:: company

		The company associated with the document.

	.. attribute:: links_dirty

		True if any linked properties in a User Defined Property Set have
		changed outside of the application.

	.. attribute:: char_count_full

		The number of characters in the document, including whitespace.

	.. attribute:: shared_doc

		The value of GKPIDDSI_SHAREDDOC.

	.. attribute:: link_base

		The base URL for converting relative links.

	.. attribute:: hlinks

		A list of hyperlinks.

	.. attribute:: hyperlinks_changed

		True if the "_PID_HLINKS" property in a User Defined Property set has
		changed outside of the application.

	.. attribute:: ver_major

		The major version of the application that wrote the document.

	.. attribute:: ver_minor

		The minor version of the application that wrote the document.

	.. attribute:: dig_sig

		A VBA digital signature.

	.. attribute:: content_type

		The document's content type.

	.. attribute:: content_status

		The document's content status.

	.. attribute:: language

		The language associated with the document.

	.. attribute:: doc_version

		The version of the document.

	.. classmethod:: from_properties(properties)

		Creates a :class:`DocSummaryInfo` from properties.

		:type properties: ``dict``
		:param properties: A dictionary of property identifiers (keys) and the
						   corresponding :class:`~lf.win.ole.ps.PropertyPacket`
						   objects.

		:rtype: :class:`DocSummaryInfo`
		:returns: The corresponding :class:`DocSummaryInfo` object.


.. class:: UserDefinedProperties

	Parsed properties from a User Defined Properties property set.

	.. attribute:: linked

		A list of linked properties, in the form of (name, pid) tuples.

	.. attribute:: guid

		The _PID_GUID property (decoded if possible).

	.. attribute:: link_base

		The _PID_LINKBASE property (decoded if possible).

	.. attribute:: hlinks

		The _PID_HLINKS property.  This is a list of tuples in the form of:
		(hash, app, office_art, info, hlink1, hlink2)

	.. classmethod:: from_properties(properties)

		Creates a :class:`UserDefinedProperties` from properties.

		:type properties: ``dict``
		:param properties: A dictionary of property identifiers (keys) and the
						   corresponding :class:`~lf.win.ole.ps.PropertyPacket`
						   objects.

		:rtype: :class:`UserDefinedProperties`
		:returns: The corresponding :class:`UserDefinedProperties` object.
