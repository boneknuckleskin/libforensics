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

"""Metadata for OLE property sets."""

# local imports
from lf.dtypes import Structuple

from lf.win.ole.ps.consts import (
    CODEPAGE_PROPERTY_IDENTIFIER, DICTIONARY_PROPERTY_IDENTIFIER,
    LOCALE_PROPERTY_IDENTIFIER, BEHAVIOR_PROPERTY_IDENTIFIER
)

__docformat__ = "restructuredtext en"
__all__ = [
    "PropertySetMetadata", "PropertiesMetadata"
]

# Property identifier to attribute (name) mapping
_pid_attr_map = {
    CODEPAGE_PROPERTY_IDENTIFIER: "code_page",
    DICTIONARY_PROPERTY_IDENTIFIER: "dictionary",
    LOCALE_PROPERTY_IDENTIFIER: "locale",
    BEHAVIOR_PROPERTY_IDENTIFIER: "behavior"
}

class PropertySetMetadata(Structuple):
    """Metadata for a :class:`~lf.win.ole.ps.PropertySet`.

    .. attribute:: byte_order

        The value of the byte order field.

    .. attribute:: version

        The version of the OLE property set.

    .. attribute:: sys_id

        The system identifier field.

    .. attribute:: clsid

        The CLSID of the associated property set.

    .. attribute:: fmtid0

        The FMTID of the first property set.

    .. attribute:: fmtid1

        The FMTID of the second property set.

    """

    _fields_ = ("byte_order", "version", "sys_id", "clsid", "fmtid0", "fmtid1")
    _auto_slots_ = True

    @classmethod
    def from_property_set(cls, property_set):
        """Creates a :class:`PropertySetMetadata` from a property set.

        :type property_set: :class:`PropertySet`
        :param property_set: The property set to examine.

        :rtype: :class:`PropertySetMetadata`
        :returns: The corresponding :class:`PropertySetMetadata` object.

        """
        return cls((
            property_set.byte_order, property_set.version, property_set.sys_id,
            property_set.clsid, property_set.fmtid0, property_set.fmtid1
        ))
    # end def from_property_set
# end class PropertySetMetadata

class PropertiesMetadata(Structuple):
    """Metadata for the properties of a :class:`PropertySet`.

    .. attribute:: code_page

        The value of the CodePage property.

    .. attribute:: dictionary

        A dictionary of property identifiers (keys) and names (values).

    .. attribute:: locale

        The value of the locale property.

    .. attribute:: behavior

        The value of the behavior property.

    .. attribute:: attr_exists

        A set of the attribute names that were found in the property set.

    """

    _fields_ = (
        "code_page", "dictionary", "locale", "behavior", "attr_exists",
    )
    _auto_slots_ = True

    @classmethod
    def from_properties(cls, properties):
        """Creates a :class:`PropertiesMetadata` object from properties.

        :type properties: ``dict``
        :param properties: A dictionary of property identifiers (keys) and the
                           corresponding :class:`PropertyPacket` objects.

        :rtype: :class:`PropertiesMetadata`
        :return: The corresponding :class:`PropertiesMetadata` object.

        """
        attr_exists = set()
        properties_dict = dict()

        for (pid, property) in properties.items():
            if pid in _pid_attr_map:
                attr_name = _pid_attr_map[pid]
                properties_dict[attr_name] = property.value
                attr_exists.add(attr_name)
            # end if
        # end for

        if "code_page" in properties_dict:
            if properties_dict["code_page"] < 0:
                properties_dict["code_page"] += 0xFFFF + 1
            # end if
        # end if

        properties_dict["attr_exists"] = attr_exists
        value = [properties_dict.get(name) for name in cls._fields_]

        return cls(value)
    # end def from_properties
# end class PropertiesMetadata
