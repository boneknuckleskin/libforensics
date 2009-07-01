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
New and "improved" extractor module.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "ExtractorFactory", "Extractor", "ListExtractor", "extractor_factory"
]

from operator import itemgetter
from struct import Struct
from collections import namedtuple
from itertools import groupby

from lf.utils.dict import NAryTree, CachingDict

from lf.struct.datastruct import Primitive, DataStruct, Array
from lf.struct.excepts import ExtractionError, StructError

# Used during extraction to do nothing
def _null_tuple(args):
    return args[0]
# end def _null_tuple

class ExtractorFactory():
    """
    Creates extractors from data structures.

    .. attribute:: namedtuple_cache

        A CachingDict object, to keep track of named tuples as they are
        created.
    """

    def __init__(self):
        """Initializes an ExtractorFactory object."""

        self.namedtuple_cache = CachingDict()
    # end def __init__

    @staticmethod
    def make_namedtuple_factory(data_struct):
        """
        Makes a namedtuple factory function.

        :parameters:
            A DataStruct object.

        :rtype: function
        :returns: A factory function that creates a named tuple.
        """

        klass = data_struct.__class__
        if hasattr(klass, "__name__"):
            name = "".join([
                "__NT_", klass.__name__
            ])
        else:
            name = "__NT_AnonymousStruct"
        # end if

        fields = [field.field_name for field in data_struct.fields]

        return(namedtuple(name, fields)._make)
    # end def make_namedtuple_factory

    def get_grouping_info(self, data_struct):
        """
        Gets information necessary to group the fields after they've been
        extracted.

        :parameters:
            data_struct
                A DataStruct object, describing the data structure.

        :rtype: tuple
        :returns: A tuple of (groupbys, tuple_factories) that can be iterated
                  over, to rebuild the hierarchical structure.
        """

        namedtuple_cache = self.namedtuple_cache

        # First thing we do is convert the data_struct into a binary tree, and
        # find the leaves.
        struct_tree = NAryTree(data_struct.flatten())
        leaves = struct_tree.get_leaf_ids()

        # Now we get the named tuples, and the groupbys
        groupbys = list()
        tuple_facts = list()

        while leaves[0] != 1:
            already_seen = list()
            current_groupby = list()
            current_tuple_facts = list()
            leaves_to_delete = list()
            marker = 1

            # Process the leaves
            for leaf_id in leaves:
                if leaf_id & 0x01:
                    if leaf_id not in already_seen:
                        # It's odd and we haven't already seen the id.  This
                        # implies that one of the previous siblings has
                        # children.  So this node will be a standalone.

                        current_groupby.append(marker)
                        current_tuple_facts.append(_null_tuple)
                        already_seen.append(leaf_id)
                        marker *= -1
                    # end if
                else:
                    # Otherwise figure out if we have a subtree of just
                    # primitives (terminals)
                    is_terminal_subtree = False
                    siblings = struct_tree.get_sibling_ids(leaf_id)

                    for sibling_id in siblings:
                        if struct_tree.has_children(sibling_id):
                            break
                        # end if
                    else:
                        is_terminal_subtree = True
                    # end for

                    # Insert the current leaf_id into siblings, so when we
                    # process the list, we don't have to make a special
                    # exception for the current leaf_id
                    siblings.insert(0, leaf_id)

                    if is_terminal_subtree:
                        # Insert the current leaf_id, so the for loop includes
                        for sibling_id in siblings:
                            current_groupby.append(marker)
                            already_seen.append(sibling_id)
                            leaves_to_delete.append(sibling_id)
                        else:
                            marker *= -1
                        # end while


                        # Create the named tuple (if necessary)
                        parent_id = leaf_id // 2
                        parent_obj = struct_tree[parent_id]
                        parent_class = parent_obj.__class__

                        if isinstance(parent_obj, Array):
                            current_tuple_facts.append(tuple)
                        elif parent_class in namedtuple_cache:
                            current_tuple_facts.append(
                                namedtuple_cache[parent_class]
                            )
                        else:
                            namedtuple_factory = \
                                self.make_namedtuple_factory(parent_obj)

                            namedtuple_cache[parent_class] = namedtuple_factory

                            current_tuple_facts.append(namedtuple_factory)
                        # end if
                    else:
                        # Make an alternating pattern
                        for sibling_id in siblings:
                            if struct_tree.has_children(sibling_id):
                                break
                            # end if

                            current_groupby.append(marker)
                            current_tuple_facts.append(_null_tuple)
                            already_seen.append(sibling_id)
                            marker *= -1
                        # end for
                    # end if
                # end if
            # end for

            # Save current grouping information
            groupbys.append(current_groupby)
            tuple_facts.append(current_tuple_facts)

            # Get rid of the leaves we can delete (leaves which make up a
            # terminal subtree)
            for leaf_id in leaves_to_delete:
                del struct_tree[leaf_id]
            # end for

            # Build up a new list of leaves
            leaves = struct_tree.get_leaf_ids()
        # end while

        return (groupbys, tuple_facts)
    # end def get_grouping_info

    @staticmethod
    def get_struct_strings(data_struct):
        """
        Creates strings for the standard library struct module.

        :parameters:
            data_struct
                A DataStruct object, describing the data structure.

        :rtype: list
        :returns: A list of strings suitable for the standard library struct
                  module.
        """

        struct_tree = NAryTree(data_struct.flatten())

        primitives = list()
        composites = list()

        # Separate the primitives and the composites
        for node_id in struct_tree.walk_postorder():
            if struct_tree.has_children(node_id):
                composites.append(node_id)
            else:
                primitives.append(node_id)
        # end for

        # Create a mapping of primitives and their byte order
        byte_orders = dict()
        for composite in composites:
            children = struct_tree.get_children_ids(composite)

            for child in children:
                if child in primitives:
                    byte_orders[child] = struct_tree[composite].byte_order
                # end if
            # end for
        # end for

        # Walk through the list of primitives, making new strings when the byte
        # order changes.
        format_strs = list()
        groupby_iter = groupby(primitives, byte_orders.__getitem__)

        for (byte_order, group_iter) in groupby_iter:
            format_str = [byte_order]
            format_str.extend(
                struct_tree[node_id].format_str for node_id in group_iter
            )
            format_strs.append("".join(format_str))
        # end for

        return format_strs
    # end def get_struct_strings

    @staticmethod
    def get_sizes_so_far(data_struct):
        """
        Calculates the cumulative number of bytes needed, at each field
        position.

        :parameters:
            data_struct
                A DataStruct object that describes the data structure.

        :rtype: list
        :returns: A list of the cumulative number of bytes needed at each field
                  position.
        """
        struct_tree = NAryTree(data_struct.flatten())
        leaves = struct_tree.get_leaf_ids()

        sizes_so_far = [0]
        for leaf_id in leaves:
            size = struct_tree[leaf_id].size
            sizes_so_far.append(size + sizes_so_far[-1])
        # end for
        del sizes_so_far[0]

        return sizes_so_far
    # end def get_sizes_so_far

    def make(self, data_struct):
        """
        Makes an Extractor.

        :parameters:
            data_struct
                A DataStruct object, describing the data structure.

        :raises:
            StructError
                If data_struct.fields contains any composite data structures.

        :rtype: Extractor
        :returns: An extractor that extracts data_struct from bytes.
        """
        grouping_info = self.get_grouping_info(data_struct)
        struct_strings = self.get_struct_strings(data_struct)
        sizes_so_far = self.get_sizes_so_far(data_struct)

        return Extractor(struct_strings, grouping_info, sizes_so_far)
    # end def make

    def make_list(self, count, data_struct):
        """
        Makes a ListExtractor.

        :parameters:
            count
                The number of data_structs to extract at a time.

            data_struct
                A DataStruct object, describing the data structure.

        :rtype: ListExtractor
        :returns: An extractor that can extract count data_structs from bytes.
        """

        for field in data_struct.fields:
            if isinstance(field, DataStruct):
                raise StructError("data_struct can not contain composites")
            # end if
        # end for

        (groupbys, tuple_factories) = self.get_grouping_info(data_struct)
        struct_string = self.get_struct_strings(data_struct)[0]
        sizes_so_far = self.get_sizes_so_far(data_struct)
        tuple_factory = tuple_factories[0][0]

        return ListExtractor(
            count, struct_string, tuple_factory, sizes_so_far
        )
    # end def make_list
