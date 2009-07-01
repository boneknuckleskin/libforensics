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
Data structures for the FAT file system

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
    "BPB_FAT1216", "BPB_FAT32", "EXT_BPB", "BootSector_FAT1216",
    "BootSector_FAT32", "FSInfo", "FATEntry_FAT12", "FATEntry_FAT16",
    "FATEntry_FAT32", "DirEntry", "LFNDirEntry"
]

from lf.struct.datastruct import DataStruct, LITTLE_ENDIAN
from lf.struct.datatype import Bytes
from lf.windows.types import WORD, BYTE, DWORD

class BPB_FAT1216(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        WORD("bytes_per_sect"),
        BYTE("sects_per_clust"),
        WORD("rsvd_sect_count"),
        BYTE("fat_count"),
        WORD("root_ent_count"),
        WORD("tot_sects_16"),
        BYTE("media_descr"),
        WORD("sects_per_fat"),
        WORD("sects_per_track"),
        WORD("head_count"),
        DWORD("hidden_sects"),
        DWORD("tot_sects_32")
    ]
# end class BPB_FAT1216

class BPB_FAT32(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        WORD("bytes_per_sect"),
        BYTE("sects_per_clust"),
        WORD("rsvd_sect_count"),
        BYTE("fat_count"),
        WORD("root_ent_count"),
        BYTE("tot_sects_16"),
        BYTE("media_descr"),
        WORD("sects_per_fat"),
        WORD("sects_per_track"),
        WORD("head_count"),
        DWORD("hidden_sects"),
        DWORD("tot_sects_32"),
        DWORD("sects_per_fat_32"),
        WORD("ext_flags"),
        WORD("ver"),
        DWORD("root_clust"),
        WORD("fsinfo_sect"),
        WORD("bkup_boot_sect"),
        Bytes(12, "rsvd")
    ]
# end class BPB_FAT32

class EXT_BPB(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        BYTE("drive_num"),
        BYTE("rsvd"),
        BYTE("ext_boot_sig"),
        DWORD("serial_num"),
        Bytes(11, "label"),
        Bytes(8, "type")
    ]
# end class EXT_BPB_FAT1216

class BootSector_FAT1216(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Bytes(3, "jmp_instrs"),
        Bytes(8, "oem_id"),
        BPB_FAT1216("bpb"),
        EXT_BPB("ext_bpb"),
        Bytes(448, "boot_code"),
        WORD("trail_sig")
    ]
# end class BootSector_FAT1216

class BootSector_FAT32(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Bytes(3, "jmp_instrs"),
        Bytes(8, "oem_id"),
        BPB_FAT32("bpb"),
        EXT_BPB("ext_bpb"),
        Bytes(420, "boot_code"),
        WORD("trail_sig")
    ]
# end class BootSector_FAT32

class FSInfo(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("lead_sig"),
        Bytes(480, "rsvd1"),
        DWORD("struct_sig"),
        DWORD("free_count"),
        DWORD("next_free"),
        Bytes(12, "rsvd2"),
        DWORD("trail_sig")
    ]
# end class FSInfo

class FATEntry_FAT12(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        WORD("entry")
    ]
# end class FATEntry_FAT12

class FATEntry_FAT16(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        WORD("entry")
    ]
# end class FATEntry_FAT16

class FATEntry_FAT32(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("entry")
    ]
# end class FATEntry_FAT32

class DirEntry(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Bytes(11, "name"),
        BYTE("attr"),
        BYTE("nt_flags"),
        BYTE("ctime_hun"),
        WORD("ctime"),
        WORD("cdate"),
        WORD("adate"),
        WORD("clust_hi"),
        WORD("mtime"),
        WORD("mdate"),
        WORD("clust_lo"),
        DWORD("size")
    ]
# end class DirEntry

class LFNDirEntry(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        BYTE("ord"),
        Bytes(10, "name1"),
        BYTE("attr"),
        BYTE("flags"),
        BYTE("checksum"),
        Bytes(12, "name2"),
        WORD("clust_lo"),
        Bytes(4, "name3")
    ]
# end class LFNDirEntry
