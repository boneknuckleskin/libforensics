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
Various classes that are implemented with dictionaries.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "BinaryTree", "NAryTree", "CachingDict"
]

from collections import OrderedDict

class BinaryTree(dict):
    """
    'Light-weight' binary tree.

    All keys must be non-negative integers.  The root node is 1.  Therefore the
    left child is id * 2, and the right child is (id * 2) + 1.
    """

    def __init__(self, *args, **kwds):
        """
        Initializes a BinaryTree object.

        :raises:
            TypeError
                If any of the keys are invalid (other than non-negative
                integers).
        """

        super(BinaryTree, self).__init__(*args, **kwds)

        for key in self:
            if isinstance(key, int):
                if key >= 1:
                    continue
                # end if
            # end if

            raise TypeError("Invalid key {0} for a BinaryTree".format(key))
        # end for
    # end def __init__

    def __setitem__(self, key, value):
        """
        self[key] = value

        :raises:
            TypeError
                If key is invalid.
        """

        if not isinstance(key, int):
                raise TypeError("Invalid type of key {0}".format(key))
        elif key < 1:
                raise TypeError("Invalid type of key {0}".format(key))
        # end if

        super(BinaryTree, self).__setitem__(key, value)
    # end def __setitem__

    def is_internal(self, node_id):
        """
        Checks to see if a node is an internal node (has children).

        :parameters:
            node_id
                The identifier of the node to check.

        :raises:
            TypeError
                If node_id is not a valid key.

            KeyError
                If node_id does not exist.

        :rtype: bool
        :returns: True if node_id has children, False otherwise.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id not in self:
            raise KeyError("Key not found {0}".format(node_id))
        # end if

        return ((node_id * 2) in self) or (((node_id * 2) + 1) in self)
    # end def is_internal


    def is_external(self, node_id):
        """
        Checks to see if a node is an external node (leaf).

        :parameters:
            node_id
                The identifier of the node to check.

        :raises:
            TypeError
                If node_id is an invalid key.

            KeyError
                If node_id does not exist.

        :rtype: bool
        :returns: True if node_id does not have children, False otherwise.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id not in self:
            raise KeyError("Key not found {0}".format(node_id))
        # end if

        if ((node_id * 2) + 1) in self:
            return False
        # end if

        return \
            ((node_id * 2) not in self) and (((node_id * 2) + 1) not in self)
    # end def is_external

    def get_left_child_id(self, node_id):
        """
        Returns the left child of a node.

        :parameters:
            node_id
                The key for the node to find the children for.

        :raises:
            TypeError
                If node_id is invalid

        :rtype: int
        :returns: The id of the left child.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        # end if

        return node_id * 2
    # end def get_left_child

    def get_right_child_id(self, node_id):
        """
        Returns the left child of a node.

        :parameters:
            node_id
                The key for the node to find the children for.

        :raises:
            TypeError
                If node_id is invalid

        :rtype: int
        :returns: The id of the left child.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        # end if

        return (node_id * 2) + 1
    # end def get_right_child_id

    def has_left_child(self, node_id):
        """
        Checks to see if a node has a left child.

        :parameters:
            node_id
                The key for the node to check.

        :raises:
            TypeError
                If node_id is an invalid key.

            KeyError
                If node_id does not exist.

        :rtype: bool
        :returns: True if node_id has a left child, False otherwise.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id not in self:
            raise KeyError("Key not found {0}".format(node_id))
        # end if

        return (node_id * 2) in self
    # end def has_left_child

    def has_right_child(self, node_id):
        """
        Checks to see if a node has a right child.

        :parameters:
            node_id
                The key for the node to check.

        :raises:
            TypeError
                If node_id is an invalid key.

            KeyError
                If node_id does not exist.

        :rtype: bool
        :returns: True if node_id has a right child, False otherwise.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id not in self:
            raise KeyError("Key not found {0}".format(node_id))
        # end if

        return ((node_id * 2) + 1) in self
    # end def has_right_child

    has_children = is_internal
    is_leaf = is_external
# end class BinaryTree

class NAryTree(BinaryTree):
    """
    Uses a BinaryTree to support multiple items.

    Children are left nodes, siblings are right nodes.
    """

    def has_children(self, node_id):
        return self.has_left_child(node_id)
    # end def has_children

    def get_children_ids(self, node_id):
        """
        Retrieves the children of a node.

        :parameters:
            node_id
                The parent node, to find the children for.

        :raises:
            TypeError
                If node_id is invalid.

            KeyError
                If node_id does not exist.

        :rtype: list
        :returns: A list of the identifiers of the children.
        """

        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id not in self:
            raise KeyError("Key not found {0}".format(node_id))
        # end if

        child_id = self.get_left_child_id(node_id)
        if child_id not in self:
            return list()
        # end if

        children = [child_id]
        children.extend(self.get_sibling_ids(child_id))

        return children
    # end def get_children_ids

    def has_siblings(self, node_id):
        return self.hasright_child(node_id)
    # end def has_siblings

    def get_sibling_ids(self, node_id):
        """
        Retrieves a list of siblings (to the right) of a node.

        :parameters:
            node_id
                The identifier of the node to start with.

        :raises:
            TypeError
                If node_id is an invalid type of key.

            KeyError
                If key does not exist.

        :rtype: list
        :returns: A list of nodes (not including key) to the right of key.
        """
        if not isinstance(node_id, int):
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id < 1:
            raise TypeError("Invalid type of key {0}".format(node_id))
        elif node_id not in self:
            raise KeyError("Key not found {0}".format(node_id))
        # end if

        siblings = list()

        next_id = (node_id * 2) + 1

        while next_id in self:
            siblings.append(next_id)
            next_id = (next_id * 2) + 1
        # end while

        return siblings
    # end def get_sibling_ids

    def walk_postorder(self):
        """
        Iterates through the tree, in a post-order fashion.

        :rtype: iterator
        :returns: An iterator, that walks through the keys of the tree, in a
                  post-order fashion.
        """

        first_nodes = self.get_children_ids(1)
        stack = [(1, iter(first_nodes))]

        while stack:
            (parent_id, node_iter) = stack.pop()

            for node_id in node_iter:
                if not self.has_children(node_id):
                    yield node_id
                else:
                    # Save current information to the stack
                    stack.append((parent_id, node_iter))

                    # Save new information to the stack
                    children = self.get_children_ids(node_id)
                    stack.append((node_id, iter(children)))

                    break
                # end if
            else:
                yield parent_id
            # end for
        # end while
    # end def walk_postorder

    def get_leaf_ids(self):
        """
        Finds all of the leaves in the tree.

        :rtype: list
        :returns: A list of the keys of all of the leaves in the tree.
        """

        leaves = list()
        for node_id in self.walk_postorder():
            if not self.has_children(node_id):
                leaves.append(node_id)
            # end if
        # end for

        return leaves
    # end def get_leaf_ids
# end class NAryTree

class CachingDict(OrderedDict):
    """
    Implements a caching dictionary.

    .. attribute:: _max_cache_size

        The maximum number of entries in the cache.
    """

    _max_cache_size = 500

    def __setitem__(self, key, value):
        """self[key] = value"""

        if key not in self:
            if len(self) >= self._max_cache_size:
                for index in range(len(self) - self._max_cache_size + 1):
                    self.popitem(last=False)
                # end for
            # end if
        # end if

        super(CachingDict, self).__setitem__(key, value)
    # end def __setitem__
# end class CachingDict
