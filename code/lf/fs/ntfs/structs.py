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
Data structures for NTFS.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
]

from lf.core.struct.datastruct import DataStruct, LITTLE_ENDIAN, Bytes, Array
from lf.core.struct.microsoft_types import WORD, BYTE
from lf.core.struct.microsoft_types import UCHAR, USHORT, ULONG, ULONGLONG, VCN
from lf.core.struct.microsoft_types import LCN, FILETIME, LONGLONG
from lf.core.struct.microsoft_structs import GUID

class BPB(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        WORD("bytes_per_sect"),
        BYTE("sects_per_clust"),
        WORD("rsvd_sects"),
        BYTE("rsvd")
        WORD("rsvd1"),
        WORD("unused"),
        BYTE("media"),
        WORD("rsvd2"),
        WORD("sects_per_track"),
        WORD("heads"),
        DWORD("unused1"),
    ]
# end class BPB

class ExtendedBPB(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("unused"),
        LONGLONG("tot_sects"),
        LCN("mft_lcn"),
        LCN("mft_mirror_lcn"),
        DWORD("clusts_per_mft"),
        DWORD("clusts_per_index"),
        LONGLONG("serial_num"),
        DWORD("checksum")
    ]
# end class ExtendedBPB

class BootSector(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Bytes(3, "jmp_instrs"),
        Bytes(8, "oem_id"),
        BPB("bpb"),
        ExtendedBPB("ext_bpb"),
        Bytes(426, "boot_code"),
        WORD("end_sig")
    ]
# end class BootSector

class MultiSectorHeader(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        Array(4, UCHAR, "sig"),
        USHORT("usa_offset"),
        USHORT("usa_size")
    ]
# end class MultiSectorHeader

class MFTSegmentReference(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        ULONG("seg_num_lo"),
        USHORT("seg_num_hi"),
        USHORT("seq_num")
    ]
# end class MFTSegmentReference

class FileRecordHeader(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        MultiSectorHeader("multi_sector_header"),
        ULONGLONG("lsn"),
        USHORT("seq_num"),
        USHORT("link_count"),
        USHORT("attr_offset"),
        USHORT("flags"),
        ULONG("real_size"),
        ULONG("alloc_size"),
        MFTSegmentReference("base_mft_ref"),
        USHORT("next_attr_id")
    ]
# end class FileRecordHeader

# Common fields for MFT attributes
class AttributeHeader(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        ULONG("next_attr_id"),
        ULONG("attr_size"),
        UCHAR("form_code"),
        UCHAR("name_size"),
        USHORT("name_offset"),
        USHORT("flags"),
        USHORT("attr_id")
    ]
# end class AttributeHeader

class ResidentAttribute(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        AttributeHeader("header"),
        ULONG("value_size"),
        USHORT("value_offset")
    ]
# end class ResidentAttribute

class NonResidentAttribute(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        AttributeHeader("header"),
        VCN("vcn_lo"),
        VCN("vcn_hi"),
        USHORT("mapping_pairs_offset"),
        USHORT("compress_unit_size"),
        Bytes(5, "rsvd"),
        LONGLONG("alloc_size"),
        LONGLONG("file_size"),
        LONGLONG("valid_data_size"),
        LONGLONG("total_alloc")
    ]
# end class NonResidentAttribute

class StandardInformationOld(DataStruct):
    """For older versions of NTFS"""

    byte_order = LITTLE_ENDIAN
    fields = [
        FILETIME("btime"),
        FILETIME("mtime"),
        FILETIME("ctime"),
        FILETIME("atime"),
        ULONG("flags"),
        ULONG("max_version")
        ULONG("version")
        ULONG("class_id"),
    ]
# end class StandardInformationOld

class StandardInformation(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        FILETIME("btime"),
        FILETIME("mtime"),
        FILETIME("ctime"),
        FILETIME("atime"),
        ULONG("flags"),
        ULONG("max_version"),
        ULONG("version"),
        ULONG("class_id"),
        ULONG("owner_id"),
        ULONG("security_id"),
        ULONGLONG("quota_charged"),
        LONGLONG("usn")
    ]
# end class StandardInformation

class FileName(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        MFTSegmentReference("parent_dir"),
        FILETIME("btime"),
        FILETIME("mtime"),
        FILETIME("ctime"),
        FILETIME("atime"),
        LONGLONG("alloc_size"),
        LONGLONG("real_size"),
        ULONG("flags"),
        ULONG("reparse"),
        UCHAR("name_size"),
        UCHAR("namespace")
    ]
# end class FileName

class AttributeList(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        ULONG("attr_type"),
        USHORT("size")
        UCHAR("name_size"),
        UCHAR("name_offset"),
        VCN("start_vcn"),
        MFTSegmentReference("mft_ref"),
        USHORT("attr_id")
    ]
# end class AttributeList

class ObjectID(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        GUID("object_id"),
        GUID("birth_volume_id"),
        GUID("birth_object_id"),
        GUID("domain_id")
    ]
# end class ObjectID

class ReparsePointHeader(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        DWORD("tag"),
        WORD("data_size"),
        WORD("rsvd")
    ]
# end class ReparsePointHeader

class SymbolicLinkReparsePoint(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        ReparsePointHeader("header"),
        WORD("target_name_offset"),
        WORD("target_name_size"),
        WORD("source_name_offset"),
        WORD("source_name_size"),
        DWORD("flags")
    ]
# end class SymbolicLinkReparsePoint

class MountReparsePoint(DataStruct):
    byte_order = LITTLE_ENDIAN
    fields = [
        ReparsePointHeader("header"),
        WORD("target_name_offset"),
        WORD("target_name_size"),
        WORD("source_name_offset"),
        WORD("source_name_size"),
        DWORD("flags")
    ]
# end class MountReparsePoint
