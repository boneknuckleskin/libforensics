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

"""Constants for virtual key codes."""

__docformat__ = "restructuredtext en"
__all__ = [
    "VK_LBUTTON", "VK_RBUTTON", "VK_CANCEL", "VK_MBUTTON", "VK_BACK", "VK_TAB",
    "VK_CLEAR", "VK_RETURN", "VK_SHIFT", "VK_CONTROL", "VK_MENU", "VK_PAUSE",
    "VK_CAPITAL", "VK_ESCAPE", "VK_SPACE", "VK_PRIOR", "VK_NEXT", "VK_END",
    "VK_HOME", "VK_LEFT", "VK_UP", "VK_RIGHT", "VK_DOWN", "VK_SELECT",
    "VK_EXECUTE", "VK_SNAPSHOT", "VK_INSERT", "VK_DELETE", "VK_HELP",
    "VK_LWIN", "VK_RWIN", "VK_APPS", "VK_NUMPAD0", "VK_NUMPAD1", "VK_NUMPAD2",
    "VK_NUMPAD3", "VK_NUMPAD4", "VK_NUMPAD5", "VK_NUMPAD6", "VK_NUMPAD7",
    "VK_NUMPAD8", "VK_NUMPAD9", "VK_MULTIPLY", "VK_ADD", "VK_SEPARATOR",
    "VK_SUBTRACT", "VK_DECIMAL", "VK_DIVIDE", "VK_F1", "VK_F2", "VK_F3",
    "VK_F4", "VK_F5", "VK_F6", "VK_F7", "VK_F8", "VK_F9", "VK_F10", "VK_F11",
    "VK_F12", "VK_F13", "VK_F14", "VK_F15", "VK_F16", "VK_F17", "VK_F18",
    "VK_F19", "VK_F20", "VK_F21", "VK_F22", "VK_F23", "VK_F24", "VK_NUMLOCK",
    "VK_SCROLL", "VK_LSHIFT", "VK_RSHIFT", "VK_LCONTROL", "VK_RCONTROL",
    "VK_LMENU", "VK_RMENU", "VK_PACKET", "VK_ATTN", "VK_CRSEL", "VK_EXSEL",
    "VK_EREOF", "VK_PLAY", "VK_ZOOM", "VK_NONAME", "VK_PA1", "VK_OEM_CLEAR",
    "VK_KEYLOCK", "VK_OEM_SCROLL", "VK_OEM_1", "VK_OEM_PLUS", "VK_OEM_COMMA",
    "VK_OEM_MINUS", "VK_OEM_PERIOD", "VK_OEM_2", "VK_OEM_3", "VK_OEM_4",
    "VK_OEM_5", "VK_OEM_6", "VK_OEM_7", "VK_OEM_8", "VK_OEM_AX", "VK_OEM_102",
    "VK_DBE_ALPHANUMERIC", "VK_DBE_KATAKANA", "VK_DBE_HIRAGANA",
    "VK_DBE_SBCSCHAR", "VK_DBE_DBCSCHAR", "VK_DBE_ROMAN", "VK_DBE_NOROMAN",
    "VK_DBE_ENTERWORDREGISTERMODE", "VK_DBE_ENTERIMECONFIGMODE",
    "VK_DBE_FLUSHSTRING", "VK_DBE_CODEINPUT", "VK_DBE_NOCODEINPUT",

    "virtual_key_code_names"
]

