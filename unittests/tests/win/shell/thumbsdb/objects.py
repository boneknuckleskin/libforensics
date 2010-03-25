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

"""Unit tests for the lf.win.shell.thumbsdb.objects module."""

# stdlib imports
from unittest import TestCase
from os.path import join
from datetime import datetime
from hashlib import md5

# local imports
from lf.dec import RawIStream, ByteIStream, SEEK_SET
from lf.time import FILETIMETodatetime
from lf.win.ole.cfb import CompoundFile
from lf.win.shell.thumbsdb.objects import (
    CatalogEntry, Catalog, Thumbnail, ThumbsDb
)

__docformat__ = "restructuredtext en"
__all__ = [
    "CatalogEntryTestCase", "CatalogTestCase", "ThumbnailTestCase",
    "ThumbsDbTestCase"
]

class CatalogEntryTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x3E\x00\x00\x00")  # size
        data.extend(b"\x01\x00\x00\x00")  # id/index
        data.extend(b"\x00\x68\x67\x4F\xB7\xA3\xCA\x01")  # mtime
        data.extend(b"d\x00a\x00n\x00g\x00e\x00r\x00-\x00s\x00i\x00")  # name
        data.extend(b"g\x00n\x00-\x00s\x00h\x00o\x00c\x00k\x00")  # more name
        data.extend(b".\x00j\x00p\x00g\x00\x00\x00")  # more name

        stream = ByteIStream(data)
        ce0 = CatalogEntry.from_stream(stream)
        ce1 = CatalogEntry.from_stream(stream, 0)

        for ce in (ce0, ce1):
            ae(ce.size, 0x3E)
            ae(ce.id, 1)
            ae(ce.stream_name, "1")
            ae(ce.mtime, datetime(2010, 2, 2, 3,  25, 4))
        # end for
    # end def test_from_stream
# end def CatalogEntryTestCase

class CatalogTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        # catalog header
        data.extend(b"\x10\x00\x07\x00")  # unknown 1 and 2
        data.extend(b"\x02\x00\x00\x00")  # item_count
        data.extend(b"\x00\x01\x02\x03")  # width
        data.extend(b"\x04\x05\x06\x07")  # height

        # first entry
        data.extend(b"\x2E\x00\x00\x00")  # size
        data.extend(b"\x01\x00\x00\x00")  # id/index
        data.extend(b"\x95\x98\x50\xB7\xA3\xCA\x01")  # mtime
        data.extend(b"z\x00o\x00o\x00l\x00e\x00m\x00u\x00r\x00")  # name
        data.extend(b"1\x00.\x00j\x00p\x00g\x00\x00")  # more name

        # second entry
        data.extend(b"\x3E\x00\x00\x00")  # size
        data.extend(b"\x02\x00\x00\x00")  # id/index
        data.extend(b"\x00\x68\x67\x4F\xB7\xA3\xCA\x01")  # mtime
        data.extend(b"d\x00a\x00n\x00g\x00e\x00r\x00-\x00s\x00i\x00")  # name
        data.extend(b"g\x00n\x00-\x00s\x00h\x00o\x00c\x00k\x00")  # more name
        data.extend(b".\x00j\x00p\x00g\x00\x00\x00")  # more name

        stream = ByteIStream(data)

        cat0 = Catalog.from_stream(stream)
        cat1 = Catalog.from_stream(stream, 0)

        entries = [
            CatalogEntry.from_stream(stream, 16),
            CatalogEntry.from_stream(stream, 62)
        ]

        for cat in (cat0, cat1):
            ae(cat.width, 0x03020100)
            ae(cat.height, 0x07060504)
            ae(cat.item_count, 2)
            ae(cat.entries, entries)
        # end for
    # end def test_from_stream
# end class CatalogTestCase

class ThumbnailTestCase(TestCase):
    def test_from_stream(self):
        ae = self.assertEqual

        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # unknown1
        data.extend(b"\x04\x05\x06\x07")  # unknown2
        data.extend(b"\x05\x00\x00\x00")  # size
        data.extend(b"\xFF\xD8\x08\x09\x0A")  # data
        stream = ByteIStream(data)

        thumb1 = Thumbnail.from_stream(stream)
        thumb2 = Thumbnail.from_stream(stream, 0)

        for thumb in (thumb1, thumb2):
            ae(thumb.size, 0x5)
            ae(thumb.data, b"\xFF\xD8\x08\x09\x0A")
        # end for


        data = bytearray()
        data.extend(b"\x00\x01\x02\x03")  # unknown1
        data.extend(b"\x05\x00\x00\x00")  # size
        data.extend(b"\x04\x05\x06\x07")  # unknown2
        data.extend(b"\x08\x09\x0A\x0B")  # unknown3
        data.extend(b"\xFF\xD8\x0C\x0D\x0E")  # data
        stream = ByteIStream(data)

        thumb1 = Thumbnail.from_stream(stream)
        thumb2 = Thumbnail.from_stream(stream, 0)

        for thumb in (thumb1, thumb2):
            ae(thumb.size, 0x5)
            ae(thumb.data, b"\xFF\xD8\x0C\x0D\x0E")
        # end for
    # end def test_from_stream
