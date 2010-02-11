:mod:`lf.dtypes` --- Data Types
===============================

.. module:: lf.dtypes
   :synopsis: Describe and interpret the meaning of bytes
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module converts information represented as binary data (Python
:class:`bytes` objects) into Python objects.


Overview
--------
There are three components to the data typing system in LibForensics:

	1. Describing the type and structure of information (i.e. a :mod:`ctypes`
	   wrapper)
	2. Translating a :class:`bytes` object into Python objects (**D**\ ata
	   **A**\ ccess **L**\ ayer or DAL)
	3. A standard protocol for using the :mod:`ctypes` wrappers and the DAL.

Describing data types
---------------------
The :mod:`ctypes` module is used to extract various data types (e.g. integers,
floating point values, structures, etc.) from a stream of bytes.  To facilitate
this, LibForensics provides a (restricted) wrapper for the :mod:`ctypes`
module.

LibForensics supports several primitive data types, including 8/16/32/64 bit
signed and unsigned integers, 32/64 bit floating point values, records
(a.k.a. structs, data structures), and arrays.

Records (structures) are a data type that is composed of one or more primitive
data types.  The description of a record is a class, where the class attributes
represent the fields of the record.  At runtime, a metaclass is used to
translate a :class:`Record` class into a :mod:`ctypes` object.  The
:mod:`ctypes` object is accessible as the :attr:`_ctype_` attribute.

The following snippet shows how to create a record with three fields:

	>>> from lf.dtypes import LERecord, uint8, int16, uint32
	>>> class SomeStruct(LERecord):
	... 	field1 = uint8
	... 	field2 = uint32
	... 	field3 = int16
	...
	>>> ctypes_obj = SomeStruct._ctype_


Class Hierarchy
^^^^^^^^^^^^^^^
.. graphviz:: 

	digraph dtypes_hierarchy {
		fontname = "Courier New"
		fontsize = 10

		node [
			fontname = "Courier New"
			fontsize = 10
			shape = "record"
		]

		DataType [
			label = "{DataType\l|_size_\l|\l}"
		]

		Primitive [
			label = "{Primitive\l|_ctype_\l|\l}"
		]

		bits [
			label = "{Bits\l|\l|\l}"
		]

		bit [
			label = "{Bit\l|\l|\l}"
		]

		Basic [
			label = "{Basic\l|\l|\l}"
		]

		Composite [
			label = "{Composite\l" + 
					"|_fields_\l_pack_\l_anonymous_\l_ctype_name_" +
					"\l_byte_order_\l" + 
					"|\l}"
		]

		BitType [
			label = "{BitType\l|_int_type_\l_fields_\l|\l}"
		]

		raw [
			label = "{raw\l|\l|\l}"
		]

		Native [
			label = "{Native\l|\l|\l}"
		]

		edge [
			arrowhead = "none"
			arrowtail = "empty"
		]

		DataType -> Primitive;
		DataType -> bits;
		bits -> bit;
		Primitive -> Composite;
		Primitive -> Basic;
		Basic -> BitType;
		Basic -> raw;
		Basic -> Native;
	}


:class:`Primitive` data types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:class:`Primitive` data types are data types that can be used by themselves, or
grouped together to create :class:`Composite` data types.

LibForensics provides 2 types of :class:`Primitive` data types:

	1. :class:`Basic` -- Primitive data types that can not be decomposed
	2. :class:`Composite` -- Primitive data types composed of other primtive
	   data types.


:class:`Basic` data types
^^^^^^^^^^^^^^^^^^^^^^^^^
:class:`Basic` data types are "basic building blocks".  They can be used by
themselves, or can be grouped together to create :class:`Composite` data types.
:class:`Basic` data types however are not further decomposable.

LibForensics provides 3 types of :class:`Basic` data types:

	1. :class:`Native` -- Data types with native ctypes support.
	2. :class:`BitType` -- Data types with access to individual bits.
	3. :class:`raw` -- Data type for a raw stream of bytes.


:class:`Composite` data types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:class:`Composite` data types are data types composed of one or more
:class:`Primitive` data types.  This includes :class:`Basic` data types, as
well as other :class:`Composite` data types.

LibForensics provides 2 types of :class:`Composite` data types:

	1. :class:`Record` (a.k.a. structs, data structures) -- Composite data
	   types where the elements do not need to be the same type.
	2. Arrays -- Composite data types where the elements are identical types.


