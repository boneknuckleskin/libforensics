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

"""Codecs for Microsoft Windows OEM code page 720."""

# stdlib imports
import codecs

__docformat__ = "restructuredtext en"
__all__ = [
    "getregentry"
]

class Codec(codecs.Codec):
    """Codec class for code page 720."""

    def encode(self, input, errors="strict"):
        return codecs.charmap_encode(input, errors, encoding_table)
    # end def encode

    def decode(self, input, errors="strict"):
        return codecs.charmap_decode(input, errors, decoding_table)
    # end def decode
# end class Codec

class IncrementalEncoder(codecs.IncrementalEncoder):
    """Incremental encoder for code page 720."""

    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_table)[0]
    # end def encode
# end def IncrementalEncoder

class IncrementalDecoder(codecs.IncrementalDecoder):
    """Incremental decoder for code page 720."""

    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_table)[0]
    # end def decode
# end class IncrementalDecoder

class StreamWriter(Codec, codecs.StreamWriter):
    """Stream writer for code page 720."""

    pass
# end StreamWriter

class StreamReader(Codec, codecs.StreamReader):
    """Stream reader for code page 720."""

    pass
# end class StreamReader

def getregentry():
    info = codecs.CodecInfo(
        name = "cp720",
        encode = Codec().encode,
        decode = Codec().decode,
        incrementalencoder = IncrementalEncoder,
        incrementaldecoder = IncrementalDecoder,
        streamreader = StreamReader,
        streamwriter = StreamWriter
    )

    return info
# end def getregentry

# Based on information from
# http://msdn.microsoft.com/en-us/goglobal/cc305157.aspx

