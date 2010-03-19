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

"""Generic constants for working with file systems"""

__docformat__ = "restructuredtext en"
__all__ = [
    "FILE_ATTRIBUTE_READONLY", "FILE_ATTRIBUTE_HIDDEN",
    "FILE_ATTRIBUTE_SYSTEM", "FILE_ATTRIBUTE_DIRECTORY",
    "FILE_ATTRIBUTE_ARCHIVE", "FILE_ATTRIBUTE_NORMAL",
    "FILE_ATTRIBUTE_TEMPORARY", "FILE_ATTRIBUTE_SPARSE_FILE",
    "FILE_ATTRIBUTE_REPARSE_POINT", "FILE_ATTRIBUTE_COMPRESSED",
    "FILE_ATTRIBUTE_OFFLINE", "FILE_ATTRIBUTE_NOT_CONTENT_INDEX",
    "FILE_ATTRIBUTE_ENCRYPED",

    "DRIVE_UNKNOWN", "DRIVE_NO_ROOT_DIR", "DRIVE_REMOVABLE", "DRIVE_FIXED",
    "DRIVE_REMOTE", "DRIVE_CDROM", "DRIVE_RAMDISK"

]

FILE_ATTRIBUTE_READONLY = 1
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
FILE_ATTRIBUTE_DIRECTORY = 0x10
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_NORMAL = 0x80
FILE_ATTRIBUTE_TEMPORARY = 0x100
FILE_ATTRIBUTE_SPARSE_FILE = 0x200
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
FILE_ATTRIBUTE_COMPRESSED = 0x800
FILE_ATTRIBUTE_OFFLINE = 0x1000
FILE_ATTRIBUTE_NOT_CONTENT_INDEX = 0x2000
FILE_ATTRIBUTE_ENCRYPED = 0x4000

DRIVE_UNKNOWN = 0
DRIVE_NO_ROOT_DIR = 1
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3
DRIVE_REMOTE = 4
DRIVE_CDROM = 5
DRIVE_RAMDISK = 6

