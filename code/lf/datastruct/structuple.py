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
Tuples with attribute-style access.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "make"
]

from operator import itemgetter
from itertools import count
from keyword import iskeyword

_valid_name_characters = \
    "abcdefhigjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

class MetaStructuple(type):
    """Meta class for Structuples."""

    def __new__(cls, name, bases, clsdict):
        field_names = clsdict["_fields"]
        field_indices = clsdict["_indices"]

        for (field_name, position) in zip(field_names, field_indices):
            clsdict[field_name] = property(itemgetter(position))
        # end for

        return super(MetaStructuple, cls).__new__(cls, name, bases, clsdict)
    # end def __new__
# end class MetaStructuple

def make(name, fields, rename=False):
    """
    Makes a new Structuple class.

    :parameters:
        name
            The name for the newly created class.

        fields
            A string, dictionary, or iterable describing the names of the
            fields and thier positions.  If a string or iterable, the positions
            are determined by the order in which the fields occur, starting
            with position 0 (first element).  If a dictionary, the keys are the
            names of the fields, and the positions are the values.

        rename
            If true, automatically renames duplicate field names to
            field_name__XXX, where XXX is the position of the field.
    """

    if isinstance(fields, dict):
        field_names = tuple(fields.keys())
    else:
        if isinstance(fields, str):
            fields = fields.replace(",", " ")
            field_names = fields.split()
        else:
            try:
                field_iter = iter(fields)
            except TypeError:
                raise TypeError("fields must be a str, dict, or iter")
            # end try

            field_names = list(field_iter)
        # end if

        already_seen = list()
        for (index, field_name) in enumerate(field_names):
            if field_name in already_seen:
                if rename:
                    field_name = "{0}__{1}".format(field_name, index)
                    already_seen.append(field_name)
                else:
                    raise ValueError(
                        "Duplicate field name {0}".format(field_name)
                    )
                # end if
            else:
                already_seen.append(field_name)
            # end if
        # end for

        field_names = tuple(already_seen)
        fields = dict(zip(field_names, count()))
    # end if

    field_positions = tuple([fields[field_name] for field_name in field_names])

    for field_name in field_names:
        if field_name[0].lower() not in "abcdefghijklmnopqrstuvwxyz":
            raise ValueError("Field names can only start with a letter: {0}".
                format(field_name)
            )
        elif iskeyword(field_name):
            err_msg = "Field names can not be keywords: {0}".format(field_name)
            raise ValueError("Field names can not be keywords: {0}".format(
                field_name
            ))
        # end if

        for char in field_name[1:]:
            if char not in _valid_name_characters:
                raise ValueError("Field names can only contain underscores and"
                    "alphanumeric characters: {0}".format(field_name)
                )
            # end if
        # end for
    # end for

    clsdict = {
        "_fields": field_names, "_indices": field_positions,
        "__slots__": tuple()
    }

    return MetaStructuple(name, (tuple,), clsdict)
# end def make
