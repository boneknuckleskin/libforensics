:mod:`lf.win.ole.ps` --- OLE property sets
==========================================

.. module:: lf.win.ole.ps
   :synopsis: OLE property sets
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This package provides support to work with OLE property sets.  Microsoft OLE
property sets are a generic format for persisting metadata.  They are commonly
used with OLE structured storage (e.g. :mod:`lf.win.ole.cfb`)

Several of the classes take a :attr:`decoder` parameter.  This parameter is
used to decode (interpret) embedded strings.

Additionally, some of the classes truncate strings at the first NULL byte. Any
class that does truncate a string can only do so if a valid decoder is
available.

Inheritance Diagrams
--------------------

Base classes
^^^^^^^^^^^^

.. graphviz::

	digraph oleps_base_classes {
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

		Packet [
			label = "{Packet\l|\l|}"
		]

		ActiveStructuple [
			label = "{ActiveStructuple\l|\l|}"
		]

		ActivePacket [
			label = "{ActivePacket\l|\l|}"
		]

		PropertyPacket [
			label = "{PropertyPacket\l|size\lvalue\l|}"
		]

		ValuePacket [
			label = "{ValuePacket\l|size\lvalue\l|}"
		]

		Packet -> ActivePacket;
		ActiveStructuple -> ActivePacket;
		ActivePacket -> PropertyPacket;
		ActivePacket -> ValuePacket;
	}

Common OLE data types
^^^^^^^^^^^^^^^^^^^^^

.. graphviz::


	digraph oleps_common_data_types {
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

		ValuePacket [
			label = "{ValuePacket\l|size\lvalue\l|}"
		]

		CURRENCY [
			label = "{CURRENCY\l|\l|}"
		]

		DATE [
			label = "{DATE\l|\l|}"
		]

		CodePageString [
			label = "{CodePageString\l|\l|}"
		]

		DECIMAL [
			label = "{DECIMAL\l|\l|}"
		]

		UnicodeString [
			label = "{UnicodeString\l|\l|}"
		]

		FILETIME [
			label = "{FILETIME\l|\l|}"
		]

		BLOB [
			label = "{BLOB\l|\l|}"
		]

		IndirectPropertyName [
			label = "{IndirectPropertyName\l|\l|}"
		]

		ClipboardData [
			label = "{ClipboardData\l|\l|}"
		]

		GUID [
			label = "{GUID\l|\l|}"
		]

		VersionedStream [
			label = "{VersionedStream\l|\l|}"
		]

		HRESULT [
			label = "{HRESULT\l|\l|}"
		]

		Array [
			label = "{Array\l|\l|}"
		]

		Vector [
			label = "{Vector\l|\l|}"
		]

		Sequence [
			label = "{Sequence\l|\l|}"
		]

		ValuePacket -> CURRENCY;
		ValuePacket -> DATE;
		ValuePacket -> CodePageString;
		ValuePacket -> DECIMAL;
		ValuePacket -> UnicodeString;
		ValuePacket -> FILETIME;
		ValuePacket -> BLOB;
		CodePageString -> IndirectPropertyName;
		ValuePacket -> ClipboardData;
		ValuePacket -> GUID;
		ValuePacket -> VersionedStream;
		ValuePacket -> HRESULT;
		ValuePacket -> Array;
		ValuePacket -> Vector;
		ValuePacket -> Sequence;
	}

