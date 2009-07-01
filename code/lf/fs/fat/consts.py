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
Constants for the FAT file system.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
    "MAX_CLUST_COUNT_FAT12", "MAX_CLUST_COUNT_FAT16", "UNALLOC_FAT",
    "EOC_FAT12", "EOC_FAT16", "EOC_FAT32", "BAD_FAT12", "BAD_FAT16",
    "BAD_FAT32", "ATTR_READ_ONLY", "ATTR_HIDDEN", "ATTR_SYSTEM",
    "ATTR_VOLUME_ID", "ATTR_DIRECTORY", "ATTR_ARCHIVE", "ATTR_CHANGEABLE",
    "ATTR_LONG_NAME", "ATTR_LONG_NAME_MASK", "LAST_LONG_ENTRY",
    "UNALLOC_DIR_ENTRY", "LONG_NAME_MAX", "MIN_ORD", "MAX_ORD", "LAST_ORD_MASK"
]

MAX_CLUST_COUNT_FAT12 = 0xFF5
MAX_CLUST_COUNT_FAT16 = 0xFFF5

UNALLOC_FAT = 0x0

EOC_FAT12 = 0xFF8
EOC_FAT16 = 0xFFF8
EOC_FAT32 = 0xFFFFFF8

BAD_FAT12 = 0xFF7
BAD_FAT16 = 0xFFF7
BAD_FAT32 = 0xFFFFFF7

ATTR_READ_ONLY = 0x01
ATTR_HIDDEN = 0x02
ATTR_SYSTEM = 0x04
ATTR_VOLUME_ID = 0x08
ATTR_DIRECTORY = 0x10
ATTR_ARCHIVE = 0x20
ATTR_CHANGEABLE = ATTR_READ_ONLY | ATTR_HIDDEN | ATTR_SYSTEM | ATTR_ARCHIVE
ATTR_LONG_NAME = ATTR_READ_ONLY | ATTR_HIDDEN | ATTR_SYSTEM | ATTR_VOLUME_ID
ATTR_LONG_NAME_MASK = ATTR_LONG_NAME | ATTR_DIRECTORY

LAST_LONG_ENTRY = 0x40
UNALLOC_DIR_ENTRY = 0xE5
LONG_NAME_MAX = 0xFF
MIN_ORD = 1
MAX_ORD = 20
LAST_ORD_MASK = 0x40
