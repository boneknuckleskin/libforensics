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

"""Window state constants"""

__docformat__ = "restructuredtext en"
__all__ = [
    "SW_HIDE", "SW_SHOWNORMAL", "SW_SHOWMINIMIZED", "SW_SHOWMAXIMIZED",
    "SW_SHOWNOACTIVATE", "SW_SHOW", "SW_MINIMIZE", "SW_SHOWMINNOACTIVATE",
    "SW_SHOWNA", "SW_RESTORE", "SW_SHOWDEFAULT",

    "sw_names"
]

SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10

sw_names = {
    SW_HIDE: "SW_HIDE",
    SW_SHOWNORMAL: "SW_SHOWNORMAL",
    SW_SHOWMINIMIZED: "SW_SHOWMINIMIZED",
    SW_SHOWMAXIMIZED: "SW_SHOWMAXIMIZED",
    SW_SHOWNOACTIVATE: "SW_SHOWNOACTIVATE",
    SW_SHOW: "SW_SHOW",
    SW_MINIMIZE: "SW_MINIMIZE",
    SW_SHOWMINNOACTIVE: "SW_SHOWMINNOACTIVE",
    SW_SHOWNA: "SW_SHOWNA",
    SW_RESTORE: "SW_RESTORE",
    SW_SHOWDEFAULT: "SW_SHOWDEFAULT"
}
