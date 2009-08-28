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
Unit tests for the lf.datatype.extract module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from copy import copy
from unittest import TestCase
from struct import pack
from itertools import chain

from lf.utils.dict import NAryTree
from lf.datatype.builtin import (
    char, int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32,
    float64, raw
)
from lf.datatype.bits import bits, BitTypeU8, BitTypeU16
from lf.datatype.composite import LERecord, BERecord, ExtractableArray, array
from lf.datatype.extract import Extractor, PASS_THRU
from lf.datatype.excepts import ExtractionError

class BT_S(BitTypeU8):
    X = bits(2)
# end class BT_S

class BT_BB(BitTypeU16):
    DD = bits(3)
    EE = bits(2)
# end class BT_BB

class DS_F(LERecord):
    K = int8
    L = raw(3)
    M = float64
# end class DS_F

class DS_T(BERecord):
    Z = int16
    AA = uint16
# end class DS_T

class DS_C(BERecord):
    F = DS_F
    G = uint32
# end class DS_C

class DS_H(BERecord):
    N = uint8
    O = array(BT_S, 2)
    P = int32
    Q = array(DS_T, 2)
# end class DS_H

class DS_W(LERecord):
    bit_field1 = BT_BB
    CC = int64
    bit_field2 = BT_BB
# end class DS_W

class DS_R(BERecord):
    U = uint64
    V = float32
    W = DS_W
# end class DS_R

class DS_J(LERecord):
    R = DS_R
# end class DS_J

class DS_D(BERecord):
    H = DS_H
    I = uint8
    J = DS_J
# end class DS_D

class DS_A(BERecord):
    B = char
    C = DS_C
    D = DS_D
    E = int8
# end class DS_A

