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

"""Ctypes classes for shell link files"""

# local imports
from lf.win.shell.link.dtypes import (
    HotKey, ShellLinkHeader, LinkInfoHeader, VolumeIDHeader, CNRLHeader,
    ConsoleDataBlock, ConsoleFEDataBlock, DarwinDataBlock,
    ExpandableStringsDataBlock, EnvironmentVariableDataBlock,
    IconEnvironmentDataBlock, DarwinDataBlock, KnownFolderDataBlock,
    SpecialFolderDataBlock, TrackerDataBlock, TrackerDataBlockFooter,
    DataBlockHeader, FileAttributes, LinkFlags, DomainRelativeObjId
)

__docformat__ = "restructuredtext en"
__all__ = [
    "hot_key", "shell_link_header", "link_info_header", "volume_id_header",
    "cnrl_header", "console_data_block", "console_fe_data_block",
    "darwin_data_block", "expandable_strings_data_block",
    "environment_variable_data_block", "icon_environment_data_block",
    "known_folder_data_block", "special_folder_data_block",
    "tracker_data_block", "tracker_data_block_footer", "data_block_header",
    "file_attributes", "link_flags", "domain_relative_obj_id"
]

hot_key = HotKey._ctype_
shell_link_header = ShellLinkHeader._ctype_
link_info_header = LinkInfoHeader._ctype_
volume_id_header =  VolumeIDHeader._ctype_
cnrl_header = CNRLHeader._ctype_
console_data_block = ConsoleDataBlock._ctype_
console_fe_data_block = ConsoleFEDataBlock._ctype_
darwin_data_block = DarwinDataBlock._ctype_
environment_variable_data_block = EnvironmentVariableDataBlock._ctype_
expandable_strings_data_block = ExpandableStringsDataBlock._ctype_
icon_environment_data_block = IconEnvironmentDataBlock._ctype_
known_folder_data_block = KnownFolderDataBlock._ctype_
special_folder_data_block = SpecialFolderDataBlock._ctype_
tracker_data_block = TrackerDataBlock._ctype_
tracker_data_block_footer = TrackerDataBlockFooter._ctype_
data_block_header = DataBlockHeader._ctype_
file_attributes = FileAttributes._ctype_
link_flags = LinkFlags._ctype_
domain_relative_obj_id = DomainRelativeObjId._ctype_