Typed Property Value (TPV) classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. graphviz::

	digraph oleps_tpv_classes {
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

		PropertyPacket [
			label = "{PropertyPacket\l|size\lvalue\l|}"
		]

		TypedPropertyValue [
			label = "{TypedPropertyValue\l|type\l_ctype\l|}"
		]

		VT_EMPTY [
			label = "{VT_EMPTY\l|\l|}"
		]

		VT_NULL [
			label = "{VT_NULL\l|\l|}"
		]

		VT_I2 [
			label = "{VT_I2\l|\l|}"
		]

		VT_I4 [
			label = "{VT_I4\l|\l|}"
		]

		VT_R4 [
			label = "{VT_R4\l|\l|}"
		]

		VT_R8 [
			label = "{VT_R8\l|\l|}"
		]

		VT_CY [
			label = "{VT_CY\l|\l|}"
		]

		VT_DATE [
			label = "{VT_DATE\l|\l|}"
		]

		VT_LPSTR [
			label = "{VT_LPSTR\l|\l|}"
		]

		VT_ERROR [
			label = "{VT_ERROR\l|\l|}"
		]

		VT_BOOL [
			label = "{VT_BOOL\l|\l|}"
		]

		VT_DECIMAL [
			label = "{VT_DECIMAL\l|\l|}"
		]

		VT_I1 [
			label = "{VT_I1\l|\l|}"
		]

		VT_UI1 [
			label = "{VT_UI1\l|\l|}"
		]

		VT_UI2 [
			label = "{VT_UI2\l|\l|}"
		]

		VT_UI4 [
			label = "{VT_UI4\l|\l|}"
		]

		VT_I8 [
			label = "{VT_I8\l|\l|}"
		]

		VT_UI8 [
			label = "{VT_UI8\l|\l|}"
		]

		VT_INT [
			label = "{VT_INT\l|\l|}"
		]

		VT_UINT [
			label = "{VT_UINT\l|\l|}"
		]

		VT_BSTR [
			label = "{VT_BSTR\l|\l|}"
		]

		VT_LPWSTR [
			label = "{VT_LPWSTR\l|\l|}"
		]

		VT_FILETIME [
			label = "{VT_FILETIME\l|\l|}"
		]

		VT_BLOB [
			label = "{VT_BLOB\l|\l|}"
		]

		VT_STREAM [
			label = "{VT_STREAM\l|\l|}"
		]

		VT_STORAGE [
			label = "{VT_STORAGE\l|\l|}"
		]

		VT_STREAMED_OBJECT [
			label = "{VT_STREAMED_OBJECT\l|\l|}"
		]

		VT_STORED_OBJECT [
			label = "{VT_STORED_OBJECT\l|\l|}"
		]

		VT_BLOB_OBJECT [
			label = "{VT_BLOB_OBJECT\l|\l|}"
		]

		VT_CF [
			label = "{VT_CF\l|\l|}"
		]

		VT_CLSID [
			label = "{VT_CLSID\l|\l|}"
		]

		VT_VERSIONED_STREAM [
			label = "{VT_VERSIONED_STREAM\l|\l|}"
		]

		VT_ARRAY [
			label = "{VT_ARRAY\l|\l|}"
		]

		VT_VECTOR [
			label = "{VT_VECTOR\l|\l|}"
		]

		PropertyPacket -> TypedPropertyValue;
		TypedPropertyValue -> VT_EMPTY;
		TypedPropertyValue -> VT_NULL;
		TypedPropertyValue -> VT_I2;
		TypedPropertyValue -> VT_I4;
		TypedPropertyValue -> VT_R4;
		TypedPropertyValue -> VT_R8;
		TypedPropertyValue -> VT_CY;
		TypedPropertyValue -> VT_DATE;
		TypedPropertyValue -> VT_LPSTR;
		TypedPropertyValue -> VT_ERROR;
		TypedPropertyValue -> VT_BOOL;
		TypedPropertyValue -> VT_DECIMAL;
		TypedPropertyValue -> VT_I1;
		TypedPropertyValue -> VT_UI1;
		TypedPropertyValue -> VT_UI2;
		TypedPropertyValue -> VT_UI4;
		TypedPropertyValue -> VT_I8;
		TypedPropertyValue -> VT_UI8;
		VT_I4 -> VT_INT;
		VT_UI4 -> VT_UINT;
		TypedPropertyValue -> VT_BSTR;
		TypedPropertyValue -> VT_LPWSTR;
		TypedPropertyValue -> VT_FILETIME;
		TypedPropertyValue -> VT_BLOB;
		VT_BSTR -> VT_STREAM;
		VT_BSTR -> VT_STORAGE;
		VT_BSTR -> VT_STREAMED_OBJECT;
		VT_BSTR -> VT_STORED_OBJECT;
		VT_BLOB -> VT_BLOB_OBJECT;
		TypedPropertyValue -> VT_CF;
		TypedPropertyValue -> VT_CLSID;
		TypedPropertyValue -> VT_VERSIONED_STREAM;
		TypedPropertyValue -> VT_ARRAY;
		TypedPropertyValue -> VT_VECTOR;


	}


Base Classes
------------

.. class:: Packet

	Base class for packet types.

.. class:: ActivePacket

	Base class for a packet type that can read from streams/ctypes.

