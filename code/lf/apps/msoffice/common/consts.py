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
Constants for shared Microsoft office constants.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

PIDSI_CODEPAGE = 1
PIDSI_TITLE = 2
PIDSI_SUBJECT = 3
PIDSI_AUTHOR = 4
PIDSI_KEYWORDS = 5
PIDSI_COMMENTS = 6
PIDSI_TEMPLATE = 7
PIDSI_LAST_AUTHOR = 8
PIDSI_REV_NUMBER = 9
PIDSI_EDIT_TIME = 0xA
PIDSI_LAST_PRINTED_TIME = 0xB
PIDSI_CREATE_TIME = 0xC
PIDSI_SAVE_TIME = 0xD
PIDSI_PAGE_COUNT = 0xE
PIDSI_WORD_COUNT = 0xF
PIDSI_CHAR_COUNT = 0x10
PIDSI_THUMBNAIL = 0x11
PIDSI_APP_NAME = 0x12
PIDSI_DOC_SECURITY = 0x13

PIDDSI_CODEPAGE = 1
PIDDSI_CATEGORY = 2
PIDDSI_PRESFORMAT = 3
PIDDSI_BYTECOUNT = 4
PIDDSI_LINECOUNT = 5
PIDDSI_PARACOUNT = 6
PIDDSI_SLIDECOUNT = 7
PIDDSI_NOTECOUNT = 8
PIDDSI_HIDDENCOUNT = 9
PIDDSI_MMCLIPCOUNT = 0xA
PIDDSI_SCALE = 0xB
PIDDSI_HEADINGPAIR = 0xC
PIDDSI_DOCPARTS = 0xD
PIDDSI_MANAGER = 0xE
PIDDSI_COMPANY = 0xF
PIDDSI_LINKSDIRTY = 0x10
PIDDSI_CCHWITHSPACES = 0x11
PIDDSI_SHAREDDOC = 0x13
PIDDSI_LINKBASE = 0x14
PIDDSI_HLINKS = 0x15
PIDDSI_HYPERLINKSCHANGED = 0x16
PIDDSI_VERSION = 0x17
PIDDSI_DIGSIG = 0x18
PIDDSI_CONTENTTYPE = 0x1A
PIDDSI_CONTENTSTATUS = 0x1B
PIDDSI_LANGUAGE = 0x1C
PIDDSI_DOCVERSION = 0x1D

SUMMARY_INFORMATION_NAME = "\x05SummaryInformation"
DOC_SUMMARY_INFORMATION_NAME = "\x05DocumentSummaryInformation"
