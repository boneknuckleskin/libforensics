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

"""Unit tests for the lf.apps.msoffice.shared.objects module."""

# stdlib imports
import codecs
from os.path import join
from itertools import chain
from uuid import UUID
from unittest import TestCase

# local imports
from lf.dec import ByteIStream, RawIStream, SEEK_SET
from lf.time import FILETIMETodatetime
from lf.win.ole.cfb import CompoundFile
from lf.win.ole.ps.consts import (
    FMTID_SummaryInformation, FMTID_DocSummaryInformation
)
from lf.win.ole.ps import (
    VT_I2, VT_FILETIME, VT_I4, VT_BOOL, VT_VECTOR, CodePageString, VT_EMPTY,
    Dictionary, VT_BLOB, VT_CF, VT_LPSTR, VT_R8
)
from lf.apps.msoffice.shared.ctypes import (
    property_set_system_identifier
)
from lf.apps.msoffice.shared.objects import (
    PropertySetSystemIdentifier, VtThumbnailValue, VtThumbnail, Lpstr,
    UnalignedLpstr, VtVecUnalignedLpstrValue, VtVecUnalignedLpstr,
    Lpwstr, VtVecLpwstrValue, VtVecLpwstr, VtString, VtUnalignedString,
    VtHeadingPair, VtVecHeadingPairValue, VtVecHeadingPair, VtDigSigValue,
    VtDigSig, VtHyperlink, VecVtHyperlink, VtHyperlinkValue, VtHyperlinks,
    DigSigBlob, DigSigInfoSerialized, PropertySetStreamHeader, PropertyFactory,
    Builder
)

class PropertySetSystemIdentifierTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = ByteIStream(b"\x00\x01\x03\x02")
        pssi0 = PropertySetSystemIdentifier.from_stream(data)
        pssi1 = PropertySetSystemIdentifier.from_stream(data, 0)

        for pssi in (pssi0, pssi1):
            ae(pssi.os_ver_major, 0)
            ae(pssi.os_ver_minor, 1)
            ae(pssi.os_type, 0x0203)
        # end for
    # end def test_from_stream

    def test_from_ctype(self):
        ae = self.assertEqual

        data = b"\x00\x01\x03\x02"
        pssi = property_set_system_identifier.from_buffer_copy(data)
        pssi = PropertySetSystemIdentifier.from_ctype(pssi)

        ae(pssi.os_ver_major, 0)
        ae(pssi.os_ver_minor, 1)
        ae(pssi.os_type, 0x0203)
    # end def test_from_ctype
# end class PropertySetSystemIdentifierTestCase

class VtThumbnailValueTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x0D\x00\x00\x00")  # cb
        data.extend(b"\x01\x02\x03\x04")  # cftag
        data.extend(b"\x05\x06\x07\x08")  # formatId (exists)
        data.extend(b"\x09\x0A\x0B\x0C\x0D")  # cfDataBytes
        stream = ByteIStream(data)

        vttv0 = VtThumbnailValue.from_stream(stream)
        vttv1 = VtThumbnailValue.from_stream(stream, 0)

        for vttv in (vttv0, vttv1):
            ae(vttv.size, 20)
            ae(vttv.data, b"\x09\x0A\x0B\x0C\x0D")
            ae(vttv.tag, 0x04030201)
            ae(vttv.format_id, 0x08070605)
            ae(vttv.value, vttv.data)
            ae(vttv.format, vttv.tag)
        # end for

        data[4:8] = b"\x00\x00\x00\x00"
        stream = ByteIStream(data)

        vttv0 = VtThumbnailValue.from_stream(stream)
        vttv1 = VtThumbnailValue.from_stream(stream, 0)

        for vttv in (vttv0, vttv1):
            ae(vttv.size, 20)
            ae(vttv.data, b"\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D")
            ae(vttv.tag, 0)
            ae(vttv.format_id, None)
            ae(vttv.value, vttv.data)
            ae(vttv.format, vttv.tag)
        # end for
    # end def test_from_stream
# end class VtThumbnailValueTestCase

class VtThumbnailTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x47\x00\x00\x00")  # wType (VT_CF), padding
        data.extend(b"\x0D\x00\x00\x00")  # cb
        data.extend(b"\x01\x02\x03\x04")  # cftag
        data.extend(b"\x05\x06\x07\x08")  # formatId (exists)
        data.extend(b"\x09\x0A\x0B\x0C\x0D")  # cfDataBytes
        stream = ByteIStream(data)

        vtt0 = VtThumbnail.from_stream(stream)
        vtt1 = VtThumbnail.from_stream(stream, 0)
        value = VtThumbnailValue.from_stream(stream, 4)

        for vtt in (vtt0, vtt1):
            ae(vtt.type, 0x47)
            ae(vtt.size, 24)
            ae(vtt.value, value)
        # end for


        data[8:12] = b"\x00\x00\x00\x00"
        stream = ByteIStream(data)

        vtt0 = VtThumbnail.from_stream(stream)
        vtt1 = VtThumbnail.from_stream(stream, 0)
        value = VtThumbnailValue.from_stream(stream, 4)

        for vtt in (vtt0, vtt1):
            ae(vtt.type, 0x47)
            ae(vtt.size, 24)
            ae(vtt.value, value)
        # end for
    # end def test_from_stream
# end class VtThumbnailTestCase

class LpstrTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        lpstr = Lpstr.from_stream(stream)
        ae(lpstr.size, 16)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        lpstr = Lpstr.from_stream(stream, 0, decoder)
        ae(lpstr.size, 16)
        ae(lpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[4:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = Lpstr.from_stream(stream, 0)
        ae(lpstr.size, 16)
        ae(lpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        lpstr = Lpstr.from_stream(stream, 0, decoder)
        ae(lpstr.size, 16)
        ae(lpstr.value, "abcd")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[4:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        lpstr = Lpstr.from_stream(stream)
        ae(lpstr.size, 16)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        lpstr = Lpstr.from_stream(stream, 0, decoder)
        ae(lpstr.size, 16)
        ae(lpstr.value, "ab")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[4:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        lpstr = Lpstr.from_stream(stream)
        ae(lpstr.size, 16)
        ae(lpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        lpstr = Lpstr.from_stream(stream, 0, decoder)
        ae(lpstr.size, 16)
        ae(lpstr.value, "ab")
    # end def test_from_stream
# end def LpstrTestCase

class UnalignedLpstrTestCase(TestCase):
    def setUp(self):
        self.obj = UnalignedLpstr
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        ualpstr = UnalignedLpstr.from_stream(stream)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        ualpstr = UnalignedLpstr.from_stream(stream, 0, decoder)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[4:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        ualpstr = UnalignedLpstr.from_stream(stream, 0)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        ualpstr = UnalignedLpstr.from_stream(stream, 0, decoder)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, "abcd")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[4:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        ualpstr = UnalignedLpstr.from_stream(stream)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        ualpstr = UnalignedLpstr.from_stream(stream, 0, decoder)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, "ab")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[4:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        ualpstr = UnalignedLpstr.from_stream(stream)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        ualpstr = UnalignedLpstr.from_stream(stream, 0, decoder)
        ae(ualpstr.size, 14)
        ae(ualpstr.value, "ab")
    # end def test_from_stream
# end class UnalignedLpstrTestCase

class LpwstrTestCase(TestCase):
    def setUp(self):
        self.obj = Lpwstr
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        lpwstr = Lpwstr.from_stream(stream)
        ae(lpwstr.size, 12)
        ae(lpwstr.value, "abc")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00\x00\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        lpwstr = Lpwstr.from_stream(stream, 1)
        ae(lpwstr.size, 12)
        ae(lpwstr.value, "ab\x00")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        lpwstr = Lpwstr.from_stream(stream, 1)
        ae(lpwstr.size, 12)
        ae(lpwstr.value, "a\x00b")
    # end def test_from_stream
# end class LpwstrTestCase

class VtVecLpwstrValueTestCase(TestCase):
    def setUp(self):
        self.obj = VtVecLpwstrValue
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # count

        data.extend(b"\x02\x00\x00\x00")  # lpwstr 0 - character count
        data.extend(b"a\x00b\x00")  # lpwstr 0 - value

        data.extend(b"\x03\x00\x00\x00")  # lpwstr 1 - character count
        data.extend(b"a\x00b\x00c\x00")  # lpwstr 1 - value
        data.extend(b"\x64\x53")  # lpwstr 1 - pad

        data.extend(b"\x01\x00\x00\x00")  # lpwstr 2 - character count
        data.extend(b"a\x00")  # lpwstr 2 - value
        data.extend(b"\x64\x53")  # lpwstr 2 - pad

        stream = ByteIStream(data)
        vtvlv0 = VtVecLpwstrValue.from_stream(stream)
        vtvlv1 = VtVecLpwstrValue.from_stream(stream, 0)

        for vtvlv in (vtvlv0, vtvlv1):
            ae(vtvlv.size, 32)
            ae(vtvlv.scalar_count, 3)
            ae(vtvlv.value, ["ab", "abc", "a"])
        # end for
    # end def test_from_stream
# end class VtVecLpwstrValueTestCase

class VtVecLpwstrTestCase(TestCase):
    def setUp(self):
        self.obj = VtVecLpwstr
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x1F\x10\x64\x53")  # ttype (VT_VECTOR|VT_LWPSTR), pad
        data.extend(b"\x03\x00\x00\x00")  # count

        data.extend(b"\x02\x00\x00\x00")  # lpwstr 0 - character count
        data.extend(b"a\x00b\x00")  # lpwstr 0 - value

        data.extend(b"\x03\x00\x00\x00")  # lpwstr 1 - character count
        data.extend(b"a\x00b\x00c\x00")  # lpwstr 1 - value
        data.extend(b"\x64\x53")  # lpwstr 1 - pad

        data.extend(b"\x01\x00\x00\x00")  # lpwstr 2 - character count
        data.extend(b"a\x00")  # lpwstr 2 - value
        data.extend(b"\x64\x53")  # lpwstr 2 - pad

        stream = ByteIStream(data)
        vtvl0 = VtVecLpwstr.from_stream(stream)
        vtvl1 = VtVecLpwstr.from_stream(stream, 0)

        for vtvl in (vtvl0, vtvl1):
            ae(vtvl.type, 0x101F)
            ae(vtvl.size, 36)
            ae(vtvl.value.size, 32)
            ae(vtvl.value.scalar_count, 3)
            ae(vtvl.value.value, ["ab", "abc", "a"])
        # end for
    # end def test_from_stream
# end class VtVecLpwstrTestCase

class VtVecUnalignedLpstrValueTestCase(TestCase):
    def setUp(self):
        self.obj = VtVecUnalignedLpstrValue
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # count
        data.extend(b"\x04\x00\x00\x00")  # str 0 - size
        data.extend(b"a\x00b\x00")  # str 0 - value
        data.extend(b"\x03\x00\x00\x00")  # str1 - size
        data.extend(b"a\x00b")  # str 1 - value
        data.extend(b"\x05\x00\x00\x00")  # str2 - size
        data.extend(b"a\x00b\x00\x00")  # str2 - value
        stream = ByteIStream(data)

        vtvulv0 = VtVecUnalignedLpstrValue.from_stream(stream)
        vtvulv1 = VtVecUnalignedLpstrValue.from_stream(stream, 0)

        for vtvulv in (vtvulv0, vtvulv1):
            ae(vtvulv.size, 28)
            ae(vtvulv.scalar_count, 3)
            ae(vtvulv.value, [
                UnalignedLpstr((8, b"a\x00b\x00")),
                UnalignedLpstr((7, b"a\x00b")),
                UnalignedLpstr((9, b"a\x00b\x00\x00"))
            ])
        # end for

        vtvulv = VtVecUnalignedLpstrValue.from_stream(stream, 0, decoder)

        ae(vtvulv.size, 28)
        ae(vtvulv.scalar_count, 3)
        ae(vtvulv.value, [
            UnalignedLpstr((8, "ab")),
            UnalignedLpstr((7, "a")),
            UnalignedLpstr((9, "ab"))
        ])
    # end def test_from_stream
# end class VtVecUnalignedLpstrValueTestCase

class VtVecUnalignedLpstrTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x1E\x10\x64\x53")  # type == VT_VECTOR | VT_LPSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # count
        data.extend(b"\x04\x00\x00\x00")  # str 0 - size
        data.extend(b"a\x00b\x00")  # str 0 - value
        data.extend(b"\x03\x00\x00\x00")  # str1 - size
        data.extend(b"a\x00b")  # str 1 - value
        data.extend(b"\x05\x00\x00\x00")  # str2 - size
        data.extend(b"a\x00b\x00\x00")  # str2 - value
        stream = ByteIStream(data)

        vtvul0 = VtVecUnalignedLpstr.from_stream(stream)
        vtvul1 = VtVecUnalignedLpstr.from_stream(stream, 0)
        value = VtVecUnalignedLpstrValue.from_stream(stream, 4)

        for vtvul in (vtvul0, vtvul1):
            ae(vtvul.type, 0x101E)
            ae(vtvul.size, 32)
            ae(vtvul.value, value)
        # end for

        vtvul = VtVecUnalignedLpstr.from_stream(stream, 0, decoder)
        value = VtVecUnalignedLpstrValue.from_stream(stream, 4, decoder)

        ae(vtvul.type, 0x101E)
        ae(vtvul.size, 32)
        ae(vtvul.value, value)
    # end def test_from_stream
# end class VtVecUnalignedLpstrTestCase

class VtStringTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        # First test the VT_LPSTR test case...
        data = bytearray()
        data.extend(b"\x1E\x00\x64\x53")  # type == VT_LPSTR, pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)

        # w/o embedded nulls, w/o null terminator, w/o decoder
        vts = VtString.from_stream(stream)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00c\x00d\x00e\x00")

        # w/o embedded nulls, w/o null terminator, w/decoder
        vts = VtString.from_stream(stream, 0, decoder)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "abcde")

        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        vts = VtString.from_stream(stream, 0)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00c\x00d\x00\x00\x00")

        # w/o embedded nulls, w/null terminator, w/decoder
        vts = VtString.from_stream(stream, 0, decoder)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "abcd")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        vts = VtString.from_stream(stream)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        vts = VtString.from_stream(stream, 0, decoder)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "ab")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        vts = VtString.from_stream(stream)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        vts = VtString.from_stream(stream, 0, decoder)
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "ab")


        # Now test the VT_LPWSTR test case...
        data = bytearray()
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        vts = VtString.from_stream(stream)
        ae(vts.type, 0x1F)
        ae(vts.size, 16)
        ae(vts.value, "abc")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00\x00\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        vts = VtString.from_stream(stream, 1)
        ae(vts.type, 0x1F)
        ae(vts.size, 16)
        ae(vts.value, "ab\x00")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        vts = VtString.from_stream(stream, 1)
        ae(vts.type, 0x1F)
        ae(vts.size, 16)
        ae(vts.value, "a\x00b")
    # end def test_from_stream
# end class VtStringTestCase

class VtUnalignedStringTestCase(TestCase):
    def setUp(self):
        self.obj = VtUnalignedString
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        # First the UnalignedLpstr test case...
        data = bytearray()
        data.extend(b"\x1E\x00\x64\x53")  # type == VT_LPSTR, pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)


        # w/o embedded nulls, w/o null terminator, w/o decoder
        vtuas = VtUnalignedString.from_stream(stream)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, b"a\x00b\x00c\x00d\x00e\x00")


        # w/o embedded nulls, w/o null terminator, w/decoder
        vtuas = VtUnalignedString.from_stream(stream, 0, decoder)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, "abcde")


        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        vtuas = VtUnalignedString.from_stream(stream, 0)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, b"a\x00b\x00c\x00d\x00\x00\x00")


        # w/o embedded nulls, w/null terminator, w/decoder
        vtuas = VtUnalignedString.from_stream(stream, 0, decoder)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, "abcd")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        vtuas = VtUnalignedString.from_stream(stream)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        vtuas = VtUnalignedString.from_stream(stream, 0, decoder)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, "ab")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        vtuas = VtUnalignedString.from_stream(stream)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        vtuas = VtUnalignedString.from_stream(stream, 0, decoder)
        ae(vtuas.type, 0x1E)
        ae(vtuas.size, 18)
        ae(vtuas.value, "ab")


        # Now the Lpwstr test case...
        data = bytearray()
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        vtuas = VtUnalignedString.from_stream(stream)
        ae(vtuas.type, 0x1F)
        ae(vtuas.size, 16)
        ae(vtuas.value, "abc")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00\x00\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        vtuas = VtUnalignedString.from_stream(stream, 1)
        ae(vtuas.type, 0x1F)
        ae(vtuas.size, 16)
        ae(vtuas.value, "ab\x00")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        vtuas = VtUnalignedString.from_stream(stream, 1)
        ae(vtuas.type, 0x1F)
        ae(vtuas.size, 16)
        ae(vtuas.value, "a\x00b")
    # end def test_from_stream