class ExtractorTestCase(TestCase):
    def setUp(self):
        self.extractor = Extractor(DS_A)
        self.results = (
            b"\x00", 1, b"\x02\x03\x04", 1.1801778615788355e-250, 0x0D0E0F10,
            17, 2, 4, 3, 4, 0x14151617, 0x1819, 0x1A1B, 0x1C1D, 0x1E1F, 32,
            0x2122232425262728, 3.778502846978754e-14, 5, 1, 369,
            0x363534333231302F, 7, 2, 449, 57
        )
        self.data = b"".join([pack("B", x) for x in range(58)])
        self.record_strings = [ ">c", "<b3sd", ">IBBBihHhHBQf", "<HqH", ">b"]
        self.size_at = [
            1, 2, 5, 13, 17, 18, 19, 20, 24, 26, 28, 30, 32, 33, 41, 45, 47,
            55, 57, 58
        ]

        self.groupbys = [
            [
                 1,
                -1, -1, -1,
                 1,
                -1,
                 1, 1, 1, 1,
                -1,
                 1, 1,
                -1, -1,
                 1,
                -1,
                 1,
                -1, -1, -1, -1, -1, -1, -1,
                 1
            ],

            [
                 1,
                -1, -1,
                 1,
                -1,
                 1,
                -1, -1,
                 1,
                -1, -1, -1,
                 1
            ],

            [
                 1,
                -1,
                 1, 1, 1, 1,
                -1,
                 1,
                -1
            ],

            [
                 1,
                -1,
                 1, 1, 1,
                -1
            ],

            [
                 1, 1, 1, 1
            ],
        ]

        self.factories = [
            [
                PASS_THRU,
                DS_F._factory_,
                PASS_THRU,
                PASS_THRU,
                list,
                PASS_THRU,
                DS_T._factory_,
                DS_T._factory_,
                PASS_THRU,
                PASS_THRU,
                PASS_THRU,
                DS_W._factory_,
                PASS_THRU
            ],

            [
                PASS_THRU,
                DS_C._factory_,
                PASS_THRU,
                PASS_THRU,
                PASS_THRU,
                list,
                PASS_THRU,
                DS_R._factory_,
                PASS_THRU
            ],

            [
                PASS_THRU,
                PASS_THRU,
                DS_H._factory_,
                PASS_THRU,
                DS_J._factory_,
                PASS_THRU
            ],

            [
                PASS_THRU,
                PASS_THRU,
                DS_D._factory_,
                PASS_THRU
            ],

            [
                DS_A._factory_
            ],
        ]

        self.decoders_at = [6, 8, 18, 22]
        self.decoders = [
            BT_S._decoder_, BT_S._decoder_, BT_BB._decoder_,
            BT_BB._decoder_
        ]
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual
        at = self.assertTrue

        extractor = self.extractor

        at(hasattr(extractor, "struct_objs"))
        at(hasattr(extractor, "groupbys"))
        at(hasattr(extractor, "factories"))
        at(hasattr(extractor, "size"))
        at(hasattr(extractor, "size_at"))

        ae(len(extractor.struct_objs), 5)
        for index, struct_obj in enumerate(extractor.struct_objs):
            ae(struct_obj.format.decode("ascii"), self.record_strings[index])
        # end for

        ae(extractor.size, 58)
    # end def test__init__

    def test_extract(self):
        af = self.assertFalse
        ae = self.assertEqual
        at = self.assertTrue
        ar = self.assertRaises

        data = self.data
        results = self.results

        values = self.extractor.extract(data, flatten=True)
        ae(len(values), 26)
        ae(values, results)

        for datum in (data, b"".join([data, data])):
            values = self.extractor.extract(datum, flatten=False)
            at(hasattr(values, "_fields"))
            at(hasattr(values, "_indices"))
            ae(values._fields, ("B", "C", "D", "E"))
            ae(values._indices, (0, 1, 2, 3))
            ae(values[0], results[0])
            ae(values[3], results[25])

            at(hasattr(values.C, "_fields"))
            ae(values.C._fields, ("F", "G"))
            ae(values.C._indices, (0, 1))
            ae(values.C[1], results[4])

            at(hasattr(values.D, "_fields"))
            ae(values.D._fields, ("H", "I", "J"))
            ae(values.D._indices, (0, 1, 2))
            ae(values.D[1], results[15])

            at(hasattr(values.C.F, "_fields"))
            ae(values.C.F._fields, ("K", "L", "M"))
            ae(values.C.F._indices, (0, 1, 2))
            ae(values.C.F, results[1:4])

            at(hasattr(values.D.H, "_fields"))
            ae(values.D.H._fields, ("N", "O", "P", "Q"))
            ae(values.D.H._indices, (0, 1, 2, 3))
            ae(values.D.H.N, results[5])
            ae(values.D.H.P, results[10])

            at(hasattr(values.D.J, "_fields"))
            ae(values.D.J._fields, ("R",))
            ae(values.D.J._indices, (0,))

            at(isinstance(values.D.H.O, list))
            af(hasattr(values.D.H.O, "_fields"))
            ae(len(values.D.H.O), 4)
            ae(values.D.H.O[0], results[6])
            ae(values.D.H.O[1], results[7])
            ae(values.D.H.O[2], results[8])
            ae(values.D.H.O[3], results[9])

            at(isinstance(values.D.H.Q, list))
            af(hasattr(values.D.H.Q, "_fields"))
            ae(len(values.D.H.Q), 2)
            ae(values.D.H.Q[0], (results[11], results[12]))
            ae(values.D.H.Q[1], (results[13], results[14]))

            at(hasattr(values.D.J.R, "_fields"))
            ae(values.D.J.R._fields, ("U", "V", "W"))
            ae(values.D.J.R._indices, (0, 1, 2))
            ae(values.D.J.R.U, results[16])
            ae(values.D.J.R.V, results[17])

            af(hasattr(values.D.H.O, "_fields"))

            at(hasattr(values.D.H.Q[0], "_fields"))
            ae(values.D.H.Q[0]._fields, ("Z", "AA"))
            ae(values.D.H.Q[0]._indices, (0, 1))

            at(hasattr(values.D.H.Q[1], "_fields"))
            ae(values.D.H.Q[1]._fields, ("Z", "AA"))
            ae(values.D.H.Q[1]._indices, (0, 1))

            at(hasattr(values.D.J.R.W, "_fields"))
            ae(values.D.J.R.W._fields,
                (
                    "DD", "EE", "bits_pad_",
                    "CC",
                    "DD__4", "EE__5", "bits_pad___6"
                )
            )
            ae(values.D.J.R.W._indices, (0, 1, 2, 3, 4, 5, 6))
            ae(values.D.J.R.W.CC, results[21])
            ae(values.D.J.R.W, results[18:25])
        # end for

        ar(ExtractionError, self.extractor.extract, data[:3])
    # end def test_extract

    def test_extract_partial(self):
        at = self.assertTrue
        ae = self.assertEqual
        extractor = self.extractor
        results = self.results
        data = self.data

        values = extractor.extract_partial(data)
        ae(values, results)

        values = extractor.extract_partial(b"")
        ae(values, tuple())

        values = extractor.extract_partial(data[:7])
        ae(len(values), 3)
        ae(values, results[:3])

        values = extractor.extract_partial(data[:32])
        ae(len(values), 15)
        ae(values, results[:15])

        values = extractor.extract_partial(data[:45])
        ae(len(values), 18)
        ae(values, results[:18])

        values = extractor.extract_partial(data[:46])
        ae(len(values), 18)
        ae(values, results[:18])

        values = extractor.extract_partial(data[:47])
        ae(len(values), 21)
        ae(values, results[:21])
    # end def test_extract_partial

    def test_get_grouping_info(self):
        ae = self.assertEqual
        groupbys = self.groupbys
        factories = self.factories
        decoders_at = self.decoders_at
        decoders = self.decoders


        struct_tree = NAryTree(DS_A._flatten())
        (test_groupbys, test_factories) = \
            self.extractor.get_grouping_info(struct_tree)

        ae(len(test_groupbys), len(groupbys))
        for (test_groupby, groupby) in zip(test_groupbys, groupbys):
            for(test_key, key) in zip(test_groupby, groupby):
                ae(test_key, key)
            # end for
        # end for

        ae(len(test_factories), len(factories))
        factories_iter = zip(test_factories, factories)
        for (test_factory, factory) in factories_iter:
            factory_func_iter = zip(test_factory, factory)
            for (test_func, func) in factory_func_iter:
                ae(test_func, func)
            # end for
        # end for
    # end def test_get_grouping_info

    def test_get_decoding_info(self):
        ae = self.assertEqual
        decoders_at = self.decoders_at
        decoders = self.decoders

        struct_tree = NAryTree(DS_A._flatten(expand_bits=False))
        (test_decoders_at, test_decoders) = \
            self.extractor.get_decoding_info(struct_tree)

        ae(test_decoders_at, decoders_at)

        ae(len(test_decoders), len(decoders))
        for (test_decoder, decoder) in zip(test_decoders, decoders):
            ae(test_decoder, decoder)
        # end for
    # end def test_get_decoding_info

    def test_get_record_strings(self):
        struct_tree = NAryTree(DS_A._flatten(expand_bits=False))
        test_record_strings = self.extractor.get_record_strings(struct_tree)
        self.assertEqual(test_record_strings, self.record_strings)
    # end def test_get_record_strings

    def test_get_size_at(self):

        struct_tree = NAryTree(DS_A._flatten(expand_bits=False))
        test_size_at = self.extractor.get_size_at(struct_tree)
        self.assertEqual(test_size_at, self.size_at)
    # end def test_get_size_at
