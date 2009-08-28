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
    "Extractor"
]

from copy import copy
from operator import itemgetter
from struct import Struct
from itertools import groupby

from lf.utils.dict import NAryTree

from lf.datatype.bits import BitType
from lf.datatype.composite import Extractable
from lf.datatype.excepts import ExtractionError

PASS_THRU = 0

class Extractor():
    """
    Extracts a data structure from a bytes object.

    .. attribute:: struct_objs

        A list of Struct objects that extract the fields of the data structure.

    .. attribute:: groupbys

        A list of lists, used to iteratively rebuild the hierarchical
        structure.

    .. attribute:: factories

        A list of lists, used to iteratively rebuild the hierarchical
        structure.

    .. attribute:: decoders_at

        A list of locations that need a decoder applied (prior to recreating
        the hierarchical structure.)

    .. attribute:: decoders

        A list of decoders to represent bit fields.

    .. attribute:: size

        The minimum number of bytes needed to extract the data structure.

    .. attribute:: size_at

        A list of the cumulative size at each field position.
    """

    def __init__(self, record):
        """
        Initializes an Extractor object.

        :parameters:
            record
                A Extractable object/class to extract.
        """

        record_tree = NAryTree(record._flatten(expand_bits=False))
        leaf_ids = record_tree.get_leaf_ids()

        record_strings = self.get_record_strings(record_tree, leaf_ids)
        size_at = self.get_size_at(record_tree, leaf_ids)
        decoding_info = self.get_decoding_info(record_tree, leaf_ids)

        record_tree = NAryTree(record._flatten(expand_bits=True))
        grouping_info = self.get_grouping_info(record_tree)

        struct_objs = list()
        size = 0
        for record_string in record_strings:
            struct_obj = Struct(record_string)
            struct_objs.append(struct_obj)
            size += struct_obj.size
        # end for

        self.struct_objs = struct_objs
        self.groupbys = grouping_info[0]
        self.factories = grouping_info[1]
        self.decoders_at = decoding_info[0]
        self.decoders = decoding_info[1]
        self.size_at = size_at
        self.size = size
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

        for (location, decoder) in zip(self.decoders_at, self.decoders):
            values[location:location + 1] = decoder.decode(values[location])
        # end for

        if flatten:
            return tuple(values)
        # end if


        group_info_iter = zip(self.groupbys, self.factories)
        for (groupbys, factories) in group_info_iter:
            groupby_iter = groupby(zip(groupbys, values), itemgetter(0))

            new_values = list()
            for (index, (marker, group)) in enumerate(groupby_iter):
                factory = factories[index]
                just_values = list(map(itemgetter(1), group))

                if factory == PASS_THRU:
                    new_values.extend(just_values)
                else:
                    new_values.append(factory(just_values))
                    # end if
                # end if
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
        decoders_at = self.decoders_at
        decoders = self.decoders

        if bytes_obj_len >= self.size:
            return self.extract(bytes_obj, flatten=True)
        elif bytes_obj_len < self.size_at[0]:
            return tuple()
        # end if

        padding = b"\x00" * (self.size - bytes_obj_len)
        padded_bytes_obj = b"".join([bytes_obj, padding])
        values = self.extract(padded_bytes_obj, flatten=True)

        bit_count = 0
        for (index, size_at) in enumerate(self.size_at[1:], 1):
            if bytes_obj_len < size_at:
                values = values[:bit_count + index]
                break
            elif bytes_obj_len == size_at:
                try:
                    bit_count += \
                        decoders[decoders_at.index(bit_count+index)].count - 1
                except ValueError:
                    pass
                except:
                    raise
                # end try

                values = values[:bit_count + index + 1]
                break
            # end if

            try:
                bit_count += \
                    decoders[decoders_at.index(bit_count + index)].count - 1
            except ValueError:
                pass
            except:
                raise
            # end try
        # end for

        return values
    # end def extract_partial

    @staticmethod
    def get_decoding_info(record_tree, leaf_ids=None):
        """
        Gets information necessary to decode the fields after they've been
        extracted.

        :parameters:
            record_tree
                An NAryTree built with a flattened version of the data
                structure.  The call to flatten() should have expand_bits set
                to False.

            leaf_ids
                An optional list of the identifiers of the leaves of
                record_tree.

        :rtype: tuple
        :returns: A tuple of (decoders_at, decoders) that can be iterated over
                  to decode the individual bit fields.
        """

        if leaf_ids is None:
            leaf_ids = record_tree.get_leaf_ids()
        # end if

        decoders = list()
        decoders_at = list()
        counter = 0
        added_field_count = 0

        for leaf_id in leaf_ids:
            field = record_tree[leaf_id]

            if hasattr(field, "_decoder_"):
                decoder = field._decoder_
                decoders.append(decoder)
                decoders_at.append(counter + added_field_count)
                added_field_count += (decoder.count - 1)
            # end if

            counter += 1
        # end for

        return (decoders_at, decoders)
    # end def get_decoding_info

    @staticmethod
    def get_grouping_info(record_tree, leaf_ids=None):
        """
        Gets information necessary to group the fields after they've been
        extracted.

        :parameters:
            record_tree
                An NAryTree built with a flattened version of the data
                structure.  The call to flatten() should have expand_bits set
                to false.  NOTE: This function will modify the values of
                record_tree.

            leaf_ids
                An optional list of the identifiers of the leaves of
                record_tree.  This list of leaf_ids should have been retrieved
                from a record_tree which had the expand_bits set to true, when
                it was built.

        :rtype: tuple
        :returns: A tuple of (groupbys, factories) that can be iterated
                  over to rebuild the hierarchical structure.
        """


        if leaf_ids is None:
            leaf_ids = record_tree.get_leaf_ids()
        # end if

        groupbys = list()
        factories = list()

        while leaf_ids[0] != 1:
            already_seen = list()
            current_groupby = list()
            current_factories = list()
            leaf_ids_to_delete = list()
            marker = 1

            # Process the leaves
            for leaf_id in leaf_ids:
                if leaf_id in already_seen:
                    continue
                # end if

                if leaf_id & 0x01:
                    # It's odd and we haven't alaready seen the leaf_id.  This
                    # implies that one of the previous siblings had children.
                    # So this field will be a standalone.

                    current_groupby.append(marker)
                    current_factories.append(PASS_THRU)
                    already_seen.append(leaf_id)
                    marker *= -1
                else:
                    # Otherwise figure out if we have a subtree of just
                    # primitives (terminals)
                    is_terminal_subtree = False
                    sibling_ids = record_tree.get_sibling_ids(leaf_id)

                    for sibling_id in sibling_ids:
                        if (sibling_id * 2) in record_tree:
                            break
                        # end if
                    else:
                        is_terminal_subtree = True
                    # end for

                    # Insert the current leaf_id into siblings, so when we
                    # process the list, we don't have to make a special
                    # exception for the current leaf_id
                    sibling_ids.insert(0, leaf_id)

                    if is_terminal_subtree:
                        # Insert the current leaf_id, so the for loop includes
                        for sibling_id in sibling_ids:
                            current_groupby.append(marker)
                            already_seen.append(sibling_id)
                            leaf_ids_to_delete.append(sibling_id)
                        else:
                            marker *= -1
                        # end while

                        # Create the tuple factory (if necessary)
                        parent_id = leaf_id // 2
                        parent_field = record_tree[parent_id]
                        if not isinstance(parent_field, BitType):
                            current_factories.append(
                                parent_field._factory_
                            )
                        # end if
                    else:
                        # Make an alternating pattern
                        for sibling_id in sibling_ids:
                            if (sibling_id * 2) in record_tree:
                                break
                            # end if

                            current_groupby.append(marker)
                            current_factories.append(PASS_THRU)
                            already_seen.append(sibling_id)
                            marker *= -1
                        # end for
                    # end if
                # end if
            # end for

            # Save current grouping information
            groupbys.append(current_groupby)
            factories.append(current_factories)

            # Get rid of the leaves we can delete (leaves which make up a
            # terminal subtree)
            for leaf_id in leaf_ids_to_delete:
                del record_tree[leaf_id]
            # end for

            # Build up a new list of leaves
            leaf_ids = record_tree.get_leaf_ids()
        # end while

        return (groupbys, factories)
    # end def get_grouping_info

    @staticmethod
    def get_record_strings(record_tree, leaf_ids=None):
        """
        Creates strings for the standard library struct module.

        :parameters:
            record_tree
                An NAryTree built from a flattened version of the data
                structure.

            leaf_ids
                An optional list of the identifiers of the leaves of
                record_tree.

        :rtype: list
        :returns: A list of strings suitable for the standard library struct
                  module.
        """

        if leaf_ids is None:
            leaf_ids = record_tree.get_leaf_ids()
        # end if

        byte_orders = dict()
        for leaf_id in leaf_ids:
            if leaf_id & 0x1:
                left_sib = (leaf_id - 1) // 2
                if left_sib in byte_orders:
                    byte_orders[leaf_id] = byte_orders[left_sib]
                else:
                    parent_id = record_tree.get_parent_id(leaf_id)
                    parent_field = record_tree[parent_id]

                    while not hasattr(parent_field, "_byte_order_"):
                        parent_id = record_tree.get_parent_id(parent_id)
                        parent_field = record_tree[parent_id]
                    # end while

                    byte_orders[leaf_id] = parent_field._byte_order_
                # end if
            else:
                parent_id = leaf_id // 2
                parent_field = record_tree[parent_id]

                while not hasattr(parent_field, "_byte_order_"):
                    parent_id = record_tree.get_parent_id(parent_id)
                    parent_field = record_tree[parent_id]
                # end while

                byte_orders[leaf_id] = parent_field._byte_order_
            # end if
        # end for

        # Walk through the list of primitives, making new strings when the byte
        # order changes.
        format_strs = list()
        groupby_iter = groupby(leaf_ids, byte_orders.__getitem__)

        for (byte_order, group_iter) in groupby_iter:
            format_str = [byte_order]
            format_str.extend(
                [record_tree[node_id]._format_ for node_id in group_iter]
            )
            format_strs.append("".join(format_str))
        # end for

        return format_strs
    # end def get_record_strings

    @staticmethod
    def get_size_at(record_tree, leaf_ids=None):
        """
        Calculates the cumulative number of bytes needed, at each field
        position.

        :parameters:
            record_tree
                An NAryTree built from a flattened version of the data
                structure.

            leaf_ids
                An optional list of the identifiers of the leaves of
                record_tree.

        :rtype: list
        :returns: A list of the cumulative number of bytes needed at each field
                  position.
        """

        if leaf_ids is None:
            leaf_ids = record_tree.get_leaf_ids()
        # end if

        size_at = [0]
        for leaf_id in leaf_ids:
            field = record_tree[leaf_id]
            size_at.append(field._size_ + size_at[-1])
        # end for
        del size_at[0]

        return size_at
    # end def get_size_at
# end class Extractor