# end class VtUnalignedStringTestCase

class VtHeadingPairTestCase(TestCase):
    def setUp(self):
        self.obj = VtHeadingPair
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        # Check the lpstr test case..
        heading_str_data = bytearray()
        heading_str_data.extend(b"\x1E\x00\x64\x53")  # type == VT_LPSTR, pad
        heading_str_data.extend(b"\x03\x00\x00\x00")  # size
        heading_str_data.extend(b"a\x00b")  # value

        vt_i4_data = b"\x03\x00\x64\x53\x01\x02\x03\x04"

        data = b"".join([heading_str_data, vt_i4_data])
        stream = ByteIStream(data)

        vthp0 = VtHeadingPair.from_stream(stream)
        vthp1 = VtHeadingPair.from_stream(stream, 0)

        header_parts = VT_I4((3, 8, 0x04030201))
        for vthp in (vthp0, vthp1):
            ae(vthp.size, 19)
            ae(vthp.heading_str, VtUnalignedString((0x1E, 0xB, b"a\x00b")))
            ae(vthp.header_parts, header_parts)
            ae(vthp.value, vthp.heading_str)
        # end for

        vthp = VtHeadingPair.from_stream(stream, 0, decoder)
        ae(vthp.size, 19)
        ae(vthp.heading_str, VtUnalignedString((0x1E, 0xB, "a")))
        ae(vthp.header_parts, header_parts)
        ae(vthp.value, vthp.heading_str)


        # Now check the lpwstr test case...
        heading_str_data = bytearray()
        heading_str_data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        heading_str_data.extend(b"\x03\x00\x00\x00")  # count
        heading_str_data.extend(b"a\x00b\x00c\x00")  # value
        heading_str_data.extend(b"\x00\x00")  # padding

        data = b"".join([heading_str_data, vt_i4_data])
        stream = ByteIStream(data)

        vthp0 = VtHeadingPair.from_stream(stream)
        vthp1 = VtHeadingPair.from_stream(stream, 0)

        for vthp in (vthp0, vthp1):
            ae(vthp.size, 24)
            ae(vthp.heading_str, VtUnalignedString((0x1F, 0x10, "abc")))
            ae(vthp.header_parts, header_parts)
            ae(vthp.value, vthp.heading_str)
        # end for
    # end def test_from_stream
# end class VtHeadingPairTestCase

class VtVecHeadingPairValueTestCase(TestCase):
    def setUp(self):
        self.obj = VtVecHeadingPairValue
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x04\x00\x00\x00")  # count

        # First VtHeadingPair
        data.extend(b"\x1E\x00\x64\x53")  # VT_LPSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b")  # value
        data.extend(b"\x03\x00\x64\x53\x04\x03\x02\x01")  # VT_I4

        # Second VtHeadingPair
        data.extend(b"\x1F\x00\x64\x53")  # VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # char count
        data.extend(b"a\x00b\x00c\x00")  # value
        data.extend(b"\x00\x00")  # pad
        data.extend(b"\x03\x00\x64\x53\x04\x03\x02\x01")

        stream = ByteIStream(data)
        vtvhpv0 = VtVecHeadingPairValue.from_stream(stream)
        vtvhpv1 = VtVecHeadingPairValue.from_stream(stream, 0)

        header_parts = VT_I4((3, 8, 0x01020304))
        heading_str0 = VtUnalignedString((0x1E, 0xB, b"a\x00b"))
        heading_str1 = VtUnalignedString((0x1F, 0x10, "abc"))
        for vtvhpv in (vtvhpv0, vtvhpv1):
            ae(vtvhpv.size, 47)
            ae(vtvhpv.scalar_count, 4)
            ae(vtvhpv.value[0].size, 19)
            ae(vtvhpv.value[0].heading_str, heading_str0)
            ae(vtvhpv.value[0].header_parts, header_parts)
            ae(vtvhpv.value[1].size, 24)
            ae(vtvhpv.value[1].heading_str, heading_str1)
            ae(vtvhpv.value[1].header_parts, header_parts)
        # end for


        vtvhpv = VtVecHeadingPairValue.from_stream(stream, 0, decoder)
        heading_str0 = VtUnalignedString((0x1E, 0xB, "a"))
        ae(vtvhpv.size, 47)
        ae(vtvhpv.scalar_count, 4)
        ae(vtvhpv.value[0].size, 19)
        ae(vtvhpv.value[0].heading_str, heading_str0)
        ae(vtvhpv.value[0].header_parts, header_parts)
        ae(vtvhpv.value[1].size, 24)
        ae(vtvhpv.value[1].heading_str, heading_str1)
        ae(vtvhpv.value[1].header_parts, header_parts)
    # end def test_from_stream
# end class VtVecHeadingPairValueTestCase

class VtVecHeadingPairTestCase(TestCase):
    def setUp(self):
        self.obj = VtVecHeadingPair
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        decoder = codecs.getdecoder("utf_16_le")

        data = bytearray()
        data.extend(b"\x0C\x10\x64\x53")  # VT_VECTOR | VT_VARIANT
        data.extend(b"\x04\x00\x00\x00")  # count

        # First VtHeadingPair
        data.extend(b"\x1E\x00\x64\x53")  # VT_LPSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b")  # value
        data.extend(b"\x03\x00\x64\x53\x04\x03\x02\x01")  # VT_I4

        # Second VtHeadingPair
        data.extend(b"\x1F\x00\x64\x53")  # VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # char count
        data.extend(b"a\x00b\x00c\x00")  # value
        data.extend(b"\x00\x00")  # pad
        data.extend(b"\x03\x00\x64\x53\x04\x03\x02\x01")

        stream = ByteIStream(data)
        vtvhp0 = VtVecHeadingPair.from_stream(stream)
        vtvhp1 = VtVecHeadingPair.from_stream(stream, 0)
        value = VtVecHeadingPairValue.from_stream(stream, 4)

        for vtvhp in (vtvhp0, vtvhp1):
            ae(vtvhp.type, 0x100C)
            ae(vtvhp.size, 51)
            ae(vtvhp.value, value)
        # end for


        vtvhp = VtVecHeadingPair.from_stream(stream, 0, decoder)
        value = VtVecHeadingPairValue.from_stream(stream, 4, decoder)
        ae(vtvhp.type, 0x100C)
        ae(vtvhp.size, 51)
        ae(vtvhp.value, value)
    # end def test_from_stream
