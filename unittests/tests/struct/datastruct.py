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
Unit tests for the lf.struct.datastruct module

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

from unittest import TestCase, main
from lf.struct.datastruct import DataStruct, Array
from lf.struct.datatype import Int8, Int16, Int32

class DataStructTestCase(TestCase):
    def setUp(self):
        class TestDataStruct0(DataStruct):
            fields = [Int8("0_int8"), Int16("0_int16")]
        # end class TestDataStruct0

        class TestDataStruct1(DataStruct):
            fields = [
                Int8("1_int8"),
                TestDataStruct0("1_test_data_struct0"),
                Int16("1_int16")
            ]
        # end class TestDataStruct1

        self.data_struct0 = TestDataStruct0("field_name0")
        self.data_struct1 = TestDataStruct1("field_name1")
    # end def setUp

    def test_flatten(self):
        ae = self.assertEqual
        at = self.assertTrue

        data_struct0 = self.data_struct0
        data_struct1 = self.data_struct1

        dict_init0 = [
            (1, data_struct0),
            (2, data_struct0.fields[0]),
            (5, data_struct0.fields[1])
        ]

        dict_init1 = [
            (1, data_struct1),
            (2, data_struct1.fields[0]),
            (5, data_struct1.fields[1]),
            (10, data_struct1.fields[1].fields[0]),
            (21, data_struct1.fields[1].fields[1]),
            (11, data_struct1.fields[2])
        ]

        flattened0 = self.data_struct0.flatten()
        flattened1 = self.data_struct1.flatten()

        control_dict0 = dict(dict_init0)
        control_dict1 = dict(dict_init1)
        test_dict0 = dict(flattened0)
        test_dict1 = dict(flattened1)

        ae(len(control_dict0), len(test_dict0))
        ae(len(control_dict1), len(test_dict1))

        for key in control_dict0:
            at(key in test_dict0)
            ae(control_dict0[key], test_dict0[key])
        # end for

        for key in control_dict1:
            at(key in test_dict1)
            ae(control_dict1[key], test_dict1[key])
        # end for
    # end def test_flatten

    def test_size(self):
        self.assertEqual(self.data_struct0.size, 3)
        self.assertEqual(self.data_struct1.size, 6)
    # end def test_size
# end class DataStructTestCase

class ArrayTestCase(TestCase):
    def setUp(self):
        class TestDataStruct(DataStruct):
            fields = [Int8("int8"), Int16("int16")]
        # end class TestDataStruct

        data_struct = TestDataStruct()
        self.data_struct = data_struct
        self.int32 = Int32("int32")
        self.array0 = Array(3, data_struct)
        self.array1 = Array(5, self.int32)
    # end def setUp

    def test__init__(self):
        ae = self.assertEqual

        ae(len(self.array0.fields), 3)
        ae(len(self.array1.fields), 5)

        for field in self.array0.fields:
            ae(field.__class__, self.data_struct.__class__)
        # end for

        for field in self.array1.fields:
            ae(field.__class__, self.int32.__class__)
        # end for
    # end def test__init__

    def test_size(self):
        self.assertEqual(self.array0.size, 9)
        self.assertEqual(self.array1.size, 20)
    # end def test_size

    def test_flatten(self):
        ae = self.assertEqual
        at = self.assertTrue
        array0 = self.array0
        array1 = self.array1

        dict0_init = [
            (1, array0),
            (2, array0.fields[0]),
            (4, array0.fields[0].fields[0]),
            (9, array0.fields[0].fields[1]),
            (5, array0.fields[1]),
            (10, array0.fields[1].fields[0]),
            (21, array0.fields[1].fields[1]),
            (11, array0.fields[2]),
            (22, array0.fields[2].fields[0]),
            (45, array0.fields[2].fields[1])
        ]

        dict1_init = [
            (1, array1),
            (2, array1.fields[0]),
            (5, array1.fields[1]),
            (11, array1.fields[2]),
            (23, array1.fields[3]),
            (47, array1.fields[4])
        ]

        control_dict0 = dict(dict0_init)
        control_dict1 = dict(dict1_init)

        test_dict0 = dict(array0.flatten())
        test_dict1 = dict(array1.flatten())

        ae(len(control_dict0), len(test_dict0))
        ae(len(control_dict1), len(test_dict1))

        for key in control_dict0:
            at(key in test_dict0)
            ae(control_dict0[key], test_dict0[key])
        # end for

        for key in control_dict1:
            at(key in test_dict1)
            ae(control_dict1[key], test_dict1[key])
        # end for
    # end def test_flatten
