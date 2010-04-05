# Copyright 2010 Michael Murr
#
# This file is part of LibForensics.
#
# LibForensics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibForensics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with LibForensics.  If not, see <http://www.gnu.org/licenses/>.

"""Unit tests for the lf.win.ole.ps.objects module."""

# stdlib imports
import codecs
import os.path
from unittest import TestCase, main
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from itertools import chain

# local imports
from lf.dec import RawIStream, ByteIStream, SEEK_SET
from lf.time import FILETIMETodatetime
from lf.win import ctypes as win_ctypes
from lf.win.codepage.consts import CP_WINUNICODE
from lf.win.ole.cfb import CompoundFile
from lf.win.ole import varenum
from lf.win.ole.ps.ctypes import (
    typed_property_value_header, typed_property_value_vt_i2,
    typed_property_value_vt_r4, typed_property_value_vt_r8,
    typed_property_value_vt_cy, typed_property_value_vt_date,
    typed_property_value_vt_error, typed_property_value_vt_ui2,
    typed_property_value_vt_decimal, typed_property_value_vt_i1,
    typed_property_value_vt_ui1, typed_property_value_vt_ui4,
    typed_property_value_vt_i8, typed_property_value_vt_ui8,
    typed_property_value_vt_i4, typed_property_value_vt_filetime,
    typed_property_value_vt_clsid
)
from lf.win.ole.ps.objects import (
    PropertySetStreamHeader, DictionaryEntry, PropertySetHeader, Dictionary,
    CURRENCY, DATE, CodePageString, DECIMAL, UnicodeString, FILETIME, BLOB,
    IndirectPropertyName, ClipboardData, GUID, VersionedStream, HRESULT, Array,
    Vector,

    VT_EMPTY, VT_NULL, VT_I2, VT_I4, VT_R4, VT_R8, VT_CY, VT_DATE, VT_LPSTR,
    VT_ERROR, VT_BOOL, VT_UI2, VT_DECIMAL, VT_I1, VT_UI1, VT_UI4, VT_I8,
    VT_UI8, VT_INT, VT_UINT, VT_BSTR, VT_LPWSTR, VT_I4, VT_FILETIME, VT_BLOB,
    VT_STREAM, VT_STORAGE, VT_STREAMED_OBJECT, VT_STORED_OBJECT,
    VT_BLOB_OBJECT, VT_CF, VT_CLSID, VT_VERSIONED_STREAM,

    Sequence, VT_ARRAY, VT_VECTOR, PropertyFactory,
    Builder
)

__docformat__ = "restructuredtexten"
__all__ = [
    "PropertySetStreamHeaderTestCase", "PropertySetHeaderTestCase",
    "DictionaryEntryTestCase", "CURRENCYTestCase", "DATETestCase",
    "CodePageStringTestCase", "DECIMALTestCase", "UnicodeStringTestCase",
    "FILETIMETestCase", "BLOBTestCase", "IndirectPropertyNameTestCase",
    "ClipboardDataTestCase", "GUIDTestCase", "VersionedStreamTestCase",
    "HRESULTTestCase", "ArrayTestCase", "VectorTestCase", "SequenceTestCase",
    "VT_EMPTYTestCase", "VT_NULLTestCase", "VT_I2TestCase", "VT_I4TestCase",
    "VT_R4TestCase", "VT_R8TestCase", "VT_CYTestCase", "VT_DATETestCase",
    "VT_LPSTRTestCase", "VT_ERRORTestCase", "VT_BOOLTestCase",
    "VT_DECIMALTestCase", "VT_I1TestCase", "VT_UI1TestCase", "VT_UI2TestCase",
    "VT_UI4TestCase", "VT_I8TestCase", "VT_UI8TestCase", "VT_INTTestCase",
    "VT_UINTTestCase", "VT_BSTRTestCase", "VT_LPWSTRTestCase",
    "VT_FILETIMETestCase", "VT_BLOBTestCase", "VT_STREAMTestCase",
    "VT_STORAGETestCase", "VT_STREAMED_OBJECTTestCase",
    "VT_STORED_OBJECTTestCase", "VT_BLOB_OBJECTTestCase", "VT_CFTestCase",
    "VT_CLSIDTestCase", "VT_VERSIONED_STREAMTestCase", "VT_ARRAYTestCase",
    "VT_VECTORTestCase", "PropertyFactoryTestCase", "BuilderTestCase"
]

class PropertySetStreamHeaderTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data0 = bytearray([x for x in range(48)])
        data1 = bytes([x for x in range(68)])

        data0[24:28] = b"\x01\x00\x00\x00"

        pss0 = PropertySetStreamHeader.from_stream(ByteIStream(data0))
        pss1 = PropertySetStreamHeader.from_stream(ByteIStream(data1))

        ae(pss0.byte_order, 0x0100)
        ae(pss1.byte_order, 0x0100)

        ae(pss0.version, 0x0302)
        ae(pss1.version, 0x0302)

        ae(pss0.sys_id, b"\x04\x05\x06\x07")
        ae(pss1.sys_id, b"\x04\x05\x06\x07")

        clsid = UUID(
            bytes_le =
            b"\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17"
        )

        ae(pss0.clsid, clsid)
        ae(pss1.clsid, clsid)

        ae(pss0.property_set_count, 1)
        ae(pss1.property_set_count, 0x1B1A1918)

        fmtid0 = UUID(
            bytes_le =
            b"\x1C\x1D\x1E\x1F\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B"
        )

        ae(pss0.fmtid0, fmtid0)
        ae(pss1.fmtid0, fmtid0)

        ae(pss0.offset0, 0x2F2E2D2C)
        ae(pss1.offset0, 0x2F2E2D2C)

        fmtid1 = UUID(
            bytes_le =
            b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F"
        )

        ae(pss0.fmtid1, None)
        ae(pss1.fmtid1, fmtid1)

        ae(pss0.offset1, None)
        ae(pss1.offset1, 0x43424140)
    # end def test_from_stream
# end class PropertySetStreamHeaderTestCase

class PropertySetHeaderTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend([x for x in range(48)])
        data[4:8] = b"\x05\x00\x00\x00"

        stream = ByteIStream(data)
        psh0 = PropertySetHeader.from_stream(stream)
        psh1 = PropertySetHeader.from_stream(stream, 0)

        for psh in (psh0, psh1):
            ae(psh.size, 0x03020100)
            ae(psh.pair_count, 5)
            ae(len(psh.pids_offsets), 5)
            ae(psh.pids_offsets[0x0B0A0908], 0x0F0E0D0C)
            ae(psh.pids_offsets[0x13121110], 0x17161514)
            ae(psh.pids_offsets[0x1B1A1918], 0x1F1E1D1C)
            ae(psh.pids_offsets[0x23222120], 0x27262524)
            ae(psh.pids_offsets[0x2B2A2928], 0x2F2E2D2C)
        # end for
    # end def test_from_stream
# end class PropertySetHeaderTestCase

class DictionaryEntryTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray([x for x in range(64)])
        data[4:8] = b"\x13\x00\x00\x00"
        stream = ByteIStream(data)

        de = DictionaryEntry.from_stream(stream, 0)
        ae(de.size, 27)
        ae(de.pid, 0x03020100)
        ae(de.name, data[8:27])
        ae(de.name, de.value)

        de = DictionaryEntry.from_stream(stream, 0, code_page=CP_WINUNICODE)
        ae(de.size, 48)
        ae(de.pid, 0x03020100)
        ae(de.name, data[8:46])

        de = DictionaryEntry.from_stream(stream, 0, decoder=decoder)
        ae(de.size, 27)
        ae(de.pid, 0x03020100)
        ae(de.name, decoder(data[8:27], "ignore")[0])

        de = DictionaryEntry.from_stream(stream, 0, CP_WINUNICODE, decoder)
        ae(de.size, 48)
        ae(de.pid, 0x03020100)
        ae(de.name, decoder(data[8:46])[0])

        data[10:12] = b"\x00\x00"
        stream = ByteIStream(data)

        de = DictionaryEntry.from_stream(stream, 0, CP_WINUNICODE, decoder)
        ae(de.size, 48)
        ae(de.pid, 0x03020100)
        ae(de.name, "\u0908")
    # end def test_from_stream
# end class DictionaryEntryTestCase

class DictionaryTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        entry0 = bytearray()
        entry0.extend(b"\x00\x00\x00\x00")  # pid
        entry0.extend(b"\x03\x00\x00\x00")  # size
        entry0.extend(b"a\x00b")  # string

        entry1 = bytearray()
        entry1.extend(b"\x01\x01\x01\x01")  # pid
        entry1.extend(b"\x02\x00\x00\x00")  # size
        entry1.extend(b"a\x00") # string

        entry2 = bytearray()
        entry2.extend(b"\x02\x02\x02\x02")  # pid
        entry2.extend(b"\x01\x00\x00\x00")  # size
        entry2.extend(b"\xFF")

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # count
        data.extend(entry0)
        data.extend(entry1)
        data.extend(entry2)

        stream = ByteIStream(data)
        stream.seek(10, SEEK_SET)

        dictionary = Dictionary.from_stream(stream, 0)
        mapping = dictionary.mapping

        ae(dictionary.size, 36)
        ae(dictionary.property_count, 3)
        ae(len(mapping), 3)
        ae(mapping[0], b"a\x00b")
        ae(mapping[0x01010101], b"a\x00")
        ae(mapping[0x02020202], b"\xFF")

        dictionary = Dictionary.from_stream(stream, 0, decoder=decoder)
        mapping = dictionary.mapping

        ae(dictionary.size, 36)
        ae(len(mapping), 3)
        ae(mapping[0], "a")
        ae(mapping[0x01010101], "a")
        ae(mapping[0x02020202], b"\xFF")


        entry0 = bytearray()
        entry0.extend(b"\x00\x00\x00\x00")  # pid
        entry0.extend(b"\x03\x00\x00\x00")  # size
        entry0.extend(b"a\x00b\x00c\x00\x01\x02")  # string

        entry1 = bytearray()
        entry1.extend(b"\x01\x01\x01\x01")  # pid
        entry1.extend(b"\x03\x00\x00\x00")  # size
        entry1.extend(b"a\x00b\x00c\x00\x00\x00")  # string

        entry2 = bytearray()
        entry2.extend(b"\x02\x02\x02\x02") # pid
        entry2.extend(b"\x03\x00\x00\x00") # size
        entry2.extend(b"a\x00\x00\x00b\x00c\x00")  # string

        entry3 = bytearray()
        entry3.extend(b"\x03\x03\x03\x03")  # pid
        entry3.extend(b"\x04\x00\x00\x00")  # size
        entry3.extend(b"a\x00b\x00c\x00\x00\x00")  # string

        entry4 = bytearray()
        entry4.extend(b"\x04\x04\x04\x04")  # pid
        entry4.extend(b"\x04\x00\x00\x00")  # size
        entry4.extend(b"a\x00b\x00c\x00d\x00")  # string

        data = bytearray()
        data.extend(b"\x05\x00\x00\x00")  # count
        data.extend(entry0)
        data.extend(entry1)
        data.extend(entry2)
        data.extend(entry3)
        data.extend(entry4)

        stream = ByteIStream(data)
        stream.seek(10, SEEK_SET)

        dictionary = Dictionary.from_stream(stream, 0, CP_WINUNICODE)
        mapping = dictionary.mapping

        ae(dictionary.size, 84)
        ae(dictionary.property_count, 5)
        ae(len(mapping), 5)
        ae(mapping[0], b"a\x00b\x00c\x00")
        ae(mapping[0x01010101], b"a\x00b\x00c\00")
        ae(mapping[0x02020202], b"a\x00\x00\x00b\x00")
        ae(mapping[0x03030303], b"a\x00b\x00c\x00\x00\x00")
        ae(mapping[0x04040404], b"a\x00b\x00c\x00d\x00")

        dictionary = Dictionary.from_stream(stream, 0, CP_WINUNICODE, decoder)
        mapping = dictionary.mapping

        ae(dictionary.size, 84)
        ae(dictionary.property_count, 5)
        ae(len(mapping), 5)
        ae(mapping[0], "abc")
        ae(mapping[0x01010101], "abc")
        ae(mapping[0x02020202], "a")
        ae(mapping[0x03030303], "abc")
        ae(mapping[0x04040404], "abcd")
    # end def test_from_stream
# end class DictionaryTestCase

class CURRENCYTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = b"\xA8\xF2\x50\x00\x00\x00\x00\x00"

        stream = ByteIStream(data)
        curr0 = CURRENCY.from_stream(stream)
        curr1 = CURRENCY.from_stream(stream, 0)

        for curr in (curr0, curr1):
            ae(curr.value, Decimal("530.5000"))
            ae(curr.size, 8)
        # end for
    # end def test_from_stream
# end class CURRENCYTESTCase

class DATETestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = b"\x00\x00\x00\x00\x00\x00\x0A\x40"

        stream = ByteIStream(data)
        date0 = DATE.from_stream(stream)
        date1 = DATE.from_stream(stream, 0)

        for date in (date0, date1):
            ae(date.value, datetime(1900, 1, 2, 6, 0, 0))
            ae(date.size, 8)
        # end for
    # end def test_from_stream
# end class DATETestCase

class CodePageStringTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\xFF")  # characters
        stream = ByteIStream(data)

        cps = CodePageString.from_stream(stream)
        ae(cps.value, b"\x01\x02\x03")
        ae(cps.size, 8)


        data = bytearray()
        data.extend(b"\xAA")  # padding
        data.extend(b"\x02\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\x04")  # characters
        stream = ByteIStream(data)

        cps = CodePageString.from_stream(stream, 1, decoder)
        ae(cps.value, "\u0201")
        ae(cps.size, 8)


        data = bytearray()
        data.extend(b"\xBB")  # padding
        data.extend(b"\x06\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        cps = CodePageString.from_stream(stream, 1, decoder)
        ae(cps.value, "a\x00b")
        ae(cps.size, 12)
    # end def test_from_stream
# end class CodePageStringTestCase

class DECIMALTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data0 = bytearray()
        data0.extend(b"\xFF\xFF")  # reserved
        data0.extend(b"\x03")  # scale
        data0.extend(b"\x00")  # sign
        data0.extend(b"\x34\xA8\x23\x08")  # hi32
        data0.extend(b"\x00\x53\x64\xFF\x3E\xAB\x45\x80")  # lo64
        stream = ByteIStream(data0)

        dec = DECIMAL.from_stream(stream)
        ae(dec.size, 16)
        ae(dec.value, Decimal("2518986808300068601514447.616"))


        data1 = bytearray()
        data1.extend(b"\x01")  # padding
        data1.extend(b"\xFF\xFF")  # reserved
        data1.extend(b"\x03")  # scale
        data1.extend(b"\x80")  # sign
        data1.extend(b"\x34\xA8\x23\x08")  # hi32
        data1.extend(b"\x00\x53\x64\xFF\x3E\xAB\x45\x80")  # lo64
        stream = ByteIStream(data1)

        dec = DECIMAL.from_stream(stream, 1)
        ae(dec.size, 16)
        ae(dec.value, Decimal("-2518986808300068601514447.616"))
    # end def test_from_stream
# end class DECIMALTestCase

class UnicodeStringTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        us = UnicodeString.from_stream(stream)
        ae(us.size, 12)
        ae(us.value, "abc")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00\x00\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        us = UnicodeString.from_stream(stream, 1)
        ae(us.size, 12)
        ae(us.value, "ab\x00")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        us = UnicodeString.from_stream(stream, 1)
        ae(us.size, 12)
        ae(us.value, "a\x00b")
    # end def test_from_stream
# end class UnicodeStringTestCase

class FILETIMETestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        stream = ByteIStream(b"\xFF\x00\x0E\x15\x91\xC4\x95\xC2\x01")
        filetime = FILETIME.from_stream(stream, 1)

        ae(filetime.size, 8)
        ae(filetime.value, datetime(2002, 11, 27, 3, 25, 0))


        stream = ByteIStream(b"\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF")
        filetime = FILETIME.from_stream(stream, 1)

        ae(filetime.size, 8)
        ae(filetime.value, 0xFFFFFFFFFFFFFFFF)
    # end def test_from_stream
# end class FILETIMETestCase

class BLOBTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\x04")  # bytes
        stream = ByteIStream(data)

        blob0 = BLOB.from_stream(stream)
        blob1 = BLOB.from_stream(stream, 0)

        for blob in (blob0, blob1):
            ae(blob.size, 8)
            ae(blob.value, b"\x01\x02\x03")
        # end for
    # end def test_from_stream
# end class BLOBTestCase

class IndirectPropertyNameTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\xFF")  # characters
        stream = ByteIStream(data)

        cps = IndirectPropertyName.from_stream(stream)
        ae(cps.value, b"\x01\x02\x03")
        ae(cps.size, 8)


        data = bytearray()
        data.extend(b"\xAA")  # padding
        data.extend(b"\x02\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\x04")  # characters
        stream = ByteIStream(data)

        cps = IndirectPropertyName.from_stream(stream, 1, decoder)
        ae(cps.value, "\u0201")
        ae(cps.size, 8)


        data = bytearray()
        data.extend(b"\xBB")  # padding
        data.extend(b"\x06\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        cps = IndirectPropertyName.from_stream(stream, 1, decoder)
        ae(cps.value, "a\x00b")
        ae(cps.size, 12)
    # end def test_from_stream
# end class IndirectPropertyNameTestCase

class ClipboardDataTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x07\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\x04")  # format
        data.extend(b"\x05\x06\x07\x08")  # data
        stream = ByteIStream(data)

        cd0 = ClipboardData.from_stream(stream)
        cd1 = ClipboardData.from_stream(stream, 0)

        for cd in (cd0, cd1):
            ae(cd.size, 12)
            ae(cd.format, b"\x01\x02\x03\x04")
            ae(cd.data, b"\x05\x06\x07")
        # end for
    # end def test_from_stream
# end class ClipboardDataTestCase

class GUIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend([x for x in range(16)])
        stream = ByteIStream(data)

        guid0 = GUID.from_stream(stream)
        guid1 = GUID.from_stream(stream, 0)

        for guid in (guid0, guid1):
            ae(guid.size, 16)
            ae(guid.value, UUID(bytes_le=data))
        # end for
    # end def test_from_stream
# end class GUIDTestCase

class VersionedStreamTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend([x for x in range(16)])  # version guid
        data.extend(b"\x06\x00\x00\x00")  # stream name (size)
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # stream name (string)
        stream = ByteIStream(data)

        vs = VersionedStream.from_stream(stream)
        ae(vs.size, 28)
        ae(vs.version_guid, UUID(bytes_le=bytes([x for x in range(16)])))
        ae(vs.stream_name, b"a\x00b\x00c\x00")
        ae(vs.value, b"a\x00b\x00c\x00")

        vs = VersionedStream.from_stream(stream, 0, decoder)
        ae(vs.size, 28)
        ae(vs.version_guid, UUID(bytes_le=bytes([x for x in range(16)])))
        ae(vs.stream_name, "abc")
        ae(vs.value, "abc")


        data[20:] = b"a\x00\x00\x00b\x00\xFF\xFF"
        stream = ByteIStream(data)

        vs = VersionedStream.from_stream(stream, 0, decoder)
        ae(vs.size, 28)
        ae(vs.version_guid, UUID(bytes_le=bytes([x for x in range(16)])))
        ae(vs.stream_name, "a\x00b")
        ae(vs.value, "a\x00b")
    # end def test_from_stream
# end class VersionedStreamTestCase

class HRESULTTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = b"\xBD\x42\x57\xAE"
        hresult = HRESULT.from_stream(ByteIStream(data))

        ae(hresult.size, 4)
        ae(hresult.value.s, 1)
        ae(hresult.value.r, 0)
        ae(hresult.value.c, 1)
        ae(hresult.value.n, 0)
        ae(hresult.value.x, 1)
        ae(hresult.value.facility, 0x0657)
        ae(hresult.value.code, 0x42BD)


        data = b"\x00\xBD\x42\x57\x56"
        hresult = HRESULT.from_stream(ByteIStream(data), 1)

        ae(hresult.size, 4)
        ae(hresult.value.s, 0)
        ae(hresult.value.r, 1)
        ae(hresult.value.c, 0)
        ae(hresult.value.n, 1)
        ae(hresult.value.x, 0)
        ae(hresult.value.facility, 0x0657)
        ae(hresult.value.code, 0x42BD)
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        hresult = win_ctypes.hresult_le.from_buffer_copy(b"\xBD\x42\x57\xAE")
        hresult = HRESULT.from_ctype(hresult)

        ae(hresult.size, 4)
        ae(hresult.value.s, 1)
        ae(hresult.value.r, 0)
        ae(hresult.value.c, 1)
        ae(hresult.value.n, 0)
        ae(hresult.value.x, 1)
        ae(hresult.value.facility, 0x0657)
        ae(hresult.value.code, 0x42BD)

        hresult = win_ctypes.hresult_le.from_buffer_copy(b"\xBD\x42\x57\x56")
        hresult = HRESULT.from_ctype(hresult)

        ae(hresult.size, 4)
        ae(hresult.value.s, 0)
        ae(hresult.value.r, 1)
        ae(hresult.value.c, 0)
        ae(hresult.value.n, 1)
        ae(hresult.value.x, 0)
        ae(hresult.value.facility, 0x0657)
        ae(hresult.value.code, 0x42BD)
    # end def test_from_ctype
# end class HRESULTTestCase

class ArrayTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x02\x00\x00\x00\x03\x00\x00\x00") # type (VT_I2) / count
        data.extend(b"\x03\x00\x00\x00\x07\x00\x00\x00") # dimension 0
        data.extend(b"\x02\x00\x00\x00\x08\x00\x00\x00") # dimension 1
        data.extend(b"\x01\x00\x00\x00\x09\x00\x00\x00") # dimension 2

        data.extend(b"\x00\x00") # element 0
        data.extend(b"\x01\x00") # element 1
        data.extend(b"\x02\x00") # element 2
        data.extend(b"\x03\x00") # element 3
        data.extend(b"\x04\x00") # element 4
        data.extend(b"\x05\x00") # element 5

        stream = ByteIStream(data)
        array0 = Array.from_stream(stream)
        array1 = Array.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.size, 44)
            ae(array.value, [0, 1, 2, 3, 4, 5])
            ae(array.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(array.scalar_type, 2)
            ae(array.dimension_count, 3)
        # end for


        stream = ByteIStream(data[:-2])
        array0 = Array.from_stream(stream)
        array1 = Array.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.size, 44)
            ae(array.value, [0, 1, 2, 3, 4])
            ae(array.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(array.scalar_type, 2)
            ae(array.dimension_count, 3)
        # end for


        stream = ByteIStream(data[:-1])
        array0 = Array.from_stream(stream)
        array1 = Array.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.size, 44)
            ae(array.value, [0, 1, 2, 3, 4])
            ae(array.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(array.scalar_type, 2)
            ae(array.dimension_count, 3)
        # end for


        data = bytearray()
        data.extend(b"\x0C\x00\x00\x00")  # scalar type
        data.extend(b"\x03\x00\x00\x00")  # dimension count
        data.extend(b"\x03\x00\x00\x00\x07\x00\x00\x00")  # dimension 0
        data.extend(b"\x01\x00\x00\x00\x08\x00\x00\x00")  # dimension 1
        data.extend(b"\x00\x00\x00\x00\x09\x00\x00\x00")  # dimension 2

        data.extend(b"\x08\x00\x64\x53")  # element 0 - VT_BSTR
        data.extend(b"\x06\x00\x00\x00")  # size of data field
        data.extend(b"a\x00\x00\x00b\x00\x64\x53")  # data (incl, padding)

        data.extend(b"\x00\x00\x64\x53")  # element 1 - VT_NULL

        data.extend(b"\x12\x00\x64\x53")  # element 2 - VT_UI2
        data.extend(b"\xFE\xFF\x64\x53")  # data (incl. padding)

        stream = ByteIStream(data)
        value = [
            VT_BSTR((8, 16, b"a\x00\x00\x00b\x00")),
            VT_EMPTY((0, 4, None)),
            VT_UI2((18, 8, 0xFFFE))
        ]

        array0 = Array.from_stream(stream)
        array1 = Array.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.size, 60)
            ae(array.value, value)
            ae(array.scalar_type, 0xC)
            ae(array.dimensions, [(3, 7), (1, 8), (0, 9)])
            ae(array.dimension_count, 3)
        # end for

        stream = ByteIStream(data[:-3])
        value[0] = VT_BSTR((8, 16, "a\x00b"))
        value = value[:-1]
        array0 = Array.from_stream(stream, decoder=decoder)
        array1 = Array.from_stream(stream, 0, decoder)

        for array in (array0, array1):
            ae(array.size, 52)
            ae(array.value, value)
            ae(array.scalar_type, 0xC)
            ae(array.dimensions, [(3, 7), (1, 8), (0, 9)])
            ae(array.dimension_count, 3)
        # end for
    # end def test_from_stream
# end class ArrayTestCase

class VectorTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x05\x00\x00\x00")  # length

        data.extend(b"\x00\x00") # element 0
        data.extend(b"\x01\x00") # element 1
        data.extend(b"\x02\x00") # element 2
        data.extend(b"\x03\x00") # element 3
        data.extend(b"\x04\x00") # element 4

        stream = ByteIStream(data)
        vector0 = Vector.from_stream(stream, 2)
        vector1 = Vector.from_stream(stream, 2, 0)

        for vector in (vector0, vector1):
            ae(vector.size, 16)
            ae(vector.value, [0, 1, 2, 3, 4])
            ae(vector.scalar_count, 5)
        # end for


        stream = ByteIStream(data[:-2])
        vector0 = Vector.from_stream(stream, 2)
        vector1 = Vector.from_stream(stream, 2, 0)

        for vector in (vector0, vector1):
            ae(vector.size, 12)
            ae(vector.value, [0, 1, 2, 3])
            ae(vector.scalar_count, 5)
        # end for


        stream = ByteIStream(data[:-1])
        vector0 = Vector.from_stream(stream, 2)
        vector1 = Vector.from_stream(stream, 2, 0)

        for vector in (vector0, vector1):
            ae(vector.size, 12)
            ae(vector.value, [0, 1, 2, 3])
            ae(vector.scalar_count, 5)
        # end for


        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # length

        data.extend(b"\x08\x00\x64\x53")  # element 0 - VT_BSTR
        data.extend(b"\x06\x00\x00\x00")  # size of data field
        data.extend(b"a\x00\x00\x00b\x00\x64\x53")  # data (incl, padding)

        data.extend(b"\x00\x00\x64\x53")  # element 1 - VT_NULL

        data.extend(b"\x12\x00\x64\x53")  # element 2 - VT_UI2
        data.extend(b"\xFE\xFF\x64\x53")  # data (incl. padding)

        stream = ByteIStream(data)
        value = [
            VT_BSTR((8, 16, b"a\x00\x00\x00b\x00")),
            VT_EMPTY((0, 4, None)),
            VT_UI2((18, 8, 0xFFFE))
        ]

        vector0 = Vector.from_stream(stream, 0xC)
        vector1 = Vector.from_stream(stream, 0xC, 0)

        for vector in (vector0, vector1):
            ae(vector.size, 32)
            ae(vector.value, value)
            ae(vector.scalar_count, 3)
        # end for

        stream = ByteIStream(data[:-3])
        value[0] = VT_BSTR((8, 16, "a\x00b"))
        value = value[:-1]
        vector0 = Vector.from_stream(stream, 0xC, decoder=decoder)
        vector1 = Vector.from_stream(stream, 0xC, 0, decoder)

        for vector in (vector0, vector1):
            ae(vector.size, 24)
            ae(vector.value, value)
            ae(vector.scalar_count, 3)
        # end for
    # end def test_from_stream
# end class VectorTestCase

class SequenceTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        ar = self.assertRaises
        from_stream = Sequence.from_stream

        pt = varenum
        decoder = codecs.getdecoder("utf_16_le")

        data = b"\x00\x00\xFF\xFF" * 3
        value = [VT_EMPTY((0, 4, None))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_EMPTY, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        data = b"\x01\x00\xFF\xFF" * 3
        value = [VT_NULL((1, 4, None))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_NULL, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        data = b"\xFF\xFF\xFE\xFF\xFD\xFF"
        value = [-1, -2, -3]
        vp = from_stream(ByteIStream(data), pt.VT_I2, 3)
        ae(vp.size, 8)
        ae(vp.value, value)


        data = b"\xFF\xFF\xFF\xFF\xFE\xFF\xFF\xFF\xFD\xFF\xFF\xFF"
        value = [-1, -2, -3]
        vp = from_stream(ByteIStream(data), pt.VT_I4, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        value = [
            3.140000104904175, 0.6452999711036682, 100.2300033569336
        ]
        data = b"\xC3\xF5\x48\x40\x61\x32\x25\x3F\xC3\x75\xC8\x42"
        vp = from_stream(ByteIStream(data), pt.VT_R4, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\x1F\x85\xEB\x51\xB8\x1E\x09\x40")
        data.extend(b"\x4A\x7B\x83\x2F\x4C\xA6\xE4\x3F")
        data.extend(b"\x1F\x85\xEB\x51\xB8\x0E\x59\x40")
        value = [3.14, 0.6453, 100.23]
        vp = from_stream(ByteIStream(data), pt.VT_R8, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\xA8\xF2\x50\x00\x00\x00\x00\x00")
        data.extend(b"\xA8\xF2\x50\x00\x00\x00\x00\x00")
        data.extend(b"\xA8\xF2\x50\x00\x00\x00\x00\x00")
        value = [CURRENCY.from_stream(ByteIStream(data[:8]), 0)] * 3
        vp = from_stream(ByteIStream(data), pt.VT_CY, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\x00\x00\x00\x00\x00\x00\x0A\x40")
        data.extend(b"\x00\x00\x00\x00\x00\x00\x0A\x40")
        data.extend(b"\x00\x00\x00\x00\x00\x00\x0A\x40")
        value = [DATE.from_stream(ByteIStream(data[:8]))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_DATE, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\x01\x00\x00\x00a\x00\x00\x00")
        data.extend(b"\x01\x00\x00\x00a\x00\x00\x00")
        data.extend(b"\x01\x00\x00\x00a\x00\x00\x00")
        value = [CodePageString.from_stream(ByteIStream(data[:5]))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_BSTR, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")
        data.extend(b"\x00\x01\x02\x03")
        data.extend(b"\x00\x01\x02\x03")
        value = [HRESULT.from_stream(ByteIStream(data[:4]))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_ERROR, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\x00\x01\x00\x01\x00\x01\x00\x01")
        value = [0x100] * 3
        vp = from_stream(ByteIStream(data), pt.VT_BOOL, 3)
        ae(vp.size, 8)
        ae(vp.value, value)


        data = bytearray()
        decimal = bytearray()
        decimal.extend(b"\x64\x53")  # reserved
        decimal.extend(b"\x03")  # scale
        decimal.extend(b"\x00")  # sign
        decimal.extend(b"\x34\xA8\x23\x08")  # hi32
        decimal.extend(b"\x00\x53\x64\xFF\x3E\xAB\x45\x80")  # lo64
        data.extend(decimal * 3)
        value = DECIMAL((16, Decimal("2518986808300068601514447.616")))
        value = [value] * 3
        vp = from_stream(ByteIStream(data), pt.VT_DECIMAL, 3)
        ae(vp.size, 48)
        ae(vp.value, value)


        data = b"\xFF\xFE\xFD"
        value = [-1, -2, -3]
        vp = from_stream(ByteIStream(data), pt.VT_I1, 3)
        ae(vp.size, 4)
        ae(vp.value, value)

        data = b"\xFF\xFE\xFD"
        value = [0xFF, 0xFE, 0xFD]
        vp = from_stream(ByteIStream(data), pt.VT_UI1, 3)
        ae(vp.size, 4)
        ae(vp.value, value)

        data = b"\xFF\xFF\xFE\xFF\xFD\xFF"
        value = [0xFFFF, 0xFFFE, 0xFFFD]
        vp = from_stream(ByteIStream(data), pt.VT_UI2, 3)
        ae(vp.size, 8)
        ae(vp.value, value)


        data = b"\xFF\xFF\xFF\xFF\xFE\xFF\xFF\xFF\xFD\xFF\xFF\xFF"
        value = [0xFFFFFFFF, 0xFFFFFFFE, 0xFFFFFFFD]
        vp = from_stream(ByteIStream(data), pt.VT_UI4, 3)
        ae(vp.size, 12)
        ae(vp.value, value)

        data = b"\xFD\xFF\xFF\xFF\xFF\xFF\xFF\xFF" * 3
        value = [-3, -3, -3]
        vp = from_stream(ByteIStream(data), pt.VT_I8, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\xFD\xFF\xFF\xFF\xFF\xFF\xFF\xFF" * 3
        value = [0xFFFFFFFFFFFFFFFD] * 3
        vp = from_stream(ByteIStream(data), pt.VT_UI8, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\xFD\xFF\xFF\xFF" * 3
        value = [-3] * 3
        vp = from_stream(ByteIStream(data), pt.VT_INT, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        data = b"\xFD\xFF\xFF\xFF" * 3
        value = [0xFFFFFFFD] * 3
        vp = from_stream(ByteIStream(data), pt.VT_UINT, 3)
        ae(vp.size, 12)
        ae(vp.value, value)


        data = b"\x06\x00\x00\x00a\x00\x00\x00b\x00\x00\x00" * 3
        value = [CodePageString((12, "a"))] * 3
        vp = \
            from_stream(ByteIStream(data), pt.VT_LPSTR, 3, decoder=decoder)
        ae(vp.size, 36)
        ae(vp.value, value)


        data = b"\x03\x00\x00\x00a\x00b\x00c\x00\xFF\xFF" * 3
        value = [UnicodeString((12, "abc"))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_LPWSTR, 3)
        ae(vp.size, 36)
        ae(vp.value, value)


        data = b"\x00\x0E\x15\x91\xC4\x95\xC2\x01" * 3
        value = [FILETIME((8, datetime(2002, 11, 27, 3, 25, 0)))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_FILETIME, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x03\x00\x00\x00\x64\x53\x12\x00" * 3
        value = [BLOB((8, b"\x64\x53\x12"))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_BLOB, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x02\x00\x00\x00\x01\x02\x03\x04" * 3
        value = [IndirectPropertyName((8, "\u0201"))] * 3
        vp = \
            from_stream(ByteIStream(data), pt.VT_STREAM, 3, decoder=decoder)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x02\x00\x00\x00\x01\x02\x03\x04" * 3
        value = [IndirectPropertyName((8, "\u0201"))] * 3
        vp = \
            from_stream(ByteIStream(data), pt.VT_STORAGE, 3, decoder=decoder)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x02\x00\x00\x00\x01\x02\x03\x04" * 3
        value = [IndirectPropertyName((8, "\u0201"))] * 3
        vp = from_stream(
            ByteIStream(data), pt.VT_STREAMED_OBJECT, 3, decoder=decoder
        )
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x02\x00\x00\x00\x01\x02\x03\x04" * 3
        value = [IndirectPropertyName((8, "\u0201"))] * 3
        vp = from_stream(
            ByteIStream(data), pt.VT_STORED_OBJECT, 3, decoder=decoder
        )
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x02\x00\x00\x00\x01\x02\x03\x04" * 3
        value = [BLOB((8, b"\x01\x02"))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_BLOB_OBJECT, 3)
        ae(vp.size, 24)
        ae(vp.value, value)


        data = b"\x07\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08" * 3
        value = [
            ClipboardData((12, b"\x05\x06\x07", b"\x01\x02\x03\x04"))
        ] * 3
        vp = from_stream(ByteIStream(data), pt.VT_CF, 3)
        ae(vp.size, 36)
        ae(vp.value, value)


        data = bytes([x for x in range(16)] * 3)
        uuid = UUID(bytes_le=data[:16])
        value = [GUID((16, uuid))] * 3
        vp = from_stream(ByteIStream(data), pt.VT_CLSID, 3)
        ae(vp.size, 48)
        ae(vp.value, value)


        data = bytearray()
        data.extend([x for x in range(16)])  # version guid
        data.extend(b"\x06\x00\x00\x00")  # size of stream name
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # stream name
        data = bytes(data * 3)
        value = [VersionedStream((28, "abc", uuid))] * 3
        vp = from_stream(
            ByteIStream(data), pt.VT_VERSIONED_STREAM, 3, decoder=decoder
        )
        ae(vp.size, 84)
        ae(vp.value, value)


        data = bytearray()
        data.extend(b"\x1E\x00\x64\x53")  # type (VT_LPSTR) and pad
        data.extend(b"\x02\x00\x00\x00\x01\x02\x03\x04")  # size / characters

        data.extend(b"\x01\x00\x64\x53")  # type (VT_NULL) and pad

        data.extend(b"\x02\x00\x64\x53")  # type (VT_I2) and pad
        data.extend(b"\x34\x12\xFF\xFF")  # value / value_pad
        data = bytes(data * 3)
        value = [
            VT_LPSTR((0x1E, 12, "\u0201")),
            VT_NULL((0x01, 4, None)),
            VT_I2((0x02, 8, 0x1234))
        ] * 3
        vp = from_stream(ByteIStream(data), pt.VT_VARIANT, 9, decoder=decoder)
        ae(vp.size, 72)
        ae(vp.value, value)


        ar(ValueError, from_stream, ByteIStream(b""), 0xFFFF, 3)
    # end def test_from_stream
# end class SequenceTestCase

class TPVMixin():
    def test_from_stream(self):
        ae = self.assertEqual

        for tpv in self.tpvs:
            ae(tpv.type, self.tpv_type)
            ae(tpv.size, self.tpv_size)
            ae(tpv.value, self.tpv_value)
        # end for
    # end def test_from_stream
# end class TPVMixin

class VT_EMPTYTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x00\x00")  # type = VT_EMPTY
        data.extend(b"\x64\x53")  # pad
        stream = ByteIStream(data)

        tpv0 = VT_EMPTY.from_stream(stream)
        tpv1 = VT_EMPTY.from_stream(stream, 0)

        self.tpv_value = None
        self.tpv_type = varenum.VT_EMPTY
        self.tpv_size = 4

        self.tpvs = [tpv0, tpv1]
    # end def setUp
# end class VT_EMPTYTestCase

class VT_NULLTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x01\x00")  # type = VT_NULL
        data.extend(b"\x64\x53")  # pad
        stream = ByteIStream(data)

        tpv0 = VT_NULL.from_stream(stream)
        tpv1 = VT_NULL.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = None
        self.tpv_type = varenum.VT_NULL
        self.tpv_size = 4
    # end def setUp
# end class VT_NULLTestCase

class VT_I2TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x02\x00")  # type = VT_I2
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFD\xFF")  # value == -3
        data.extend(b"\x64\x53")  # value padding
        stream = ByteIStream(data)

        tpv0 = VT_I2.from_stream(stream)
        tpv1 = VT_I2.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -3
        self.tpv_type = varenum.VT_I2
        self.tpv_size = 8
    # end def setUp
# end class VT_I2TestCase

class VT_I4TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x03\x00")  # type = VT_I4
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFD\xFF\xFF\xFF")  # value == -3
        stream = ByteIStream(data)

        tpv0 = VT_I4.from_stream(stream)
        tpv1 = VT_I4.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -3
        self.tpv_type = varenum.VT_I4
        self.tpv_size = 8
    # end def setUp
# end class VT_I4TestCase

class VT_R4TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x04\x00")  # type = VT_R4
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xC3\xF5\x48\xC0")  # value == -3.140000104904175
        stream = ByteIStream(data)

        tpv0 = VT_R4.from_stream(stream)
        tpv1 = VT_R4.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -3.140000104904175
        self.tpv_type = varenum.VT_R4
        self.tpv_size = 8
    # end def setUp
# end class VT_R4TestCase

class VT_R8TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x05\x00")  # type = VT_R8
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x1F\x85\xEB\x51\xB8\x1E\x09\xC0")  # value == -3.14
        stream = ByteIStream(data)

        tpv0 = VT_R8.from_stream(stream)
        tpv1 = VT_R8.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -3.14
        self.tpv_type = varenum.VT_R8
        self.tpv_size = 12
    # end def setUp
# end class VT_R8TestCase

class VT_CYTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x06\x00")  # type = VT_CY
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xA8\xF2\x50\x00\x00\x00\x00\x00") # value == 530.500
        stream = ByteIStream(data)

        tpv0 = VT_CY.from_stream(stream)
        tpv1 = VT_CY.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = Decimal("530.500")
        self.tpv_type = varenum.VT_CY
        self.tpv_size = 12
    # end def setUp
# end class VT_CYTestCase

class VT_DATETestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x07\x00")  # type = VT_DATE
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x00\x00\x00\x00\x00\x00\x0A\x40")  # value == 1/2/1900
        stream = ByteIStream(data)

        tpv0 = VT_DATE.from_stream(stream)
        tpv1 = VT_DATE.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = datetime(1900, 1, 2, 6, 0, 0)
        self.tpv_type = varenum.VT_DATE
        self.tpv_size = 12
    # end def setUp
# end class VT_DATETestCase

class VT_LPSTRTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x1E\x00")  # type == VT_LPSTR
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = VT_LPSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_LPSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_LPSTR.from_stream(stream, 0)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = VT_LPSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcd")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = VT_LPSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_LPSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_LPSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = VT_LPSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_LPSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab")
    # end def test_from_stream
# end class VT_LPSTRTestCase

class VT_ERRORTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x0A\x00")  # type == VT_ERROR
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x05\x00\x07\x80")  # value == access denied
        stream = ByteIStream(data)

        error0 = VT_ERROR.from_stream(stream)
        error1 = VT_ERROR.from_stream(stream, 0)

        for error in (error0, error1):
            ae(error.type, varenum.VT_ERROR)
            ae(error.size, 8)
            ae(error.value.s, 1)
            ae(error.value.r, 0)
            ae(error.value.c, 0)
            ae(error.value.n, 0)
            ae(error.value.r, 0)
            ae(error.value.facility, 7)
            ae(error.value.code, 5)
        # end for
    # end def test_from_stream
# end class VT_ERRORTestCase

class VT_BOOLTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x0B\x00")  # type = VT_I4
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x02\x01")  # value == 0x0102
        data.extend(b"\x64\x53")  # pad
        stream = ByteIStream(data)

        tpv0 = VT_BOOL.from_stream(stream)
        tpv1 = VT_BOOL.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = 0x0102
        self.tpv_type = varenum.VT_BOOL
        self.tpv_size = 8
    # end def setUp
# end class VT_BOOLTestCase

class VT_DECIMALTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x0E\x00")  # type = VT_DECIMAL
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFF\xFF")  # reserved
        data.extend(b"\x03")  # scale
        data.extend(b"\x80")  # sign
        data.extend(b"\x34\xA8\x23\x08")  # hi32
        data.extend(b"\x00\x53\x64\xFF\x3E\xAB\x45\x80")  # lo64
        stream = ByteIStream(data)

        tpv0 = VT_DECIMAL.from_stream(stream)
        tpv1 = VT_DECIMAL.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = Decimal("-2518986808300068601514447.616")
        self.tpv_type = varenum.VT_DECIMAL
        self.tpv_size = 20
    # end def setUp
# end class VT_DECIMALTestCase

class VT_I1TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x10\x00")  # type = VT_I1
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFD\xFF\xFF\xFF")  # value == -3
        stream = ByteIStream(data)

        tpv0 = VT_I1.from_stream(stream)
        tpv1 = VT_I1.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -3
        self.tpv_type = varenum.VT_I1
        self.tpv_size = 8
    # end def setUp
# end class VT_I1TestCase

class VT_UI1TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x11\x00")  # type = VT_UI1
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFD\xFF\xFF\xFF")  # value == 0xFD
        stream = ByteIStream(data)

        tpv0 = VT_UI1.from_stream(stream)
        tpv1 = VT_UI1.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = 0xFD
        self.tpv_type = varenum.VT_UI1
        self.tpv_size = 8
    # end def setUp
# end class VT_UI1TestCase

class VT_UI2TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x12\x00")  # type = VT_UI2
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFD\xFF\xFE\xFE")  # value == 0xFFFD
        stream = ByteIStream(data)

        tpv0 = VT_UI2.from_stream(stream)
        tpv1 = VT_UI2.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = 0xFFFD
        self.tpv_type = varenum.VT_UI2
        self.tpv_size = 8
    # end def setUp
# end class VT_UI2TestCase

class VT_UI4TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x13\x00")  # type = VT_UI4
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFF\xFE\xFD\xFC")  # value == 0xFCFDFEFF
        stream = ByteIStream(data)

        tpv0 = VT_UI4.from_stream(stream)
        tpv1 = VT_UI4.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = 0xFCFDFEFF
        self.tpv_type = varenum.VT_UI4
        self.tpv_size = 8
    # end def setUp
# end class VT_UI4TestCase

class VT_I8TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x14\x00")  # type = VT_I8
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8")  # value ==
                                                          # -506097522914230529
        stream = ByteIStream(data)
        tpv0 = VT_I8.from_stream(stream)
        tpv1 = VT_I8.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -506097522914230529
        self.tpv_type = varenum.VT_I8
        self.tpv_size = 12
    # end def setUp
# end class VT_I8TestCase

class VT_UI8TestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x15\x00")  # type = VT_UI8
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8")  # value ==
                                                          # 0xF8F9FAFBFCFDFEFF
        stream = ByteIStream(data)
        tpv0 = VT_UI8.from_stream(stream)
        tpv1 = VT_UI8.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = 0xF8F9FAFBFCFDFEFF
        self.tpv_type = varenum.VT_UI8
        self.tpv_size = 12
    # end def setUp
# end class VT_UI8TestCase

class VT_INTTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x16\x00")  # type = VT_INT
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFD\xFF\xFF\xFF")  # value == -3
        stream = ByteIStream(data)
        tpv0 = VT_INT.from_stream(stream)
        tpv1 = VT_INT.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = -3
        self.tpv_type = varenum.VT_INT
        self.tpv_size = 8
    # end def setUp
# end class VT_INTTestCase

class VT_UINTTestCase(TestCase, TPVMixin):
    def setUp(self):
        data = bytearray()
        data.extend(b"\x17\x00")  # type = VT_UINT
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\xFF\xFE\xFD\xFC")  # value == 0xFCFDFEFF
        stream = ByteIStream(data)
        tpv0 = VT_UINT.from_stream(stream)
        tpv1 = VT_UINT.from_stream(stream, 0)

        self.tpvs = [tpv0, tpv1]
        self.tpv_value = 0xFCFDFEFF
        self.tpv_type = varenum.VT_UINT
        self.tpv_size = 8
    # end def setUp
# end class VT_UINTTestCase

class VT_BSTRTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x08\x00")  # type == VT_BSTR
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = VT_BSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_BSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_BSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = VT_BSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcd\x00")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = VT_BSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_BSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00cd")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_BSTR.from_stream(stream)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = VT_BSTR.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_BSTR)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00c\x00")
    # end def test_from_stream
# end class VT_BSTRTestCase

class VT_LPWSTRTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("ascii")

        data = bytearray()
        data.extend(b"\x1F\x00")  # type
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x05\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)

        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, False)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/default decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "abcde")


        # w/o embedded nulls, w/o null terminator, w/best guess decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, None)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "abcde")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, decoder)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpwstr = VT_LPWSTR.from_stream(stream, 0, False)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/default decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "abcd\x00")


        # w/o embedded nulls, w/null terminator, w/best guess decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, None)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "abcd\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, decoder)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "a\x00b\x00c\x00d\x00\x00\x00")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00d\x00e\x00"
        stream = ByteIStream(data)

        lpwstr = VT_LPWSTR.from_stream(stream, 0, False)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, b"a\x00b\x00\x00\x00d\x00e\x00")


        # w/embedded nulls, w/o null terminator, w/default decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "ab\x00de")


        # w/embedded nulls, w/o null terminator, w/best guess decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, None)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "ab\x00de")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, decoder)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "a\x00b\x00\x00\x00d\x00e\x00")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpwstr = VT_LPWSTR.from_stream(stream, 0, False)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, b"a\x00b\x00\x00\x00d\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/default decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "ab\x00d\x00")


        # w/embedded nulls, w/null terminator, w/best guess decoder
        lpwstr = VT_LPWSTR.from_stream(stream, 0, None)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "ab\x00d\x00")


        # w/embedded nulls, w/null terminator, w/decoder)
        lpwstr = VT_LPWSTR.from_stream(stream, 0, decoder)
        ae(lpwstr.type, varenum.VT_LPWSTR)
        ae(lpwstr.size, 20)
        ae(lpwstr.value, "a\x00b\x00\x00\x00d\x00\x00\x00")
    # end def test_from_stream
# end class VT_LPWSTRTestCase

class VT_FILETIMETestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x40\x00")  # type == VT_FILETIME
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x00\x0E\x15\x91\xC4\x95\xC2\x01")  # value == 11/27/2002
                                                          #          3:25 am
        stream = ByteIStream(data)

        filetime0 = VT_FILETIME.from_stream(stream)
        filetime1 = VT_FILETIME.from_stream(stream, 0)

        for filetime in (filetime0, filetime1):
            ae(filetime.type, varenum.VT_FILETIME)
            ae(filetime.size, 12)
            ae(filetime.value, datetime(2002, 11, 27, 3, 25, 0))
        # end for


        data[4:] = b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        stream = ByteIStream(data)

        filetime0 = VT_FILETIME.from_stream(stream)
        filetime1 = VT_FILETIME.from_stream(stream, 0)

        for filetime in (filetime0, filetime1):
            ae(filetime.type, varenum.VT_FILETIME)
            ae(filetime.size, 12)
            ae(filetime.value, 0xFFFFFFFFFFFFFFFF)
        # end for
    # end def test_from_stream
# end class VT_FILETIMETestCase

class VT_BLOBTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x41\x00")  # type == VT_BLOB
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x02\x00\x00\x00")  # size == 2
        data.extend(b"\xFE\xFC")  # data
        stream = ByteIStream(data)

        blob0 = VT_BLOB.from_stream(stream)
        blob1 = VT_BLOB.from_stream(stream, 0)

        for blob in (blob0, blob1):
            ae(blob.type, varenum.VT_BLOB)
            ae(blob.size, 12)
            ae(blob.value, b"\xFE\xFC")
        # end for
    # end def test_from_stream
# end class VT_BLOBTestCase

class VT_STREAMTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x42\x00")  # type == VT_STREAM
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = VT_STREAM.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STREAM.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STREAM.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STREAM.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcd\x00")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = VT_STREAM.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STREAM.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00cd")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STREAM.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STREAM.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAM)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00c\x00")
    # end def test_from_stream
# end class VT_STREAMTestCase

class VT_STORAGETestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x43\x00")  # type == VT_STORAGE
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = VT_STORAGE.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STORAGE.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STORAGE.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STORAGE.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcd\x00")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = VT_STORAGE.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STORAGE.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00cd")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STORAGE.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STORAGE.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORAGE)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00c\x00")
    # end def test_from_stream
# end class VT_STORAGETestCase

class VT_STREAMED_OBJECTTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x44\x00")  # type == VT_STREAMED_OBJECT
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = VT_STREAMED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STREAMED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STREAMED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STREAMED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcd\x00")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = VT_STREAMED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STREAMED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00cd")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STREAMED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STREAMED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STREAMED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00c\x00")
    # end def test_from_stream
# end class VT_STREAMED_OBJECTTestCase

class VT_STORED_OBJECTTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x45\x00")  # type == VT_STORED_OBJECT
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = VT_STORED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STORED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STORED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STORED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "abcd\x00")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = VT_STORED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = VT_STORED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00cd")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = VT_STORED_OBJECT.from_stream(stream)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = VT_STORED_OBJECT.from_stream(stream, 0, decoder)
        ae(lpstr.type, varenum.VT_STORED_OBJECT)
        ae(lpstr.size, 20)
        ae(lpstr.value, "ab\x00c\x00")
    # end def test_from_stream
# end class VT_STORED_OBJECTTestCase

class VT_BLOB_OBJECTTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x46\x00")  # type == VT_BLOB_OBJECT
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x02\x00\x00\x00")  # size == 2
        data.extend(b"\xFE\xFC")  # data
        stream = ByteIStream(data)

        blob0 = VT_BLOB_OBJECT.from_stream(stream)
        blob1 = VT_BLOB_OBJECT.from_stream(stream, 0)

        for blob in (blob0, blob1):
            ae(blob.type, varenum.VT_BLOB_OBJECT)
            ae(blob.size, 12)
            ae(blob.value, b"\xFE\xFC")
        # end for
    # end def test_from_stream
# end class VT_BLOB_OBJECTTestCase

class VT_CFTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x47\x00")  # type == VT_CF
        data.extend(b"\x64\x53")  # pad
        data.extend(b"\x07\x00\x00\x00")  # size
        data.extend(b"\x01\x02\x03\x04")  # format
        data.extend(b"\x05\x06\x07\x08")  # data
        stream = ByteIStream(data)

        cf0 = VT_CF.from_stream(stream)
        cf1 = VT_CF.from_stream(stream, 0)

        for cf in (cf0, cf1):
            ae(cf.type, varenum.VT_CF)
            ae(cf.size, 16)
            ae(cf.value.size, 12)
            ae(cf.value.format, b"\x01\x02\x03\x04")
            ae(cf.value.data, b"\x05\x06\x07")
            ae(cf.value.value, b"\x05\x06\x07")
        # end for
    # end def test_from_stream
# end class VT_CFTestCase

class VT_CLSIDTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x48\x00")  # type == VT_CLSID
        data.extend(b"\x64\x53")  # pad
        data.extend([x for x in range(16)])  # clsid
        stream = ByteIStream(data)

        clsid0 = VT_CLSID.from_stream(stream)
        clsid1 = VT_CLSID.from_stream(stream, 0)

        for clsid in (clsid0, clsid1):
            ae(clsid.type, varenum.VT_CLSID)
            ae(clsid.size, 20)
            ae(clsid.value, UUID(bytes_le=data[4:]))
        # end for
    # end def test_from_stream
# end class VT_CLSIDTestCase

class VT_VERSIONED_STREAMTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x49\x00")  # type == VT_VERSIONED_STREAM
        data.extend(b"\x64\x53")  # pad
        data.extend([x for x in range(16)])  # version guid
        data.extend(b"\x06\x00\x00\x00")  # stream name (size)
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # stream name (string)
        stream = ByteIStream(data)

        vs0 = VT_VERSIONED_STREAM.from_stream(stream)
        vs1 = VT_VERSIONED_STREAM.from_stream(stream, 0)

        for vs in (vs0, vs1):
            ae(vs.type, varenum.VT_VERSIONED_STREAM)
            ae(vs.size, 32)
            ae(vs.value.size, 28)
            ae(
                vs.value.version_guid,
                UUID(bytes_le=bytes([x for x in range(16)]))
            )
            ae(vs.value.stream_name, b"a\x00b\x00c\x00")
            ae(vs.value.value, b"a\x00b\x00c\x00")
        # end for

        vs0 = VT_VERSIONED_STREAM.from_stream(stream, 0, decoder)
        vs1 = VT_VERSIONED_STREAM.from_stream(stream, 0, decoder)
        for vs in (vs0, vs1):
            ae(vs.type, varenum.VT_VERSIONED_STREAM)
            ae(vs.size, 32)
            ae(vs.value.size, 28)
            ae(
                vs.value.version_guid,
                UUID(bytes_le=bytes([x for x in range(16)]))
            )
            ae(vs.value.stream_name, "abc")
        # end for


        data[24:] = b"a\x00\x00\x00b\x00\xFF\xFF"
        stream = ByteIStream(data)

        vs0 = VT_VERSIONED_STREAM.from_stream(stream, 0, decoder)
        vs1 = VT_VERSIONED_STREAM.from_stream(stream, 0, decoder)

        for vs in (vs0, vs1):
            ae(vs.type, varenum.VT_VERSIONED_STREAM)
            ae(vs.size, 32)
            ae(vs.value.size, 28)
            ae(
                vs.value.version_guid,
                UUID(bytes_le=bytes([x for x in range(16)]))
            )
            ae(vs.value.stream_name, "a\x00b")
            ae(vs.value.value, "a\x00b")
        # end for
    # end def test_from_stream
# end class VT_VERSIONED_STREAMTestCase

class VT_ARRAYTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x02\x20\x64\x53")  # type (VT_I2 | VT_ARRAY) / pad
        data.extend(b"\x02\x00\x00\x00\x03\x00\x00\x00") # type (VT_I2) / count
        data.extend(b"\x03\x00\x00\x00\x07\x00\x00\x00") # dimension 0
        data.extend(b"\x02\x00\x00\x00\x08\x00\x00\x00") # dimension 1
        data.extend(b"\x01\x00\x00\x00\x09\x00\x00\x00") # dimension 2

        data.extend(b"\x00\x00") # element 0
        data.extend(b"\x01\x00") # element 1
        data.extend(b"\x02\x00") # element 2
        data.extend(b"\x03\x00") # element 3
        data.extend(b"\x04\x00") # element 4
        data.extend(b"\x05\x00") # element 5

        stream = ByteIStream(data)
        array0 = VT_ARRAY.from_stream(stream)
        array1 = VT_ARRAY.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.type, 0x2002)
            ae(array.size, 48)
            ae(array.value.size, 44)
            ae(array.value.value, [0, 1, 2, 3, 4, 5])
            ae(array.value.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(array.value.scalar_type, 2)
            ae(array.value.dimension_count, 3)
        # end for


        stream = ByteIStream(data[:-2])
        array0 = VT_ARRAY.from_stream(stream)
        array1 = VT_ARRAY.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.type, 0x2002)
            ae(array.size, 48)
            ae(array.value.size, 44)
            ae(array.value.value, [0, 1, 2, 3, 4])
            ae(array.value.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(array.value.scalar_type, 2)
            ae(array.value.dimension_count, 3)
        # end for


        stream = ByteIStream(data[:-1])
        array0 = VT_ARRAY.from_stream(stream)
        array1 = VT_ARRAY.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.type, 0x2002)
            ae(array.size, 48)
            ae(array.value.size, 44)
            ae(array.value.value, [0, 1, 2, 3, 4])
            ae(array.value.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(array.value.scalar_type, 2)
            ae(array.value.dimension_count, 3)
        # end for


        data = bytearray()
        data.extend(b"\x0C\x20\x64\x53")  # type (VT_ARRAY | VT_VARIANT) / pad
        data.extend(b"\x0C\x00\x00\x00")  # scalar type
        data.extend(b"\x03\x00\x00\x00")  # dimension count
        data.extend(b"\x03\x00\x00\x00\x07\x00\x00\x00")  # dimension 0
        data.extend(b"\x01\x00\x00\x00\x08\x00\x00\x00")  # dimension 1
        data.extend(b"\x00\x00\x00\x00\x09\x00\x00\x00")  # dimension 2

        data.extend(b"\x08\x00\x64\x53")  # element 0 - VT_BSTR
        data.extend(b"\x06\x00\x00\x00")  # size of data field
        data.extend(b"a\x00\x00\x00b\x00\x64\x53")  # data (incl, padding)

        data.extend(b"\x00\x00\x64\x53")  # element 1 - VT_NULL

        data.extend(b"\x12\x00\x64\x53")  # element 2 - VT_UI2
        data.extend(b"\xFE\xFF\x64\x53")  # data (incl. padding)

        stream = ByteIStream(data)
        value = [
            VT_BSTR((8, 16, b"a\x00\x00\x00b\x00")),
            VT_EMPTY((0, 4, None)),
            VT_UI2((18, 8, 0xFFFE))
        ]

        array0 = VT_ARRAY.from_stream(stream)
        array1 = VT_ARRAY.from_stream(stream, 0)

        for array in (array0, array1):
            ae(array.type, 0x200C)
            ae(array.size, 64)
            ae(array.value.size, 60)
            ae(array.value.value, value)
            ae(array.value.scalar_type, 0xC)
            ae(array.value.dimensions, [(3, 7), (1, 8), (0, 9)])
            ae(array.value.dimension_count, 3)
        # end for

        stream = ByteIStream(data[:-3])
        value[0] = VT_BSTR((8, 16, "a\x00b"))
        value = value[:-1]
        array0 = VT_ARRAY.from_stream(stream, decoder=decoder)
        array1 = VT_ARRAY.from_stream(stream, 0, decoder)

        for array in (array0, array1):
            ae(array.type, 0x200C)
            ae(array.size, 56)
            ae(array.value.size, 52)
            ae(array.value.value, value)
            ae(array.value.scalar_type, 0xC)
            ae(array.value.dimensions, [(3, 7), (1, 8), (0, 9)])
            ae(array.value.dimension_count, 3)
        # end for
    # end def test_from_stream
# end class VT_ARRAYTestCase

class VT_VECTORTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x02\x10\x64\x53")  # type (VT_I2 | VT_VECTOR) / pad
        data.extend(b"\x05\x00\x00\x00")  # length

        data.extend(b"\x00\x00") # element 0
        data.extend(b"\x01\x00") # element 1
        data.extend(b"\x02\x00") # element 2
        data.extend(b"\x03\x00") # element 3
        data.extend(b"\x04\x00") # element 4

        stream = ByteIStream(data)
        vector0 = VT_VECTOR.from_stream(stream)
        vector1 = VT_VECTOR.from_stream(stream, 0)

        for vector in (vector0, vector1):
            ae(vector.type, 0x1002)
            ae(vector.size, 20)
            ae(vector.value.size, 16)
            ae(vector.value.value, [0, 1, 2, 3, 4])
            ae(vector.value.scalar_count, 5)
        # end for


        stream = ByteIStream(data[:-2])
        vector0 = VT_VECTOR.from_stream(stream)
        vector1 = VT_VECTOR.from_stream(stream, 0)

        for vector in (vector0, vector1):
            ae(vector.type, 0x1002)
            ae(vector.size, 16)
            ae(vector.value.size, 12)
            ae(vector.value.value, [0, 1, 2, 3])
            ae(vector.value.scalar_count, 5)
        # end for


        stream = ByteIStream(data[:-1])
        vector0 = VT_VECTOR.from_stream(stream)
        vector1 = VT_VECTOR.from_stream(stream, 0)

        for vector in (vector0, vector1):
            ae(vector.type, 0x1002)
            ae(vector.size, 16)
            ae(vector.value.size, 12)
            ae(vector.value.value, [0, 1, 2, 3])
            ae(vector.value.scalar_count, 5)
        # end for


        data = bytearray()
        data.extend(b"\x0C\x10\x64\x53")  # type (VT_VECTOR | VT_VARIANT) / pad
        data.extend(b"\x03\x00\x00\x00")  # length

        data.extend(b"\x08\x00\x64\x53")  # element 0 - VT_BSTR
        data.extend(b"\x06\x00\x00\x00")  # size of data field
        data.extend(b"a\x00\x00\x00b\x00\x64\x53")  # data (incl, padding)

        data.extend(b"\x00\x00\x64\x53")  # element 1 - VT_NULL

        data.extend(b"\x12\x00\x64\x53")  # element 2 - VT_UI2
        data.extend(b"\xFE\xFF\x64\x53")  # data (incl. padding)

        stream = ByteIStream(data)
        value = [
            VT_BSTR((8, 16, b"a\x00\x00\x00b\x00")),
            VT_EMPTY((0, 4, None)),
            VT_UI2((18, 8, 0xFFFE))
        ]

        vector0 = VT_VECTOR.from_stream(stream)
        vector1 = VT_VECTOR.from_stream(stream, 0)

        for vector in (vector0, vector1):
            ae(vector.type, 0x100C)
            ae(vector.size, 36)
            ae(vector.value.size, 32)
            ae(vector.value.value, value)
            ae(vector.value.scalar_count, 3)
        # end for

        stream = ByteIStream(data[:-3])
        value[0] = VT_BSTR((8, 16, "a\x00b"))
        value = value[:-1]
        vector0 = VT_VECTOR.from_stream(stream, decoder=decoder)
        vector1 = VT_VECTOR.from_stream(stream, 0, decoder)

        for vector in (vector0, vector1):
            ae(vector.type, 0x100C)
            ae(vector.size, 28)
            ae(vector.value.size, 24)
            ae(vector.value.value, value)
            ae(vector.value.scalar_count, 3)
        # end for
    # end def test_from_stream
# end class VT_VECTORTestCase

class PropertyFactoryTestCase(TestCase):
    def test_make(self):
        ae = self.assertEqual
        make = PropertyFactory.make
        uuid = UUID(bytes_le=bytes([x for x in range(16)]))

        pt = varenum
        decoder = codecs.getdecoder("utf_16_le")
        properties = list()

        data = b"\x00\x00\xFF\xFF"
        stream = ByteIStream(data)

        properties.append(make(stream))
        properties.append(make(stream, 0))

        for property in properties:
            ae(property, VT_EMPTY((0, 4, None)))
        # end for


        data = b"\x01\x00\xFF\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_NULL((1, 4, None)))
        # end for


        data = b"\x02\x00\x64\x53\xFF\xFF\x64\x53"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_I2((pt.VT_I2, 8, -1)))
        # end for


        data = b"\x03\x00\x64\x53\xFF\xFF\xFF\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_I4((pt.VT_I4, 8, -1)))
        # end for


        data = b"\x04\x00\x64\x53\xC3\xF5\x48\x40"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_R4((pt.VT_R4, 8, 3.140000104904175)))
        # end for


        data = b"\x05\x00\x64\x53\x1F\x85\xEB\x51\xB8\x1E\x09\x40"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_R8((pt.VT_R8, 12, 3.14)))
        # end for


        data = b"\x06\x00\x64\x53\xA8\xF2\x50\x00\x00\x00\x00\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_CY((pt.VT_CY, 12, Decimal("530.5"))))
        # end for


        data = b"\x07\x00\x64\x53\x00\x00\x00\x00\x00\x00\x0A\x40"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)
        control = VT_DATE((pt.VT_DATE, 12, datetime(1900, 1, 2, 6, 0)))

        for property in properties:
            ae(property, control)
        # end for


        data = b"\x08\x00\x64\x53\x01\x00\x00\x00a\x00\x00\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_BSTR((pt.VT_BSTR, 12, b"a")))
        # end for

        data = b"\x08\x00\x64\x53\x02\x00\x00\x00a\x00\x00\x00"
        stream = ByteIStream(data)
        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property, VT_BSTR((pt.VT_BSTR, 12, "a")))
        # end for


        data = b"\x0A\x00\x64\x53\x00\x01\x02\x03"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        hresult = HRESULT.from_stream(ByteIStream(b"\x00\x01\x02\x03"))
        for property in properties:
            ae(property, VT_ERROR((pt.VT_ERROR, 8, hresult.value)))
        # end for


        data = b"\x0B\x00\x64\x53\x01\x02\x64\x53"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_BOOL((pt.VT_BOOL, 8, 0x0201)))
        # end for


        data = bytearray()
        data.extend(b"\x0E\x00\x64\x53")
        data.extend(b"\x64\x53")  # reserved
        data.extend(b"\x03")  # scale
        data.extend(b"\x00")  # sign
        data.extend(b"\x34\xA8\x23\x08")  # hi32
        data.extend(b"\x00\x53\x64\xFF\x3E\xAB\x45\x80")  # lo64
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)
        value = VT_DECIMAL((
            pt.VT_DECIMAL, 20, Decimal("2518986808300068601514447.616")
        ))

        for property in properties:
            ae(property, value)
        # end for


        data = b"\x10\x00\x64\x53\xFF\x00\x00\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_I1((pt.VT_I1, 8, -1)))
        # end for


        data = b"\x11\x00\x64\x53\xFF\x00\x00\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_UI1((pt.VT_UI1, 8, 0xFF)))
        # end for


        data = b"\x12\x00\x64\x53\xFE\xFF\x00\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_UI2((pt.VT_UI2, 8, 0xFFFE)))
        # end for


        data = b"\x13\x00\x64\x53\xFC\xFD\xFE\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_UI4((pt.VT_UI4, 8, 0xFFFEFDFC)))
        # end for


        data = b"\x14\x00\x64\x53\xFD\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_I8((pt.VT_I8, 12, -3)))
        # end for


        data = b"\x15\x00\x64\x53\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_UI8((pt.VT_UI8, 12, 0xFFFEFDFCFBFAF9F8)))
        # end for


        data = b"\x16\x00\x64\x53\xFD\xFF\xFF\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_INT((pt.VT_INT, 8, -3)))
        # end for


        data = b"\x17\x00\x64\x53\xFC\xFD\xFE\xFF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_UINT((pt.VT_UINT, 8, 0xFFFEFDFC)))
        # end for


        data = b"\x1E\x00\x64\x53\x06\x00\x00\x00a\x00\x00\x00b\x00\x00\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_LPSTR((pt.VT_LPSTR, 16, b"a\x00\x00\x00b\x00")))
        # end for

        stream = ByteIStream(data)
        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property, VT_LPSTR((pt.VT_LPSTR, 16, "a")))
        # end for


        data = b"\x1F\x00\x64\x53\x03\x00\x00\x00a\x00b\x00c\x00"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_LPWSTR((pt.VT_LPWSTR, 16, "abc")))
        # end for


        data = b"\x40\x00\x64\x53\x00\x0E\x15\x91\xC4\x95\xC2\x01"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)
        value = \
            VT_FILETIME((pt.VT_FILETIME, 12, datetime(2002, 11, 27, 3, 25, 0)))

        for property in properties:
            ae(property, value)
        # end for


        data = b"\x41\x00\x64\x53\x03\x00\x00\x00\xAB\xCD\xEF"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_BLOB((pt.VT_BLOB, 12, b"\xAB\xCD\xEF")))
        # end for


        data = b"\x42\x00\x64\x53\x02\x00\x00\x00\x01\x02"
        stream = ByteIStream(data)

        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property, VT_STREAM((pt.VT_STREAM, 12, "\u0201")))
        # end for


        data = b"\x43\x00\x64\x53\x02\x00\x00\x00\x01\x02"
        stream = ByteIStream(data)

        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property, VT_STORAGE((pt.VT_STORAGE, 12, "\u0201")))
        # end for


        data = b"\x44\x00\x64\x53\x02\x00\x00\x00\x01\x02"
        stream = ByteIStream(data)

        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)
        value = VT_STREAMED_OBJECT((pt.VT_STREAMED_OBJECT, 12, "\u0201"))

        for property in properties:
            ae(property, value)
        # end for


        data = b"\x45\x00\x64\x53\x02\x00\x00\x00\x01\x02"
        stream = ByteIStream(data)

        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property, VT_STORED_OBJECT((pt.VT_STORED_OBJECT, 12, "\u0201")))
        # end for


        data = b"\x46\x00\x64\x53\x02\x00\x00\x00ab"
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_BLOB_OBJECT((pt.VT_BLOB_OBJECT, 12, b"ab")))
        # end for


        data = bytearray()
        data.extend(b"\x47\x00\x64\x53")
        data.extend(b"\x07\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08")
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)
        cf_value = ClipboardData.from_stream(stream, 4)
        value = VT_CF((pt.VT_CF, 16, cf_value))

        for property in properties:
            ae(property, value)
        # end for


        data = bytearray()
        data.extend(b"\x48\x00\x64\x53")
        data.extend([x for x in range(16)])
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property, VT_CLSID((pt.VT_CLSID, 20, uuid)))
        # end for


        data = bytearray()
        data.extend(b"\x49\x00\x64\x53")
        data.extend([x for x in range(16)])
        data.extend(b"\x06\x00\x00\x00")
        data.extend(b"a\x00b\x00c\x00")
        stream = ByteIStream(data)

        properties[0] = make(stream)
        properties[1] = make(stream, 0)
        vs_value = VersionedStream.from_stream(stream, 4)
        value = VT_VERSIONED_STREAM((pt.VT_VERSIONED_STREAM, 32, vs_value))

        for property in properties:
            ae(property, value)
        # end for

        stream = ByteIStream(data)
        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)
        vs_value = VersionedStream.from_stream(stream, 4, decoder)
        value = VT_VERSIONED_STREAM((pt.VT_VERSIONED_STREAM, 32, vs_value))

        for property in properties:
            ae(property, value)
        # end for


        data = bytearray()
        data.extend(b"\x02\x20\x64\x53")  # type (VT_I2 | VT_ARRAY) / pad
        data.extend(b"\x02\x00\x00\x00\x03\x00\x00\x00") # type (VT_I2) / count
        data.extend(b"\x03\x00\x00\x00\x07\x00\x00\x00") # dimension 0
        data.extend(b"\x02\x00\x00\x00\x08\x00\x00\x00") # dimension 1
        data.extend(b"\x01\x00\x00\x00\x09\x00\x00\x00") # dimension 2

        data.extend(b"\x00\x00") # element 0
        data.extend(b"\x01\x00") # element 1
        data.extend(b"\x02\x00") # element 2
        data.extend(b"\x03\x00") # element 3
        data.extend(b"\x04\x00") # element 4
        data.extend(b"\x05\x00") # element 5

        stream = ByteIStream(data)
        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x2002)
            ae(property.size, 48)
            ae(property.value.size, 44)
            ae(property.value.value, [0, 1, 2, 3, 4, 5])
            ae(property.value.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(property.value.scalar_type, 2)
            ae(property.value.dimension_count, 3)
        # end for


        stream = ByteIStream(data[:-2])
        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x2002)
            ae(property.size, 48)
            ae(property.value.size, 44)
            ae(property.value.value, [0, 1, 2, 3, 4])
            ae(property.value.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(property.value.scalar_type, 2)
            ae(property.value.dimension_count, 3)
        # end for


        stream = ByteIStream(data[:-1])
        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x2002)
            ae(property.size, 48)
            ae(property.value.size, 44)
            ae(property.value.value, [0, 1, 2, 3, 4])
            ae(property.value.dimensions, [(3, 7), (2, 8), (1, 9)])
            ae(property.value.scalar_type, 2)
            ae(property.value.dimension_count, 3)
        # end for


        data = bytearray()
        data.extend(b"\x0C\x20\x64\x53")  # type (VT_ARRAY | VT_VARIANT) / pad
        data.extend(b"\x0C\x00\x00\x00")  # scalar type
        data.extend(b"\x03\x00\x00\x00")  # dimension count
        data.extend(b"\x03\x00\x00\x00\x07\x00\x00\x00")  # dimension 0
        data.extend(b"\x01\x00\x00\x00\x08\x00\x00\x00")  # dimension 1
        data.extend(b"\x00\x00\x00\x00\x09\x00\x00\x00")  # dimension 2

        data.extend(b"\x08\x00\x64\x53")  # element 0 - VT_BSTR
        data.extend(b"\x06\x00\x00\x00")  # size of data field
        data.extend(b"a\x00\x00\x00b\x00\x64\x53")  # data (incl, padding)

        data.extend(b"\x00\x00\x64\x53")  # element 1 - VT_NULL

        data.extend(b"\x12\x00\x64\x53")  # element 2 - VT_UI2
        data.extend(b"\xFE\xFF\x64\x53")  # data (incl. padding)

        stream = ByteIStream(data)
        value = [
            VT_BSTR((8, 16, b"a\x00\x00\x00b\x00")),
            VT_EMPTY((0, 4, None)),
            VT_UI2((18, 8, 0xFFFE))
        ]

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x200C)
            ae(property.size, 64)
            ae(property.value.size, 60)
            ae(property.value.value, value)
            ae(property.value.scalar_type, 0xC)
            ae(property.value.dimensions, [(3, 7), (1, 8), (0, 9)])
            ae(property.value.dimension_count, 3)
        # end for

        stream = ByteIStream(data[:-3])
        value[0] = VT_BSTR((8, 16, "a\x00b"))
        value = value[:-1]
        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property.type, 0x200C)
            ae(property.size, 56)
            ae(property.value.size, 52)
            ae(property.value.value, value)
            ae(property.value.scalar_type, 0xC)
            ae(property.value.dimensions, [(3, 7), (1, 8), (0, 9)])
            ae(property.value.dimension_count, 3)
        # end for


        data = bytearray()
        data.extend(b"\x02\x10\x64\x53")  # type (VT_I2 | VT_VECTOR) / pad
        data.extend(b"\x05\x00\x00\x00")  # length

        data.extend(b"\x00\x00") # element 0
        data.extend(b"\x01\x00") # element 1
        data.extend(b"\x02\x00") # element 2
        data.extend(b"\x03\x00") # element 3
        data.extend(b"\x04\x00") # element 4

        stream = ByteIStream(data)
        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x1002)
            ae(property.size, 20)
            ae(property.value.size, 16)
            ae(property.value.value, [0, 1, 2, 3, 4])
            ae(property.value.scalar_count, 5)
        # end for


        stream = ByteIStream(data[:-2])
        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x1002)
            ae(property.size, 16)
            ae(property.value.size, 12)
            ae(property.value.value, [0, 1, 2, 3])
            ae(property.value.scalar_count, 5)
        # end for


        stream = ByteIStream(data[:-1])
        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x1002)
            ae(property.size, 16)
            ae(property.value.size, 12)
            ae(property.value.value, [0, 1, 2, 3])
            ae(property.value.scalar_count, 5)
        # end for


        data = bytearray()
        data.extend(b"\x0C\x10\x64\x53")  # type (VT_VECTOR | VT_VARIANT) / pad
        data.extend(b"\x03\x00\x00\x00")  # length

        data.extend(b"\x08\x00\x64\x53")  # element 0 - VT_BSTR
        data.extend(b"\x06\x00\x00\x00")  # size of data field
        data.extend(b"a\x00\x00\x00b\x00\x64\x53")  # data (incl, padding)

        data.extend(b"\x00\x00\x64\x53")  # element 1 - VT_NULL

        data.extend(b"\x12\x00\x64\x53")  # element 2 - VT_UI2
        data.extend(b"\xFE\xFF\x64\x53")  # data (incl. padding)

        stream = ByteIStream(data)
        value = [
            VT_BSTR((8, 16, b"a\x00\x00\x00b\x00")),
            VT_EMPTY((0, 4, None)),
            VT_UI2((18, 8, 0xFFFE))
        ]

        properties[0] = make(stream)
        properties[1] = make(stream, 0)

        for property in properties:
            ae(property.type, 0x100C)
            ae(property.size, 36)
            ae(property.value.size, 32)
            ae(property.value.value, value)
            ae(property.value.scalar_count, 3)
        # end for

        stream = ByteIStream(data[:-3])
        value[0] = VT_BSTR((8, 16, "a\x00b"))
        value = value[:-1]
        properties[0] = make(stream, decoder=decoder)
        properties[1] = make(stream, 0, decoder)

        for property in properties:
            ae(property.type, 0x100C)
            ae(property.size, 28)
            ae(property.value.size, 24)
            ae(property.value.value, value)
            ae(property.value.scalar_count, 3)
        # end for
    # end def test_make