# end class VtVecHeadingPairTestCase

class DigSigInfoSerializedTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x03\x00\x00\x00")  # signature size
        data.extend(b"\x24\x00\x00\x00")  # sig offset
        data.extend(b"\x02\x00\x00\x00")  # signing cert store size
        data.extend(b"\x27\x00\x00\x00")  # signing cert store offset
        data.extend(b"\x04\x00\x00\x00")  # project name size
        data.extend(b"\x29\x00\x00\x00")  # project name offset
        data.extend(b"\x00\x01\x02\x03")  # timestamp
        data.extend(b"\x01\x00\x00\x00")  # timestamp_buf size
        data.extend(b"\x2D\x00\x00\x00")  # timestamp_buff offset
        data.extend(b"\x00\x01\x02")  # signature
        data.extend(b"\x03\x04")  # signing cert store
        data.extend(b"\x05\x06\x07\x08")  # project name
        data.extend(b"\x09")  # timestamp_buf
        stream = ByteIStream(data)

        dsis0 = DigSigInfoSerialized.from_stream(stream, 0)
        dsis1 = DigSigInfoSerialized.from_stream(stream, 0, 0)

        for dsis in (dsis0, dsis1):
            ae(dsis.size, 0x2E)
            ae(dsis.sig_offset, 0x24)
            ae(dsis.sig_size, 0x3)
            ae(dsis.cert_store_size, 0x2)
            ae(dsis.cert_store_offset, 0x27)
            ae(dsis.proj_name_size, 0x4)
            ae(dsis.proj_name_offset, 0x29)
            ae(dsis.timestamp, 0x03020100)
            ae(dsis.timestamp_buf_size, 0x1)
            ae(dsis.timestamp_buf_offset, 0x2D)
            ae(dsis.sig_buf, b"\x00\x01\x02")
            ae(dsis.cert_store_buf, b"\x03\x04")
            ae(dsis.proj_name_buf, "\u0605\u0807")
            ae(dsis.timestamp_buf, b"\x09")
        # end for

        data.extend(b"\x10\x11\x12")  # signature
        data.extend(b"\x13\x14")  # signing cert store
        data.extend(b"\x15\x16\x17\x18")  # project name
        data.extend(b"\x19")  # timestamp_buf
        stream = ByteIStream(data)

        dsis = DigSigInfoSerialized.from_stream(stream, 10, 0)
        ae(dsis.size, 0x38)
        ae(dsis.sig_offset, 0x24)
        ae(dsis.sig_size, 0x3)
        ae(dsis.cert_store_size, 0x2)
        ae(dsis.cert_store_offset, 0x27)
        ae(dsis.proj_name_size, 0x4)
        ae(dsis.proj_name_offset, 0x29)
        ae(dsis.timestamp, 0x03020100)
        ae(dsis.timestamp_buf_size, 0x1)
        ae(dsis.timestamp_buf_offset, 0x2D)
        ae(dsis.sig_buf, b"\x10\x11\x12")
        ae(dsis.cert_store_buf, b"\x13\x14")
        ae(dsis.proj_name_buf, "\u1615\u1817")
        ae(dsis.timestamp_buf, b"\x19")
    # end def test_from_stream
# end class DigSigInfoSerializedTestCase

class DigSigBlobTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x30\x00\x00\x00")  # size of siginfo + padding
        data.extend(b"\x08\x00\x00\x00")  # siginfo offset

        # Below is the siginfo field
        data.extend(b"\x03\x00\x00\x00")  # signature size
        data.extend(b"\x24\x00\x00\x00")  # sig offset
        data.extend(b"\x02\x00\x00\x00")  # signing cert store size
        data.extend(b"\x27\x00\x00\x00")  # signing cert store offset
        data.extend(b"\x04\x00\x00\x00")  # project name size
        data.extend(b"\x29\x00\x00\x00")  # project name offset
        data.extend(b"\x00\x01\x02\x03")  # timestamp
        data.extend(b"\x01\x00\x00\x00")  # timestamp_buf size
        data.extend(b"\x2d\x00\x00\x00")  # timestamp_buff offset
        data.extend(b"\x00\x01\x02")  # signature
        data.extend(b"\x03\x04")  # signing cert store
        data.extend(b"\x05\x06\x07\x08")  # project name
        data.extend(b"\x09")  # timestamp_buf
        stream = ByteIStream(data)

        dsb0 = DigSigBlob.from_stream(stream)
        dsb1 = DigSigBlob.from_stream(stream, 0)

        for dsb in (dsb0, dsb1):
            ae(dsb.size, 56)
            ae(dsb.sig_info_offset, 8)
            ae(dsb.sig_info, DigSigInfoSerialized.from_stream(stream, 0, 8))
            ae(dsb.value, dsb.sig_info)
        # end for
    # end def test_from_stream
# end class DigSigBlobTestCase

class VtDigSigValueTestCase(TestCase):
    def setUp(self):
        self.obj = VtDigSigValue
    # end def setup

    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        # VtDigSigValue header
        data.extend(b"\x38\x00\x00\x00")  # data size

        # DigSigBlob header
        data.extend(b"\x30\x00\x00\x00")  # siginfo + padding size
        data.extend(b"\x08\x00\x00\x00")  # siginfo offset

        # DigSigInfoSerialized
        data.extend(b"\x03\x00\x00\x00")  # signature size
        data.extend(b"\x24\x00\x00\x00")  # sig offset
        data.extend(b"\x02\x00\x00\x00")  # signing cert store size
        data.extend(b"\x27\x00\x00\x00")  # signing cert store offset
        data.extend(b"\x04\x00\x00\x00")  # project name size
        data.extend(b"\x29\x00\x00\x00")  # project name offset
        data.extend(b"\x00\x01\x02\x03")  # timestamp
        data.extend(b"\x01\x00\x00\x00")  # timestamp_buf size
        data.extend(b"\x2d\x00\x00\x00")  # timestamp_buff offset
        data.extend(b"\x00\x01\x02")  # signature
        data.extend(b"\x03\x04")  # signing cert store
        data.extend(b"\x05\x06\x07\x08")  # project name
        data.extend(b"\x09")  # timestamp_buf
        stream = ByteIStream(data)

        vtdsv0 = VtDigSigValue.from_stream(stream)
        vtdsv1 = VtDigSigValue.from_stream(stream, 0)

        for vtdsv in (vtdsv0, vtdsv1):
            ae(vtdsv.size, 56)
            ae(vtdsv.value, DigSigBlob.from_stream(stream, 4))
        # end for
    # end def test_from_stream
# end class VtDigSigValueTestCase

class VtDigSigTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        # VtDigSig header
        data.extend(b"\x41\x00\x64\x53")  # type, padding

        # VtDigSigValue header
        data.extend(b"\x38\x00\x00\x00")  # data size

        # DigSigBlob header
        data.extend(b"\x30\x00\x00\x00")  # siginfo + padding size
        data.extend(b"\x08\x00\x00\x00")  # siginfo offset

        # DigSigInfoSerialized
        data.extend(b"\x03\x00\x00\x00")  # signature size
        data.extend(b"\x24\x00\x00\x00")  # sig offset
        data.extend(b"\x02\x00\x00\x00")  # signing cert store size
        data.extend(b"\x27\x00\x00\x00")  # signing cert store offset
        data.extend(b"\x04\x00\x00\x00")  # project name size
        data.extend(b"\x29\x00\x00\x00")  # project name offset
        data.extend(b"\x00\x01\x02\x03")  # timestamp
        data.extend(b"\x01\x00\x00\x00")  # timestamp_buf size
        data.extend(b"\x2d\x00\x00\x00")  # timestamp_buff offset
        data.extend(b"\x00\x01\x02")  # signature
        data.extend(b"\x03\x04")  # signing cert store
        data.extend(b"\x05\x06\x07\x08")  # project name
        data.extend(b"\x09")  # timestamp_buf
        stream = ByteIStream(data)

        vtds0 = VtDigSig.from_stream(stream)
        vtds1 = VtDigSig.from_stream(stream, 0)

        for vtds in (vtds0, vtds1):
            ae(vtds.type, 0x41)
            ae(vtds.size, 60)
            ae(vtds.value, VtDigSigValue.from_stream(stream, 4))
        # end for
    # end def test_from_stream
# end class VtDigSigTestCase

class VtHyperlinkTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x03\x00\x64\x53\x01\x02\x03\x04")  # VT_I4 (dwHash)
        data.extend(b"\x03\x00\x64\x53\x05\x06\x07\x08")  # VT_I4 (dwapp)
        data.extend(b"\x03\x00\x64\x53\x09\x0A\x0B\x0C")  # VT_I4 (dwOfficeArt)
        data.extend(b"\x03\x00\x64\x53\x0D\x0E\x0F\x00")  # VT_I4 (dwInfo)

        # VtString (hlink1)
        data.extend(b"\x1F\x00\x64\x53")  # TPV header
        data.extend(b"\x02\x00\x00\x00")  # count of characters
        data.extend(b"a\x00b\x00")  # data

        # VtString (hlink2)
        data.extend(b"\x1E\x00\x64\x53")  # TPV header
        data.extend(b"\x04\x00\x00\x00")  # cout of characters
        data.extend(b"\x01\x02\x03\x04")  # data
        stream = ByteIStream(data)

        vth0 = VtHyperlink.from_stream(stream)
        vth1 = VtHyperlink.from_stream(stream, 0)

        for vth in (vth0, vth1):
            ae(vth.size, 56)
            ae(vth.hash, VT_I4((3, 8, 0x04030201)))
            ae(vth.app, VT_I4((3, 8, 0x08070605)))
            ae(vth.office_art, VT_I4((3, 8, 0x0C0B0A09)))
            ae(vth.info, VT_I4((3, 8, 0x000F0E0D)))
            ae(vth.hlink1, VtString((0x1F, 12, "ab")))
            ae(vth.hlink2, VtString((0x1E, 12, b"\x01\x02\x03\x04")))
            ae(vth.value, vth.hlink2)
        # end for


        decoder = codecs.getdecoder("utf_16_le")
        vth = VtHyperlink.from_stream(stream, 0, decoder)

        ae(vth.size, 56)
        ae(vth.hash, VT_I4((3, 8, 0x04030201)))
        ae(vth.app, VT_I4((3, 8, 0x08070605)))
        ae(vth.office_art, VT_I4((3, 8, 0x0C0B0A09)))
        ae(vth.info, VT_I4((3, 8, 0x000F0E0D)))
        ae(vth.hlink1, VtString((0x1F, 12, "ab")))
        ae(vth.hlink2, VtString((0x1E, 12, "\u0201\u0403")))
        ae(vth.value, vth.hlink2)
    # end def test_from_stream
# end class VtHyperlinkTestCase

class VecVtHyperlinkTestCase(TestCase):
    def setUp(self):
        self.obj = VecVtHyperlink
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x06\x00\x00\x00")  # count

        # VtHyperlink (first 4 fields)
        data.extend(b"\x03\x00\x64\x53\x01\x02\x03\x04")  # VT_I4 (dwHash)
        data.extend(b"\x03\x00\x64\x53\x05\x06\x07\x08")  # VT_I4 (dwapp)
        data.extend(b"\x03\x00\x64\x53\x09\x0A\x0B\x0C")  # VT_I4 (dwOfficeArt)
        data.extend(b"\x03\x00\x64\x53\x0D\x0E\x0F\x00")  # VT_I4 (dwInfo)

        # VtString (hlink1)
        data.extend(b"\x1F\x00\x64\x53")  # TPV header
        data.extend(b"\x02\x00\x00\x00")  # count of characters
        data.extend(b"a\x00b\x00")  # data

        # VtString (hlink2)
        data.extend(b"\x1E\x00\x64\x53")  # TPV header
        data.extend(b"\x04\x00\x00\x00")  # cout of characters
        data.extend(b"\x01\x02\x03\x04")  # data
        stream = ByteIStream(data)

        vvth0 = VecVtHyperlink.from_stream(stream)
        vvth1 = VecVtHyperlink.from_stream(stream, 0)

        vth = VtHyperlink((
            56,
            VT_I4((3, 8, 0x04030201)),
            VT_I4((3, 8, 0x08070605)),
            VT_I4((3, 8, 0x0C0B0A09)),
            VT_I4((3, 8, 0x000F0E0D)),
            VtString((0x1F, 12, "ab")),
            VtString((0x1E, 12, b"\x01\x02\x03\x04")),
        ))

        for vvth in (vvth0, vvth1):
            ae(vvth.size, 60)
            ae(vvth.scalar_count, 6)
            ae(len(vvth.hyperlinks), 1)
            ae(vvth.hyperlinks[0], vth)
            ae(vvth.hyperlinks[0].value, vvth.value[0].hlink2)
            ae(vvth.value, vvth.hyperlinks)
        # end for


        vth = VtHyperlink((
            56,
            VT_I4((3, 8, 0x04030201)),
            VT_I4((3, 8, 0x08070605)),
            VT_I4((3, 8, 0x0C0B0A09)),
            VT_I4((3, 8, 0x000F0E0D)),
            VtString((0x1F, 12, "ab")),
            VtString((0x1E, 12, "\u0201\u0403")),
        ))

        decoder = codecs.getdecoder("utf_16_le")
        vvth = VecVtHyperlink.from_stream(stream, 0, decoder)

        ae(vvth.size, 60)
        ae(vvth.scalar_count, 6)
        ae(len(vvth.hyperlinks), 1)
        ae(vvth.hyperlinks[0], vth)
        ae(vvth.value, vvth.hyperlinks)
    # end def test_from_stream
# end class VecVtHyperlinkTestCase

