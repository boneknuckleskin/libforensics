:mod:`lf.win.dtypes` --- Common data types for Microsoft Windows artifacts
==========================================================================

.. module:: lf.win.dtypes
   :synopsis: Commmon data types for Microsoft Windows artifacts
.. moduleauthor:: Michael Murr <mmurr@codeforensics.net>

This module provides support for several data types that are common to multiple
Microsoft Windows artifacts.

Native data types
-----------------
The following data types inherit from :class:`lf.dtypes.Native`.

.. class:: BYTE
.. class:: CHAR
.. class:: DOUBLE
.. class:: DWORD
.. class:: DWORD32
.. class:: DWORD64
.. class:: DWORDLONG
.. class:: FILETIME
.. class:: HFILE
.. class:: INT
.. class:: INT8
.. class:: INT16
.. class:: INT32
.. class:: INT64
.. class:: LARGE_INTEGER
.. class:: LONG
.. class:: LONG32
.. class:: LONG64
.. class:: LONGLONG
.. class:: POINTER_32
.. class:: POINTER_64
.. class:: REAL
.. class:: REAL32
.. class:: SHORT
.. class:: UCHAR
.. class:: UINT
.. class:: UINT8
.. class:: UINT16
.. class:: UINT32
.. class:: UINT64
.. class:: ULONG
.. class:: ULONG32
.. class:: ULONG64
.. class:: ULONGLONG
.. class:: UNSIGNED32
.. class:: UNSIGNED64
.. class:: USHORT
.. class:: UTIME
.. class:: WCHAR
.. class:: WORD
.. class:: QWORD
.. class:: SHORT
.. class:: ATOM
.. class:: ATTRIBUTE_TYPE_CODE
.. class:: BOOLEAN
.. class:: COLORREF
.. class:: CURRENCY
.. class:: DATE
.. class:: HRESULT
.. class:: LANGID
.. class:: LCN
.. class:: LGRPID
.. class:: USN
.. class:: VARIANT_BOOL
.. class:: VCN

Record data types
-----------------
The following data types inherit from :class:`lf.dtypes.Record`.

.. class:: GUID_LE
.. class:: GUID_BE
.. class:: CLSID_LE
.. class:: CLSID_BE
.. class:: LCID_LE
.. class:: LCID_BE
.. class:: FILETIME_LE
.. class:: FILETIME_BE
.. class:: HRESULT_LE
.. class:: HRESULT_BE
.. class:: DECIMAL_LE
.. class:: DECIMAL_BE