# end class PropertyFactoryTestCase

class BuilderTestCase(TestCase):
    def test_build(self):
        ae = self.assertEqual

        blair_props = list()
        sample_props = list()

        blair_path = os.path.join("data", "doc", "blair.doc")
        sample_path = os.path.join("data", "doc", "sample.doc")

        blair_cfb = CompoundFile(RawIStream(blair_path))
        sample_cfb = CompoundFile(RawIStream(sample_path))

        blair_si_stream = blair_cfb.get_stream(3)
        blair_dsi_stream = blair_cfb.get_stream(4)

        sample_si_stream = sample_cfb.get_stream(39)
        sample_dsi_stream = sample_cfb.get_stream(40)

        blair_props.append(Builder.build(blair_si_stream))
        blair_props.append(Builder.build(blair_si_stream, 0))
        blair_props.append(Builder.build(blair_dsi_stream))
        blair_props.append(Builder.build(blair_dsi_stream, 0))

        sample_props.append(Builder.build(sample_si_stream))
        sample_props.append(Builder.build(sample_si_stream, 0))
        sample_props.append(Builder.build(sample_dsi_stream))
        sample_props.append(Builder.build(sample_dsi_stream, 0))

        control_pids_offsets = {
            0x1: 0x98,
            0x2: 0xA0,
            0x3: 0xEC,
            0x4: 0xF8,
            0x5: 0x108,
            0x6: 0x114,
            0x7: 0x120,
            0x8: 0x134,
            0x9: 0x144,
            0x12: 0x150,
            0xA: 0x16C,
            0xB: 0x178,
            0xC: 0x184,
            0xD: 0x190,
            0xE: 0x19C,
            0xF: 0x1A4,
            0x10: 0x1AC,
            0x13: 0x1B4
        }

        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VT_LPSTR((
                0x1E,
                76,
                "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND"
                " INTIMIDATION"
            )),
            3: VT_LPSTR((0x1E, 12,"")),
            4: VT_LPSTR((0x1E, 16, "default")),
            5: VT_LPSTR((0x1E, 12, "")),
            6: VT_LPSTR((0x1E, 12, "")),
            7: VT_LPSTR((0x1E, 20, "Normal.dot")),
            8: VT_LPSTR((0x1E, 16, "MKhan")),
            9: VT_LPSTR((0x1E, 12, "4")),
            18: VT_LPSTR((0x1E, 28, "Microsoft Word 8.0")),
            10: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x6B49D200)
            )),
            11: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01C2C8A7296E8E00)
            )),
            12: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01C2CB66F65A2200)
            )),
            13: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01C2CB75E8F86400)
            )),
            14: VT_I4((3, 8, 1)),
            15: VT_I4((3, 8, 0xF23)),
            16: VT_I4((3, 8, 0x564A)),
            19: VT_I4((3, 8, 0))
        }

        for prop in blair_props[:2]:
            ae(prop.byte_order, 0xFFFE)
            ae(prop.version, 0)
            ae(prop.sys_id, b"\x04\x00\x02\x00")
            ae(prop.clsid, UUID(int=0))
            ae(prop.property_set_count, 1)
            ae(prop.fmtid0, UUID("f29f85e0-4ff9-1068-ab91-08002b27b3d9"))
            ae(prop.offset0, 48)
            ae(prop.fmtid1, None)
            ae(prop.offset1, None)
            ae(prop.property_set_1, None)

            ae(prop.property_set_0.size, 0x1BC)
            ae(prop.property_set_0.pair_count, 0x12)
            ae(prop.property_set_0.pids_offsets, control_pids_offsets)
            ae(prop.property_set_0.properties, control_properties)
        # end for

        control_pids_offsets_0 = {
                0x1: 0x68,
                0xF: 0x70,
                0x5: 0x80,
                0x6: 0x88,
                0x11: 0x90,
                0x17: 0x98,
                0x0B: 0xA0,
                0x10: 0xA8,
                0x13: 0xB0,
                0x16: 0xB8,
                0x0D: 0xC0,
                0x0C: 0x110
            }

        control_pids_offsets_1 = {
            0: 0x20,
            0x1: 0x36,
            0x2: 0x3E
        }

        control_properties_0 = {
            0x1: VT_I2((2, 8, 0x4E4)),
            0xF: VT_LPSTR((0x1E, 16, "default")),
            0x5: VT_I4((3, 8, 0xB8)),
            0x6: VT_I4((3, 8, 0x2C)),
            0x11: VT_I4((3, 8, 0x69F8)),
            0x17: VT_I4((3, 8, 0x81531)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),
            0xD: VT_VECTOR((
                0x101E,
                0x50,
                Vector((
                    76,
                    1,
                    [
                        CodePageString((
                            72,
                            "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, "
                            "DECEPTION AND INTIMIDATION"
                        ))
                    ]
                ))
            )),
            0xC: VT_VECTOR((
                0x100C,
                28,
                Vector((
                    24,
                    2,
                    [
                        VT_LPSTR((0x1E, 16, "Title")),
                        VT_EMPTY((0, 4, None))
                    ],
                ))
            ))
        }

        control_properties_1 = {
            0: Dictionary((
                24,
                {
                    2: "_PID_GUID"
                },
                1
            )),
            1: VT_I2((2, 8, 0x4E4)),
            2: VT_BLOB((
                0x41,
                0x58,
                b"\x7B\x00\x35\x00\x45\x00\x32\x00"
                b"\x43\x00\x32\x00\x45\x00\x36\x00"
                b"\x43\x00\x2D\x00\x38\x00\x41\x00"
                b"\x31\x00\x36\x00\x2D\x00\x34\x00"
                b"\x36\x00\x46\x00\x33\x00\x2D\x00"
                b"\x38\x00\x38\x00\x34\x00\x33\x00"
                b"\x2D\x00\x37\x00\x46\x00\x37\x00"
                b"\x33\x00\x39\x00\x46\x00\x41\x00"
                b"\x31\x00\x32\x00\x39\x00\x30\x00\x31\x00\x7D\x00\x00\x00"
            ))
        }

        for prop in blair_props[2:]:
            ae(prop.byte_order, 0xFFFE)
            ae(prop.version, 0)
            ae(prop.sys_id, b"\x04\x00\x02\x00")
            ae(prop.clsid, UUID(int=0))
            ae(prop.property_set_count, 2)
            ae(prop.fmtid0, UUID("d5cdd502-2e9c-101b-9397-08002b2cf9ae"))
            ae(prop.offset0, 68)
            ae(prop.fmtid1, UUID("d5cdd505-2e9c-101b-9397-08002b2cf9ae"))
            ae(prop.offset1, 372)

            ae(prop.property_set_0.size, 0x130)
            ae(prop.property_set_0.pair_count, 0xC)
            ae(prop.property_set_0.pids_offsets, control_pids_offsets_0)
            ae(prop.property_set_0.properties, control_properties_0)

            ae(prop.property_set_1.size, 0x98)
            ae(prop.property_set_1.pair_count, 3)
            ae(prop.property_set_1.pids_offsets, control_pids_offsets_1)
            ae(prop.property_set_1.properties, control_properties_1)
        # end for

        control_pids_offsets = {
            1: 0x98,
            2: 0xA0,
            3: 0xB4,
            4: 0xCC,
            5: 0xE4,
            6: 0x100,
            7: 0x128,
            8: 0x138,
            9: 0x148,
            0x12: 0x154,
            0xA: 0x174,
            0xC: 0x180,
            0xD: 0x18C,
            0xE: 0x198,
            0xF: 0x1A0,
            0x10: 0x1A8,
            0x13: 0x1B0,
            0x11: 0x1B8
        }

        sample_si_stream.seek(0x214, SEEK_SET)
        sample_si_stream.seek(0x1F4, SEEK_SET)
        cf_data = sample_si_stream.read(0x0254AA)
        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VT_LPSTR((0x1E, 20, "title_value")),
            3: VT_LPSTR((0x1E, 24, "subject_value")),
            4: VT_LPSTR((0x1E, 24, "author_value")),
            5: VT_LPSTR((0x1E, 28, "keyword0 keyword1")),
            6: VT_LPSTR((0x1E, 40, "Comments in the comments box")),
            7: VT_LPSTR((0x1E, 16, "Normal")),
            8: VT_LPSTR((0x1E, 16, "lftest2")),
            9: VT_LPSTR((0x1E, 12, "24")),
            0x12: VT_LPSTR((0x1E, 32, "Microsoft Office Word")),
            0xA: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x1176592E00)
            )),
            0xC: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01CAA3C0F0A6EC00)
            )),
            0xD: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01CAA3D361570400)
            )),
            0xE: VT_I4((3, 8, 7)),
            0xF: VT_I4((3, 8, 0xAA)),
            0x10: VT_I4((3, 8, 0x0550)),
            0x13: VT_I4((3, 8, 8)),
            0x11: VT_CF((
                0x47,
                0x0254B8,
                ClipboardData((
                    0x0254B4,
                    cf_data,
                    b"\xFF\xFF\xFF\xFF"
                ))
            ))
        }

        for prop in sample_props[:2]:
            ae(prop.byte_order, 0xFFFE)
            ae(prop.version, 0)
            ae(prop.sys_id, b"\x05\x01\x02\x00")
            ae(prop.clsid, UUID(int=0))
            ae(prop.fmtid0, UUID("f29f85e0-4ff9-1068-ab91-08002b27b3d9"))
            ae(prop.offset0, 48)
            ae(prop.fmtid1, None)
            ae(prop.offset1, None)
            ae(prop.property_set_1, None)

            ae(prop.property_set_0.size, 0x25670)
            ae(prop.property_set_0.pair_count, 0x12)
            ae(prop.property_set_0.pids_offsets, control_pids_offsets)
            ae(prop.property_set_0.properties, control_properties)
        # end for

        control_pids_offsets_0 = {
           1: 0x80,
           2: 0x88,
           0xE: 0xA0,
           0xF: 0xB8,
           0x1B: 0xD0,
           5: 0xE8,
           6: 0xF0,
           0x11: 0xF8,
           0x17: 0x100,
           0xB: 0x108,
           0x10: 0x110,
           0x13: 0x118,
           0x16: 0x120,
           0xD: 0x128,
           0xC: 0x17B
        }

        control_pids_offsets_1 = {
            0: 0xB8,
            1: 0x23D,
            2: 0x245,
            3: 0x279,
            4: 0x725,
            5: 0x739,
            6: 0x745,
            7: 0x74D,
            8: 0x755,
            9: 0x75D,
            0xA: 0x769,
            0xB: 0x775,
            0xC: 0x781,
            0xD: 0x78D,
            0xE: 0x799,
            0xF: 0x7A1,
            0x10: 0x7A9,
            0x1000010: 0x7B5,
            0x11: 0x7CD,
            0x1000011: 0x7D9,
            0x12: 0x7F1,
            0x1000012: 0x7FD
        }

        sample_dsi_stream.seek(0x445, SEEK_SET)
        blob_data0 = sample_dsi_stream.read(0x2A)

        sample_dsi_stream.seek(0x479, SEEK_SET)
        blob_data1 = sample_dsi_stream.read(0x4A4)

        control_properties_0 = {
            1: VT_I2((2, 8, 1252)),
            2: VT_LPSTR((0x1E, 24, "category_value")),
            0xE: VT_LPSTR((0x1E, 24, "manager_value")),
            0xF: VT_LPSTR((0x1E, 24, "company_value")),
            0x1B: VT_LPSTR((0x1E, 24, "status_value")),
            5: VT_I4((3, 8, 0x55)),
            6: VT_I4((3, 8, 0x1D)),
            0x11: VT_I4((3, 8, 0x5DD)),
            0x17: VT_I4((3, 8, 0x0C0000)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),

            # This entry is bizarre because it is really a vector of unaligned
            # strings.  The OLE-PS spec. doesn't have an unaligned string data
            # type though.  This is interpreted properly in lf.apps.msoffice.
            0xD: VT_VECTOR((
                0x101E,
                0x434F5424,
                Vector((
                    0x434F5420,
                    5,
                    [
                        CodePageString((16, "title_value")),
                        CodePageString((8, "")),
                        CodePageString((0x434F5404, " Entry 1"))
                    ]
                    )),
            )),
            0xC: VT_VECTOR((
                0x100C,
                36,
                Vector((
                    32,
                    4,
                    [
                        # These are also off, since they are unaligned strings
                        VT_LPSTR((0x1E, 16, "Title")),
                        VT_NULL((0, 4, None)),
                        VT_NULL((0, 4, None)),
                        VT_NULL((0, 4, None))
                    ]
                ))
            ))
        }

        control_properties_1 = {
            0: Dictionary((
                392,
                {
                    2: "_PID_LINKBASE",
                    3: "_PID_HLINKS",
                    4: "text_name",
                    5: "date_name",
                    6: "number_name_0",
                    7: "number_name_1",
                    8: "number_name_2",
                    9: "number_name_3",
                    0xA: "number_name_4",
                    0xB: "number_name_5",
                    0xC: "number_name_6",
                    0xD: "number_name_7",
                    0xE: "yes_name_yes",
                    0xF: "yes_name_no",
                    0x10: "link_to_bookmark_name1",
                    0x11: "link_to_bookmark_name2",
                    0x12: "link_to__1326562448"
                },
               17
            )),
            1: VT_I2((2, 8, 1252)),
            2: VT_BLOB((0x41, 52, blob_data0)),
            3: VT_BLOB((0x41, 0x4AC, blob_data1)),
            4: VT_LPSTR((0x1E, 20, "text_value")),
            5: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0xE039A15D3D4000)
            )),
            6: VT_I4((0x3, 8, 0x64)),
            7: VT_I4((0x3, 8, 0x2710)),
            8: VT_I4((0x3, 8, 0x186A0)),
            9: VT_R8((0x5, 12, 1000000000000.0)),
            0xA: VT_R8((0x5, 12, -100.0)),
            0xB: VT_R8((0x5, 12, -100000.0)),
            0xC: VT_R8((0x5, 12, -10000.0)),
            0xD: VT_R8((0x5, 12, -1000000000000.0)),
            0xE: VT_BOOL((0xB, 8, 0xFFFF)),
            0xF: VT_BOOL((0xB, 8, 0)),
            0x10: VT_LPSTR((0x1E, 12, "")),
            0x1000010: VT_LPSTR((0x1E, 24, "bookmark_name1")),
            0x11: VT_LPSTR((0x1E, 12, "")),
            0x1000011: VT_LPSTR((0x1E, 24, "bookmark_name2")),
            0x12: VT_LPSTR((0x1E, 12, "")),
            0x1000012: VT_LPSTR((0x1E, 20, "_1326562448"))
        }

        for prop in sample_props[2:]:
            ae(prop.byte_order, 0xFFFE)
            ae(prop.version, 0)
            ae(prop.sys_id, b"\x05\x01\x02\x00")
            ae(prop.clsid, UUID(int=0))
            ae(prop.property_set_count, 2)
            ae(prop.fmtid0, UUID("d5cdd502-2e9c-101b-9397-08002b2cf9ae"))
            ae(prop.offset0, 68)
            ae(prop.fmtid1, UUID("d5cdd505-2e9c-101b-9397-08002b2cf9ae"))
            ae(prop.offset1, 0x1F8)

            ae(prop.property_set_0.size, 0x1B4)
            ae(prop.property_set_0.pair_count, 15)
            ae(prop.property_set_0.pids_offsets, control_pids_offsets_0)
            ae(prop.property_set_0.properties, control_properties_0)

            ae(prop.property_set_1.size, 0x814)
            ae(prop.property_set_1.pair_count, 22)
            ae(prop.property_set_1.pids_offsets, control_pids_offsets_1)
            ae(prop.property_set_1.properties, control_properties_1)
        # end for
    # end def test_build

    def test_build_property_set_stream_header(self):
        ae = self.assertEqual

        data0 = bytearray([x for x in range(48)])
        data1 = bytes([x for x in range(68)])

        data0[24:28] = b"\x01\x00\x00\x00"

        pss0 = Builder.build_property_set_stream_header(ByteIStream(data0), 0)
        pss1 = Builder.build_property_set_stream_header(ByteIStream(data1))

        ae(pss0.byte_order, 0x0100)
        ae(pss1.byte_order, 0x0100)

        ae(pss0.version, 0x0302)
        ae(pss1.version, 0x0302)

        ae(pss0.sys_id, b"\x04\x05\x06\x07")
        ae(pss1.sys_id, b"\x04\x05\x06\x07")

        clsid = UUID(
            bytes_le =
            b"\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17"
        )

        ae(pss0.clsid, clsid)
        ae(pss1.clsid, clsid)

        ae(pss0.property_set_count, 1)
        ae(pss1.property_set_count, 0x1B1A1918)

        fmtid0 = UUID(
            bytes_le =
            b"\x1C\x1D\x1E\x1F\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B"
        )

        ae(pss0.fmtid0, fmtid0)
        ae(pss1.fmtid0, fmtid0)

        ae(pss0.offset0, 0x2F2E2D2C)
        ae(pss1.offset0, 0x2F2E2D2C)

        fmtid1 = UUID(
            bytes_le =
            b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F"
        )

        ae(pss0.fmtid1, None)
        ae(pss1.fmtid1, fmtid1)

        ae(pss0.offset1, None)
        ae(pss1.offset1, 0x43424140)
    # end def test_build_property_set_stream_header

    def test_build_property_set_header(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend([x for x in range(48)])
        data[4:8] = b"\x05\x00\x00\x00"

        stream = ByteIStream(data)
        psh0 = Builder.build_property_set_header(stream)
        psh1 = Builder.build_property_set_header(stream, 0)

        for psh in (psh0, psh1):
            ae(psh.size, 0x03020100)
            ae(psh.pair_count, 5)
            ae(len(psh.pids_offsets), 5)
            ae(psh.pids_offsets[0x0B0A0908], 0x0F0E0D0C)
            ae(psh.pids_offsets[0x13121110], 0x17161514)
            ae(psh.pids_offsets[0x1B1A1918], 0x1F1E1D1C)
            ae(psh.pids_offsets[0x23222120], 0x27262524)
            ae(psh.pids_offsets[0x2B2A2928], 0x2F2E2D2C)
        # end for
    # end def test_build_property_set_header

    def test_build_properties(self):
        ae = self.assertEqual

        blair_props = list()
        sample_props = list()

        blair_path = os.path.join("data", "doc", "blair.doc")
        sample_path = os.path.join("data", "doc", "sample.doc")

        blair_cfb = CompoundFile(RawIStream(blair_path))
        sample_cfb = CompoundFile(RawIStream(sample_path))

        blair_si_stream = blair_cfb.get_stream(3)
        blair_dsi_stream = blair_cfb.get_stream(4)

        sample_si_stream = sample_cfb.get_stream(39)
        sample_dsi_stream = sample_cfb.get_stream(40)

        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VT_LPSTR((
                0x1E,
                76,
                "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND"
                " INTIMIDATION"
            )),
            3: VT_LPSTR((0x1E, 12,"")),
            4: VT_LPSTR((0x1E, 16, "default")),
            5: VT_LPSTR((0x1E, 12, "")),
            6: VT_LPSTR((0x1E, 12, "")),
            7: VT_LPSTR((0x1E, 20, "Normal.dot")),
            8: VT_LPSTR((0x1E, 16, "MKhan")),
            9: VT_LPSTR((0x1E, 12, "4")),
            18: VT_LPSTR((0x1E, 28, "Microsoft Word 8.0")),
            10: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x6B49D200)
            )),
            11: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01C2C8A7296E8E00)
            )),
            12: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01C2CB66F65A2200)
            )),
            13: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01C2CB75E8F86400)
            )),
            14: VT_I4((3, 8, 1)),
            15: VT_I4((3, 8, 0xF23)),
            16: VT_I4((3, 8, 0x564A)),
            19: VT_I4((3, 8, 0))
        }

        blair_property_set_header = \
            Builder.build_property_set_header(blair_si_stream, 48)

        blair_properties = Builder.build_properties(
            blair_si_stream, blair_property_set_header, 48
        )

        ae(blair_properties, control_properties)


        control_properties = {
            0x1: VT_I2((2, 8, 0x4E4)),
            0xF: VT_LPSTR((0x1E, 16, "default")),
            0x5: VT_I4((3, 8, 0xB8)),
            0x6: VT_I4((3, 8, 0x2C)),
            0x11: VT_I4((3, 8, 0x69F8)),
            0x17: VT_I4((3, 8, 0x81531)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),
            0xD: VT_VECTOR((
                0x101E,
                0x50,
                Vector((
                    76,
                    1,
                    [
                        CodePageString((
                            72,
                            "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, "
                            "DECEPTION AND INTIMIDATION"
                        ))
                    ]
                ))
            )),
            0xC: VT_VECTOR((
                0x100C,
                28,
                Vector((
                    24,
                    2,
                    [
                        VT_LPSTR((0x1E, 16, "Title")),
                        VT_EMPTY((0, 4, None))
                    ]
                ))
            ))
        }

        blair_property_set_header = \
            Builder.build_property_set_header(blair_dsi_stream, 68)
        blair_properties = Builder.build_properties(
            blair_dsi_stream, blair_property_set_header, 68
        )
        ae(blair_properties, control_properties)


        control_properties = {
            0: Dictionary((
                24,
                {
                    2: "_PID_GUID"
                },
                1
            )),
            1: VT_I2((2, 8, 0x4E4)),
            2: VT_BLOB((
                0x41,
                0x58,
                b"\x7B\x00\x35\x00\x45\x00\x32\x00"
                b"\x43\x00\x32\x00\x45\x00\x36\x00"
                b"\x43\x00\x2D\x00\x38\x00\x41\x00"
                b"\x31\x00\x36\x00\x2D\x00\x34\x00"
                b"\x36\x00\x46\x00\x33\x00\x2D\x00"
                b"\x38\x00\x38\x00\x34\x00\x33\x00"
                b"\x2D\x00\x37\x00\x46\x00\x37\x00"
                b"\x33\x00\x39\x00\x46\x00\x41\x00"
                b"\x31\x00\x32\x00\x39\x00\x30\x00\x31\x00\x7D\x00\x00\x00"
            ))
        }

        blair_property_set_header = \
            Builder.build_property_set_header(blair_dsi_stream, 372)

        blair_properties = Builder.build_properties(
            blair_dsi_stream, blair_property_set_header, 372
        )

        ae(blair_properties, control_properties)


        sample_si_stream.seek(0x1F4, SEEK_SET)
        cf_data = sample_si_stream.read(0x0254AA)
        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VT_LPSTR((0x1E, 20, "title_value")),
            3: VT_LPSTR((0x1E, 24, "subject_value")),
            4: VT_LPSTR((0x1E, 24, "author_value")),
            5: VT_LPSTR((0x1E, 28, "keyword0 keyword1")),
            6: VT_LPSTR((0x1E, 40, "Comments in the comments box")),
            7: VT_LPSTR((0x1E, 16, "Normal")),
            8: VT_LPSTR((0x1E, 16, "lftest2")),
            9: VT_LPSTR((0x1E, 12, "24")),
            0x12: VT_LPSTR((0x1E, 32, "Microsoft Office Word")),
            0xA: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x1176592E00)
            )),
            0xC: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01CAA3C0F0A6EC00)
            )),
            0xD: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0x01CAA3D361570400)
            )),
            0xE: VT_I4((3, 8, 7)),
            0xF: VT_I4((3, 8, 0xAA)),
            0x10: VT_I4((3, 8, 0x0550)),
            0x13: VT_I4((3, 8, 8)),
            0x11: VT_CF((
                0x47,
                0x0254B8,
                ClipboardData((
                    0x0254B4,
                    cf_data,
                    b"\xFF\xFF\xFF\xFF"
                ))
            ))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_si_stream, 48
        )
        sample_properties = Builder.build_properties(
            sample_si_stream, sample_property_set_header, 48
        )
        ae(sample_properties, control_properties)


        sample_dsi_stream.seek(0x445, SEEK_SET)
        blob_data0 = sample_dsi_stream.read(0x2A)

        sample_dsi_stream.seek(0x479, SEEK_SET)
        blob_data1 = sample_dsi_stream.read(0x4A4)

        control_properties = {
            1: VT_I2((2, 8, 1252)),
            2: VT_LPSTR((0x1E, 24, "category_value")),
            0xE: VT_LPSTR((0x1E, 24, "manager_value")),
            0xF: VT_LPSTR((0x1E, 24, "company_value")),
            0x1B: VT_LPSTR((0x1E, 24, "status_value")),
            5: VT_I4((3, 8, 0x55)),
            6: VT_I4((3, 8, 0x1D)),
            0x11: VT_I4((3, 8, 0x5DD)),
            0x17: VT_I4((3, 8, 0x0C0000)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),

            # This entry is bizarre because it is really a vector of unaligned
            # strings.  The OLE-PS spec. doesn't have an unaligned string data
            # type though.  This is interpreted properly in lf.apps.msoffice.
            0xD: VT_VECTOR((
                0x101E,
                0x434F5424,
                Vector((
                    0x434F5420,
                    5,
                    [
                        CodePageString((16, "title_value")),
                        CodePageString((8, "")),
                        CodePageString((0x434F5404, " Entry 1"))
                    ],
                    )),
            )),
            0xC: VT_VECTOR((
                0x100C,
                36,
                Vector((
                    32,
                    4,
                    [
                        # These are also off, since they are unaligned strings
                        VT_LPSTR((0x1E, 16, "Title")),
                        VT_NULL((0, 4, None)),
                        VT_NULL((0, 4, None)),
                        VT_NULL((0, 4, None))
                    ],
                ))
            ))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_dsi_stream, 68
        )
        sample_properties = Builder.build_properties(
            sample_dsi_stream, sample_property_set_header, 68
        )
        ae(sample_properties, control_properties)


        control_properties = {
            0: Dictionary((
                392,
                {
                    2: "_PID_LINKBASE",
                    3: "_PID_HLINKS",
                    4: "text_name",
                    5: "date_name",
                    6: "number_name_0",
                    7: "number_name_1",
                    8: "number_name_2",
                    9: "number_name_3",
                    0xA: "number_name_4",
                    0xB: "number_name_5",
                    0xC: "number_name_6",
                    0xD: "number_name_7",
                    0xE: "yes_name_yes",
                    0xF: "yes_name_no",
                    0x10: "link_to_bookmark_name1",
                    0x11: "link_to_bookmark_name2",
                    0x12: "link_to__1326562448"
                },
               17
            )),
            1: VT_I2((2, 8, 1252)),
            2: VT_BLOB((0x41, 52, blob_data0)),
            3: VT_BLOB((0x41, 0x4AC, blob_data1)),
            4: VT_LPSTR((0x1E, 20, "text_value")),
            5: VT_FILETIME((
                0x40, 12, FILETIMETodatetime.from_int(0xE039A15D3D4000)
            )),
            6: VT_I4((0x3, 8, 0x64)),
            7: VT_I4((0x3, 8, 0x2710)),
            8: VT_I4((0x3, 8, 0x186A0)),
            9: VT_R8((0x5, 12, 1000000000000.0)),
            0xA: VT_R8((0x5, 12, -100.0)),
            0xB: VT_R8((0x5, 12, -100000.0)),
            0xC: VT_R8((0x5, 12, -10000.0)),
            0xD: VT_R8((0x5, 12, -1000000000000.0)),
            0xE: VT_BOOL((0xB, 8, 0xFFFF)),
            0xF: VT_BOOL((0xB, 8, 0)),
            0x10: VT_LPSTR((0x1E, 12, "")),
            0x1000010: VT_LPSTR((0x1E, 24, "bookmark_name1")),
            0x11: VT_LPSTR((0x1E, 12, "")),
            0x1000011: VT_LPSTR((0x1E, 24, "bookmark_name2")),
            0x12: VT_LPSTR((0x1E, 12, "")),
            0x1000012: VT_LPSTR((0x1E, 20, "_1326562448"))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_dsi_stream, 0x1F8
        )

        sample_properties = Builder.build_properties(
            sample_dsi_stream, sample_property_set_header, 0x1F8
        )

        ae(sample_properties, control_properties)
    # end def test_build_properties
# end class BuilderTestCase