VK_LBUTTON = 0x1
VK_RBUTTON = 0x2
VK_CANCEL = 0x3
VK_MBUTTON = 0x4
VK_BACK = 0x8
VK_TAB = 0x9
VK_CLEAR = 0xC
VK_RETURN = 0xD
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_PAUSE = 0x13
VK_CAPITAL = 0x14
VK_ESCAPE = 0x1B
VK_SPACE = 0x20
VK_PRIOR = 0x21
VK_NEXT = 0x22
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_SELECT = 0x29
VK_EXECUTE = 0x2B
VK_SNAPSHOT = 0x2C
VK_INSERT = 0x2D
VK_DELETE = 0x2E
VK_HELP = 0x2F
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_APPS = 0x5D
VK_NUMPAD0 = 0x60
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69
VK_MULTIPLY = 0x6A
VK_ADD = 0x6B
VK_SEPARATOR = 0x6C
VK_SUBTRACT = 0x6D
VK_DECIMAL = 0x6E
VK_DIVIDE = 0x6F
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_F13 = 0x7C
VK_F14 = 0x7D
VK_F15 = 0x7E
VK_F16 = 0x7F
VK_F17 = 0x80
VK_F18 = 0x81
VK_F19 = 0x82
VK_F20 = 0x83
VK_F21 = 0x84
VK_F22 = 0x85
VK_F23 = 0x86
VK_F24 = 0x87
VK_NUMLOCK = 0x90
VK_SCROLL = 0x91
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4
VK_RMENU = 0xA5
VK_PACKET = 0xE7
VK_ATTN = 0xF6
VK_CRSEL = 0xF7
VK_EXSEL = 0xF8
VK_EREOF = 0xF9
VK_PLAY = 0xFA
VK_ZOOM = 0xFB
VK_NONAME = 0xFC
VK_PA1 = 0xFD
VK_OEM_CLEAR = 0xFE
VK_KEYLOCK = 0xF22
VK_OEM_SCROLL = 0x91
VK_OEM_1 = 0xBA
VK_OEM_PLUS = 0xBB
VK_OEM_COMMA = 0xBC
VK_OEM_MINUS = 0xBD
VK_OEM_PERIOD = 0xBE
VK_OEM_2 = 0xBF
VK_OEM_3 = 0xC0
VK_OEM_4 = 0xDB
VK_OEM_5 = 0xDC
VK_OEM_6 = 0xDD
VK_OEM_7 = 0xDE
VK_OEM_8 = 0xDF
VK_OEM_AX = 0xE1
VK_OEM_102 = 0xE2
VK_DBE_ALPHANUMERIC = 0xF0
VK_DBE_KATAKANA = 0xF1
VK_DBE_HIRAGANA = 0xF2
VK_DBE_SBCSCHAR = 0xF3
VK_DBE_DBCSCHAR = 0xF4
VK_DBE_ROMAN = 0xF5
VK_DBE_NOROMAN = 0xF6
VK_DBE_ENTERWORDREGISTERMODE = 0xF7
VK_DBE_ENTERIMECONFIGMODE = 0xF8
VK_DBE_FLUSHSTRING = 0xF9
VK_DBE_CODEINPUT = 0xFA
VK_DBE_NOCODEINPUT = 0xFB

virtual_key_code_names = {
    1: "Left mouse button",
    2: "Right mouse button",
    3: "Control-break processing",
    4: "Middle mouse button",
    8: "BACKSPACE",
    9: "TAB",
    12: "CLEAR",
    13: "ENTER",
    16: "SHIFT",
    17: "CTRL",
    18: "ALT",
    19: "PAUSE",
    20: "CAPS LOCK",
    27: "ESC",
    32: "SPACEBAR",
    33: "PAGE UP",
    34: "PAGE DOWN",
    35: "END",
    36: "HOME",
    37: "LEFT ARROW",
    38: "UP ARROW",
    39: "RIGHT ARROW",
    40: "DOWN ARROW",
    41: "SELECT",
    43: "EXECUTE",
    44: "PRINT SCREEN",
    45: "INS",
    46: "DEL",
    47: "HELP",
    91: "Left Windows (Microsoft Natural Keyboard)",
    92: "Right Windows (Microsoft Natural Keyboard)",
    93: "Applications (Microsoft Natural Keyboard)",
    96: "Numeric keypad 0",
    97: "Numeric keypad 1",
    98: "Numeric keypad 2",
    99: "Numeric keypad 3",
    100: "Numeric keypad 4",
    101: "Numeric keypad 5",
    102: "Numeric keypad 6",
    103: "Numeric keypad 7",
    104: "Numeric keypad 8",
    105: "Numeric keypad 9",
    106: "Multiply",
    107: "Add",
    108: "Separator",
    109: "Subtract",
    110: "Decimal",
    111: "Divide",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    124: "F13",
    125: "F14",
    126: "F15",
    127: "F16",
    128: "F17",
    129: "F18",
    130: "F19",
    131: "F20",
    132: "F21",
    133: "F22",
    134: "F23",
    135: "F24",
    144: "NUM LOCK",
    145: "SCROLL LOCK",
    160: "Left SHIFT",
    161: "Right SHIFT",
    162: "Left CTRL",
    163: "Right CTRL",
    164: "Left ALT",
    165: "Right ALT",
    231: "Pass Unicode characters",
    246: "ATTN",
    247: "CRSEL",
    248: "EXSEL",
    249: "Erase EOF",
    250: "PLAY",
    251: "ZOOM",
    252: "Reserved",
    253: "PA1",
    254: "CLEAR",
    3874: "Key lock",
    145: "Scroll",
    186: "';:' (for US)",
    187: "'+'",
    188: "','",
    189: "'-'",
    190: "'.'",
    191: "'/?' (for US)",
    192: "'`~' (for US)",
    219: "'[{' (for US)",
    220: "'\|' (for US)",
    221: "']}' (for US)",
    222: "''\"' (for US)",
    223: "OEM 8",
    225: "AX key (Japanese AX keyboard)",
    226: "'<>' or '\|' (RT 102-key keyboard)",
    240: "Change mode to alphanumeric",
    241: "Change mode to Katakana",
    242: "Change mode to Hiragana",
    243: "Change mode to single-byte characters",
    244: "Change mode to double-byte characters",
    245: "Change mode to Roman characters",
    246: "Change mode to non-Roman characters",
    247: "Activate word registration dialog box",
    248: "Activate dialog box for setting up IME",
    249: "Delete undetermined string w/o determinig it",
    250: "Change mode to code input",
    251: "Change mode to no-code input"
}
