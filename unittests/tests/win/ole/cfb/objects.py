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

"""Unit tests for the lf.win.ole.cfb.objects module."""

# stdlib imports
from unittest import TestCase
from uuid import UUID
from time import ctime
from datetime import datetime
from os.path import join
from struct import pack, unpack

# local imports
from lf.dec import (
    RawIStream, ByteIStream, SubsetIStream, CompositeIStream, SEEK_SET
)
from lf.time import FILETIMETodatetime

from lf.win.ole.cfb.objects import (
    CompoundFile, DirEntry, Header
)
from lf.win.ole.cfb.consts import (
    HEADER_SIG, STREAM_ID_NONE, FAT_EOC
)

utcfromtimestamp = datetime.utcfromtimestamp

__docformat__ = "restructuredtext en"
__all__ = [
    "HeaderTestCase", "DirEntryTestCase", "CompoundFileTestCase"
]

class HeaderTestCase(TestCase):
    def setUp(self):
        data1 = b"".join([pack("B", x % 256) for x in range(4096)])
        data2 = b"".join([b"junk", data1])

        self.stream1 = ByteIStream(data1)
        self.stream2 = ByteIStream(data2)
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        header1 = Header.from_stream(self.stream1)
        header2 = Header.from_stream(self.stream2, 4)

        di_fat = unpack(
            "109I",
            b"".join([pack("B", x % 256) for x in range(0x4C, 0x200)])
        )

        ae(header1.sig, b"\x00\x01\x02\x03\x04\x05\x06\x07")
        ae(header2.sig, b"\x00\x01\x02\x03\x04\x05\x06\x07")

        clsid = UUID(
            bytes_le =
            b"\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17"
        )

        ae(header1.clsid, clsid)
        ae(header2.clsid, clsid)

        ae(header1.ver_minor, 0x1918)
        ae(header2.ver_minor, 0x1918)

        ae(header1.ver_major, 0x1B1A)
        ae(header2.ver_major, 0x1B1A)

        ae(header1.byte_order, 0x1D1C)
        ae(header2.byte_order, 0x1D1C)

        ae(header1.sect_shift, 0x1F1E)
        ae(header2.sect_shift, 0x1F1E)

        ae(header1.mini_sect_shift, 0x2120)
        ae(header2.mini_sect_shift, 0x2120)

        ae(header1.rsvd, b"\x22\x23\x24\x25\x26\x27")
        ae(header2.rsvd, b"\x22\x23\x24\x25\x26\x27")

        ae(header1.dir_sect_count, 0x2B2A2928)
        ae(header2.dir_sect_count, 0x2B2A2928)

        ae(header1.fat_sect_count, 0x2F2E2D2C)
        ae(header2.fat_sect_count, 0x2F2E2D2C)

        ae(header1.dir_sect_offset, 0x33323130)
        ae(header2.dir_sect_offset, 0x33323130)

        ae(header1.trans_num, 0x37363534)
        ae(header2.trans_num, 0x37363534)

        ae(header1.mini_stream_cutoff, 0x3B3A3938)
        ae(header2.mini_stream_cutoff, 0x3B3A3938)

        ae(header1.mini_fat_sect_offset, 0x3F3E3D3C)
        ae(header2.mini_fat_sect_offset, 0x3F3E3D3C)

        ae(header1.mini_fat_sect_count, 0x43424140)
        ae(header2.mini_fat_sect_count, 0x43424140)

        ae(header1.di_fat_sect_offset, 0x47464544)
        ae(header2.di_fat_sect_offset, 0x47464544)

        ae(header1.di_fat_sect_count, 0x4B4A4948)
        ae(header2.di_fat_sect_count, 0x4B4A4948)

        ae(header1.di_fat, list(di_fat))
        ae(header2.di_fat, list(di_fat))
    # end def test_from_stream
# end class HeaderTestCase