.. class:: PropertyPacket

	Base class for packet types associated with a property.

	.. attribute:: size

		The total number of bytes in the packet, including any header, value,
		and padding fields.

	.. attribute:: value

		The represented value.

.. class:: ValuePacket

	Base class for packet types associated with the value of a property.

	.. attribute:: size

		The total number of bytes in the packet, including any header, value,
		and padding fields.

	.. attribute:: value

		The represented value.


Headers
-------

.. class:: PropertySetStreamHeader

	Represents the header of a PropertySetStream structure (packet).

	.. attribute:: byte_order

		The byte order field.

	.. attribute:: version

		The version of the OLE property set.

	.. attribute:: sys_id

		The system identifier field.

	.. attribute:: clsid

		The CLSID of the associated property set(s).

	.. attribute:: property_set_count

		The number of property sets in the stream.

	.. attribute:: fmtid0

		A GUID that identifies the property set format of the first property
		set.

	.. attribute:: offset0

		The offset of the first property set, relative to the start of the
		:class:`PropertySetStreamHeader` structure.

	.. attribute:: fmtid1

		A GUID that identifiers the property set format of the second property
		set.  If there is only one property set, this is set to ``None``.

	.. attribute:: offset1

		The offset of the second property set, relative to the start of the
		:class:`PropertySetStreamHeader` structure.  If there is only one
		property set, this is set to ``None``.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`PropertySetStreamHeader` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the PropertySetStreamHeader
					   structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetStreamHeader`
		:returns: The corresponding :class:`PropertySetStreamHeader` object.

.. class:: PropertySetHeader

	Represents the header of a PropertySet structure. (packet)

	.. attribute:: size

		The total size (in bytes) of the PropertySetHeader structure.

	.. attribute:: pair_count

		The number of pid/offset pairs.

	.. attribute:: pids_offsets

		A dictionary of property identifiers and the corresponding properties.

	.. classmethod:: from_stream(stream, offset=None)

		Creates a :class:`PropertySetHeader` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the PropertySetHeader structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetHeader`
		:returns: The corresponding :class:`PropertySetHeader` object.


Special Properties
------------------

.. class:: Dictionary

	Represents a Dictionary property.

	.. attribute:: property_count

		A count of the number of properties in the mapping.  This is a field in
		the data type (i.e. not len(mapping)).

	.. attribute:: mapping

		A dictionary of property identifiers (keys) and names (values).

	.. attribute:: value

		An alias for the :attr:`mapping` attribute.

	.. classmethod::
		from_stream(stream, offset=None, code_page=None, decoder=None)

		Creates a :class:`Dictionary` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the Dictionary property.

		:type offset: ``int``
		:param offset: The start of the property in :attr:`stream`.

		:type code_page: ``int``
		:param code_page: The value of the CodePage property.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the names.

		:rtype: :class:`Dictionary`
		:returns: The corresponding :class:`Dictionary` object.

.. class:: DictionaryEntry

	Represents a DictionaryEntry structure (packet).

	.. attribute:: pid

		The property identifier

	.. attribute:: name

		The name associated with the property identifier.

	.. attribute:: value

		An alias for the :attr:`name` attribute.

	.. classmethod::
		from_stream(stream, offset=None, code_page=None, decoder=None)

		Creates a :class:`DictionaryEntry` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the DictionaryEntry property.

		:type offset: ``int``
		:param offset: The start of the property in :attr:`stream`.

		:type code_page: ``int``
		:param code_page: The value of the CodePage property.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the names.

		:rtype: :class:`DictionaryEntry`
		:returns: The corresponding :class:`DictionaryEntry` object.

Common OLE data types
---------------------

.. class:: CURRENCY

	Represents a CURRENCY structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`CURRENCY` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the CURRENCY structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`CURRENCY`
		:returns: The corresponding :class:`CURRENCY` object.

.. class:: DATE

	Represents a DATE structure (packet).
	
	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`DATE` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the DATE structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`DATE`
		:returns: The corresponding :class:`DATE` object.

.. class:: CodePageString

	Represents a CodePageString structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`CodePageString` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the CodePageString structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`CodePageString`
		:returns: The corresponding :class:`CodePageString` object.

.. class:: DECIMAL

	Represents a DECIMAL structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`DECIMAL` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the DECIMAL structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`DECIMAL`
		:returns: The corresponding :class:`DECIMAL` object.