decoding_table = (
    "\x00"    # 0x00 -> NULL
    "\x01"    # 0x01 -> START OF HEADING
    "\x02"    # 0x02 -> START OF TEXT
    "\x03"    # 0x03 -> END OF TEXT
    "\x04"    # 0x04 -> END OF TRANSMISSION
    "\x05"    # 0x05 -> ENQUIRY
    "\x06"    # 0x06 -> ACKNOWLEDGE
    "\x07"    # 0x07 -> BELL
    "\x08"    # 0x08 -> BACKSPACE
    "\x09"    # 0x09 -> HORIZONTAL TABULATION
    "\x0A"    # 0x0A -> LINE FEED
    "\x0B"    # 0x0B -> VERTICAL TABULATION
    "\x0C"    # 0x0C -> FORM FEED
    "\x0D"    # 0x0D -> CARRIAGE RETURN
    "\x0E"    # 0x0E -> SHIFT OUT
    "\x0F"    # 0x0F -> SHIFT IN
    "\x10"    # 0x10 -> DATA LINK ESCAPE
    "\x11"    # 0x11 -> DEVICE CONTROL ONE
    "\x12"    # 0x12 -> DEVICE CONTROL TWO
    "\x13"    # 0x13 -> DEVICE CONTROL THREE
    "\x14"    # 0x14 -> DEVICE CONTROL FOUR
    "\x15"    # 0x15 -> NEGATIVE ACKNOWLEDGE
    "\x16"    # 0x16 -> SYNCHRONOUS IDLE
    "\x17"    # 0x17 -> END OF TRANSMISSION BLOCK
    "\x18"    # 0x18 -> CANCEL
    "\x19"    # 0x19 -> END OF MEDIUM
    "\x1A"    # 0x1A -> SUBSTITUTE
    "\x1B"    # 0x1B -> ESCAPE
    "\x1C"    # 0x1C -> FILE SEPARATOR
    "\x1D"    # 0x1D -> GROUP SEPARATOR
    "\x1E"    # 0x1E -> RECORD SEPARATOR
    "\x1F"    # 0x1F -> UNIT SEPARATOR
    "\x20"    # 0x20 -> SPACE
    "\x21"    # 0x21 -> EXCLAMATION MARK
    "\x22"    # 0x22 -> QUOTATION MARK
    "\x23"    # 0x23 -> NUMBER SIGN
    "\x24"    # 0x24 -> DOLLAR SIGN
    "\x25"    # 0x25 -> PERCENT SIGN
    "\x26"    # 0x26 -> AMPERSAND
    "\x27"    # 0x27 -> APOSTROPHE
    "\x28"    # 0x28 -> LEFT PARENTHESIS
    "\x29"    # 0x29 -> RIGHT PARENTHESIS
    "\x2A"    # 0x2A -> ASTERISK
    "\x2B"    # 0x2B -> PLUS SIGN
    "\x2C"    # 0x2C -> COMMA
    "\x2D"    # 0x2D -> HYPHEN-MINUS
    "\x2E"    # 0x2E -> FULL STOP
    "\x2F"    # 0x2F -> SOLIDUS
    "\x30"    # 0x30 -> DIGIT ZERO
    "\x31"    # 0x31 -> DIGIT ONE
    "\x32"    # 0x32 -> DIGIT TWO
    "\x33"    # 0x33 -> DIGIT THREE
    "\x34"    # 0x34 -> DIGIT FOUR
    "\x35"    # 0x35 -> DIGIT FIVE
    "\x36"    # 0x36 -> DIGIT SIX
    "\x37"    # 0x37 -> DIGIT SEVEN
    "\x38"    # 0x38 -> DIGIT EIGHT
    "\x39"    # 0x39 -> DIGIT NINE
    "\x3A"    # 0x3A -> COLON
    "\x3B"    # 0x3B -> SEMICOLON
    "\x3C"    # 0x3C -> LESS-THAN SIGN
    "\x3D"    # 0x3D -> EQUALS SIGN
    "\x3E"    # 0x3E -> GREATER-THAN SIGN
    "\x3F"    # 0x3F -> QUESTION MARK
    "\x40"    # 0x40 -> COMMERCIAL AT
    "\x41"    # 0x41 -> LATIN CAPITAL LETTER A
    "\x42"    # 0x42 -> LATIN CAPITAL LETTER B
    "\x43"    # 0x43 -> LATIN CAPITAL LETTER C
    "\x44"    # 0x44 -> LATIN CAPITAL LETTER D
    "\x45"    # 0x45 -> LATIN CAPITAL LETTER E
    "\x46"    # 0x46 -> LATIN CAPITAL LETTER F
    "\x47"    # 0x47 -> LATIN CAPITAL LETTER G
    "\x48"    # 0x48 -> LATIN CAPITAL LETTER H
    "\x49"    # 0x49 -> LATIN CAPITAL LETTER I
    "\x4A"    # 0x4A -> LATIN CAPITAL LETTER J
    "\x4B"    # 0x4B -> LATIN CAPITAL LETTER K
    "\x4C"    # 0x4C -> LATIN CAPITAL LETTER L
    "\x4D"    # 0x4D -> LATIN CAPITAL LETTER M
    "\x4E"    # 0x4E -> LATIN CAPITAL LETTER N
    "\x4F"    # 0x4F -> LATIN CAPITAL LETTER O
    "\x50"    # 0x50 -> LATIN CAPITAL LETTER P
    "\x51"    # 0x51 -> LATIN CAPITAL LETTER Q
    "\x52"    # 0x52 -> LATIN CAPITAL LETTER R
    "\x53"    # 0x53 -> LATIN CAPITAL LETTER S
    "\x54"    # 0x54 -> LATIN CAPITAL LETTER T
    "\x55"    # 0x55 -> LATIN CAPITAL LETTER U
    "\x56"    # 0x56 -> LATIN CAPITAL LETTER V
    "\x57"    # 0x57 -> LATIN CAPITAL LETTER W
    "\x58"    # 0x58 -> LATIN CAPITAL LETTER X
    "\x59"    # 0x59 -> LATIN CAPITAL LETTER Y
    "\x5A"    # 0x5A -> LATIN CAPITAL LETTER Z
    "\x5B"    # 0x5B -> LEFT SQUARE BRACKET
    "\x5C"    # 0x5C -> REVERSE SOLIDUS
    "\x5D"    # 0x5D -> RIGHT SQUARE BRACKET
    "\x5E"    # 0x5E -> CIRCUMFLEX ACCENT
    "\x5F"    # 0x5F -> LOW LINE
    "\x60"    # 0x60 -> GRAVE ACCENT
    "\x61"    # 0x61 -> LATIN SMALL LETTER A
    "\x62"    # 0x62 -> LATIN SMALL LETTER B
    "\x63"    # 0x63 -> LATIN SMALL LETTER C
    "\x64"    # 0x64 -> LATIN SMALL LETTER D
    "\x65"    # 0x65 -> LATIN SMALL LETTER E
    "\x66"    # 0x66 -> LATIN SMALL LETTER F
    "\x67"    # 0x67 -> LATIN SMALL LETTER G
    "\x68"    # 0x68 -> LATIN SMALL LETTER H
    "\x69"    # 0x69 -> LATIN SMALL LETTER I
    "\x6A"    # 0x6A -> LATIN SMALL LETTER J
    "\x6B"    # 0x6B -> LATIN SMALL LETTER K
    "\x6C"    # 0x6C -> LATIN SMALL LETTER L
    "\x6D"    # 0x6D -> LATIN SMALL LETTER M
    "\x6E"    # 0x6E -> LATIN SMALL LETTER N
    "\x6F"    # 0x6F -> LATIN SMALL LETTER O
    "\x70"    # 0x70 -> LATIN SMALL LETTER P
    "\x71"    # 0x71 -> LATIN SMALL LETTER Q
    "\x72"    # 0x72 -> LATIN SMALL LETTER R
    "\x73"    # 0x73 -> LATIN SMALL LETTER S
    "\x74"    # 0x74 -> LATIN SMALL LETTER T
    "\x75"    # 0x75 -> LATIN SMALL LETTER U
    "\x76"    # 0x76 -> LATIN SMALL LETTER V
    "\x77"    # 0x77 -> LATIN SMALL LETTER W
    "\x78"    # 0x78 -> LATIN SMALL LETTER X
    "\x79"    # 0x79 -> LATIN SMALL LETTER Y
    "\x7A"    # 0x7A -> LATIN SMALL LETTER Z
    "\x7B"    # 0x7B -> LEFT CURLY BRACKET
    "\x7C"    # 0x7C -> VERTICAL LINE
    "\x7D"    # 0x7D -> RIGHT CURLY BRACKET
    "\x7E"    # 0x7E -> TILDE
    "\x7F"    # 0x7F -> DELETE
    "\uFFFE"  # 0x80 -> UNDEFINED
    "\uFFFE"  # 0x81 -> UNDEFINED
    "\xE9"    # 0x82 -> LATIN SMALL LETTER E WITH ACUTE
    "\xE2"    # 0x83 -> LATIN SMALL LETTER A WITH CIRCUMFLEX
    "\uFFFE"  # 0x84 -> UNDEFINED
    "\xE0"    # 0x85 -> LATIN SMALL LETTER A WITH GRAVE
    "\uFFFE"  # 0x86 -> UNDEFINED
    "\xE7"    # 0x87 -> LATIN SMALL LETTER C WITH CEDILLA
    "\xEA"    # 0x88 -> LATIN SMALL LETTER E WITH CIRCUMFLEX
    "\xEB"    # 0x89 -> LATIN SMALL LETTER E WITH DIAERESIS
    "\xE8"    # 0x8A -> LATIN SMALL LETTER E WITH GRAVE
    "\xEF"    # 0x8B -> LATIN SMALL LETTER I WITH DIAERESIS
    "\xEE"    # 0x8C -> LATIN SMALL LETTER I WITH CIRCUMFLEX
    "\uFFFE"  # 0x8D -> UNDEFINED
    "\uFFFE"  # 0x8E -> UNDEFINED
    "\uFFFE"  # 0x8F -> UNDEFINED
    "\uFFFE"  # 0x90 -> UNDEFINED
    "\u0651"  # 0x91 -> ARABIC SHADDA
    "\u0652"  # 0x92 -> ARABIC SUKUN
    "\xF4"    # 0x93 -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    "\xA4"    # 0x94 -> CURRENCY SIGN
    "\u0640"  # 0x95 -> ARABIC TATWEEL
    "\xFB"    # 0x96 -> LATIN SMALL LETTER U WITH CIRCUMFLEX
    "\xF9"    # 0x97 -> LATIN SMALL LETTER U WITH GRAVE
    "\u0621"  # 0x98 -> ARABIC LETTER HAMZA
    "\u0622"  # 0x99 -> ARABIC LETTER ALEF WITH MADDA ABOVE
    "\u0623"  # 0x9A -> ARABIC LETTER ALEF WITH HAMZA ABOVE
    "\u0624"  # 0x9B -> ARABIC LETTER WAW WITH HAMZA ABOVE
    "\xA3"    # 0x9C -> POUND SIGN
    "\u0625"  # 0x9D -> ARABIC LETTER ALEF WITH HAMZA BELOW
    "\u0626"  # 0x9E -> ARABIC LETTER YEH WITH HAMZA ABOVE
    "\u0627"  # 0x9F -> ARABIC LETTER ALEF
    "\u0628"  # 0xA0 -> ARABIC LETTER BEH
    "\u0629"  # 0xA1 -> ARABIC LETTER TEH MARBUTA
    "\u062A"  # 0xA2 -> ARABIC LETTER TEH
    "\u062B"  # 0xA3 -> ARABIC LETTER THEH
    "\u062C"  # 0xA4 -> ARABIC LETTER JEEM
    "\u062D"  # 0xA5 -> ARABIC LETTER HAH
    "\u062E"  # 0xA6 -> ARABIC LETTER KHAH
    "\u062F"  # 0xA7 -> ARABIC LETTER DAL
    "\u0630"  # 0xA8 -> ARABIC LETTER THAL
    "\u0631"  # 0xA9 -> ARABIC LETTER REH
    "\u0632"  # 0xAA -> ARABIC LETTER ZAIN
    "\u0633"  # 0xAB -> ARABIC LETTER SEEN
    "\u0634"  # 0xAC -> ARABIC LETTER SHEEN
    "\u0635"  # 0xAD -> ARABIC LETTER SAD
    "\xAB"    # 0xAE -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    "\xBB"    # 0xAF -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "\u2591"  # 0xB0 -> LIGHT SHADE
    "\u2592"  # 0xB1 -> MEDIUM SHADE
    "\u2593"  # 0xB2 -> DARK SHADE
    "\u2502"  # 0xB3 -> BOX DRAWINGS LIGHT VERTICAL
    "\u2524"  # 0xB4 -> BOX DRAWINGS LIGHT VERTICAL AND LEFT
    "\u2561"  # 0xB5 -> BOX DRAWINGS VERTICAL SINGLE AND LEFT DOUBLE
    "\u2562"  # 0xB6 -> BOX DRAWINGS VERTICAL DOUBLE AND LEFT SINGLE
    "\u2556"  # 0xB7 -> BOX DRAWINGS DOWN DOUBLE AND LEFT SINGLE
    "\u2555"  # 0xB8 -> BOX DRAWINGS DOWN SINGLE AND LEFT DOUBLE
    "\u2563"  # 0xB9 -> BOX DRAWINGS DOUBLE VERTICAL AND LEFT
    "\u2551"  # 0xBA -> BOX DRAWINGS DOUBLE VERTICAL
    "\u2557"  # 0xBB -> BOX DRAWINGS DOUBLE DOWN AND LEFT
    "\u255D"  # 0xBC -> BOX DRAWINGS DOUBLE UP AND LEFT
    "\u255C"  # 0xBD -> BOX DRAWINGS UP DOUBLE AND LEFT SINGLE
    "\u255B"  # 0xBE -> BOX DRAWINGS UP SINGLE AND LEFT DOUBLE
    "\u2510"  # 0xBF -> BOX DRAWINGS LIGHT DOWN AND LEFT
    "\u2514"  # 0xC0 -> BOX DRAWINGS LIGHT UP AND RIGHT
    "\u2534"  # 0xC1 -> BOX DRAWINGS LIGHT UP AND HORIZONTAL
    "\u252C"  # 0xC2 -> BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
    "\u251C"  # 0xC3 -> BOX DRAWINGS LIGHT VERTICAL AND RIGHT
    "\u2500"  # 0xC4 -> BOX DRAWINGS LIGHT HORIZONTAL
    "\u253C"  # 0xC5 -> BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
    "\u255E"  # 0xC6 -> BOX DRAWINGS VERTICAL SINGLE AND RIGHT DOUBLE
    "\u255F"  # 0xC7 -> BOX DRAWINGS VERTICAL DOUBLE AND RIGHT SINGLE
    "\u255A"  # 0xC8 -> BOX DRAWINGS DOUBLE UP AND RIGHT
    "\u2554"  # 0xC9 -> BOX DRAWINGS DOUBLE DOWN AND RIGHT
    "\u2569"  # 0xCA -> BOX DRAWINGS DOUBLE UP AND HORIZONTAL
    "\u2566"  # 0xCB -> BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
    "\u2560"  # 0xCC -> BOX DRAWINGS DOUBLE VERTICAL AND RIGHT
    "\u2550"  # 0xCD -> BOX DRAWINGS DOUBLE HORIZONTAL
    "\u256C"  # 0xCE -> BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
    "\u2567"  # 0xCF -> BOX DRAWINGS UP SINGLE AND HORIZONTAL DOUBLE
    "\u2568"  # 0xD0 -> BOX DRAWINGS UP DOUBLE AND HORIZONTAL SINGLE
    "\u2564"  # 0xD1 -> BOX DRAWINGS DOWN SINGLE AND HORIZONTAL DOUBLE
    "\u2565"  # 0xD2 -> BOX DRAWINGS DOWN DOUBLE AND HORIZONTAL SINGLE
    "\u2559"  # 0xD3 -> BOX DRAWINGS UP DOUBLE AND RIGHT SINGLE
    "\u2558"  # 0xD4 -> BOX DRAWINGS UP SINGLE AND RIGHT DOUBLE
    "\u2552"  # 0xD5 -> BOX DRAWINGS DOWN SINGLE AND RIGHT DOUBLE
    "\u2553"  # 0xD6 -> BOX DRAWINGS DOWN DOUBLE AND RIGHT SINGLE
    "\u256B"  # 0xD7 -> BOX DRAWINGS VERTICAL DOUBLE AND HORIZONTAL SINGLE
    "\u256A"  # 0xD8 -> BOX DRAWINGS VERTICAL SINGLE AND HORIZONTAL DOUBLE
    "\u2518"  # 0xD9 -> BOX DRAWINGS LIGHT UP AND LEFT
    "\u250C"  # 0xDA -> BOX DRAWINGS LIGHT DOWN AND RIGHT
    "\u2588"  # 0xDB -> FULL BLOCK
    "\u2584"  # 0xDC -> LOWER HALF BLOCK
    "\u258C"  # 0xDD -> LEFT HALF BLOCK
    "\u2590"  # 0xDE -> RIGHT HALF BLOCK
    "\u2580"  # 0xDF -> UPPER HALF BLOCK
    "\u0636"  # 0xE0 -> ARABIC LETTER DAD
    "\u0637"  # 0xE1 -> ARABIC LETTER TAH
    "\u0638"  # 0xE2 -> ARABIC LETTER ZAH
    "\u0639"  # 0xE3 -> ARABIC LETTER AIN
    "\u063A"  # 0xE4 -> ARABIC LETTER GHAIN
    "\u0641"  # 0xE5 -> ARABIC LETTER FEH
    "\xB5"    # 0xE6 -> MICRO SIGN
    "\u0642"  # 0xE7 -> ARABIC LETTER QAF
    "\u0643"  # 0xE8 -> ARABIC LETTER KAF
    "\u0644"  # 0xE9 -> ARABIC LETTER LAM
    "\u0645"  # 0xEA -> ARABIC LETTER MEEM
    "\u0646"  # 0xEB -> ARABIC LETTER NOON
    "\u0647"  # 0xEC -> ARABIC LETTER HEH
    "\u0648"  # 0xED -> ARABIC LETTER WAW
    "\u0649"  # 0xEE -> ARABIC LETTER ALEF MAKSURA
    "\u064A"  # 0xEF -> ARABIC LETTER YEH
    "\u2261"  # 0xF0 -> IDENTICAL TO
    "\u064B"  # 0xF1 -> ARABIC FATHATAN
    "\u064C"  # 0xF2 -> ARABIC DAMMATAN
    "\u064D"  # 0xF3 -> ARABIC KASRATAN
    "\u064E"  # 0xF4 -> ARABIC FATHA
    "\u064F"  # 0xF5 -> ARABIC DAMMA
    "\u0650"  # 0xF6 -> ARABIC KASRA
    "\u2248"  # 0xF7 -> ALMOST EQUAL TO
    "\xB0"    # 0xF8 -> DEGREE SIGN
    "\u2219"  # 0xF9 -> BULLET OPERATOR
    "\xB7"    # 0xFA -> MIDDLE DOT
    "\u221A"  # 0xFB -> SQUARE ROOT
    "\u207F"  # 0xFC -> SUPERSCRIPT LATIN SMALL LETTER N
    "\xB2"    # 0xFD -> SUPERSCRIPT TWO
    "\u25A0"  # 0xFE -> BLACK SQUARE
    "\xA0"    # 0xFF -> NO-BREAK SPACE
)

encoding_table = codecs.charmap_build(decoding_table)
