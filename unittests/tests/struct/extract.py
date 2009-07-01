# Copyright 2009 Michael Murr
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

"""
Unit tests for the lf.struct.extract module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase
from collections import namedtuple
from struct import pack
from itertools import chain

from lf.struct.datatype import Int8, Int16, UInt32, Bytes
from lf.struct.datastruct import DataStruct_BE, DataStruct_LE, Array
from lf.struct.extract import ExtractorFactory, Extractor, ListExtractor
from lf.struct.excepts import ExtractionError

class DS0(DataStruct_LE):
    fields = [
        Int8("field0"),
        Int16("field1")
    ]
# end class DS0
namedtuple0 = namedtuple("namedtuple0", ["field0", "field1"])._make

class DS1(DataStruct_BE):
    fields = [
        UInt32("field0"),
        UInt32("field1"),
        UInt32("field2")
    ]
# end class DS1
namedtuple1 = namedtuple("namedtuple1", ["field0", "field1", "field2"])._make

class DS2(DataStruct_BE):
    fields = [
        DS1("field0")
    ]
# end class DS2
namedtuple2 = namedtuple("namedtuple2", ["field0"])._make

class DS(DataStruct_BE):
    fields = [
        Bytes(3, "field0"),
        Array(3, DS0(), "field1"),
        DS2("field2")
    ]
# end class DS
namedtuple3 = namedtuple("namedtuple3", ["field0", "field1", "field2"])._make

def _nop(args):
    return args[0]
# end def _nop

_struct_strings = [">3s", "<bhbhbh", ">III"]

_groupbys = [
    [1, -1, -1, 1, 1, -1, -1, 1, 1, 1],
    [1, -1, -1, -1, 1],
    [1, 1, 1]
]

_tuple_factories = [
    [_nop, namedtuple0, namedtuple0, namedtuple0, namedtuple1],
    [_nop, tuple, namedtuple2],
    [namedtuple3]
]

_sizes_so_far = [3, 4, 6, 7, 9, 10, 12, 16, 20, 24]

class ExtractorTestCase(TestCase):
    def setUp(self):
        group_info = (_groupbys, _tuple_factories)
        self.extractor = Extractor(_struct_strings, group_info, _sizes_so_far)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        at = self.assertTrue
        extractor = self.extractor

        at(hasattr(extractor, "struct_objs"))
        at(hasattr(extractor, "groupbys"))
        at(hasattr(extractor, "tuple_factories"))
        at(hasattr(extractor, "size"))
        at(hasattr(extractor, "sizes_so_far"))

        ae(len(extractor.struct_objs), 3)
        for index, struct_obj in enumerate(extractor.struct_objs):
            ae(struct_obj.format.decode("ascii"), _struct_strings[index])
        # end for

        ae(len(extractor.groupbys), 3)
        for index, _groupby in enumerate(extractor.groupbys):
            ae(_groupby, _groupbys[index])
        # end for

        ae(len(extractor.tuple_factories), 3)
        for index, tuple_factory in enumerate(extractor.tuple_factories):
            ae(tuple_factory, _tuple_factories[index])
        # end for

        ae(len(_sizes_so_far), 10)
        for index, size_so_far in enumerate(extractor.sizes_so_far):
            ae(size_so_far, _sizes_so_far[index])
        # end for

        ae(extractor.size, 24)
    # end def test__init__

    def test_extract(self):
        ae = self.assertEqual
        at = self.assertTrue
        ar = self.assertRaises

        data = [pack("B", x) for x in range(24)]
        data = b"".join(data)
        results = [
            b"\x00\x01\x02",
            0x03, 0x0504,
            0x06, 0x0807,
            0x09, 0x0B0A,
            0x0C0D0E0F, 0x10111213, 0x14151617
        ]

        values = self.extractor.extract(data, flatten=True)
        ae(len(values), 10)

        for index, value in enumerate(values):
            ae(value, results[index])
        # end for

        for datum in (data, b"".join([data, data])):
            values = self.extractor.extract(datum, flatten=False)
            at(hasattr(values, "_fields"))
            at(values._fields, ("field0", "field1", "field2"))
            ae(values.field0, results[0])
            at(isinstance(values.field1, tuple))
            ae(len(values.field1), 3)

            at(hasattr(values.field1[0], "_fields"))
            ae(values.field1[0]._fields, ("field0", "field1"))
            ae(values.field1[0].field0, results[1])
            ae(values.field1[0].field1, results[2])

            at(hasattr(values.field1[1], "_fields"))
            ae(values.field1[1]._fields, ("field0", "field1"))
            ae(values.field1[1].field0, results[3])
            ae(values.field1[1].field1, results[4])

            at(hasattr(values.field1[2], "_fields"))
            ae(values.field1[2]._fields, ("field0", "field1"))
            ae(values.field1[2].field0, results[5])
            ae(values.field1[2].field1, results[6])

            at(hasattr(values.field2, "_fields"))
            ae(values.field2._fields, ("field0",))

            at(hasattr(values.field2.field0, "_fields"))
            ae(values.field2.field0._fields, ("field0", "field1", "field2"))
            ae(values.field2.field0.field0, results[7])
            ae(values.field2.field0.field1, results[8])
            ae(values.field2.field0.field2, results[9])
        # end for

        ar(ExtractionError, self.extractor.extract, data[:3])
    # end def test_extract

    def test_extract_partial(self):
        at = self.assertTrue
        ae = self.assertEqual
        extractor = self.extractor

        results = (
            b"\x00\x01\x02",
            0x03, 0x0504,
            0x06, 0x0807,
            0x09, 0x0B0A,
            0xC0D0E0F, 0x10111213, 0x14151617
        )

        data = b"".join([pack("B", x) for x in range(32)])

        values = extractor.extract_partial(data)
        ae(values, results)

        values = extractor.extract_partial(data[:7])
        ae(len(values), 4)
        for index, value in enumerate(values):
            ae(value, results[index])
        # end for

        values = extractor.extract_partial(data[:8])
        ae(len(values), 4)
        for index, value in enumerate(values):
            ae(value, results[index])
        # end for

        values = extractor.extract_partial(data[:9])
        ae(len(values), 5)
        for index, value in enumerate(values):
            ae(value, results[index])
        # end for
    # end def test_extract_partial
# end class ExtractorTestCase

class ListExtractorTestCase(TestCase):
    def setUp(self):
        struct_string = ">III"
        count = 5
        tuple_factory = namedtuple1
        sizes_so_far = [
            4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60
        ]
        size = 60

        self.sizes_so_far = sizes_so_far
        self.extractor = ListExtractor(
            count, struct_string, tuple_factory, sizes_so_far
        )
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        extractor = self.extractor

        ae(extractor.count, 5)
        ae(extractor.tuple_factory, namedtuple1)
        ae(extractor.sizes_so_far, self.sizes_so_far)
        ae(extractor.size, 60)
        ae(extractor.field_count, 3)
    # end def test__init__

    def test_extract(self):
        ae = self.assertEqual
        extractor = self.extractor
        results = [
            (0x00010203, 0x04050607, 0x08090A0B),
            (0x0C0D0E0F, 0x10111213, 0x14151617),
            (0x18191A1B, 0x1C1D1E1F, 0x20212223),
            (0x24252627, 0x28292A2B, 0x2C2D2E2F),
            (0x30313233, 0x34353637, 0x38393A3B)
        ]

        data = b"".join([pack("B", x) for x in range(60)])
        values = extractor.extract(data, flatten=False)

        ae(len(values), 5)
        for (value, result) in zip(values, results):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:72]
        values = extractor.extract(data2, flatten=False)

        ae(len(values), 6)
        results2 = list(results)
        results2.append(results[0])

        for (value, result) in zip(values, results2):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:80]
        values = extractor.extract(data2, flatten=False)

        ae(len(values), 6)
        for (value, result) in zip(values, results2):
            ae(value, result)
        # end for

        flat_results = list(chain.from_iterable(results))
        values = extractor.extract(data, flatten=True)

        ae(len(values), 15)
        for (value, result) in zip(values, flat_results):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:72]
        values = extractor.extract(data2, flatten=True)

        ae(len(values), 18)
        flat_results2 = list(flat_results)
        flat_results2.extend(flat_results[0:3])

        for (value, result) in zip(values, flat_results2):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:80]
        values = extractor.extract(data2, flatten=True)

        ae(len(values), 18)
        for (value, result) in zip(values, flat_results2):
            ae(value, result)
        # end for
    # end def test_extract
# end class ListExtractorTestCase

class ExtractorFactoryTestCase(TestCase):
    def setUp(self):
        self.extractor_factory = ExtractorFactory()
    # end def setUp

    def test_get_grouping_info(self):
        ae = self.assertEqual
        at = self.assertTrue

        groupbys, factories = \
            self.extractor_factory.get_grouping_info(DS())

        ae(len(groupbys), 3)
        ae(len(factories), 3)

        ae(len(groupbys[0]), 10)
        ae(len(groupbys[1]), 5)
        ae(len(groupbys[2]), 3)

        for index, _groupby in enumerate(groupbys):
            ae(_groupby, _groupbys[index])
        # end for

        ae(len(factories[0]), 5)
        ae(len(factories[1]), 3)
        ae(len(factories[2]), 1)

        ae(factories[0][1], factories[0][2])
        ae(factories[0][2], factories[0][3])
        ae(factories[0][1].__self__._fields, ("field0", "field1"))
        ae(factories[0][4].__self__._fields, ("field0" ,"field1", "field2"))

        ae(factories[1][1], tuple)
        ae(factories[1][2].__self__._fields, ("field0",))

        ae(factories[2][0].__self__._fields, ("field0", "field1", "field2"))

    # end def test_get_grouping_info

    def test_make_namedtuple_factory(self):
        ae = self.assertEqual
        factory = self.extractor_factory

        ntf = factory.make_namedtuple_factory(DS())
        ae(ntf.__self__._fields, ("field0", "field1", "field2"))

        ntf = factory.make_namedtuple_factory(DS2())
        ae(ntf.__self__._fields, ("field0",))

        ntf = factory.make_namedtuple_factory(DS1())
        ae(ntf.__self__._fields, ("field0", "field1", "field2"))

        ntf = factory.make_namedtuple_factory(DS0())
        ae(ntf.__self__._fields, ("field0", "field1"))
    # end def test_make_namedtuple_factory

    def test_get_struct_strings(self):
        ss = self.extractor_factory.get_struct_strings(DS())
        self.assertEqual(ss, _struct_strings)
    # end def test_get_struct_strings

    def test_get_sizes_so_far(self):
        ssf = self.extractor_factory.get_sizes_so_far(DS())
        self.assertEqual(ssf, _sizes_so_far)
    # end def test_get_sizes_so_far

    def test_make(self):
        extractor = self.extractor_factory.make(DS())
        ae = self.assertEqual
        at = self.assertTrue
        ar = self.assertRaises

        data = [pack("B", x) for x in range(24)]
        data = b"".join(data)
        results = [
            b"\x00\x01\x02",
            0x03, 0x0504,
            0x06, 0x0807,
            0x09, 0x0B0A,
            0x0C0D0E0F, 0x10111213, 0x14151617
        ]

        values = extractor.extract(data, flatten=True)
        ae(len(values), 10)

        for index, value in enumerate(values):
            ae(value, results[index])
        # end for

        for datum in (data, b"".join([data, data])):
            values = extractor.extract(datum, flatten=False)
            at(hasattr(values, "_fields"))
            at(values._fields, ("field0", "field1", "field2"))
            ae(values.field0, results[0])
            at(isinstance(values.field1, tuple))
            ae(len(values.field1), 3)

            at(hasattr(values.field1[0], "_fields"))
            ae(values.field1[0]._fields, ("field0", "field1"))
            ae(values.field1[0].field0, results[1])
            ae(values.field1[0].field1, results[2])

            at(hasattr(values.field1[1], "_fields"))
            ae(values.field1[1]._fields, ("field0", "field1"))
            ae(values.field1[1].field0, results[3])
            ae(values.field1[1].field1, results[4])

            at(hasattr(values.field1[2], "_fields"))
            ae(values.field1[2]._fields, ("field0", "field1"))
            ae(values.field1[2].field0, results[5])
            ae(values.field1[2].field1, results[6])

            at(hasattr(values.field2, "_fields"))
            ae(values.field2._fields, ("field0",))

            at(hasattr(values.field2.field0, "_fields"))
            ae(values.field2.field0._fields, ("field0", "field1", "field2"))
            ae(values.field2.field0.field0, results[7])
            ae(values.field2.field0.field1, results[8])
            ae(values.field2.field0.field2, results[9])
        # end for

        ar(ExtractionError, extractor.extract, data[:3])
    # end def test_make

    def test_make_list(self):
        extractor = self.extractor_factory.make_list(5, DS1())
        ae = self.assertEqual
        results = [
            (0x00010203, 0x04050607, 0x08090A0B),
            (0x0C0D0E0F, 0x10111213, 0x14151617),
            (0x18191A1B, 0x1C1D1E1F, 0x20212223),
            (0x24252627, 0x28292A2B, 0x2C2D2E2F),
            (0x30313233, 0x34353637, 0x38393A3B)
        ]

        data = b"".join([pack("B", x) for x in range(60)])
        values = extractor.extract(data, flatten=False)

        ae(len(values), 5)
        for (value, result) in zip(values, results):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:72]
        values = extractor.extract(data2, flatten=False)

        ae(len(values), 6)
        results2 = list(results)
        results2.append(results[0])

        for (value, result) in zip(values, results2):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:80]
        values = extractor.extract(data2, flatten=False)

        ae(len(values), 6)
        for (value, result) in zip(values, results2):
            ae(value, result)
        # end for

        flat_results = list(chain.from_iterable(results))
        values = extractor.extract(data, flatten=True)

        ae(len(values), 15)
        for (value, result) in zip(values, flat_results):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:72]
        values = extractor.extract(data2, flatten=True)

        ae(len(values), 18)
        flat_results2 = list(flat_results)
        flat_results2.extend(flat_results[0:3])

        for (value, result) in zip(values, flat_results2):
            ae(value, result)
        # end for

        data2 = data * 2
        data2 = data2[:80]
        values = extractor.extract(data2, flatten=True)

        ae(len(values), 18)
        for (value, result) in zip(values, flat_results2):
            ae(value, result)
        # end for
    # end def test_make_list
# end class ExtractoFactoryTestCase