# end class ExtractorTestCase

class ExtractableArrayTestCase(ExtractorTestCase):
    def setUp(self):
        super(ExtractableArrayTestCase, self).setUp()
        self.extractor = Extractor(ExtractableArray(DS_A, 4))
        self.decoders = self.decoders * 4
        self.results = self.results * 4
        self.data = b"".join([self.data] * 4)
        self.record_strings = [
            ">c", "<b3sd", ">IBBBihHhHBQf", "<HqH", ">bc", "<b3sd",
            ">IBBBihHhHBQf", "<HqH", ">bc", "<b3sd", ">IBBBihHhHBQf", "<HqH",
            ">bc", "<b3sd", ">IBBBihHhHBQf", "<HqH", ">b"
        ]

        decoders_at = list()
        for counter in range(4):
            offset = counter * 26
            decoders_at.extend([offset + x for x in self.decoders_at])
        # end for
        self.decoders_at = decoders_at

        size_at = list()
        for counter in range(4):
            added_size = counter * 58
            size_at.extend([added_size + size for size in self.size_at])
        # end for
        self.size_at = size_at

        new_factories = list()
        for factories in self.factories:
            new_factories.append(factories * 4)
        # end for
        new_factories.append([list])
        self.factories = new_factories

        new_groupbys = list()
        for groupby in self.groupbys:
            if groupby[0] != groupby[-1]:
                new_groupbys.append(groupby * 4)
            else:
                marker = 1
                new_groupby = list()
                for counter in range(4):
                    new_groupby.extend([marker * x for x in groupby])
                    marker *= -1
                # end for
                new_groupbys.append(new_groupby)
            # end if
        # end for
        new_groupbys.append([1, 1, 1, 1])
        self.groupbys = new_groupbys
    # end def setUp

    def test_get_grouping_info(self):
        ae = self.assertEqual
        groupbys = self.groupbys
        factories = self.factories


        struct_tree = \
            NAryTree(ExtractableArray(DS_A, 4)._flatten(expand_bits=True))

        (test_groupbys, test_factories) = \
            self.extractor.get_grouping_info(struct_tree)

        ae(len(test_groupbys), len(groupbys))
        for (test_groupby, groupby) in zip(test_groupbys, groupbys):
            for(test_key, key) in zip(test_groupby, groupby):
                ae(test_key, key)
            # end for
        # end for

        ae(len(test_factories), len(factories))
        factories_iter = zip(test_factories, factories)
        for (test_factory, factory) in factories_iter:
            for (test_func, func) in zip(test_factory, factory):
                ae(test_func, func)
            # end for
        # end for
    # end def test_get_grouping_info

    def test_get_decoding_info(self):
        ae = self.assertEqual
        decoders_at = self.decoders_at
        decoders = self.decoders
        struct_tree = NAryTree(
            ExtractableArray(DS_A, 4)._flatten(expand_bits=False)
        )
        (test_decoders_at, test_decoders) = \
            self.extractor.get_decoding_info(struct_tree)

        ae(test_decoders_at, decoders_at)

        ae(len(test_decoders), len(decoders))
        for (test_decoder, decoder) in zip(test_decoders, decoders):
            ae(test_decoder, decoder)
        # end for
    # end def test_get_grouping_info

    def test_get_record_strings(self):
        struct_tree = \
            NAryTree(ExtractableArray(DS_A, 4)._flatten(expand_bits=False))
        test_record_strings = self.extractor.get_record_strings(struct_tree)
        self.assertEqual(test_record_strings, self.record_strings)
    # end def test_get_record_strings

    def test_get_size_at(self):
        struct_tree = \
            NAryTree(ExtractableArray(DS_A, 4)._flatten(expand_bits=False))
        test_size_at = self.extractor.get_size_at(struct_tree)
        self.assertEqual(test_size_at, self.size_at)
    # end def test_get_size_at

    def test__init__(self):
        ae = self.assertEqual
        at = self.assertTrue

        extractor = self.extractor

        at(hasattr(extractor, "struct_objs"))
        at(hasattr(extractor, "groupbys"))
        at(hasattr(extractor, "factories"))
        at(hasattr(extractor, "size"))
        at(hasattr(extractor, "size_at"))

        ae(len(extractor.struct_objs), 17)
        for index, struct_obj in enumerate(extractor.struct_objs):
            ae(struct_obj.format.decode("ascii"), self.record_strings[index])
        # end for

        ae(extractor.size, 232)
    # end def test__init__

    def test_extract(self):
        af = self.assertFalse
        ae = self.assertEqual
        at = self.assertTrue
        ar = self.assertRaises

        data = self.data
        results = self.results

        values = self.extractor.extract(data, flatten=True)
        ae(len(values), 104)
        ae(values, results)

        for datum in (data, b"".join([data, data])):
            values = self.extractor.extract(datum, flatten=False)
            for counter in range(4):
                offset = counter * 26

                at(hasattr(values[counter], "_fields"))
                at(hasattr(values[counter], "_indices"))
                ae(values[counter]._fields, ("B", "C", "D", "E"))
                ae(values[counter]._indices, (0, 1, 2, 3))
                ae(values[counter][0], results[offset+0])
                ae(values[counter][3], results[offset+25])

                at(hasattr(values[counter].C, "_fields"))
                ae(values[counter].C._fields, ("F", "G"))
                ae(values[counter].C._indices, (0, 1))
                ae(values[counter].C[1], results[offset+4])

                at(hasattr(values[counter].D, "_fields"))
                ae(values[counter].D._fields, ("H", "I", "J"))
                ae(values[counter].D._indices, (0, 1, 2))
                ae(values[counter].D[1], results[offset+15])

                at(hasattr(values[counter].C.F, "_fields"))
                ae(values[counter].C.F._fields, ("K", "L", "M"))
                ae(values[counter].C.F._indices, (0, 1, 2))
                ae(values[counter].C.F, results[offset+1:offset+4])

                at(hasattr(values[counter].D.H, "_fields"))
                ae(values[counter].D.H._fields, ("N", "O", "P", "Q"))
                ae(values[counter].D.H._indices, (0, 1, 2, 3))
                ae(values[counter].D.H.N, results[offset+5])
                ae(values[counter].D.H.P, results[offset+10])

                at(hasattr(values[counter].D.J, "_fields"))
                ae(values[counter].D.J._fields, ("R",))
                ae(values[counter].D.J._indices, (0,))


                at(isinstance(values[counter].D.H.O, list))
                af(hasattr(values[counter].D.H.O, "_fields"))
                ae(len(values[counter].D.H.O), 4)
                ae(values[counter].D.H.O[0], results[offset+6])
                ae(values[counter].D.H.O[1], results[offset+7])
                ae(values[counter].D.H.O[2], results[offset+8])
                ae(values[counter].D.H.O[3], results[offset+9])

                at(isinstance(values[counter].D.H.Q, list))
                af(hasattr(values[counter].D.H.Q, "_fields"))
                ae(len(values[counter].D.H.Q), 2)
                ae(
                    values[counter].D.H.Q[0],
                    (results[offset+11], results[offset+12])
                )
                ae(
                    values[counter].D.H.Q[1],
                    (results[offset+13], results[offset+14])
                )

                at(hasattr(values[counter].D.J.R, "_fields"))
                ae(values[counter].D.J.R._fields, ("U", "V", "W"))
                ae(values[counter].D.J.R._indices, (0, 1, 2))
                ae(values[counter].D.J.R.U, results[offset+16])
                ae(values[counter].D.J.R.V, results[offset+17])

                af(hasattr(values[counter].D.H.O, "_fields"))

                at(hasattr(values[counter].D.H.Q[0], "_fields"))
                ae(values[counter].D.H.Q[0]._fields, ("Z", "AA"))
                ae(values[counter].D.H.Q[0]._indices, (0, 1))

                at(hasattr(values[counter].D.H.Q[1], "_fields"))
                ae(values[counter].D.H.Q[1]._fields, ("Z", "AA"))
                ae(values[counter].D.H.Q[1]._indices, (0, 1))

                at(hasattr(values[counter].D.J.R.W, "_fields"))
                ae(values[counter].D.J.R.W._fields,
                    (
                        "DD", "EE", "bits_pad_",
                        "CC",
                        "DD__4", "EE__5", "bits_pad___6"
                    )
                )
                ae(values[counter].D.J.R.W._indices, (0, 1, 2, 3, 4, 5, 6))
                ae(values[counter].D.J.R.W.CC, results[offset+21])
                ae(values[counter].D.J.R.W, results[offset+18:offset+25])
            # end for
        # end for

        ar(ExtractionError, self.extractor.extract, data[:3])
    # end def test_extract

    def test_extract_partial(self):
        at = self.assertTrue
        ae = self.assertEqual
        extractor = self.extractor
        results = self.results
        data = self.data

        values = extractor.extract_partial(data)
        ae(values, results)

        values = extractor.extract_partial(b"")
        ae(values, tuple())

        values = extractor.extract_partial(data[:7])
        ae(len(values), 3)
        ae(values, results[:3])

        values = extractor.extract_partial(data[:32])
        ae(len(values), 15)
        ae(values, results[:15])
        values = extractor.extract_partial(data[:45])
        ae(len(values), 18)
        ae(values, results[:18])

        values = extractor.extract_partial(data[:46])
        ae(len(values), 18)
        ae(values, results[:18])

        values = extractor.extract_partial(data[:47])
        ae(len(values), 21)
        ae(values, results[:21])
    # end def test_extract_partial
# end class ExtractableArrayTestCase
