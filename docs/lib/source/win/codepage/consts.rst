:mod:`lf.win.codepage.consts` --- Code page constants
=====================================================

.. module:: lf.win.codepage.consts
   :synopsis: Constants when working with code pages.
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

Microsoft Windows defines several code page constants.  For convenience, those
constants have been defined in this module.  In addition, the
:data:`code_page_names` attribute contains a mapping between the constant
values and the Python :mod:`codecs` encoding name.

.. data:: code_page_names

	A dictionary mapping Microsoft Windows OEM code page values to their
	equivalent :mod:`codecs` encoding name.

.. data:: CP_UNKNOWN

	Constant when the code page is unknown.


Windows OEM code pages
----------------------

.. data:: CP_WINUNICODE

	Constant for Windows Unicode (16-bit little endian).

.. data:: CP_OEM_437

	Constant for code page 437 (US).

.. data:: CP_OEM_720

	Constant for code page 720 (Arabic).

.. data:: CP_OEM_737

	Constant for code page 737 (Greek).

.. data:: CP_OEM_775

	Constant for code page 775 (Baltic).

.. data:: CP_OEM_850

	Constant for code page 850 (Multilingual Latin I).

.. data:: CP_OEM_852

	Constant for code page 852 (Latin II).

.. data:: CP_OEM_855

	Constant for code page 855 (Cyrillic).

.. data:: CP_OEM_857

	Constant for code page 857 (Turkish).

.. data:: CP_OEM_858

	Constant for code page 858 (Mulitlingual Latin I + Euro).

.. data:: CP_OEM_862

	Constant for code page 862 (Hebrew).

.. data:: CP_OEM_866

	Constant for code page 866 (Russian).


Windows OEM and ANSI code pages
-------------------------------

.. data:: CP_WINDOWS_874

	Constant for code page 874 (Thai).

.. data:: CP_WINDOWS_932

	Constant for code page 932 (Japanese Shift-JIS).

.. data:: CP_WINDOWS_936

	Constant for code page 936 (Simplified Chinese GBK).

.. data:: CP_WINDOWS_949

	Constant for code page 949 (Korean).

.. data:: CP_WINDOWS_950

	Constant for code page 950 (Traditional Chinese Big5).

.. data:: CP_WINDOWS_1258

	Constant for code page 1258 (Vietnam).


Single Byte Character Set code pages (SBCS)
-------------------------------------------
In addition to the code page constants listed below, the constants
:data:`CP_WINDOWS_874` and :data:`CP_WINDOWS_1258` are also single byte
character sets.

.. data:: CP_WINDOWS_1250

	Constant for code page 1250 (Central Europe).

.. data:: CP_WINDOWS_1251

	Constant for code page 1251 (Cyrillic).

.. data:: CP_WINDOWS_1252

	Constant for code page 1252 (Latin I).

.. data:: CP_WINDOWS_1253

	Constant for code page 1253 (Greek).

.. data:: CP_WINDOWS_1254

	Constant for code page 1254 (Turkish).

.. data:: CP_WINDOWS_1255

	Constant for code page 1255 (Hebrew).

.. data:: CP_WINDOWS_1256

	Constant for code page 1256 (Arabic).

.. data:: CP_WINDOWS_1257

	Constant for code page 1257 (Baltic).

.. data:: CP_WINDOWS_UTF8

	Constant for code page 1258 (UTF-8)

Double Byte Character Set code pages (DBCS)
-------------------------------------------

	* :data:`CP_WINDOWS_932` (Japanese Shift-JIS)
	* :data:`CP_WINDOWS_936` (Simplified Chinese GBK)
	* :data:`CP_WINDOWS_949` (Korean)
	* :data:`CP_WINDOWS_950` (Traditional Chinese Big5)


ISO 88559 code pages
--------------------

.. data:: CP_ISO_8859_1

	Constant for code page ISO-8859-1 (Latin 1).

.. data:: CP_ISO_8859_2

	Constant for code page ISO-8859-2 (Latin 2).

.. data:: CP_ISO_8859_3

	Constant for code page ISO-8859-3 (Latin 3).

.. data:: CP_ISO_8859_4

	Constant for code page ISO-8859-4 (Baltic).

.. data:: CP_ISO_8859_5

	Constant for code page ISO-8859-5 (Cyrillic).

.. data:: CP_ISO_8859_6

	Constant for code page ISO-8859-6 (Arabic).

.. data:: CP_ISO_8859_8

	Constant for code page ISO-8859-8 (Hebrew).

.. data:: CP_ISO_8859_9

	Constant for code page ISO-8859-9 (Turkish).

.. data:: CP_ISO_8859_15

	Constant for code page ISO-8859-15 (Latin 9).
