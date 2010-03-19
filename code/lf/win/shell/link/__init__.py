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

"""Windows shell link files"""

from lf.win.shell.link.objects import (
    ShellLink, FileAttributes, LinkFlags, ShellLinkHeader, StringData,
    LinkInfo, VolumeID, CNRL, ExtraDataBlock, ConsoleProps, ConsoleFEProps,
    DarwinProps, ExpandableStringsDataBlock, EnvironmentProps,
    IconEnvironmentProps, KnownFolderProps, PropertyStoreProps, ShimProps,
    SpecialFolderProps, DomainRelativeObjId, TrackerProps,
    VistaAndAboveIDListProps, TerminalBlock, ExtraDataBlockFactory,
    StringDataSet
)

__docformat__ = "restructuredtext en"
__all__ = [
    "ShellLink", "FileAttributes", "LinkFlags", "ShellLinkHeader",
    "StringData", "LinkInfo", "VolumeID", "CNRL", "ExtraDataBlock",
    "ConsoleProps", "ConsoleFEProps", "DarwinProps",
    "ExpandableStringsDataBlock", "EnvironmentProps", "IconEnvironmentProps",
    "KnownFolderProps", "PropertyStoreProps", "ShimProps",
    "SpecialFolderProps", "DomainRelativeObjId", "TrackerProps",
    "VistaAndAboveIDListProps", "TerminalBlock", "ExtraDataBlockFactory",
    "StringDataSet"
]