class DirEntryTestCase(TestCase):
    def setUp(self):
        name = ("abcdefghijklmnop" * 2).encode("utf_16_le")
        name_size = b"\x40\x00"
        bogus_name_size = b"\xFF\xFF"

        btime = b"\x00\x0E\x15\x91\xC4\x95\xC2\x01"
        mtime = b"\x90\xCB\xAE\x00\x51\x69\xC5\x01"

        data1 = bytearray(b"".join([pack("B", x) for x in range(128)]))
        data2 = bytearray(b"".join([b"junk", data1]))

        data1[0:64] = name
        data1[64:66] = name_size
        data1[100:108] = btime
        data1[108:116] = mtime

        data2[4:68] = name
        data2[68:70] = bogus_name_size
        data2[104:112] = btime
        data2[112:120] = mtime

        self.stream1 = ByteIStream(data1)
        self.stream2 = ByteIStream(data2)
    # end def setUp

    def test_from_stream(self):
        ae = self.assertEqual
        de1 = DirEntry.from_stream(self.stream1)
        de2 = DirEntry.from_stream(self.stream2, 4)

        ae(de1.name, "abcdefghijklmnop" * 2)
        ae(de2.name, "abcdefghijklmnop" * 2)

        ae(de1.name_size, 0x40)
        ae(de2.name_size, 0xFFFF)

        ae(de1.type, 0x42)
        ae(de2.type, 0x42)

        ae(de1.color, 0x43)
        ae(de2.color, 0x43)

        ae(de1.left_sid, 0x47464544)
        ae(de2.left_sid, 0x47464544)

        ae(de1.right_sid, 0x4B4A4948)
        ae(de2.right_sid, 0x4B4A4948)

        ae(de1.child_sid, 0x4F4E4D4C)
        ae(de2.child_sid, 0x4F4E4D4C)

        guid = UUID(
            bytes_le=
            b"\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F"
        )

        ae(de1.clsid, guid)
        ae(de2.clsid, guid)

        ae(de1.state, 0x63626160)
        ae(de2.state, 0x63626160)

        ae(de1.btime, datetime(2002, 11, 27, 3, 25))
        ae(de2.btime, datetime(2002, 11, 27, 3, 25))

        ae(de1.mtime, datetime(2005, 6, 4, 22, 1, 47, 465000))
        ae(de2.mtime, datetime(2005, 6, 4, 22, 1, 47, 465000))

        ae(de1.stream_sect_offset, 0x77767574)
        ae(de2.stream_sect_offset, 0x77767574)

        ae(de1.stream_size, 0x7F7E7D7C7B7A7978)
        ae(de2.stream_size, 0x7F7E7D7C7B7A7978)
    # end def test_from_stream
# end class DirEntryTestCase