The Data Access Layer (DAL)
---------------------------
One of the design goals of the :mod:`ctypes` wrapper provided by LibForensics
is to have data types that are not data-dependent.  This means that regardless
of the value of the bytes used, extracting Python values with data types
(created with the :mod:`ctypes` wrapper) should not fail.

The advantage of this type of design is that any pattern of 1s and 0s can be
used.  There are several places situations that this design is useful.  Such as
(blindly) looking for a particular data structure in unallocated space, slack
space, or without much other structural information.  Additionally, if a data
structure has been partially overwritten (e.g. it was in a file that was
deleted, and then part of the file was reallocated and overwritten) NULL bytes
can be used to make up the missing part of the data structure.

The disadvantage of this approach means that the :mod:`ctypes` wrapper does not
support any data type that requires using the value.  A common example is a
pointer data type.  The value of the pointer is a location (address).  An
invalid value for the pointer can cause problems for automated solutions.  For
example:

	>>> from ctypes import Structure, c_int8, POINTER
	>>> class Struct(Structure):
	...     _fields_ = [("field1", POINTER(c_int8))]
	... 
	>>> values = Struct.from_buffer_copy(b"\x01\x00\x00\x00\x00\x00\x00\x00")
	>>> values.field1.contents
	Segmentation fault

Depending on the situation, there are several different options for dealing
with invalid data.

Value Objects and Entities
^^^^^^^^^^^^^^^^^^^^^^^^^^
The DAL is built around two concepts: Value objects and Entities (a.k.a.
reference objects).  The primary difference between a value object and an
entity is how equality is determined.  Value objects are considered equal if
their value (or the values of their attributes) are equal.  Entity objects are
considered equal if thier identities (memory addresses, unique identifiers,
etc.) are equal.

In LibForensics, value objects are subclasses of the :class:`Structuple` class
(usually :class:`ActiveStructuple`).  Entities however, are regular
user-defined classes.

Converters
^^^^^^^^^^
Some data types have equivalents in the Python standard library.  For instance,
a 64-bite FILETIME timestamp can be represented by a :class:`datetime.datetime`
class.  Converter classes fill the role of converting from :class:`bytes` to a
standard Python object.  :class:`Converter` classes are subclasses of the
:class:`Converter` class.


Standard protocol for the :mod:`ctypes` wrappers and the DAL
--------------------------------------------------------------
In order to reduce the learning curve of the several data structures
(:class:`Record` data types) used throughout LibForensics, there is a standard
approach to naming, locating, and using the :mod:`ctypes` wrappers, and the
DAL.  The rules are:

	* The definitions of the data types are placed in a file called
	  :file:`dtypes.py`
	* A convenience module called :file:`ctypes.py` contains the
	  :attr:`_ctype_` attribute from each class defined in the
	  :file:`dtypes.py` file.
	* Classes that represent value objects are descendants of the
	  :class:`Structuple` class.
	* Classes that represent entities are regular user-defined classes (i.e.
	  they are *not* descendents of :class:`Structuple`.)
	* Classes that are used to translate a :class:`bytes` object to a standard
	  Python object inherit from the :class:`Converter` class.
	* value objects, entities, and converters  are placed in a file called
	  :file:`objects.py`


Base data types
---------------

.. class:: DataType()

	Base class for all data types.

	.. attribute:: _size_

		The size of the data type.  The units (e.g. bits or bytes) are
		dependent on the subclass.

.. class:: Primitive()

	Base class for data types that can be used to compose other data types.

	.. attribute:: _ctype_

		A :mod:`ctypes` object that reflects the data type.

Basic data types
----------------

These are data types that are the "basic building blocks".  These data types
can be used for composition, but are not composable.

.. class:: Basic()

	Base class for :class:`Basic` data types.

.. class:: raw(size)

	A data type for a raw array of bytes.

	:type size: int
	:param size: The number of bytes in the string.

	.. note::

		When using the :class:`raw` data type, the corresponding ctypes object
		is an array of c_ubyte (i.e. c_ubyte * size).  This means you will need
		to call :meth:`bytes` to get a :class:`bytes` object.

Native data types
-------------------
These are data types that have native support in the :mod:`ctypes` module.

.. class:: Native()

	Base class for :class:`Native` data types.

.. class:: int8()

	Signed 8-bit integer.

.. class:: uint8()

	Unsigned 8-bit integer.

.. class:: int16()

	Signed 16-bit integer.

.. class:: uint16()

	Unsigned 16-bit integer.

.. class:: int32()

	Signed 32-bit integer.

.. class:: uint32()

	Unsigned 32-bit integer.

