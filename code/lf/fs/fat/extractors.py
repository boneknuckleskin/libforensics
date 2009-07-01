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
Convenience module that contains pre-built extractors for the FAT file system

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
    "boot_sector_fat1216", "boot_sector_fat32", "fsinfo", "fat_entry_fat12",
    "fat_entry_fat16", "fat_entry_fat32", "dir_entry", "lfn_dir_entry"
]

from lf.struct.extract import extractor_factory as factory
from lf.fs.fat.structs import BootSector_FAT1216, BootSector_FAT32
from lf.fs.fat.structs import FSInfo, FATEntry_FAT12, FATEntry_FAT16
from lf.fs.fat.structs import FATEntry_FAT32, DirEntry, LFNDirEntry

boot_sector_fat1216 = factory.make(BootSector_FAT1216())
boot_sector_fat32 = factory.make(BootSector_FAT32())
fsinfo = factory.make(FSInfo())

fat_entry_fat12 = factory.make(FATEntry_FAT12())
fat_entry_fat16 = factory.make(FATEntry_FAT16())
fat_entry_fat32 = factory.make(FATEntry_FAT32())

dir_entry = factory.make(DirEntry())
lfn_dir_entry = factory.make(LFNDirEntry())
