:mod:`lf.win.codepage` --- Microsoft Windows OEM code pages 720 and 858
=======================================================================

.. module:: lf.win.codepage
   :synopsis: Adds support for Microsoft Windows OEM code pages 720 and 858.
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

The Python standard library does not provide support for Microsoft Windows OEM
code pages 720 and 858.  This package adds supports for these two code pages.

.. note::

	Importing this module does not automatically register the new codecs with
	the global (system) :mod:`codec` registry.  To do this, call the
	:func:`add_codecs` function.


.. function:: add_codecs()

	Adds the cp720 and cp858 codecs to the global codec registry.

.. function:: search_function(encoding_name)

	Passed to :func:`codecs.register` to locate cp720 and cp858 codecs.

	:type encoding_name: str
	:param encoding_name: The name of the encoding.

	:rtype: :class:`CodecInfo`
	:returns: A :class:`CodecInfo` object describing code pages 720 or 858.