.. class:: int64()

	Signed 64-bit integer.

.. class:: uint64()

	Unsigned 64-bit integer.

.. class:: float32()

	32-bit floating point number.

.. class:: float64()

	64-bit floating point number.

Bit-oriented data types
-----------------------
LibForensics provides support for bit-oriented data types using the
:class:`BitType`, :class:`bits`, and :class:`bit` classes.

.. class:: bits(size=1):

	Represents one or more bits.

	:type size: int
	:param size: The number of bits in the data type.

.. class:: bit()

	A convenience class to represent a single bit.

.. class:: BitType()

	A container class for bits.  This class is used to allow bits to be used as
	a :class:`Primitive` class.

	.. attribute:: _int_type_

		The ctypes integer type that encapsulates the bits.

	.. attribute:: _fields_

		A list of the fields in the BitType.  If this is None (or not present)
		it is automatically generated by a metaclass.

The following :class:`BitType` subclasses can be used as :class:`Primitive`
data types.

.. class:: BitType8()

	A bit type represented by a signed 8-bit integer.

.. class:: BitTypeU8()

	A bit type represented by an unsigned 8-bit integer.

.. class:: BitType16()

	A bit type represented by a signed 16-bit integer.

.. class:: BitTypeU16()

	A bit type represented by an unsigned 16-bit integer.

.. class:: BitType32()

	A bit type represented by a signed 32-bit integer.

.. class:: BitTypeU32()

	A bit type represented by an unsigned 32-bit integer.

.. class:: BitType64()

	A bit type represented by a signed 64-bit integer.

.. class:: BitTypeU64()

	A bit type represented by an unsigned 64-bit integer.


Composite data types
--------------------
Composite data types are data types that are composed of one or more data
types.  LibForensics supports two types of composite data types, arrays and
records (a.k.a. data structures, structs, tuples, etc.)

Arrays are an arrangement of multiple copies of a single data type.  In the
LibForensics data typing system, arrays are represented by lists.  The first
element of the list is the data type of the elements of the array.  The size of
the list denotes the number of elements in the array.

For example a data structure with a field that has 10 8-bit integers:

	>>> from lf.dtypes import LERecord, uint8
	>>> class SomeStruct(LERecord):
	...		field1 = [uint8] * 10


Records are a data structure similar to arrays, except the elements (called
fields) of the record do not have to all be the same data type.  Records are
represented by the :class:`Record` class, usually a subclass.

.. data:: LITTLE_ENDIAN

	Constant to indicate a :class:`Composite` data type fields are in little
	endian order.

.. data:: BIG_ENDIAN

	Constant to indicate a :class:`Composite` data type fields are in big
	endian order.

.. class:: Composite()

	Base class for data types that can be composed of data types.  Since this
	is a :class:`Primitive` class, subclasses can be used to both compose data
	types, as well as be composed of other classes.

	Fields are implemented as class attributes.  For instance:

		>>> from lf.dtypes import LERecord, int8, uint8
		>>> class SomeStruct(LERecord):
		...		field1 = int8
		...		field2 = uint8
		...
		>>>

	Will create a class called SomeStruct, with two fields called field1 and
	field2.

	Composite objects can also inherit from each other, adding the new fields
	to the old ones.  Continuing the previous example:

		>>> class AnotherStruct(SomeStruct):
		...		field3 = uint8
		...
		>>>

	Will create a class called AnotherStruct, with three fields called field1,
	field2, and field 3.
		

	.. attribute:: _fields_

		A list of (field name, ctype object) tuples.  If this is None, it is
		created automatically by the metaclass.

	.. attribute:: _byte_order_

		The byte ordering to use (:const:`LITTLE_ENDIAN` or
		:const:`BIG_ENDIAN`)

	.. attribute:: _pack_

		The _pack_ attribute used when creating the :attr:`_ctype_` attribute.
		The default is 1.

	.. attribute:: _anonymous_

		The value of the _anonymous_ attribute used when creating the
		:attr:`_ctype_` attribute.

	.. attribute:: _ctype_name_

		The name to use for the :attr:`_ctype_` attribute.  If this is not
		specified, a name is autogenerated by a metaclass, based on the class
		name.

.. class:: Record()

	Base class for creating record data types.

.. class:: LERecord()

	Class for creating little endian record data types.

.. class:: BERecord()

	Class for creating big endian record data types.


Data Access Layer (DAL) Support
-------------------------------
The DAL provides three types of functionality, :class:`Structuple`,
:class:`Converter`, and :class:`Reader` classes.

