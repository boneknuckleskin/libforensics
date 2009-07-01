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
Decoders for the FAT file system

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
    "ext_flags", "fs_ver", "fat12fat_entry_even", "fat12fat_entry_odd",
    "fat12fat_entry0", "fat16fat_entry0", "fat32fat_entry0", "fat16fat_entry1",
    "fat32fat_entry1", "fat32fat_entry", "dir_time", "dir_date"
]

from lf.struct.decode import Decoder

ext_flags_fields = [ ("active_fat", 0, 4), ("mirror", 7, 8) ]
ext_flags = Decoder("EXTFlags_tuple", ext_flags_fields)

fs_ver_fields = [ ("ver_maj", 8, 16), ("ver_min", 0, 8) ]
fs_ver = Decoder("FSVer_tuple", fs_ver_fields)

fat12fat_even_flags = [ ("entry", 0, 13) ]
fat12fat_even = Decoder("FAT12FAT_Even_tuple", fat12fat_even_flags)

fat12fat_odd_flags = [ ("entry", 4, 17) ]
fat12fat_odd = Decoder("FAT12FAT_Odd_tuple", fat12fat_odd_flags)

fat12fat_entry0 = Decoder("FAT12FAT_Entry0_tuple", [ ("media", 0, 9) ])
fat16fat_entry0 = Decoder("FAT16FAT_Entry0_tuple", [ ("media", 0, 9) ])
fat32fat_entry0 = Decoder("FAT32FAT_Entry0_tuple", [ ("media", 0, 9) ])

fat16fat_entry1_flags = [ ("cln_shut", 14, 15), ("hard_err", 15, 16) ]
fat16fat_entry1 = Decoder("FAT16FAT_Entry1_tuple", fat16fat_entry1_flags)

fat32fat_entry1_flags = [ ("cln_shut", 30, 31), ("hard_err", 31, 32) ]
fat32fat_entry1 = Decoder("FAT32FAT_Entry1_tuple", fat32fat_entry1_flags)

fat32fat_entry_flags = [ ("entry", 0, 28), ("rsvd", 28, 32) ]
fat32fat_entry = Decoder("FAT32FAT_Entry_tuple", fat32fat_entry_flags)

dir_date_fields = [ ("day", 0 ,5), ("month", 5, 9), ("year", 9, 16) ]
dir_date = Decoder("Dir_Date_tuple", dir_date_fields)

dir_time_fields = [ ("sec", 0, 5), ("min", 5, 11), ("hour", 11, 16) ]
dir_time = Decoder("Dir_Time_tuple", dir_time_fields)