.. class:: UnicodeString

	Represents a UnicodeString structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`UnicodeString` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the UnicodeString structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the string.

		:rtype: :class:`UnicodeString`
		:returns: The corresponding :class:`UnicodeString` object.

.. class:: FILETIME

	Represents a FILETIME structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`FILETIME` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the FILETIME structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`FILETIME`
		:returns: The corresponding :class:`FILETIME` object.

.. class:: BLOB

	Represents a BLOB structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`BLOB` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the BLOB structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`BLOB`
		:returns: The corresponding :class:`BLOB` object.

.. class:: IndirectPropertyName

	Represents an IndirectPropertyName structure (packet).

.. class:: ClipboardData

	Represents a ClipboardData structure (packet).

	.. attribute:: format

		The format field.

	.. attribute:: data

		The data field.

	.. attribute:: value

		An alias for the :attr:`data` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`ClipboardData` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the ClipboardData structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`ClipboardData`
		:returns: The corresponding :class:`ClipboardData` object.

.. class:: GUID

	Represents a GUID structure (packet).

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`GUID` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the GUID structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`GUID`
		:returns: The corresponding :class:`GUID` object.

.. class:: VersionedStream

	Represents a VersionedStream structure (packet).

	.. attribute:: version_guid

		The VersionGuid field.

	.. attribute:: stream_name

		The StreamName field.

	.. attribute:: value

		An alias for the :attr:`stream_name` attribute.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`VersionedStream` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the VersionedStream structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the stream name.

		:rtype: :class:`VersionedStream`
		:returns: The corresponding :class:`VersionedStream` object.

.. class:: HRESULT

	Represents an HRESULT structure (packet).

	.. note::

		The :attr:`value` attribute is an instance of
		:class:`lf.win.objects.HRESULT`

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a :class:`HRESULT` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the HRESULT structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`HRESULT`
		:returns: The corresponding :class:`HRESULT` object.

	.. classmethod:: from_ctype(ctype)

		Creates a :class:`HRESULT` object from a ctype.

		:type ctype: :class:`~lf.win.ctypes.hresult_le` or
					 :class:`~lf.win.ctypes.hresult_be`
		:param ctype: An hresult ctypes object.

		:rtype: :class:`HRESULT`
		:returns: The corresponding :class:`HRESULT` object.

.. class:: Array

	Represents the value from a VT_ARRAY property.

	.. attribute:: scalar_type

		The property type contained in the array.  This is an extracted value.

	.. attribute:: dimensions

		A list of the (size, index_offset) attributes for each dimension.

	.. attribute:: value

		A flattened list of the values.

	.. attribute:: dimension_count

		The number of dimensions in the array.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates an :class:`Array` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the Array structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the string properties.

		:raises ValueError: If the extracted scalar type is an invalid property
							type.

		:rtype: :class:`Array`
		:returns: The corresponding :class:`Array` object.

.. class:: Vector

	Represents the value from a VT_VECTOR packet.

	.. attribute:: value

		A list of elements in the vector.

	.. attribute:: scalar_count

		The number of elements in the vector.

	.. classmethod::
		from_stream(stream, scalar_type, offset=None, decoder=None)

		Creates a :class:`Vector` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the Vector structure.

		:type scalar_type: :const:`lf.win.ole.ps.consts.PropertyType`
		:param scalar_type: The type of the properties in the Vector structure.

		:type offset: int
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode the string properties.

		:raises ValueError: If :attr:`scalar_type` is an invalid property type.

		:rtype: :class:`Vector`
		:returns: The corresponding :class:`Vector` object.

.. class:: Sequence

	A :class:`ValuePacket` that is composed of a sequence of values.

	The :attr:`value` attribute is a list of (possibly more lists of)
	the values in the sequence.

	.. note::

		This is used internally by the :class:`Array` and :class:`Vector`
		classes to extract the individual elements.

	.. classmethod::
		from_stream(stream, ptype, count, offset=None, decoder=None)

		Creates a sequence of various properties from a stream.

		.. note::

			This method will round the size up to the nearest multiple of 4.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the sequence.

		:type ptype: :const:`lf.win.ole.ps.consts.PropertyType`
		:param ptype: The property type of the elements in the Sequence.

		:type count: ``int``
		:param count: The number of elements in the sequence.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode string properties.

		:raises ValueError: If :attr:`ptype` is an invalid property type.

		:rtype: :class:`Sequence`
		:returns: The corresponding :class:`Sequence` object.

	.. classmethod::
		from_factory(stream, factory, count, offset=None, decoder=None)

		Creates a sequence of various properties, given a factory.

		.. note::

			It is up to the calling function to round the size up to the
			nearest multiple of 4 (if necessary).

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the sequence.

		:type factory: ``function``
		:param factory: A factory function to create the properties.  This
						function must accept the same arguments as
						:func:`TypedPropertyValue.from_stream`.

		:type count: ``int``
		:param count: The number of elements in the sequence.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode string properties.

		:rtype: :class:`Sequence`
		:returns: The corresponding :class:`Sequence` object.