# end class ExtractorFactory

class Extractor():
    """
    Extracts a data structure from a bytes object.

    .. attribute:: struct_objs

        A list of Struct objects that extract the fields of the data structure.

    .. attribute:: groupbys

        A list of lists, used to iteratively rebuild the hierarchical
        structure.

    .. attribute:: tuple_factories

        A list of lists, used to iteratively rebuild the hierarchical
        structure.

    .. attribute:: size

        The minimum number of bytes needed to extract the data structure.

    .. attribute:: sizes_so_far

        A list of the cumulative sizes at each field position.
    """

    def __init__(self, struct_strings, grouping_info, sizes_so_far):
        """
        Initializes an Extractor object.

        :parameters:
            struct_strings
                A list of struct strings, used to create the struct_objs
                attribute.

            grouping_info
                A tuple of (groupbys, tuple_factories)

            sizes_so_far
                A list of the cumulative sizes at each field position.
        """

        struct_objs = list()

        for struct_string in struct_strings:
            struct_obj = Struct(struct_string)
            struct_objs.append(struct_obj)
        # end for

        self.struct_objs = struct_objs
        self.groupbys = grouping_info[0]
        self.tuple_factories = grouping_info[1]
        self.sizes_so_far = sizes_so_far
        self.size = sizes_so_far[-1]
    # end def __init__

    def extract(self, bytes_obj, flatten=False):
        """
        Extracts a data structure from a bytes object.

        :parameters:
            bytes_obj
                The bytes object that contains the raw data structure.

            flatten
                If true, the hierarchical structure is *NOT* applied.

        :raises:
            ExtractionError
                If bytes_obj is not long enough.

        :rtype: tuple
        :returns: The extracted fields
        """

        if len(bytes_obj) < self.size:
            raise ExtractionError("bytes_obj too small")
        # end if

        values = list()
        offset = 0
        for struct_obj in self.struct_objs:
            values.extend(struct_obj.unpack_from(bytes_obj, offset))
            offset += struct_obj.size
        # end for

        if flatten:
            return tuple(values)
        # end if

        group_info_iter = zip(self.groupbys, self.tuple_factories)
        for groupbys, tuple_factories in group_info_iter:
            grouped_values = groupby(zip(groupbys, values), itemgetter(0))

            new_values = list()
            for index, (marker, group) in enumerate(grouped_values):
                just_values = list(map(itemgetter(1), group))
                new_values.append(tuple_factories[index](just_values))
            # end for

            values = new_values
        # end for

        return values[0]
    # end def extract

    def extract_partial(self, bytes_obj):
        """
        Extracts as many fields as possible from a bytes object.

        :parameters:
            bytes_obj
                The bytes object that contains the raw data structure.

        :rtype: tuple
        :returns: The extracted fields.
        """

        bytes_obj_len = len(bytes_obj)

        if bytes_obj_len >= self.size:
            return self.extract(bytes_obj, flatten=True)
        # end if

        padding = b"\x00" * (self.size - bytes_obj_len)
        padded_bytes_obj = b"".join([bytes_obj, padding])
        values = self.extract(padded_bytes_obj, flatten=True)

        for index, size_so_far in enumerate(self.sizes_so_far):
            if bytes_obj_len < size_so_far:
                return values[:index]
            elif bytes_obj_len == size_so_far:
                return values[:index+1]
            # end if
        # end for

        return values
    # end def extract_partial
