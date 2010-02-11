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

"""Code page constants for Microsoft Windows."""

__docformat__ = "restructuredtext en"
__all__ = [
    "CP_UNKNOWN", "CP_WINUNICODE", "CP_OEM_437", "CP_OEM_720", "CP_OEM_737",
    "CP_OEM_775", "CP_OEM_850", "CP_OEM_852", "CP_OEM_855", "CP_OEM_857",
    "CP_OEM_858", "CP_OEM_862", "CP_OEM_866",

    "CP_WINDOWS_874", "CP_WINDOWS_932", "CP_WINDOWS_936", "CP_WINDOWS_949",
    "CP_WINDOWS_950", "CP_WINDOWS_1250", "CP_WINDOWS_1251", "CP_WINDOWS_1252",
    "CP_WINDOWS_1253", "CP_WINDOWS_1254", "CP_WINDOWS_1255", "CP_WINDOWS_1256",
    "CP_WINDOWS_1257", "CP_WINDOWS_1258", "CP_WINDOWS_UTF8",

    "CP_ISO_8859_1", "CP_ISO_8859_2", "CP_ISO_8859_3", "CP_ISO_8859_4",
    "CP_ISO_8859_5", "CP_ISO_8859_6", "CP_ISO_8859_8", "CP_ISO_8859_9",
    "CP_ISO_8859_15",

    "code_page_names"
]

CP_UNKNOWN = 0
CP_WINUNICODE = 0x4B0

CP_OEM_437 = 437
CP_OEM_720 = 720
CP_OEM_737 = 737
CP_OEM_775 = 775
CP_OEM_850 = 850
CP_OEM_852 = 852
CP_OEM_855 = 855
CP_OEM_857 = 857
CP_OEM_858 = 858
CP_OEM_862 = 862
CP_OEM_866 = 866

CP_WINDOWS_874 = 874
CP_WINDOWS_932 = 932
CP_WINDOWS_936 = 936
CP_WINDOWS_949 = 949
CP_WINDOWS_950 = 950
CP_WINDOWS_1250 = 1250
CP_WINDOWS_1251 = 1251
CP_WINDOWS_1252 = 1252
CP_WINDOWS_1253 = 1253
CP_WINDOWS_1254 = 1254
CP_WINDOWS_1255 = 1255
CP_WINDOWS_1256 = 1256
CP_WINDOWS_1257 = 1257
CP_WINDOWS_1258 = 1258
CP_WINDOWS_UTF8 = 65001

CP_ISO_8859_1 = 28591
CP_ISO_8859_2 = 28592
CP_ISO_8859_3 = 28593
CP_ISO_8859_4 = 28594
CP_ISO_8859_5 = 28595
CP_ISO_8859_6 = 28596
CP_ISO_8859_8 = 28598
CP_ISO_8859_9 = 28599
CP_ISO_8859_15 = 28605

# Mapping from constants to Python codec (string) names
code_page_names = {
    CP_WINUNICODE: "utf_16_le",

    CP_OEM_437: "cp437",
    CP_OEM_720: "cp720",
    CP_OEM_737: "cp737",
    CP_OEM_775: "cp775",
    CP_OEM_850: "cp850",
    CP_OEM_852: "cp852",
    CP_OEM_855: "cp855",
    CP_OEM_857: "cp857",
    CP_OEM_858: "cp858",
    CP_OEM_862: "cp862",
    CP_OEM_866: "cp866",

    CP_WINDOWS_874: "cp874",
    CP_WINDOWS_932: "cp932",
    CP_WINDOWS_936: "cp936",
    CP_WINDOWS_949: "cp949",
    CP_WINDOWS_950: "cp950",
    CP_WINDOWS_1250: "cp1250",
    CP_WINDOWS_1251: "cp1251",
    CP_WINDOWS_1252: "cp1252",
    CP_WINDOWS_1253: "cp1253",
    CP_WINDOWS_1254: "cp1254",
    CP_WINDOWS_1255: "cp1255",
    CP_WINDOWS_1256: "cp1256",
    CP_WINDOWS_1257: "cp1257",
    CP_WINDOWS_1258: "cp1258",
    CP_WINDOWS_UTF8: "utf_8",

    CP_ISO_8859_1: "iso8859_1",
    CP_ISO_8859_2: "iso8859_2",
    CP_ISO_8859_3: "iso8859_3",
    CP_ISO_8859_4: "iso8859_4",
    CP_ISO_8859_5: "iso8859_5",
    CP_ISO_8859_6: "iso8859_6",
    CP_ISO_8859_8: "iso8859_8",
    CP_ISO_8859_9: "iso8859_9",
    CP_ISO_8859_15: "iso8859_15"
}