# end class ArrayTestCase

class FieldIteratorTestCase(TestCase):
    def setUp(self):
        leaf_nodes = [
            Int8(), Int8(), Int8(), Int8(), Int8(), Int8(), Int8(), Int8(),
            Int8(), Int8()
        ]

        internal_nodes = list()

        class Internal0(DataStruct):
            fields = [leaf_nodes[2], leaf_nodes[3]]
        # end class Internal0
        internal_nodes.append(Internal0())

        class Internal1(DataStruct):
            fields = [leaf_nodes[1], internal_nodes[0], leaf_nodes[4]]
        # end class Internal1
        internal_nodes.append(Internal1())

        class Internal2(DataStruct):
            fields = [internal_nodes[1], leaf_nodes[5]]
        # end class Internal2
        internal_nodes.append(Internal2())

        class Internal3(DataStruct):
            fields = [leaf_nodes[6], leaf_nodes[7]]
        # end class Internal3
        internal_nodes.append(Internal3())

        #class Internal4(DataStruct):
        #    fields = [leaf_nodes[9], leaf_nodes[10], leaf_nodes[11]]
        ## end class Internal4
        internal_nodes.append(Array(3, leaf_nodes[9]))

        class Internal5(DataStruct):
            fields = [internal_nodes[4]]
        # end class Internal5
        internal_nodes.append(Internal5())

        class Internal6(DataStruct):
            fields = [internal_nodes[3], leaf_nodes[8], internal_nodes[5]]
        # end class Internal6
        internal_nodes.append(Internal6())

        class Internal7(DataStruct):
            fields = [leaf_nodes[0], internal_nodes[2], internal_nodes[6]]
        # end class Internal7
        internal_nodes.append(Internal7())

        self.data_struct = internal_nodes[7]
        leaf_node9 = internal_nodes[4].fields[0]
        leaf_node10 = internal_nodes[4].fields[1]
        leaf_node11 = internal_nodes[4].fields[2]

        self.flat_fields_postorder = [
            leaf_nodes[0], leaf_nodes[1], leaf_nodes[2], leaf_nodes[3],
            internal_nodes[0], leaf_nodes[4], internal_nodes[1], leaf_nodes[5],
            internal_nodes[2], leaf_nodes[6], leaf_nodes[7], internal_nodes[3],
            leaf_nodes[8], leaf_node9, leaf_node10, leaf_node11,
            internal_nodes[4], internal_nodes[5], internal_nodes[6],
            internal_nodes[7]
        ]

        self.flat_fields_preorder = [ internal_nodes[7], leaf_nodes[0],
            internal_nodes[2], internal_nodes[1], leaf_nodes[1],
            internal_nodes[0], leaf_nodes[2], leaf_nodes[3], leaf_nodes[4],
            leaf_nodes[5], internal_nodes[6], internal_nodes[3], leaf_nodes[6],
            leaf_nodes[7], leaf_nodes[8], internal_nodes[5], internal_nodes[4],
            leaf_node9, leaf_node10, leaf_node11
        ]

    # end def setUp

    # NOTE: This is broken... figure out a way to text post/pre order
    #def test_walk_postorder(self):
    #    iterator = FieldIterator.walk_postorder(self.data_struct)

    #    for index, field in enumerate(iterator):
    #        self.assertEqual(field, self.flat_fields_postorder[index])
    #    else:
    #        self.assertEqual(index, 19)
    #    # end for
    ## end def test_walk_postorder

    #def test_walk_preorder(self):
    #    iterator = FieldIterator.walk_preorder(self.data_struct)

    #    for index, field in enumerate(iterator):
    #        self.assertEqual(field, self.flat_fields_preorder[index])
    #    else:
    #        self.assertEqual(index, 19)
    #    # end for
    ## end def test_walk_preorder
# end class FieldIterator


if __name__ == "__main__":
    main()
# end if
