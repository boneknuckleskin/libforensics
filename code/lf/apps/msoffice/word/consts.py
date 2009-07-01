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
Constants for Microsoft Word.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
]

NFIB_WIN_WORD_1 = 0x21 # WinWord 1.0
NFIB_WIN_WORD_2 = 0x2D # WinWord 2.0
NFIB_WIN_WORD_6_16 = 0x101 # WinWord 6.0c for 16bit
NFIB_WORD_6_32 = 0x68 # Word6/32 bit
NFIB_WORD_95 = 0x68
NFIB_WORD_97 = 0xC1
NFIB_WORD_2000 = 0xD9
NFIB_WORD_2002 = 0x101
NFIB_WORD_2003 = 0x10C
NFIB_WORD_2007 = 0x112

MAGIC_WORD_97 = 0x6A62
MAGIC_WORD_98_MAC = 0x626A
MAGIC_WORD_6_7 = 0xA5DC
MAGIC_WORD_8 = 0xA5EC

magic_names = {
    MAGIC_WORD_97: "Word 97",
    MAGIC_WORD_98_MAC: "Word 98 (Mac)",
    MAGIC_WORD_6_7: "Word 6.0/7.0",
    MAGIC_WORD_8: "Word 8.0"
}

ENVR_WINDOWS = 0
ENVR_MAC = 1

ASSOC_DOT = 1
ASSOC_TITLE = 2
ASSOC_SUBJECT = 3
ASSOC_KEYWORDS = 4
ASSOC_COMMENTS = 5
ASSOC_AUTHOR = 6
ASSOC_LAST_REV_BY = 7
ASSOC_MAIL_MERGE_DATA = 8
ASSOC_MAIL_MERGE_HEADER = 9

ROLE_NONE = 0
ROLE_OWNER = 0xFFFC
ROLE_EDITOR = 0xFFFB