class VtHyperlinkValueTestCase(TestCase):
    def setUp(self):
        self.obj = VtHyperlinkValue
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x3C\x00\x00\x00")

        # VecVtHyperlink header
        data.extend(b"\x06\x00\x00\x00")  # count

        # VtHyperlink (first 4 fields)
        data.extend(b"\x03\x00\x64\x53\x01\x02\x03\x04")  # VT_I4 (dwHash)
        data.extend(b"\x03\x00\x64\x53\x05\x06\x07\x08")  # VT_I4 (dwapp)
        data.extend(b"\x03\x00\x64\x53\x09\x0A\x0B\x0C")  # VT_I4 (dwOfficeArt)
        data.extend(b"\x03\x00\x64\x53\x0D\x0E\x0F\x00")  # VT_I4 (dwInfo)

        # VtString (hlink1)
        data.extend(b"\x1F\x00\x64\x53")  # TPV header
        data.extend(b"\x02\x00\x00\x00")  # count of characters
        data.extend(b"a\x00b\x00")  # data

        # VtString (hlink2)
        data.extend(b"\x1E\x00\x64\x53")  # TPV header
        data.extend(b"\x04\x00\x00\x00")  # cout of characters
        data.extend(b"\x01\x02\x03\x04")  # data
        stream = ByteIStream(data)

        vthv0 = VtHyperlinkValue.from_stream(stream)
        vthv1 = VtHyperlinkValue.from_stream(stream, 0)

        vth = VtHyperlink((
            56,
            VT_I4((3, 8, 0x04030201)),
            VT_I4((3, 8, 0x08070605)),
            VT_I4((3, 8, 0x0C0B0A09)),
            VT_I4((3, 8, 0x000F0E0D)),
            VtString((0x1F, 12, "ab")),
            VtString((0x1E, 12, b"\x01\x02\x03\x04"))
        ))

        for vthv in (vthv0, vthv1):
            ae(vthv.size, 64)
            ae(vthv.hyperlinks.size, 60)
            ae(vthv.hyperlinks.scalar_count, 6)
            ae(len(vthv.hyperlinks.hyperlinks), 1)
            ae(vthv.hyperlinks.hyperlinks[0], vth)
            ae(vthv.hyperlinks.hyperlinks[0].value, vthv.value.value[0].hlink2)
            ae(vthv.value, vthv.hyperlinks)
        # end for


        decoder = codecs.getdecoder("utf_16_le")
        vthv = VtHyperlinkValue.from_stream(stream, 0, decoder)

        vth = VtHyperlink((
            56,
            VT_I4((3, 8, 0x04030201)),
            VT_I4((3, 8, 0x08070605)),
            VT_I4((3, 8, 0x0C0B0A09)),
            VT_I4((3, 8, 0x000F0E0D)),
            VtString((0x1F, 12, "ab")),
            VtString((0x1E, 12, "\u0201\u0403"))
        ))

        ae(vthv.size, 64)
        ae(vthv.hyperlinks.scalar_count, 6)
        ae(vthv.hyperlinks.size, 60)
        ae(len(vthv.hyperlinks.hyperlinks), 1)
        ae(vthv.hyperlinks.hyperlinks[0], vth)
        ae(vthv.hyperlinks.hyperlinks[0].value, vthv.value.value[0].hlink2)
        ae(vthv.value, vthv.hyperlinks)
    # end def test_from_stream
# end class VtHyperlinkValueTestCase

class VtHyperlinksTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()

        data.extend(b"\x41\x00\x64\x53")  # VT_BLOB, pad

        # VtHyperlinkValue header
        data.extend(b"\x3C\x00\x00\x00")  # size in bytes

        # VecVtHyperlink header
        data.extend(b"\x06\x00\x00\x00")  # count

        # VtHyperlink (first 4 fields)
        data.extend(b"\x03\x00\x64\x53\x01\x02\x03\x04")  # VT_I4 (dwHash)
        data.extend(b"\x03\x00\x64\x53\x05\x06\x07\x08")  # VT_I4 (dwapp)
        data.extend(b"\x03\x00\x64\x53\x09\x0A\x0B\x0C")  # VT_I4 (dwOfficeArt)
        data.extend(b"\x03\x00\x64\x53\x0D\x0E\x0F\x00")  # VT_I4 (dwInfo)

        # VtString (hlink1)
        data.extend(b"\x1F\x00\x64\x53")  # TPV header
        data.extend(b"\x02\x00\x00\x00")  # count of characters
        data.extend(b"a\x00b\x00")  # data

        # VtString (hlink2)
        data.extend(b"\x1E\x00\x64\x53")  # TPV header
        data.extend(b"\x04\x00\x00\x00")  # cout of characters
        data.extend(b"\x01\x02\x03\x04")  # data
        stream = ByteIStream(data)

        vth0 = VtHyperlinks.from_stream(stream)
        vth1 = VtHyperlinks.from_stream(stream, 0)
        value = VtHyperlinkValue.from_stream(stream, 4)

        for vth in (vth0, vth1):
            ae(vth.type, 0x41)
            ae(vth.size, 68)
            ae(vth.value, value)
        # end for


        decoder = codecs.getdecoder("utf_16_le")
        vth = VtHyperlinks.from_stream(stream, 0, decoder)
        value = VtHyperlinkValue.from_stream(stream, 4, decoder)

        ae(vth.type, 0x41)
        ae(vth.size, 68)
        ae(vth.value, value)
    # end def test_from_stream
# end class VtHyperlinksTestCase

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

        ae(pss0.sys_id.os_ver_major, 0x04)
        ae(pss0.sys_id.os_ver_minor, 0x05)
        ae(pss0.sys_id.os_type, 0x0706)
        ae(pss1.sys_id.os_ver_major, 0x04)
        ae(pss1.sys_id.os_ver_minor, 0x05)
        ae(pss1.sys_id.os_type, 0x0706)

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

class PropertyFactoryTestCase(TestCase):
    def test_make(self):
        ae = self.assertEqual
        at = self.assertTrue
        decoder = codecs.getdecoder("utf_16_le")

        # First test the VT_LPSTR test case...
        data = bytearray()
        data.extend(b"\x1E\x00\x64\x53")  # type == VT_LPSTR, pad
        data.extend(b"\x0A\x00\x00\x00")  # size == 10
        data.extend(b"a\x00b\x00c\x00d\x00e\x00")  # characters
        stream = ByteIStream(data)

        # w/o embedded nulls, w/o null terminator, w/o decoder
        vts = PropertyFactory.make(stream)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00c\x00d\x00e\x00")

        # w/o embedded nulls, w/o null terminator, w/decoder
        vts = PropertyFactory.make(stream, 0, decoder)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "abcde")

        # w/o embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00c\x00d\x00\x00\x00"
        stream = ByteIStream(data)

        vts = PropertyFactory.make(stream, 0)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00c\x00d\x00\x00\x00")

        # w/o embedded nulls, w/null terminator, w/decoder
        vts = PropertyFactory.make(stream, 0, decoder)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "abcd")


        # w/embedded nulls, w/o null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00d\x00"
        stream = ByteIStream(data)

        vts = PropertyFactory.make(stream)
        ae(vts.type, 0x1E)
        at(isinstance(vts, VtString))
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00\x00\x00c\x00d\x00")


        # w/embedded nulls, w/o null terminator, w/decoder
        vts = PropertyFactory.make(stream, 0, decoder)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "ab")


        # w/embedded nulls, w/null terminator, w/o decoder
        data[8:] = b"a\x00b\x00\x00\x00c\x00\x00\x00"
        stream = ByteIStream(data)

        vts = PropertyFactory.make(stream)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, b"a\x00b\x00\x00\x00c\x00\x00\x00")


        # w/embedded nulls, w/null terminator, w/decoder
        vts = PropertyFactory.make(stream, 0, decoder)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1E)
        ae(vts.size, 20)
        ae(vts.value, "ab")


        # Now test the VT_LPWSTR test case...
        data = bytearray()
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00c\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        vts = PropertyFactory.make(stream)
        ae(vts.type, 0x1F)
        at(isinstance(vts, VtString))
        ae(vts.size, 16)
        ae(vts.value, "abc")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00b\x00\x00\x00\x00\x00")  # characters
        stream = ByteIStream(data)

        vts = PropertyFactory.make(stream, 1)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1F)
        ae(vts.size, 16)
        ae(vts.value, "ab\x00")


        data = bytearray()
        data.extend(b"\x01")  # padding
        data.extend(b"\x1F\x00\x64\x53")  # type == VT_LPWSTR, pad
        data.extend(b"\x03\x00\x00\x00")  # size
        data.extend(b"a\x00\x00\x00b\x00\xFF\xFF")  # characters
        stream = ByteIStream(data)

        vts = PropertyFactory.make(stream, 1)
        at(isinstance(vts, VtString))
        ae(vts.type, 0x1F)
        ae(vts.size, 16)
        ae(vts.value, "a\x00b")
    # end def test_make