Typed Property Value (TPV) classes
----------------------------------
The following classes represent typed values of a property.

.. class:: TypedPropertyValue

	Base class for TypedPropertyValue packets.

	.. attribute:: type

		The property type.

	.. attribute:: _ctype

		A :class:`ctypes` ctype used to extract the various properties.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a TypedPropertyValue object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`TypedPropertyValue`
		:returns: The corresponding :class:`TypedPropertyValue` object.

.. class:: VT_EMPTY

	Typed value :const:`~lf.win.ole.varenum.VT_EMPTY`.

.. class:: VT_NULL

	Typed value :const:`~lf.win.ole.varenum.VT_NULL`.

.. class:: VT_I2

	Typed value :const:`~lf.win.ole.varenum.VT_I2`.

.. class:: VT_I4

	Typed value :const:`~lf.win.ole.varenum.VT_I4`.

.. class:: VT_R4

	Typed value :const:`~lf.win.ole.varenum.VT_R4`.

.. class:: VT_R8

	Typed value :const:`~lf.win.ole.varenum.VT_R8`.

.. class:: VT_CY

	Typed value :const:`~lf.win.ole.varenum.VT_CY`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_CY object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`VT_CY`
		:returns: The corresponding :class:`VT_CY` object.

.. class:: VT_DATE

	Typed value :const:`~lf.win.ole.varenum.VT_DATE`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_DATE object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`VT_DATE`
		:returns: The corresponding :class:`VT_DATE` object.

.. class:: VT_LPSTR

	Typed value :const:`~lf.win.ole.varenum.VT_LPSTR`.

	.. note::

		The :attr:`value` attribute is the :attr:`value` attribute from a
		:class:`CodePageString` object.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_LPSTR object from a stream.

		.. note::

			If a decoder is specified, then the string will be decoded and
			trimmed to the first null terminator (if found).

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`VT_LPSTR`
		:returns: The corresponding :class:`VT_LPSTR` object.

.. class:: VT_ERROR

	Typed value :const:`~lf.win.ole.varenum.VT_ERROR`.

	.. note::

		The :attr:`value` attribute is an instance of an
		:class:`~lf.win.objects.HRESULT` class.


	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_ERROR object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`VT_ERROR`
		:returns: The corresponding :class:`VT_ERROR` object.

.. class:: VT_BOOL

	Typed value :const:`~lf.win.ole.varenum.VT_BOOL`.

.. class:: VT_DECIMAL

	Typed value :const:`~lf.win.ole.varenum.VT_DECIMAL`.


	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_DECIMAL object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`VT_DECIMAL`
		:returns: The corresponding :class:`VT_DECIMAL` object.

.. class:: VT_I1

	Typed value :const:`~lf.win.ole.varenum.VT_I1`.

.. class:: VT_UI1

	Typed value :const:`~lf.win.ole.varenum.VT_UI1`.

.. class:: VT_UI2

	Typed value :const:`~lf.win.ole.varenum.VT_UI2`.

.. class:: VT_UI4

	Typed value :const:`~lf.win.ole.varenum.VT_UI4`.

.. class:: VT_I8

	Typed value :const:`~lf.win.ole.varenum.VT_I8`.

.. class:: VT_UI8

	Typed value :const:`~lf.win.ole.varenum.VT_UI8`.

.. class:: VT_INT

	Typed value :const:`~lf.win.ole.varenum.VT_INT`.

.. class:: VT_UINT

	Typed value :const:`~lf.win.ole.varenum.VT_UINT`.