class CompoundFileTestCase(TestCase):
    def setUp(self):
        sample_doc_path = ["data", "doc", "sample.doc"]
        blair_doc_path = ["data", "doc", "blair.doc"]

        sample_doc_stream = RawIStream(join(*sample_doc_path))
        blair_doc_stream = RawIStream(join(*blair_doc_path))

        self.sample_doc_stream = sample_doc_stream
        self.blair_doc_stream = blair_doc_stream
        self.sample_doc = CompoundFile(sample_doc_stream)
        self.blair_doc = CompoundFile(blair_doc_stream)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        at = self.assertTrue

        sample_doc = self.sample_doc
        blair_doc = self.blair_doc

        ae(sample_doc.ver_major, 0x3)
        ae(blair_doc.ver_major, 0x3)

        ae(sample_doc.ver_minor, 0x3E)
        ae(blair_doc.ver_minor, 0x3E)

        at(hasattr(sample_doc, "header"))
        at(hasattr(blair_doc, "header"))

        ae(sample_doc.header.sig, HEADER_SIG)
        ae(blair_doc.header.sig, HEADER_SIG)

        ae(sample_doc.header.clsid, UUID(int=0))
        ae(blair_doc.header.clsid, UUID(int=0))

        ae(sample_doc.header.ver_minor, 0x3E)
        ae(blair_doc.header.ver_minor, 0x3E)

        ae(sample_doc.header.ver_major, 0x3)
        ae(blair_doc.header.ver_major, 0x3)

        ae(sample_doc.header.byte_order, 0xFFFE)
        ae(blair_doc.header.byte_order, 0xFFFE)

        ae(sample_doc.header.sect_shift, 9)
        ae(blair_doc.header.sect_shift, 9)

        ae(sample_doc.header.mini_sect_shift, 6)
        ae(blair_doc.header.mini_sect_shift, 6)

        ae(sample_doc.header.rsvd, b"\x00\x00\x00\x00\x00\x00")
        ae(blair_doc.header.rsvd, b"\x00\x00\x00\x00\x00\x00")

        ae(sample_doc.header.dir_sect_count, 0)
        ae(blair_doc.header.dir_sect_count, 0)

        ae(sample_doc.header.fat_sect_count, 0x87)
        ae(blair_doc.header.fat_sect_count, 1)

        ae(sample_doc.header.dir_sect_offset, 0x3433)
        ae(blair_doc.header.dir_sect_offset, 0x7A)

        ae(sample_doc.header.trans_num, 0)
        ae(blair_doc.header.trans_num, 0)

        ae(sample_doc.header.mini_stream_cutoff, 0x1000)
        ae(blair_doc.header.mini_stream_cutoff, 0x1000)

        ae(sample_doc.header.mini_fat_sect_offset, 0x3435)
        ae(blair_doc.header.mini_fat_sect_offset, 0x7C)

        ae(sample_doc.header.mini_fat_sect_count, 3)
        ae(blair_doc.header.mini_fat_sect_count, 1)

        ae(sample_doc.header.di_fat_sect_offset, 0x3657)
        ae(blair_doc.header.di_fat_sect_offset, 0xFFFFFFFE)

        ae(sample_doc.header.di_fat_sect_count, 1)
        ae(blair_doc.header.di_fat_sect_count, 0)

        sample_di_fat_data = ( b"\xCA\x33\x00\x00"
            b"\xCB\x33\x00\x00\xCC\x33\x00\x00\xCD\x33\x00\x00\xCE\x33\x00\x00"
            b"\xCF\x33\x00\x00\xD0\x33\x00\x00\xD1\x33\x00\x00\xD2\x33\x00\x00"
            b"\xD3\x33\x00\x00\xD4\x33\x00\x00\xD5\x33\x00\x00\xD6\x33\x00\x00"
            b"\xD7\x33\x00\x00\xD8\x33\x00\x00\xD9\x33\x00\x00\xDA\x33\x00\x00"
            b"\xDB\x33\x00\x00\xDC\x33\x00\x00\xDD\x33\x00\x00\xDE\x33\x00\x00"
            b"\xDF\x33\x00\x00\xE0\x33\x00\x00\xE1\x33\x00\x00\xE2\x33\x00\x00"
            b"\xE3\x33\x00\x00\xE4\x33\x00\x00\xE5\x33\x00\x00\xE6\x33\x00\x00"
            b"\xE7\x33\x00\x00\xE8\x33\x00\x00\xE9\x33\x00\x00\xEA\x33\x00\x00"
            b"\xEB\x33\x00\x00\xEC\x33\x00\x00\xED\x33\x00\x00\xEE\x33\x00\x00"
            b"\xEF\x33\x00\x00\xF0\x33\x00\x00\xF1\x33\x00\x00\xF2\x33\x00\x00"
            b"\xF3\x33\x00\x00\xF4\x33\x00\x00\xF5\x33\x00\x00\xF6\x33\x00\x00"
            b"\xF7\x33\x00\x00\xF8\x33\x00\x00\xF9\x33\x00\x00\xFA\x33\x00\x00"
            b"\xFB\x33\x00\x00\xFC\x33\x00\x00\xFD\x33\x00\x00\xFE\x33\x00\x00"
            b"\xFF\x33\x00\x00\x00\x34\x00\x00\x01\x34\x00\x00\x02\x34\x00\x00"
            b"\x03\x34\x00\x00\x04\x34\x00\x00\x05\x34\x00\x00\x06\x34\x00\x00"
            b"\x07\x34\x00\x00\x08\x34\x00\x00\x09\x34\x00\x00\x0A\x34\x00\x00"
            b"\x0B\x34\x00\x00\x0C\x34\x00\x00\x0D\x34\x00\x00\x0E\x34\x00\x00"
            b"\x0F\x34\x00\x00\x10\x34\x00\x00\x11\x34\x00\x00\x12\x34\x00\x00"
            b"\x13\x34\x00\x00\x14\x34\x00\x00\x15\x34\x00\x00\x16\x34\x00\x00"
            b"\x17\x34\x00\x00\x18\x34\x00\x00\x19\x34\x00\x00\x1A\x34\x00\x00"
            b"\x1B\x34\x00\x00\x1C\x34\x00\x00\x1D\x34\x00\x00\x1E\x34\x00\x00"
            b"\x1F\x34\x00\x00\x20\x34\x00\x00\x21\x34\x00\x00\x22\x34\x00\x00"
            b"\x23\x34\x00\x00\x24\x34\x00\x00\x25\x34\x00\x00\x26\x34\x00\x00"
            b"\x27\x34\x00\x00\x28\x34\x00\x00\x29\x34\x00\x00\x2A\x34\x00\x00"
            b"\x2B\x34\x00\x00\x2C\x34\x00\x00\x2D\x34\x00\x00\x2E\x34\x00\x00"
            b"\x2F\x34\x00\x00\x30\x34\x00\x00\x31\x34\x00\x00\x32\x34\x00\x00"
            b"\x52\x34\x00\x00\xD3\x34\x00\x00\x54\x35\x00\x00\xD5\x35\x00\x00"
            b"\x56\x36\x00\x00\xD8\x36\x00\x00\x59\x37\x00\x00\xDA\x37\x00\x00"
            b"\x5B\x38\x00\x00\xDC\x38\x00\x00\x5D\x39\x00\x00\xDE\x39\x00\x00"
            b"\x5F\x3A\x00\x00\xE0\x3A\x00\x00\x61\x3B\x00\x00\xE2\x3B\x00\x00"
            b"\x63\x3C\x00\x00\xE4\x3C\x00\x00\x65\x3D\x00\x00\xE6\x3D\x00\x00"
            b"\x67\x3E\x00\x00\xE8\x3E\x00\x00\x69\x3F\x00\x00\xEA\x3F\x00\x00"
            b"\x6B\x40\x00\x00\xEC\x40\x00\x00\x6D\x41\x00\x00\xF4\x41\x00\x00"
            b"\x2E\x42\x00\x00\x2F\x42\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        )

        header_di_fat_data = list(unpack("109I", sample_di_fat_data[:436]))
        sample_di_fat_data = list(unpack("236I", sample_di_fat_data))
        ae(sample_doc.header.di_fat, header_di_fat_data)
        ae(sample_doc.di_fat, sample_di_fat_data)

        blair_di_fat_data = ( b"\x79\x00\x00\x00"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        )

        blair_di_fat_data = list(unpack("109I", blair_di_fat_data))
        ae(blair_doc.header.di_fat, blair_di_fat_data)
        ae(blair_doc.di_fat, blair_di_fat_data)

        ae(sample_doc.sect_size, 512)
        ae(blair_doc.sect_size, 512)

        ae(sample_doc.mini_sect_size, 64)
        ae(blair_doc.mini_sect_size, 64)

        ae(sample_doc.mini_stream_cutoff, 4096)
        ae(blair_doc.mini_stream_cutoff, 4096)

        stream = sample_doc.cfb_stream
        segments = [
            (stream, (x + 1) * 512, 512) for x in sample_di_fat_data[:135]
        ]
        stream = CompositeIStream(segments)
        stream.seek(0, SEEK_SET)
        sample_fat = list(unpack("17280I", stream.read()))

        stream = SubsetIStream(blair_doc.cfb_stream, (122 * 512), 512)
        stream.seek(0, SEEK_SET)
        blair_fat = list(unpack("128I", stream.read()))

        ae(sample_doc.fat, sample_fat)
        ae(blair_doc.fat, blair_fat)

        stream = sample_doc.cfb_stream
        segments = [
            (stream, (0x3436 * 512), 512),
            (stream, (0x4218 * 512), 512),
            (stream, (0x422B * 512), 512)
        ]
        stream = CompositeIStream(segments)
        stream.seek(0, SEEK_SET)
        sample_mini_fat = list(unpack("384I", stream.read()))

        stream = SubsetIStream(blair_doc.cfb_stream, (124 + 1) * 512, 512)
        stream.seek(0, SEEK_SET)
        blair_mini_fat = list(unpack("128I", stream.read()))

        ae(sample_doc.mini_fat, sample_mini_fat)
        ae(blair_doc.mini_fat, blair_mini_fat)

        stream = sample_doc.cfb_stream
        sample_mini_stream_sects = [
            0x3436, 0x3451, 0x41ef, 0x41f0, 0x41f1, 0x41f2, 0x41f3, 0x420c,
            0x420d, 0x420e, 0x420f, 0x4210, 0x4211, 0x4213, 0x4214, 0x4216,
            0x4218, 0x4219, 0x421a, 0x421c, 0x421d, 0x421e, 0x421f, 0x4220,
            0x4221, 0x4222, 0x4223, 0x4224, 0x4225, 0x4226, 0x4227, 0x4228,
            0x422b, 0x435c, 0x435d, 0x435e, 0x435f, 0x4360, 0x4361, 0x4363,
        ]
        segments = \
            [(stream, (x + 1) * 512, 512) for x in sample_mini_stream_sects]
        sample_mini_stream = CompositeIStream(segments)

        blair_mini_stream = \
            SubsetIStream(blair_doc.cfb_stream, (125 + 1) * 512, 512)

        sample_doc.mini_stream.seek(0, SEEK_SET)
        sample_mini_stream.seek(0, SEEK_SET)
        blair_doc.mini_stream.seek(0, SEEK_SET)
        blair_mini_stream.seek(0, SEEK_SET)

        ae(sample_doc.mini_stream.read(), sample_mini_stream.read())
        ae(blair_doc.mini_stream.read(), blair_mini_stream.read())

        stream = sample_doc.cfb_stream
        sample_dir_stream_sects = [
            0x3433, 0x3434, 0x3437, 0x41EE, 0x420B, 0x4212, 0x4215, 0x421B,
            0x4229, 0x422C, 0x422D, 0x4362
        ]
        segments = \
            [(stream, (x + 1) * 512, 512) for x in sample_dir_stream_sects]
        sample_dir_stream = CompositeIStream(segments)

        stream = blair_doc.cfb_stream
        blair_dir_stream_sects = [122, 123]
        segments = \
            [(stream, (x + 1) * 512, 512) for x in blair_dir_stream_sects]
        blair_dir_stream = CompositeIStream(segments)

        sample_dir_stream.seek(0, SEEK_SET)
        sample_doc.dir_stream.seek(0, SEEK_SET)
        blair_dir_stream.seek(0, SEEK_SET)
        blair_doc.dir_stream.seek(0, SEEK_SET)

        ae(sample_doc.dir_stream.read(), sample_dir_stream.read())
        ae(blair_doc.dir_stream.read(), blair_dir_stream.read())

        sample_dir_stream.seek(0, SEEK_SET)
        sample_dir_entries = dict()
        for counter in range(48):
            sample_dir_entries[counter] = \
                DirEntry.from_stream(sample_dir_stream, counter * 128)
        # end for

        blair_dir_stream.seek(0, SEEK_SET)
        blair_dir_entries = dict()
        for counter in range(8):
            blair_dir_entries[counter] = \
                DirEntry.from_stream(blair_dir_stream, counter * 128)
        # end for

        ae(sample_doc.dir_entries, sample_dir_entries)
        ae(blair_doc.dir_entries, blair_dir_entries)

        ae(sample_doc.root_dir_entry, sample_dir_entries[0])
        ae(blair_doc.root_dir_entry, blair_dir_entries[0])

        ae(sample_doc.cfb_stream, self.sample_doc_stream)
        ae(blair_doc.cfb_stream, self.blair_doc_stream)
    # end if

    def test_byte_offset(self):
        ae = self.assertEqual
        sample_doc = self.sample_doc
        blair_doc = self.blair_doc
        sects = [0, 12, 25, 256]

        for sect in sects:
            ae(sample_doc.byte_offset(sect), (sect + 1) * 512)
            ae(blair_doc.byte_offset(sect), (sect + 1) * 512)
        # end for
    # end def test_byte_offset

    def test_mini_byte_offset(self):
        ae = self.assertEqual
        sample_doc = self.sample_doc
        blair_doc = self.blair_doc
        sects = [0, 12, 25, 256]

        for sect in sects:
            ae(sample_doc.mini_byte_offset(sect), sect * 64)
            ae(blair_doc.mini_byte_offset(sect), sect * 64)
        # end for
    # end def test_mini_byte_offset

    def test_get_fat_chain(self):
        ae = self.assertEqual
        ar = self.assertRaises
        sample_doc = self.sample_doc
        blair_doc = self.blair_doc

        sample_fat = sample_doc.fat
        sample_fat_len = len(sample_doc.fat)

        for sect in [0, 20]:
            sample_fat_chain = [sect]
            next = sample_fat[sect]

            while (next < sample_fat_len) and (next != FAT_EOC):
                sample_fat_chain.append(next)
                next = sample_fat[next]
            # end while

            ae(sample_doc.get_fat_chain(sect), sample_fat_chain)
        # end for

        ar(IndexError, sample_doc.get_fat_chain, sample_fat_len+1)

        blair_fat = blair_doc.fat
        blair_fat_len = len(blair_fat)

        for sect in [0, 79]:
            blair_fat_chain = [sect]
            next = blair_fat[sect]

            while (next< blair_fat_len) and (next != FAT_EOC):
                blair_fat_chain.append(next)
                next = blair_fat[next]
            # end while

            ae(blair_doc.get_fat_chain(sect), blair_fat_chain)
        # end for

        ar(IndexError, blair_doc.get_fat_chain, blair_fat_len + 1)
    # end def test_get_fat_chain

    def test_get_mini_fat_chain(self):
        ae = self.assertEqual
        ar = self.assertRaises
        sample_doc = self.sample_doc
        blair_doc = self.blair_doc

        sample_mini_fat = sample_doc.mini_fat
        sample_mini_fat_len = len(sample_mini_fat)

        for sect in [0, 1, 63]:
            sample_mini_fat_chain = [sect]
            next = sample_mini_fat[sect]

            while (next < sample_mini_fat_len) and (next != FAT_EOC):
                sample_mini_fat_chain.append(next)
                next = sample_mini_fat[next]
            # end while

            ae(sample_doc.get_mini_fat_chain(sect), sample_mini_fat_chain)
        # end for

        ar(IndexError, sample_doc.get_mini_fat_chain, sample_mini_fat_len + 1)

        blair_mini_fat = blair_doc.mini_fat
        blair_mini_fat_len = len(blair_mini_fat)

        for sect in [0, 2, 63]:
            blair_mini_fat_chain = [sect]
            next = blair_mini_fat[sect]

            while (next < blair_mini_fat_len) and (next != FAT_EOC):
                blair_mini_fat_chain.append(next)
                next = blair_mini_fat[next]
            # end while

            ae(blair_doc.get_mini_fat_chain(sect), blair_mini_fat_chain)
        # end for

        ar(IndexError, blair_doc.get_mini_fat_chain, blair_mini_fat_len + 1)
    # end def test_get_mini_fat_chain

    def test_get_dir_entry(self):
        ae = self.assertEqual
        ar = self.assertRaises
        sample_doc = self.sample_doc
        blair_doc = self.blair_doc

        sample_dir_entries = sample_doc.dir_entries
        for sid in sample_dir_entries:
            ae(sample_doc.get_dir_entry(sid), sample_dir_entries[sid])
        # end for

        ar(IndexError, sample_doc.get_dir_entry, 0xFFFF)

        blair_dir_entries = blair_doc.dir_entries
        for sid in blair_dir_entries:
            ae(blair_doc.get_dir_entry(sid), blair_dir_entries[sid])
        # end for

        ar(IndexError, blair_doc.get_dir_entry, 0xFFFF)
    # end def test_get_dir_entry

    def test_is_valid_dir_entry(self):
        at = self.assertTrue
        af = self.assertFalse
        sample_doc = self.sample_doc
        blair_doc = self.blair_doc

        sids = list(sample_doc.dir_entries.keys())
        for sid in sids[:46]:
            entry = sample_doc.get_dir_entry(sid)
            at(sample_doc.is_valid_dir_entry(entry))
        # end for

        for sid in sids[46:]:
            entry = sample_doc.get_dir_entry(sid)
            af(sample_doc.is_valid_dir_entry(entry))
        # end for


        sids = list(blair_doc.dir_entries.keys())
        for sid in sids[:7]:
            entry = blair_doc.get_dir_entry(sid)
            at(blair_doc.is_valid_dir_entry(entry))
        # end for

        for sid in sids[7:]:
            entry = blair_doc.get_dir_entry(sid)
            af(blair_doc.is_valid_dir_entry(entry))
        # end for
    # end def is_valid_dir_entry

    def test_get_stream(self):
        ae = self.assertEqual
        ar = self.assertRaises

        sample_doc = self.sample_doc
        blair_doc = self.blair_doc

        for sid in sample_doc.dir_entries:
            dir_entry = sample_doc.dir_entries[sid]
            first_sect = dir_entry.stream_sect_offset

            if sid == 0:
                chain = sample_doc.get_fat_chain(first_sect)
                stream = sample_doc.cfb_stream
                byte_offset = sample_doc.byte_offset
                sect_size = sample_doc.sect_size
            elif dir_entry.stream_size < sample_doc.mini_stream_cutoff:
                chain = sample_doc.get_mini_fat_chain(first_sect)
                stream = sample_doc.mini_stream
                byte_offset = sample_doc.mini_byte_offset
                sect_size = sample_doc.mini_sect_size
            else:
                chain = sample_doc.get_fat_chain(first_sect)
                stream = sample_doc.cfb_stream
                byte_offset = sample_doc.byte_offset
                sect_size = sample_doc.sect_size
            # end if

            chains = list()
            start_index = 0
            delta = 1
            counter = 1
            while counter < len(chain):
                if (chain[counter] - chain[start_index]) == delta:
                    delta += 1
                    counter += 1
                    continue
                else:
                    chains.append((chain[start_index], (counter-start_index)))
                    start_index = counter
                    delta = 1
                    counter += 1
                # end if
            else:
                chains.append((chain[start_index], (counter-start_index)))
            # end while

            segments = \
                [(stream, byte_offset(x[0]), x[1] * sect_size) for x in chains]

            slack = CompositeIStream(segments)
            noslack = SubsetIStream(slack, 0, dir_entry.stream_size)

            slack.seek(0, SEEK_SET)
            noslack.seek(0, SEEK_SET)

            ae(sample_doc.get_stream(sid, slack=True).read(), slack.read())
            ae(sample_doc.get_stream(sid, slack=False).read(), noslack.read())
        # end for


        for sid in blair_doc.dir_entries:
            dir_entry = blair_doc.dir_entries[sid]
            first_sect = dir_entry.stream_sect_offset

            if sid == 0:
                chain = blair_doc.get_fat_chain(first_sect)
                stream = blair_doc.cfb_stream
                byte_offset = blair_doc.byte_offset
                sect_size = blair_doc.sect_size
            elif dir_entry.stream_size < blair_doc.mini_stream_cutoff:
                chain = blair_doc.get_mini_fat_chain(first_sect)
                stream = blair_doc.mini_stream
                byte_offset = blair_doc.mini_byte_offset
                sect_size = blair_doc.mini_sect_size
            else:
                chain = blair_doc.get_fat_chain(first_sect)
                stream = blair_doc.cfb_stream
                byte_offset = blair_doc.byte_offset
                sect_size = blair_doc.sect_size
            # end if

            chains = list()
            start_index = 0
            delta = 1
            counter = 1
            while counter < len(chain):
                if (chain[counter] - chain[start_index]) == delta:
                    delta += 1
                    counter += 1
                    continue
                else:
                    chains.append((chain[start_index], (counter-start_index)))
                    start_index = counter
                    delta = 1
                    counter += 1
                # end if
            else:
                chains.append((chain[start_index], (counter-start_index)))
            # end while

            segments = \
                [(stream, byte_offset(x[0]), x[1] * sect_size) for x in chains]

            slack = CompositeIStream(segments)
            noslack = SubsetIStream(slack, 0, dir_entry.stream_size)

            slack.seek(0, SEEK_SET)
            noslack.seek(0, SEEK_SET)

            ae(blair_doc.get_stream(sid, slack=True).read(), slack.read())
            ae(blair_doc.get_stream(sid, slack=False).read(), noslack.read())
        # end for
    # end def test_get_stream
## end class CompoundFileTestCase