# end class ThumbnailTestCase

class ThumbsDbTestCase(TestCase):
    def setUp(self):
        input_file = join("data", "thumbsdb", "thumbs.db")
        self.cfb = CompoundFile(RawIStream(input_file))
        self.tdb = ThumbsDb(self.cfb)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        ar = self.assertRaises
        tdb = self.tdb

        catalog_entries = [
            CatalogEntry((
                0x2E,
                1,
                FILETIMETodatetime.from_int(0x01CAA3B750989500),
                "zoolemur1.jpg",
                "1"
            )),
            CatalogEntry((
                0x56,
                2,
                FILETIMETodatetime.from_int(0x01CAA3B74F676800),
                "Copy (2) of danger-sign-shock.jpg",
                "2"
            )),
            CatalogEntry((
                0x5E,
                3,
                FILETIMETodatetime.from_int(0x01CAA3B74E363B00),
                "Copy (2) of Kookaburra_at_Marwell.jpg",
                "3"
            )),
            CatalogEntry((
                0x54,
                4,
                FILETIMETodatetime.from_int(0x01CAA3B74F676800),
                "Copy (2) of Makari_the_Tiger.jpg",
                "4"
            )),
            CatalogEntry((
                0x4A,
                5,
                FILETIMETodatetime.from_int(0x01CAA3B750989500),
                "Copy (2) of prairiedogs.jpg",
                "5"
            )),
            CatalogEntry((
                0x46,
                6,
                FILETIMETodatetime.from_int(0x01CAA3B750989500),
                "Copy (2) of zoolemur1.jpg",
                "6"
            )),
            CatalogEntry((
                0x4E,
                7,
                FILETIMETodatetime.from_int(0x01CAA3B74F676800),
                "Copy of danger-sign-shock.jpg",
                "7"
            )),
            CatalogEntry((
                0x56,
                8,
                FILETIMETodatetime.from_int(0x01CAA3B74E363B00),
                "Copy of Kookaburra_at_Marwell.jpg",
                "8"
            )),
            CatalogEntry((
                0x4C,
                9,
                FILETIMETodatetime.from_int(0x01CAA3B74F676800),
                "Copy of Makari_the_Tiger.jpg",
                "9"
            )),
            CatalogEntry((
                0x42,
                10,
                FILETIMETodatetime.from_int(0x01CAA3B750989500),
                "Copy of prairiedogs.jpg",
                "01"
            )),
            CatalogEntry((
                0x3E,
                11,
                FILETIMETodatetime.from_int(0x01CAA3B750989500),
                "Copy of zoolemur1.jpg",
                "11"
            )),
            CatalogEntry((
                0x3E,
                12,
                FILETIMETodatetime.from_int(0x01CAA3B74F676800),
                "danger-sign-shock.jpg",
                "21"
            )),
            CatalogEntry((
                0x46,
                13,
                FILETIMETodatetime.from_int(0x01CAA3B74E363B00),
                "Kookaburra_at_Marwell.jpg",
                "31"
            )),
            CatalogEntry((
                0x3C,
                14,
                FILETIMETodatetime.from_int(0x01CAA3B74F676800),
                "Makari_the_Tiger.jpg",
                "41"
            )),
            CatalogEntry((
                0x32,
                15,
                FILETIMETodatetime.from_int(0x01CAA3B750989500),
                "prairiedogs.jpg",
                "51"
            )),
        ]

        catalog = Catalog((96, 96, 15, catalog_entries))
        md5_hashes = {
            8: "41783146a36b0df9c0e450715439fa55",
            4: "8524c25aab60e2a76ecb3fd1215c52fa",
            2: "ca70cbc23a7e39fbeba90f027fef6e5c",
            1: "925405772966a6c3bbcedec92c2cb29a",
            3: "41783146a36b0df9c0e450715439fa55",
            6: "925405772966a6c3bbcedec92c2cb29a",
            5: "6bbeb0387e4f44aac21d582a1f2a467d",
            7: "ca70cbc23a7e39fbeba90f027fef6e5c",
            12: "ca70cbc23a7e39fbeba90f027fef6e5c",
            10: "6bbeb0387e4f44aac21d582a1f2a467d",
            9: "8524c25aab60e2a76ecb3fd1215c52fa",
            11: "925405772966a6c3bbcedec92c2cb29a",
            14: "8524c25aab60e2a76ecb3fd1215c52fa",
            13: "41783146a36b0df9c0e450715439fa55",
            15: "6bbeb0387e4f44aac21d582a1f2a467d"
        }

        ae(tdb.catalog, catalog)
        ae(tdb.thumbnails.keys(), md5_hashes.keys())
        for (key, hash) in md5_hashes.items():
            ae(md5(tdb.thumbnails[key].data).hexdigest(), hash)
        # end for

        ar(
            KeyError,
            ThumbsDb, self.cfb,"thisisnotthecatalogyouarelookingfor"
        )
    # end def test__init__
# end class ThumbsDbTestCase