.. class:: VT_BSTR

	Typed value :const:`~lf.win.ole.varenum.VT_BSTR`.

	.. note::

		The :attr:`value` attribute is the :attr:`value` attribute from a
		:class:`CodePageString`.


	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_BSTR object from a stream.

		.. note::

			If a decoder is specified, then the string will be decoded.  Unlike
			:class:`VT_LPSTR` classes, the string is *not* trimmed, since it
			may contain embedded NULLs.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`VT_BSTR`
		:returns: The corresponding :class:`VT_BSTR` object.

.. class:: VT_LPWSTR

	Typed value :const:`~lf.win.ole.varenum.VT_LPWSTR`.


	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_LPWSTR object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec, used only if the property requires a
						decoder.

		:rtype: :class:`VT_LPWSTR`
		:returns: The corresponding :class:`VT_LPWSTR` object.

.. class:: VT_FILETIME

	Typed value :const:`~lf.win.ole.varenum.VT_FILETIME`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_FILETIME object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`VT_FILETIME`
		:returns: The corresponding :class:`VT_FILETIME` object.

.. class:: VT_BLOB

	Typed value :const:`~lf.win.ole.varenum.VT_BLOB`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_BLOB object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`VT_BLOB`
		:returns: The corresponding :class:`VT_BLOB` object.

.. class:: VT_STREAM

	Typed value :const:`~lf.win.ole.varenum.VT_STREAM`.

.. class:: VT_STORAGE

	Typed value :const:`~lf.win.ole.varenum.VT_STORAGE`.

.. class:: VT_STREAMED_OBJECT

	Typed value :const:`~lf.win.ole.varenum.VT_STREAMED_OBJECT`.

.. class:: VT_STORED_OBJECT

	Type value :const:`~lf.win.ole.varenum.VT_STORED_OBJECT.`

.. class:: VT_BLOB_OBJECT

	Typed value :const:`~lf.win.ole.varenum.VT_BLOB_OBJECT`.

.. class:: VT_CF

	Typed value :const:`~lf.win.ole.varenum.VT_CF`.

	.. attribute:: value

		An instance of :class:`ClipboardData`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_CF object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`VT_CF`
		:returns: The corresponding :class:`VT_CF` object.

.. class:: VT_CLSID

	Typed value :const:`~lf.win.ole.varenum.VT_CLSID`.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_CLSID object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``None``
		:param decoder: This parameter is not used.

		:rtype: :class:`VT_CLSID`
		:returns: The corresponding :class:`VT_CLSID` object.

.. class:: VT_VERSIONED_STREAM

	Typed value :const:`~lf.win.ole.varenum.VT_VERSIONED_STREAM`.

	.. attribute:: value

		An instance of a :class:`VersionedStream` object.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_VERSIONED_STREAM object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode string properties.

		:rtype: :class:`VT_VERSIONED_STREAM`
		:returns: The corresponding :class:`VT_VERSIONED_STREAM` object.

.. class:: VT_ARRAY

	Typed value :const:`~lf.win.ole.varenum.VT_ARRAY`.

	.. attribute:: value

		An instance of an :class:`Array` object.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_ARRAY object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode string properties.

		:rtype: :class:`VT_ARRAY`
		:returns: The corresponding :class:`VT_ARRAY` object.

.. class:: VT_VECTOR

	Typed value :const:`~lf.win.ole.varenum.VT_VECTOR`.

	.. attribute:: value

		An instance of a :class:`Vector` object.

	.. classmethod:: from_stream(stream, offset=None, decoder=None)

		Creates a VT_VECTOR object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: ``codecs.codec``
		:param decoder: An optional codec to decode string properties.

		:rtype: :class:`VT_VECTOR`
		:returns: The corresponding :class:`VT_VECTOR` object.

Building properties
-------------------
These classes are used to build properties and property sets.

.. class:: PropertyFactory

	A class that makes properties.

	.. classmethod:: make(stream, offset=None, decoder=None)

		Makes a property object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the property structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode string properties.

		:rtype: :class:`PropertyPacket`
		:returns: The corresponding :class:`PropertyPacket` (or subclass)
				  object.

.. class:: PropertySet

	Represents a PropertySet structure (packet).

	.. attribute:: size

		The size in bytes of the PropertySetHeader structure.

	.. attribute:: pair_count

		The number of pid/offset pairs.

	.. attribute:: pids_offsets

		A dictionary of property identifiers and the offsets of the
		corresponding properties.

	.. attribute:: properties

		A dictionary of property identifiers and the corresponding properties.