# end class Extractor

class ListExtractor():
    """
    Extracts a list of homogenous data structures.

    Note: This class does not work with nested data structures.

    .. attribute:: struct_obj_list

        A Struct object that extracts count data structures at a time.

    .. attribute:: struct_obj_single

        A Struct object that extracts a single instance of a data structure.

    .. attribute:: count

        The number of data structures extracted by struct_obj_list.

    .. attribute:: tuple_factory

        A tuple class, used to group the extracted fields.

    .. attribute:: size

        The number of bytes needed to extract count data structures.

    .. attribute:: sizes_so_far

        A list of the cumulative number of bytes needed at each field position.

    .. attribute:: field_count

        The number of fields in the data structure.
    """

    def __init__(self, count, struct_string, tuple_factory, sizes_so_far):
        """
        Initializes a ListExtractor object.

        :parameters:
            count
                The number of data structures to extract.

            struct_string
                A format string, describing the data structure.

            tuple_factory
                A tuple class, used to group the extracted fields.

            sizes_so_far
                A list of the cumulative number of bytes needed at each field
                position.
        """

        list_struct_string = [struct_string[0]]
        list_struct_string.extend([struct_string[1:]] * count)
        list_struct_string = "".join(list_struct_string)

        struct_obj_single = Struct(struct_string)
        temp_bytes = b"\x00" * struct_obj_single.size
        field_count = len(struct_obj_single.unpack(temp_bytes))


        self.struct_obj_list = Struct(list_struct_string)
        self.struct_obj_single = struct_obj_single
        self.count = count
        self.tuple_factory = tuple_factory
        self.sizes_so_far = sizes_so_far
        self.size = self.struct_obj_list.size
        self.field_count = field_count
    # end def __init__

    def extract(self, bytes_obj, flatten=False):
        """
        Extracts data structures from a bytes object.

        :parameters:
            bytes_obj
                A bytes object that contains the raw data structure.

            flatten
                If true, does not group the extracted fields.

        :rtype: tuple
        :returns: A tuple of the extracted fields.
        """

        bytes_obj_len = len(bytes_obj)
        struct_obj_list = self.struct_obj_list
        struct_obj_single = self.struct_obj_single

        list_size = self.size
        list_count = bytes_obj_len // list_size

        single_size = struct_obj_single.size
        remainder = bytes_obj_len % list_size
        single_count = remainder // single_size

        group_count = bytes_obj_len // single_size
        field_count = self.field_count
        tuple_factory = self.tuple_factory

        values = list()
        offset = 0
        for index in range(list_count):
            values.extend(struct_obj_list.unpack_from(bytes_obj, offset))
            offset += list_size
        # end for

        for index in range(single_count):
            values.extend(struct_obj_single.unpack_from(bytes_obj, offset))
            offset += single_size
        # end for

        if flatten:
            return tuple(values)
        # end if

        grouped_values = list()
        for index in range(group_count):
            start = index * field_count
            stop = start + field_count
            grouped_values.append(tuple_factory(values[start:stop]))
        # end for

        return grouped_values
    # end def extract
# end class ListExractor

extractor_factory = ExtractorFactory()
