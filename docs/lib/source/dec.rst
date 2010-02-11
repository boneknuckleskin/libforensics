:mod:`lf.dec` --- Digital Evidence Containers
=============================================

.. module:: lf.dec
   :synopsis: Digital Evidence Containers
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

Digital Evidence Containers (DECs) are files that contain one or more items of
digital evidence.  Common examples are DD, E01, and AFF files.

In the framework, DECs are represented by two types of classes, containers and
streams.  Containers represent the container file, while streams are the
logical representation of the digital evidence.

To use a DEC, initialize the container, and then use the :meth:`Container.list`
and :meth:`Container.open` to enumerate and open streams inside the container.
For example::

	>>> raw_file = Raw.open("/path/to/image.dd")
	>>> raw_file.list()
	[StreamInfo(id=0)]
	>>> raw_stream = raw_file.open(0)

For container types that need to manage the stream position (i.e. aren't just
wrappers around an existing stream type) there exists the
:class:`ManagedIStream` class.

Containers
----------

.. class:: Container

	Base class for container files.  Subclasses are required to implement the
	:meth:`list` and :meth:`open` methods.

	.. attribute:: stream

		If a container type only supports a single evidence stream (e.g. raw/dd
		files) then this is the stream.  Otherwise this is ``None``.

	.. method:: list

		Lists streams inside a container

		:rtype: list
		:returns: A list of StreamInfo objects, describing the streams inside
				  the container.

	.. method:: open

		Opens a stream for use.

		:rtype: IStream
		:returns: The appropriate stream.

.. class:: SingleStreamContainer

	A convenience class for containers that only have a single stream.
	Subclasses are required to set the :attr:``stream`` attribute.

.. class:: Raw(name)

	A container for raw/dd files.

	:type name: str
	:param name: The name of the raw/dd file.

.. class:: Byte(bytes_)

	A container file for a bytes or bytearray object.

	:type bytes_: bytes or bytearray
	:param bytes_: The bytes or bytearray object to wrap around.

.. class:: Subset(stream, start, size)

	A container for a stream whose contents are a subset of another stream.

	:type stream: IStream
	:param stream: The stream to wrap around.

	:type start: int
	:param start: The start of the subset.

	:type size: int
	:param size: The maximum size (in bytes) of the subset.

.. class:: Composite(segments)

	A container for a stream composed of subsets of other streams.

	:type segments: list of tuples
	:param segments: A list of tuples, where the elements of each tuple are:

		1. The stream to read from.
		2. The offset in the stream for the start of the segment.
		3. The number of bytes in the segment.

.. class:: SplitRaw(names)

	A container for a raw/dd file that has been split into pieces.

	:type names: list of strings
	:param names: A list of the names of the raw/dd files.

StreamInfo Objects
------------------

StreamInfo objects are used to describe information (e.g. name of file) about a
stream.

.. class:: StreamInfo(id=0)

	Creates a new StreamInfo object with the value ``id``.

	.. attribute:: id

		A container-unique identifier for the stream.

Stream Objects
--------------

.. class:: IStream

	Base class for input streams.  All input streams are required to be
	seekable (random access).  Subclasses are required to implement the
	:meth:`seek`, :meth:`tell`, and :meth:`readinto` methods.

	.. attribute:: size

		The size of the stream in bytes.  If this value is not known, it is
		``None``.

	.. method:: seek(offset, whence=SEEK_SET)

		Positions the stream at offset, relative to whence.  Valid values for
		whence are the same as the Python :mod:`io` module.  They are:

			* SEEK_SET - The start of the stream.
			* SEEK_CUR - Current stream position.
			* SEEK_END - The end of the stream.

		:type offset: int
		:param offset: The position of the cursor

		:type whence: int
		:param whence: Tells :meth:`seek` how to interpret ``offset``.

        :except ValueError: If the stream is closed, whence is not one of the
	        SEEK_* constants, or whence is SEEK_SET and offset is negative.

		:rtype: int
		:returns: The new position in the stream.

	.. method:: tell

		Returns the absolute position of the stream.

		:except ValueError: If the stream is closed.

		:rtype: int
		:returns: The position in the stream.

	.. method:: readable

		True if the stream is readable.

	.. method:: readinto(b)

		Reads up to len(b) bytes into b.

		:type b: bytearray
		:param b: A bytearray to hold the bytes read from the stream.

		:except ValueError: If the stream is closed.

		:rtype: int
		:returns: The number of bytes read.

.. class:: ManagedIStream

	An IStream that keeps track of stream position.  This class is useful when
	implementing your own stream types.  The :meth:`seek`, and :meth:`tell`
	methods are provided.

	The :meth:`seek` and :meth:`tell` methods update the :attr:`_position`
	attribute.

	.. note::

		In order for this class to properly implement the :meth:`seek` method,
		subclasses are required to set the :attr:`size` attribute.

	.. attribute:: _position

		The absolute position of the stream.

.. class:: IStreamWrapper(stream, size=None)

	An IStream that wraps around an existing Python :mod:`io` stream.

	:type stream: IStream
	:param stream: The underlying stream to wrap around.

	:type size: int or None
	:param size: The size of the stream (in bytes) or ``None`` if not known.

	.. attribute:: _stream

		The underlying stream to wrap around.

.. class:: RawIStream(name)

	A stream for raw/dd files.

	:type name: str
	:param name: The name of the raw/dd image file.

	.. attribute:: name

		The name of the raw/dd file.

	.. note::

		This class raises :exc:`IOError` (instead of :exc:`ValueError`) in the
		:meth:`seek` method if the ``offset`` parameter is negative, and
		``whence`` is :const:`SEEK_SET`.

.. class:: ByteIStream(bytes_)

	A stream for a bytes or bytearray object.

	:type bytes_: bytes or bytearray
	:param bytes_: The bytes or bytearray object to read from.

.. class:: SubsetIStream(stream, start, size)

	A stream that is a subset of another stream.

	:type stream: IStream
	:param stream: The stream to wrap around.

	:type start: int
	:param start: The start of the subset.

	:type size: int
	:param size: The size (in bytes) of the subset.

	.. attribute:: _stream

		The stream that is wrapped around.

	.. attribute:: _start

		The start of the subset, in the :attr:`_stream` attribute.

.. class:: CompositeIStream(segments)

	A stream composed of subsets of other streams.

	:type segments: list of tuples
	:param segments: A list of tuples where the elements of each tuple are:

		1. The stream to read from.
		2. The offset in the stream of the start of the segment.
		3. The number of bytes in the segment.

	.. attribute:: _segments

		A list of (stream, start, size) tuples.

.. class:: SplitRawIStream(names)

	A stream for a raw/dd file that has been split into pieces.

	:type names: list of strings
	:param names: A list of the names of the raw/dd files.

	.. attribute:: _names

		A list of the names of the raw/dd files.
