:mod:`lf.win.shell.thumbsdb` --- Thumbnail cache (thumbs.db) files
==================================================================

.. module:: lf.win.shell.thumbsdb
   :synopsis: Thumbnail cache (thumbs.db) files
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module contains classes to read Microsoft Windows thumbnail cache
(thumbs.db) files.

.. class:: ThumbsDb(cfb)

	Represents a thumbs.db file.

	:type cfb: :class:`~lf.win.ole.cfb.CompoundFile`
	:param cfb: An OLE compound file that represents the thumbs.db file.

	:raises KeyError: If :attr:`catalog_name` is not found in :attr:`cfb`.

	.. attribute:: catalog

		An instance of a :class:`Catalog` object.

	.. attribute:: thumbnails

		A dictionary of :class:`Thumbnail` objects.  The keys are the numeric
		indices.


.. class:: Thumbnail

	Represents a thumbnail in a thumbs.db file.

	.. attribute:: size

		The total size of the entry.

	.. attribute:: data

		The raw thumbnail data.

	.. classmethod:: from_stream(stream, offset=None):

		Creates a :class:`Thumbnail` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`Thumbnail`
		:returns: The corresponding :class:`Thumbnail` object.


.. class:: Catalog

	Represents the catalog of information in a thumbs.db file.

	.. attribute:: width

		The width (in pixels) of the thumbnails.

	.. attribute:: height

		The height (in pixels) of the thumbnails.

	.. attribute:: item_count

		The number of catalog entries. (extracted)

	.. attribute:: entries

		A list of :class:`CatalogEntry` objects describing the thumbnails.

	.. classmethod:: from_stream(stream, offset=None):

		Creates a :class:`Catalog` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`Catalog`
		:returns: The corresponding :class:`Catalog` object.


.. class:: CatalogEntry

	Represents an entry in a :class:`Catalog`.

	.. attribute:: size

		The total size of the catalog entry.

	.. attribute:: id

		The numeric identifier of the thumbnail, used to determine the
		corresponding stream name.  Sometimes called the index.

	.. attribute:: mtime

		The time the thumbnail was last modified.

	.. attribute:: file_name

		The name of the file the thumbnail is associated with.

	.. attribute:: stream_name

		The name of the corresponding OLE stream. (computed)

	.. classmethod:: from_stream(stream, offset=None):

		Creates a :class:`CatalogEntry` object from a stream.

		:type stream: :class:`~lf.dec.IStream`
		:param stream: A stream that contains the structure.

		:type offset: ``int``
		:param offset: The start of the structure in :attr:`stream`.

		:rtype: :class:`CatalogEntry`
		:returns: The corresponding :class:`CatalogEntry` object.