.. class:: PropertySetStream

	Represents a PropertySetStream structure (packet).

	.. attribute:: byte_order

		The byte order field.

	.. attribute:: version

		The version of the OLE property set.

	.. attribute:: sys_id

		The system identifier field.

	.. attribute:: clsid

		The CLSID of the associated property set(s).

	.. attribute:: property_set_count

		The number of property sets in the stream.

	.. attribute:: fmtid0

		A GUID that identifies the property set format of the first property
		set.  If there are no property sets, this should be ``None``.

	.. attribute:: offset0

		The offset of the first property set, relative to the start of the
		:class:`PropertySetStreamHeader` structure.  If there are no property
		sets, this should be ``None``.

	.. attribute:: fmtid1

		A GUID that idientifies the property set format of the second property
		set.  If there is only one property set, this should be ``None``.

	.. attribute:: offset1

		The offset of the second property set, relative to the start of the
		:class:`PropertySetStreamHeader` structure.  If there is only one
		property set, this should be ``None``.

	.. attribute:: property_set_0

		An instance of :class:`PropertySet` that represents the first property
		set.  If there are no property sets, this should be ``None``.

	.. attribute:: property_set_1

		An instance of :class:`PropertySet` that represents the second property
		set.  If there are no property sets, this should be ``None``.

.. class:: Builder

	Builds property set streams.

	.. classmethod:: build(stream, offset=None, decoder=None)

		Builds property set streams from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the property (and related)
					   structures.

		:type offset: ``int``
		:param offset: The start of the structures in :attr:`stream`.

		:type decoder: :class:`codecs.codec`
		:param decoder: An optional codec to decode string properties.  If this
						value is ``None``, one is guessed by using the CodePage
						property.

		:rtype: :class:`PropertySetStream`
		:returns: The corresponding :class:`PropertySetStream` object.

	.. classmethod:: build_property_set_stream_header(stream, offset=None)

		Builds a :class:`PropertySetStreamHeader` object.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetStreamHeader`
		:returns: The corresponding :class:`PropertySetStreamHeader` object.

	.. classmethod:: build_property_set_header(stream, fmtid, offset=None)

		Builds a :class:`PropertySetHeader` object.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the property set header
					   structure.

		:type fmtid: :class:`UUID`
		:param fmtid: The FMTID of the property set.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`PropertySetHeader`
		:returns: The corresponding :class:`PropertySetHeader` object.

	.. classmethod::
		build_properties(stream, fmtid, property_set, offset=None, decoder=None)

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
				  corresponding :class:`PropertyPacket` objects (values).


Metadata
--------

These classes extract metadata from OLE property sets.  Right now, it is just a
subset of the existing properties in a property set.

.. class:: PropertySetMetadata

	Metadata for a :class:`~lf.win.ole.ps.PropertySet`.

	.. attribute:: byte_order

		The value of the byte order field.

	.. attribute:: version

		The version of the OLE property set.

	.. attribute:: sys_id

		The system identifier field.

	.. attribute:: clsid

		The CLSID of the associated property set.

	.. attribute:: fmtid0

		The FMTID of the first property set.

	.. attribute:: fmtid1

		The FMTID of the second property set.

	.. classmethod:: from_property_set(property_set)

		Creates a :class:`PropertySetMetadata` from a property set.

		:type property_set: :class:`PropertySet`
		:param property_set: The property set to examine.

		:rtype: :class:`PropertySetMetadata`
		:returns: The corresponding :class:`PropertySetMetadata` object.

.. class:: PropertiesMetadata

	Metadata for the properties of a :class:`PropertySet`.

	.. attribute:: code_page

		The value of the CodePage property.

	.. attribute:: dictionary

		A dictionary of property identifiers (keys) and names (values).

	.. attribute:: locale

		The value of the locale property.

	.. attribute:: behavior

		The value of the behavior property.

	.. attribute:: attr_exists

		A set of the attribute names that were found in the property set.

	.. classmethod from_properties(properties)

		Creates a :class:`PropertiesMetadata` object from properties.

		:type properties: ``dict``
		:param properties: A dictionary of property identifiers (keys) and the
						   corresponding :class:`PropertyPacket` objects.

		:rtype: :class:`PropertiesMetadata`
		:return: The corresponding :class:`PropertiesMetadata` object.
