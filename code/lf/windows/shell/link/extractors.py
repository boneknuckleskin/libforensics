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
Extractors for shell link (.lnk) files

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "header", "link_info_header", "volume_id_header", "cnrl_header",
    "data_block", "console_data_block", "darwin_data_block",
    "environment_variable_data_block", "icon_environment_data_block",
    "known_folder_data_block", "special_folder_data_block",
    "tracker_data_block", "tracker_data_block_footer"
]

from lf.datatype import Extractor

from lf.windows.shell.link.datatypes import (
    Header, LinkInfoHeader, VolumeIDHeader, CNRLHeader, DataBlock,
    ConsoleDataBlock, DarwinDataBlock, EnvironmentVariableDataBlock,
    IconEnvironmentDataBlock, KnownFolderDataBlock, SpecialFolderDataBlock,
    TrackerDataBlock, TrackerDataBlockFooter
)

header = Extractor(Header())
link_info_header = Extractor(LinkInfoHeader())
volume_id_header = Extractor(VolumeIDHeader())
cnrl_header = Extractor(CNRLHeader())
data_block = Extractor(DataBlock())
console_data_block = Extractor(ConsoleDataBlock())
darwin_data_block = Extractor(DarwinDataBlock())
environment_variable_data_block = Extractor(EnvironmentVariableDataBlock())
icon_environment_data_block = Extractor(IconEnvironmentDataBlock())
known_folder_data_block = Extractor(KnownFolderDataBlock())
special_folder_data_block = Extractor(SpecialFolderDataBlock())
tracker_data_block = Extractor(TrackerDataBlock())
tracker_data_block_footer = Extractor(TrackerDataBlockFooter())
