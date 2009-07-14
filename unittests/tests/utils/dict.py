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
Unit tests for lf.utils.dict module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)

"""

__docformat__ = "restructuredtext en"

from unittest import TestCase
from lf.utils.dict import BinaryTree, NAryTree, CachingDict

class BinaryTreeTestCase(TestCase):
    def setUp(self):
        node_ids = [
            1, 2, 5, 10, 20, 41, 21, 11, 22, 44, 89, 45, 91, 182, 364, 729,
            1459
        ]

        init = [(node_id, "{0}".format(node_id)) for node_id in node_ids]
        self.tree = BinaryTree(init)
    # end def setUp

    def test__init__(self):
        ar = self.assertRaises

        ar(TypeError, BinaryTree, [("1", 1)])
        ar(TypeError, BinaryTree, [(-1, 1)])
        ar(TypeError, BinaryTree, [(0, 1)])
    # end def test__init__

    def test__setitem__(self):
        ar = self.assertRaises

        ar(TypeError, BinaryTree.__setitem__, "1", 1)
        ar(TypeError, BinaryTree.__setitem__, -1, 1)
        ar(TypeError, BinaryTree.__setitem__, 0, 1)
    # end def test__setitem__

    def test_is_internal(self):
        ae = self.assertEqual
        ar = self.assertRaises

        results = {
            1: True,
            2: True,
            5: True,
            10: True,
            20: True,
            41: False,
            21: False,
            11: True,
            22: True,
            44: True,
            89: False,
            45: True,
            91: True,
            182: True,
            364: True,
            729: True,
            1459: False
        }

        for key, value in results.items():
            ae(self.tree.is_internal(key), value)
        # end for

        ar(TypeError, self.tree.is_internal, "1")
    # end def test_is_internal

    def test_is_external(self):
        ae = self.assertEqual
        ar = self.assertRaises

        results = {
            1: False,
            2: False,
            5: False,
            10: False,
            20: False,
            41: True,
            21: True,
            11: False,
            22: False,
            44: False,
            89: True,
            45: False,
            91: False,
            182: False,
            364: False,
            729: False,
            1459: True
        }

        for key, value in results.items():
            ae(self.tree.is_external(key), value)
        # end for

        ar(TypeError, self.tree.is_external, "1")
    # end def test_is_external

    def test_get_left_child_id(self):
        ae = self.assertEqual
        ar = self.assertRaises

        for key in self.tree:
            ae(self.tree.get_left_child_id(key), key * 2)
        # end for

        ar(TypeError, self.tree.get_left_child_id, "1")
    # end def test_get_left_child_id

    def test_has_left_child(self):
        ae = self.assertEqual
        ar = self.assertRaises

        results = {
            1: True,
            2: False,
            5: True,
            10: True,
            20: False,
            41: False,
            21: False,
            11: True,
            22: True,
            44: False,
            89: False,
            45: False,
            91: True,
            182: True,
            364: False,
            729: False,
            1459: False
        }

        for key, value in results.items():
            ae(self.tree.has_left_child(key), value)
        # end for

        ar(TypeError, self.tree.has_left_child, "1")
    # end def test_has_left_child

    def test_get_right_child_id(self):
        ae = self.assertEqual
        ar = self.assertRaises

        for key in self.tree:
            ae(self.tree.get_right_child_id(key), (key * 2) + 1)
        # end for

        ar(TypeError, self.tree.get_right_child_id, "1")
        ar(TypeError, self.tree.get_right_child_id, -1)
        ar(TypeError, self.tree.get_right_child_id, 0)
    # end def test_get_right_child_id

    def test_has_right_child(self):
        ae = self.assertEqual
        ar = self.assertRaises

        results = {
            1: False,
            2: True,
            5: True,
            10: True,
            20: True,
            41: False,
            21: False,
            11: False,
            22: True,
            44: True,
            89: False,
            45: True,
            91: False,
            182: False,
            364: True,
            729: True,
            1459: False
        }

        for key, value in results.items():
            ae(self.tree.has_right_child(key), value)
        # end for

        ar(TypeError, self.tree.has_right_child, "1")
    # end def test_has_right_child
# end class BinaryTreeTestCase

class NAryTreeTestCase(TestCase):
    def setUp(self):
        node_ids = [
            1, 2, 5, 10, 20, 41, 21, 11, 22, 44, 89, 45, 91, 182, 364, 729,
            1459
        ]

        self.node_ids = node_ids
        init = [(node_id, "{0}".format(node_id)) for node_id in node_ids]
        self.tree = NAryTree(init)
    # end def setUp

    def test_get_children_ids(self):
        ae = self.assertEqual
        ar = self.assertRaises

        results = {
            1: [2, 5, 11],
            2: [],
            5: [10, 21],
            10: [20, 41],
            20: [],
            41: [],
            21: [],
            11: [22, 45, 91],
            22: [44, 89],
            44: [],
            89: [],
            45: [],
            91: [182],
            182: [364, 729, 1459],
            364: [],
            729: [],
            1459: []
        }

        for key, value in results.items():
            ae(self.tree.get_children_ids(key), value)
        # end for

        ar(TypeError, self.tree.get_children_ids, "1")
    # end def test_get_children_ids

    def test_get_sibling_ids(self):
        ae = self.assertEqual
        ar = self.assertRaises

        results = {
            1: [],
            2: [5, 11],
            5: [11],
            10: [21],
            20: [41],
            41: [],
            21: [],
            11: [],
            22: [45, 91],
            44: [89],
            89: [],
            45: [91],
            91: [],
            182: [],
            364: [729, 1459],
            729: [1459],
            1459: []
        }

        for key, value in results.items():
            ae(self.tree.get_sibling_ids(key), value)
        # end for

        ar(TypeError, self.tree.get_sibling_ids, "1")
    # end def test_get_sibling_ids:

    def test_walk_postorder(self):
        ae = self.assertEqual
        results = [
            2, 20, 41, 10, 21, 5, 44, 89, 22, 45, 364, 729, 1459, 182, 91, 11,
            1
        ]

        for index, node_id in enumerate(self.tree.walk_postorder()):
            ae(node_id, results[index])
        # end for
    # end def walk_postorder

    def test_get_leaf_ids(self):
        ae = self.assertEqual
        results = [2, 20, 41, 21, 44, 89, 45, 364, 729, 1459]

        for index, node_id in enumerate(self.tree.get_leaf_ids()):
            ae(node_id, results[index])
        # end for
    # end def test_get_leaf_ids

    def test_get_parent_id(self):
        fue = self.failUnlessEqual
        results = [
            1, 1, 5, 10, 10, 5, 1, 11, 22, 22, 11, 11, 91, 182, 182, 182
        ]

        for (index, node_id) in enumerate(self.node_ids[1:]):
            fue(self.tree.get_parent_id(node_id), results[index])
        # end for
    # end def test_get_parent_id
# end class NAryTreeTestCase

class CachingDictTestCase(TestCase):
    def setUp(self):
        self.caching_dict = CachingDict()
    # end def setUp

    def test__setitem__(self):
        ae = self.assertEqual
        ar = self.assertRaises
        cd = self.caching_dict

        results = [(x, "{0}".format(x), x+1) for x in range(500)]
        results.extend([(x, "{0}".format(x), 500) for x in range(500, 525)])

        for key, value, size in results:
            cd[key] = value
            ae(len(cd), size)
        # end for

        for x in range(25):
            ar(KeyError, cd.__getitem__, x)
        # end for
    # end def test__setitem__
# end class CachingDictTestCase
