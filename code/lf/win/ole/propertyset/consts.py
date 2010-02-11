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
Constants for Property Sets.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

from uuid import UUID

__docformat__ = "restructuredtext en"
__all__ = [
]

FMTID_SummaryInformation = UUID("{F29F85E0-4FF9-1068-AB91-08002B27B3D9}")
FMTID_DocSummaryInformation = UUID("{D5CDD502-2E9C-101B-9397-08002B2CF9AE}")
FMTID_UserDefinedProperties = UUID("{D5CDD505-2E9C-101B-9397-08002B2CF9AE}")
FMTID_GlobalInfo = UUID("{56616F00-C154-11CE-8553-00AA00A1F95B}")
FMTID_ImageContents = UUID("{56616400-C154-11CE-8553-00AA00A1F95B}")
FMTID_ImageInfo = UUID("{56616500-C154-11CE-8553-00AA00A1F95B}")
FMTID_PropertyBag = UUID("{20001801-5DE6-11D1-8E38-00C04FB9386D}")

PID_MAX_NORMAL = 0x7FFFFFFF
PID_DICTIONARY = 0
PID_CODEPAGE = 1
PID_LOCALE = 0x80000000
PID_BEHAVIOR = 0x80000003

CP_WINUNICODE = 1200
CP_WINDOWS_1250 = 1250
CP_WINDOWS_1252 = 1252