:class:`Structuple` classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: structuple(name, fields, aliases=None, auto_slots=False, rename=False)

	Factory function to create new :class:`Structuple` classes.

	:type name: str
	:param name: The name for the new :class:`Structuple` class.

	:type fields: iterable
	:param fields: A string, dictionary, or iterable of the names of the
				   attributes and their positions.  If this is a string or
				   iterable, the positions are determined by the order in which
				   the names occur, starting with position 0 (first element).
				   If this is a dictionary, the keys are the names of the
				   attributes, and the positions are the values.

	:type aliases: :class:`dict`
	:param aliases: A dictionary of aliases for attributes.  The keys are the
					names of the aliases, and the values are the names of the
					attributes the aliases should point to.

	:type auto_slots: ``bool``
	:param auto_slots: If true, the :attr:`__slots__` attribute is
					   automatically defined for the created class and all
					   subclasses, until a subclass sets the
					   :attr:`_auto_slots_` attribute to ``False``.

	:type rename: ``bool``
	:param rename: If ``True``, duplicate attribute names are automatically
				   renamed to field_name__XXX, where XXX is the position of the
				   name.

	:rtype: :class:`Structuple`
	:returns: The newly created class.

.. class:: Structuple(iterable)

	Base class for creating tuples with named attribute access.

	:param iterable: An optional iterator (or object that supports iteration)
				     to provide initial values.

	.. attribute:: _fields_

		A list of names of the attributes, in the same order as the
		corresponding elements of the tuple.

	.. attribute:: _aliases_

		A dictionary to describe attributes that are aliases for other
		attributes.  The keys are the alias names, and the values are the names
		of the attributes they should point to.

	.. attribute:: _auto_slots_

		If ``True``, then the :attr:`__slots__` attribute is created
		automatically for all subclasses, until a subclass sets _auto_slots_ to
		``False``.

.. class:: ActiveStructuple(iterable)

	Base class for value objects.

	:param iterable: An optional iterator (or object that supports iteration)
					 to provide initial values.

	.. attribute:: _takes_stream

		True if the :meth:`from_stream` method is implemented.

	.. attribute:: _takes_ctype

		True if the :meth:`from_ctype` method is implemented.

	.. classmethod:: from_bytes(bytes_)

		Creates an ActiveStructuple from a :class:`bytes` object.  

		.. note:: 

			This method is available if :attr:`_takes_stream` is ``True``.

		:type bytes_: :class:`bytes`
		:param bytes_: A :class:`bytes` object to read from.

		:rtype: :class:`ActiveStructuple`
		:returns: The corresponding :class:`ActiveStructuple`

	.. classmethod:: from_stream(stream, offset=None)

		Creates an ActiveStructuple from an :class:`~lf.dec.IStream` object.

		.. note::

			This method is available if :attr:`_takes_stream` is ``True``.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the :class:`ActiveStructuple`

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the :class:`ActiveStructuple`

		:rtype: :class:`ActiveStructuple`
		:returns: The corresponding :class:`ActiveStructuple`

	.. classmethod:: from_ctype(ctype)

		Creates an ActiveStructuple from a :mod:`ctypes` object.

		.. note::

			This method is available if :attr:`_takes_ctype` is ``True``.

		:type ctype: :class:`ctypes._CData`
		:param ctype: A :mod:`ctypes` object that describes the values of the
					  attributes.

		:rtype: :class:`ActiveStructuple`
		:returns: The corresponding :class:`ActiveStructuple`.

.. class:: CtypesWrapper()

	An :class:`ActiveStructuple` that is a wrapper around a :mod:`ctypes`
	object.  This class provides :meth:`from_stream` and
	:meth:`from_ctype` methods.

	.. attribute:: _ctype_

		The :mod:`ctypes` instance to wrap.

:class:`Converter` classes
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Converter()

	Base class to convert data into a native Python object.

	.. attribute:: _takes_stream

		True if the :meth:`from_stream` method is implemented.

	.. attribute:: _takes_ctype

		True if the :meth:`from_ctype` method is implemented.

	.. classmethod:: from_bytes(bytes_)

        Creates a Python object from a :class:`bytes` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type bytes_: :class:`bytes`
        :param bytes_: A :class:`bytes` object to read from.

        :rtype: object
        :returns: The corresponding Python object.

	.. classmethod:: from_stream(stream, offset=None):

        Creates a Python object from an :class:`~lf.dec.IStream` object.

        .. note::

            This method is available if :attr:`_takes_stream` is ``True``.

        :type stream: :class:`~lf.dec.IStream`
        :param stream: A stream that contains the Python object.

        :type offset: :class:`int` or :keyword:`None`
        :param offset: The start of the Python object.

        :rtype: object
        :returns: The corresponding Python object.

	.. classmethod:: from_ctype(ctype)

        Creates a Python object from a :mod:`ctypes` object.

        .. note::

            This method is available if :attr:`_takes_ctype` is ``True``.

        :type ctype: :class:`ctypes._CData`
        :param ctype: A :mod:`ctypes` object that describes the values of the
                      attributes.

        :rtype: object
        :returns: The corresponding Python object.