# end class PropertyFactoryTestCase

class BuilderTestCase(TestCase):
    def setUp(self):
        blair_path = join("data", "doc", "blair.doc")
        sample_path = join("data", "doc", "sample.doc")

        blair_cfb = CompoundFile(RawIStream(blair_path))
        sample_cfb = CompoundFile(RawIStream(sample_path))

        self.blair_si_stream = blair_cfb.get_stream(3)
        self.sample_si_stream = sample_cfb.get_stream(39)
        self.blair_dsi_stream = blair_cfb.get_stream(4)
        self.sample_dsi_stream = sample_cfb.get_stream(40)
    # end def setUp

    def test_build_property_set_stream_header(self):
        ae = self.assertEqual

        data0 = bytearray([x for x in range(48)])
        data1 = bytes([x for x in range(68)])

        data0[24:28] = b"\x01\x00\x00\x00"

        pss0 = Builder.build_property_set_stream_header(ByteIStream(data0), 0)
        pss1 = Builder.build_property_set_stream_header(ByteIStream(data1))

        ae(pss0, PropertySetStreamHeader.from_stream(ByteIStream(data0)))
        ae(pss1, PropertySetStreamHeader.from_stream(ByteIStream(data1)))
    # end def test_build_property_set_stream_header

    def test_build_summary_info_properties(self):
        ae = self.assertEqual

        blair_si_stream = self.blair_si_stream
        sample_si_stream = self.sample_si_stream

        blair_props = list()
        sample_props = list()

        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VtString((
                0x1E,
                76,
                "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND"
                " INTIMIDATION"
            )),
            3: VtString((0x1E, 12,"")),
            4: VtString((0x1E, 16, "default")),
            5: VtString((0x1E, 12, "")),
            6: VtString((0x1E, 12, "")),
            7: VtString((0x1E, 20, "Normal.dot")),
            8: VtString((0x1E, 16, "MKhan")),
            9: VtString((0x1E, 12, "4")),
            18: VtString((0x1E, 28, "Microsoft Word 8.0")),
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
            Builder.build_property_set_header(blair_si_stream, None, 48)
        blair_properties = Builder.build_summary_info_properties(
            blair_si_stream, None, blair_property_set_header, 48
        )

        ae(blair_properties, control_properties)


        sample_si_stream.seek(0x1F8, SEEK_SET)
        cf_data = sample_si_stream.read(0x0254A6)
        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VtString((0x1E, 20, "title_value")),
            3: VtString((0x1E, 24, "subject_value")),
            4: VtString((0x1E, 24, "author_value")),
            5: VtString((0x1E, 28, "keyword0 keyword1")),
            6: VtString((0x1E, 40, "Comments in the comments box")),
            7: VtString((0x1E, 16, "Normal")),
            8: VtString((0x1E, 16, "lftest2")),
            9: VtString((0x1E, 12, "24")),
            0x12: VtString((0x1E, 32, "Microsoft Office Word")),
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
            0x11: VtThumbnail((
                0x47,
                0x0254B8,
                VtThumbnailValue((
                    0x0254B4,
                    cf_data,
                    0xFFFFFFFF,
                    0x3
                ))
            ))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_si_stream, None, 48
        )
        sample_properties = Builder.build_summary_info_properties(
            sample_si_stream, None, sample_property_set_header, 48
        )
        ae(sample_properties, control_properties)
    # end def test_build_summary_info_properties

    def test_build_doc_summary_info_properties(self):
        ae = self.assertEqual

        blair_dsi_stream = self.blair_dsi_stream
        sample_dsi_stream = self.sample_dsi_stream

        blair_props = list()
        sample_props = list()

        control_properties = {
            0x1: VT_I2((2, 8, 0x4E4)),
            0xF: VtString((0x1E, 16, "default")),
            0x5: VT_I4((3, 8, 0xB8)),
            0x6: VT_I4((3, 8, 0x2C)),
            0x11: VT_I4((3, 8, 0x69F8)),
            0x17: VT_I4((3, 8, 0x81531)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),
            0xD: VtVecUnalignedLpstr((
                0x101E,
                0x50,
                VtVecUnalignedLpstrValue((
                    0x4C,
                    1,
                    [
                        UnalignedLpstr((
                            0x48,
                            "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, "
                            "DECEPTION AND INTIMIDATION"
                        ))
                    ]
                ))
            )),
            0xC: VtVecHeadingPair((
                0x100C,
                30,
                VtVecHeadingPairValue((
                    26,
                    2,
                    [
                        VtHeadingPair((
                            22,
                            VtUnalignedString((0x1E, 0xE, "Title")),
                            VT_I4((3, 8, 1))
                        ))
                    ]
                ))
            ))
        }

        blair_property_set_header = \
            Builder.build_property_set_header(blair_dsi_stream, None, 68)
        blair_properties = Builder.build_doc_summary_info_properties(
            blair_dsi_stream, None, blair_property_set_header, 68
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
            Builder.build_property_set_header(blair_dsi_stream, None, 372)
        blair_properties = Builder.build_doc_summary_info_properties(
            blair_dsi_stream, None, blair_property_set_header, 372
        )
        ae(blair_properties, control_properties)


        sample_dsi_stream.seek(0x445, SEEK_SET)
        blob_data0 = sample_dsi_stream.read(0x2A)

        sample_dsi_stream.seek(0x479, SEEK_SET)
        blob_data1 = sample_dsi_stream.read(0x4A4)

        control_properties = {
            1: VT_I2((2, 8, 1252)),
            2: VtString((0x1E, 24, "category_value")),
            0xE: VtString((0x1E, 24, "manager_value")),
            0xF: VtString((0x1E, 24, "company_value")),
            0x1B: VtString((0x1E, 24, "status_value")),
            5: VT_I4((3, 8, 0x55)),
            6: VT_I4((3, 8, 0x1D)),
            0x11: VT_I4((3, 8, 0x5DD)),
            0x17: VT_I4((3, 8, 0x0C0000)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),
            0xD: VtVecUnalignedLpstr((
                0x101E,
                0x53,
                VtVecUnalignedLpstrValue((
                    0x4F,
                    5,
                    [
                        UnalignedLpstr((0x10, "title_value")),
                        UnalignedLpstr((5, "")),
                        UnalignedLpstr((0x10, "TOC Entry 1")),
                        UnalignedLpstr((0x16, "    TOC Entry 1.1")),
                        UnalignedLpstr((0x10, "TOC Entry 2")),
                    ]
                ))
            )),
            0xC: VtVecHeadingPair((
                0x100C,
                0x37,
                VtVecHeadingPairValue((
                    0x33,
                    4,
                    [
                        VtHeadingPair((
                            0x16,
                            VtUnalignedString((0x1E, 0xE, "Title")),
                            VT_I4((3, 8, 1))
                        )),
                        VtHeadingPair((
                            0x19,
                            VtUnalignedString((0x1E, 0x11, "Headings")),
                            VT_I4((3, 8, 4))
                        ))
                    ]
                ))
            ))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_dsi_stream, None, 68
        )
        sample_properties = Builder.build_doc_summary_info_properties(
            sample_dsi_stream, None, sample_property_set_header, 68
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
            4: VtString((0x1E, 20, "text_value")),
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
            0x10: VtString((0x1E, 12, "")),
            0x1000010: VtString((0x1E, 24, "bookmark_name1")),
            0x11: VtString((0x1E, 12, "")),
            0x1000011: VtString((0x1E, 24, "bookmark_name2")),
            0x12: VtString((0x1E, 12, "")),
            0x1000012: VtString((0x1E, 20, "_1326562448"))

        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_dsi_stream, None, 0x1F8
        )
        sample_properties = Builder.build_doc_summary_info_properties(
            sample_dsi_stream, None, sample_property_set_header, 0x1F8
        )
        ae(sample_properties, control_properties)
    # end def test_build_doc_summary_info_properties

    def test_build_properties(self):
        ae = self.assertEqual

        # Test the SummaryInfo stream...
        blair_si_stream = self.blair_si_stream
        sample_si_stream = self.sample_si_stream

        blair_props = list()
        sample_props = list()

        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VtString((
                0x1E,
                76,
                "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND"
                " INTIMIDATION"
            )),
            3: VtString((0x1E, 12,"")),
            4: VtString((0x1E, 16, "default")),
            5: VtString((0x1E, 12, "")),
            6: VtString((0x1E, 12, "")),
            7: VtString((0x1E, 20, "Normal.dot")),
            8: VtString((0x1E, 16, "MKhan")),
            9: VtString((0x1E, 12, "4")),
            18: VtString((0x1E, 28, "Microsoft Word 8.0")),
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

        blair_property_set_header = Builder.build_property_set_header(
            blair_si_stream, None, 48
        )
        blair_properties = Builder.build_properties(
            blair_si_stream,
            FMTID_SummaryInformation,
            blair_property_set_header,
            48
        )
        ae(blair_properties, control_properties)


        sample_si_stream.seek(0x1F8, SEEK_SET)
        cf_data = sample_si_stream.read(0x0254A6)
        control_properties = {
            1: VT_I2((2, 8, 0x4E4)),
            2: VtString((0x1E, 20, "title_value")),
            3: VtString((0x1E, 24, "subject_value")),
            4: VtString((0x1E, 24, "author_value")),
            5: VtString((0x1E, 28, "keyword0 keyword1")),
            6: VtString((0x1E, 40, "Comments in the comments box")),
            7: VtString((0x1E, 16, "Normal")),
            8: VtString((0x1E, 16, "lftest2")),
            9: VtString((0x1E, 12, "24")),
            0x12: VtString((0x1E, 32, "Microsoft Office Word")),
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
            0x11: VtThumbnail((
                0x47,
                0x0254B8,
                VtThumbnailValue((
                    0x0254B4,
                    cf_data,
                    0xFFFFFFFF,
                    0x3
                ))
            ))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_si_stream, None, 48
        )
        sample_properties = Builder.build_properties(
            sample_si_stream,
            FMTID_SummaryInformation,
            sample_property_set_header,
            48
        )
        ae(sample_properties, control_properties)


        # Now test the DocSummaryInfo streams...
        blair_dsi_stream = self.blair_dsi_stream
        sample_dsi_stream = self.sample_dsi_stream

        control_properties = {
            0x1: VT_I2((2, 8, 0x4E4)),
            0xF: VtString((0x1E, 16, "default")),
            0x5: VT_I4((3, 8, 0xB8)),
            0x6: VT_I4((3, 8, 0x2C)),
            0x11: VT_I4((3, 8, 0x69F8)),
            0x17: VT_I4((3, 8, 0x81531)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),
            0xD: VtVecUnalignedLpstr((
                0x101E,
                0x50,
                VtVecUnalignedLpstrValue((
                    0x4C,
                    1,
                    [
                        UnalignedLpstr((
                            0x48,
                            "Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, "
                            "DECEPTION AND INTIMIDATION"
                        ))
                    ]
                ))
            )),
            0xC: VtVecHeadingPair((
                0x100C,
                30,
                VtVecHeadingPairValue((
                    26,
                    2,
                    [
                        VtHeadingPair((
                            22,
                            VtUnalignedString((0x1E, 0xE, "Title")),
                            VT_I4((3, 8, 1))
                        ))
                    ]
                ))
            ))
        }

        blair_property_set_header = \
            Builder.build_property_set_header(blair_dsi_stream, None, 68)
        blair_properties = Builder.build_properties(
            blair_dsi_stream,
            FMTID_DocSummaryInformation,
            blair_property_set_header,
            68
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
            Builder.build_property_set_header(blair_dsi_stream, None, 372)
        blair_properties = Builder.build_properties(
            blair_dsi_stream,
            FMTID_DocSummaryInformation,
            blair_property_set_header,
            372
        )
        ae(blair_properties, control_properties)


        sample_dsi_stream.seek(0x445, SEEK_SET)
        blob_data0 = sample_dsi_stream.read(0x2A)

        sample_dsi_stream.seek(0x479, SEEK_SET)
        blob_data1 = sample_dsi_stream.read(0x4A4)

        control_properties = {
            1: VT_I2((2, 8, 1252)),
            2: VtString((0x1E, 24, "category_value")),
            0xE: VtString((0x1E, 24, "manager_value")),
            0xF: VtString((0x1E, 24, "company_value")),
            0x1B: VtString((0x1E, 24, "status_value")),
            5: VT_I4((3, 8, 0x55)),
            6: VT_I4((3, 8, 0x1D)),
            0x11: VT_I4((3, 8, 0x5DD)),
            0x17: VT_I4((3, 8, 0x0C0000)),
            0xB: VT_BOOL((11, 8, 0)),
            0x10: VT_BOOL((11, 8, 0)),
            0x13: VT_BOOL((11, 8, 0)),
            0x16: VT_BOOL((11, 8, 0)),
            0xD: VtVecUnalignedLpstr((
                0x101E,
                0x53,
                VtVecUnalignedLpstrValue((
                    0x4F,
                    5,
                    [
                        UnalignedLpstr((0x10, "title_value")),
                        UnalignedLpstr((5, "")),
                        UnalignedLpstr((0x10, "TOC Entry 1")),
                        UnalignedLpstr((0x16, "    TOC Entry 1.1")),
                        UnalignedLpstr((0x10, "TOC Entry 2")),
                    ]
                ))
            )),
            0xC: VtVecHeadingPair((
                0x100C,
                0x37,
                VtVecHeadingPairValue((
                    0x33,
                    4,
                    [
                        VtHeadingPair((
                            0x16,
                            VtUnalignedString((0x1E, 0xE, "Title")),
                            VT_I4((3, 8, 1))
                        )),
                        VtHeadingPair((
                            0x19,
                            VtUnalignedString((0x1E, 0x11, "Headings")),
                            VT_I4((3, 8, 4))
                        ))
                    ]
                ))
            ))
        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_dsi_stream, None, 68
        )
        sample_properties = Builder.build_properties(
            sample_dsi_stream,
            FMTID_DocSummaryInformation,
            sample_property_set_header,
            68
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
            4: VtString((0x1E, 20, "text_value")),
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
            0x10: VtString((0x1E, 12, "")),
            0x1000010: VtString((0x1E, 24, "bookmark_name1")),
            0x11: VtString((0x1E, 12, "")),
            0x1000011: VtString((0x1E, 24, "bookmark_name2")),
            0x12: VtString((0x1E, 12, "")),
            0x1000012: VtString((0x1E, 20, "_1326562448"))

        }

        sample_property_set_header = Builder.build_property_set_header(
            sample_dsi_stream, None, 0x1F8
        )
        sample_properties = Builder.build_properties(
            sample_dsi_stream,
            FMTID_DocSummaryInformation,
            sample_property_set_header,
            0x1F8
        )
        ae(sample_properties, control_properties)
    # end def test_build_properties
# end class BuilderTestCase