.. class:: StdLibConverter()

	Base class for :class:`Converters` to Python standard library objects.

:class:`Reader` classes
^^^^^^^^^^^^^^^^^^^^^^^
:class:`Reader` clsses and objects read :class:`BuiltIn` data types from
streams.  This type of operation is occurs fairly often.

.. class:: Reader()

	Convenience class to read :class:`BuiltIn` data types from a stream.

	.. classmethod:: int8(stream, offset=None):

		Reads a signed 8-bit integer from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint8(stream, offset=None):

		Reads an unsigned 8-bit integer from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int16_le(stream, offset=None):

		Reads a signed 16-bit integer (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint16_le(stream, offset=None):

		Reads an unsigned 16-bit integer (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int16_be(stream, offset=None):

		Reads a signed 16-bit integer (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint16_be(stream, offset=None):

		Reads an unsigned 16-bit integer (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int32_le(stream, offset=None):

		Reads a signed 32-bit integer (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint32_le(stream, offset=None):

		Reads an unsigned 32-bit integer (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int32_be(stream, offset=None):

		Reads a signed 32-bit integer (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint32_be(stream, offset=None):

		Reads an unsigned 32-bit integer (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int64_le(stream, offset=None):

		Reads a signed 64-bit integer (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint64_le(stream, offset=None):

		Reads an unsigned 64-bit integer (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int64_be(stream, offset=None):

		Reads a signed 64-bit integer (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint64_be(stream, offset=None):

		Reads an unsigned 64-bit integer (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.


	.. classmethod:: float32_le(stream, offset=None):

		Reads a 32-bit floating point number (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

	.. classmethod:: float32_be(stream, offset=None):

		Reads a 32-bit floating point number (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

	.. classmethod:: float64_le(stream, offset=None):

		Reads a 64-bit floating point number (little endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

	.. classmethod:: float64_be(stream, offset=None):

		Reads a 64-bit floating point number (big endian) from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: The stream to read data from.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

.. class:: BoundReader(stream)

	A :class:`Reader` that is bound to a :class:`~lf.dec.IStream`.

	:type stream: :class:`~lf.dec.IStream`
	:param stream: A stream that contains the values to read.

	.. classmethod:: int8(offset=None):

		Reads a signed 8-bit integer.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint8(offset=None):

		Reads an unsigned 8-bit integer.

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int16_le(offset=None):

		Reads a signed 16-bit integer (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint16_le(offset=None):

		Reads an unsigned 16-bit integer (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int16_be(offset=None):

		Reads a signed 16-bit integer (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint16_be(offset=None):

		Reads an unsigned 16-bit integer (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int32_le(offset=None):

		Reads a signed 32-bit integer (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint32_le(offset=None):

		Reads an unsigned 32-bit integer (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int32_be(offset=None):

		Reads a signed 32-bit integer (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint32_be(offset=None):

		Reads an unsigned 32-bit integer (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int64_le(offset=None):

		Reads a signed 64-bit integer (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint64_le(offset=None):

		Reads an unsigned 64-bit integer (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: int64_be(offset=None):

		Reads a signed 64-bit integer (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.

	.. classmethod:: uint64_be(offset=None):

		Reads an unsigned 64-bit integer (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the integer.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`int`
		:returns: The corresponding value.


	.. classmethod:: float32_le(offset=None):

		Reads a 32-bit floating point number (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

	.. classmethod:: float32_be(offset=None):

		Reads a 32-bit floating point number (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

	.. classmethod:: float64_le(offset=None):

		Reads a 64-bit floating point number (little endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.

	.. classmethod:: float64_be(offset=None):

		Reads a 64-bit floating point number (big endian).

		:type offset: :class:`int` or :keyword:`None`
		:param offset: The start of the floating point number.

		:except ValueError: if :attr:`stream` (starting at :attr:`offset` is
							too small.)

		:rtype: :class:`float`
		:returns: The corresponding value.
