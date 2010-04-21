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
"""Dumps record data types (data structures"""

# stdlib imports
import sys
import imp
from optparse import OptionParser, OptionGroup
from inspect import isclass

# local imports
from lf.dec import RawIStream
from lf.dtypes import Record, Basic, Native, BitType, bits, raw

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)


__docformat__ = "restructuredtext en"
__all__ = [
    "main", "RecordFormatter"
]

class RecordFormatter():
    class FieldInfo():
        """Helper class for formatting fields"""

        def __init__(self, field):
            """Initializes a FieldInfo class"""

            is_array = False
            is_record = False
            is_native = False
            is_bittype = False
            is_raw = False
            count = 0

            size = self.get_size(field)

            if isclass(field):
                type_name = field.__name__

                if issubclass(field, BitType):
                    is_bittype = True
                elif issubclass(field, Native):
                    is_native = True
                elif issubclass(field, raw):
                    is_raw = True
                elif issubclass(field, Record):
                    is_record = True
                else:
                    raise TypeError("Unknown data type {0}".format(field))
                # end if

            else:
                if isinstance(field, list):
                    is_array = True
                    count = len(field)
                    element_dtype = field[0]
                    element_info = RecordFormatter.FieldInfo(element_dtype)

                    type_name = element_info.type_name
                else:
                    type_name = field.__class__.__name__
                    if isinstance(field, Native):
                        is_native = True
                    elif isinstance(field, raw):
                        is_raw = True
                    elif isinstance(field, Record):
                        is_record = True
                    elif isinstance(field, BitType):
                        is_bittype = True
                    else:
                        raise TypeError("Unknown data type {0}".format(field))
                    # end if
                # end if
            # end if

            self.is_raw = is_raw
            self.is_native = is_native
            self.is_record = is_record
            self.is_bittype = is_bittype
            self.is_array = is_array
            self.count = count

            self.type_name = type_name
            self.size = size
        # end def __init__

        @classmethod
        def get_size(cls, dtype):
            """Determines the size of a data type"""

            if isclass(dtype):
                if issubclass(dtype, (Basic, Record)):
                    size = dtype._size_
                elif issubclass(dtype, bits):
                    size = dtype._size_
                else:
                    raise TypeError("Unknown data type {0}".format(dtype))
                # end if
            else:
                if isinstance(dtype, list):
                    count = len(dtype)
                    element_dtype = dtype[0]
                    size = cls.get_size(element_dtype) * count
                elif isinstance(dtype, (Basic, Record)):
                    size = dtype._size_
                elif isinstance(dtype, bits):
                    size = dtype._size_
                else:
                    raise TypeError("Unknown data type {0}".format(dtype))
                # end if
            # end if

            return size
        # end def get_size
    # end class FieldInfo

    class LineInfo():
        """Helper class to represent a line of output"""

        def __init__(self):
            """Initializes a LineInfo object"""

            self.offset = None
            self.bit_offset = None
            self.spacing = 0
            self.name = None
            self.type_name = None
            self.size = None
            self.count = 0
            self.data = None
            self.show_plus = True
        # end def __init__
    # end def LineInfo

    def __init__(self, obase, ibase, sbase, dbase, max_depth=0):
        """Initializes a RecordFormatter object"""

        self.offset_base = obase
        self.index_base = ibase
        self.size_base = sbase
        self.data_base = dbase
        self.max_depth = max_depth

        self.size_format_strs = {
            "b": "{size:04b}",
            "d": "{size:d}",
            "o": "{size:o}",
            "x": "{size:x}",
            "X": "{size:X}"
        }

        self.offset_format_strs = {
            "b": [
                "{byte_offset:010b}:", "{byte_offset:010b}:{bit_offset:04b}:"
            ],
            "d": ["{byte_offset:06d}:", "{byte_offset:06d}:{bit_offset:02d}:"],
            "o": ["{byte_offset:06o}:", "{byte_offset:06o}:{bit_offset:02o}:"],
            "x": ["{byte_offset:04x}:", "{byte_offset:04x}:{bit_offset:02x}:"],
            "X": ["{byte_offset:04X}:", "{byte_offset:04X}:{bit_offset:02X}:"],
        }

        self.index_format_strs = {
            "b": "{index:04b}",
            "d": "{index:d}",
            "o": "{index:o}",
            "x": "{index:x}",
            "X": "{index:X}"
        }

        self.data_format_strs = {
            "b": "{data:04b}",
            "d": "{data:d}",
            "o": "{data:o}",
            "x": "0x{data:x}",
            "X": "0x{data:X}"
        }

        self.offset_width = 10
        self.name_width = 26

        # Used temporarily during formatting...
        self.raw_data_len = 0
    # end def __init__

    def format(self, record, raw_data=None):
        """Formats a Record data type for output"""

        FieldInfo = RecordFormatter.FieldInfo
        format_header = self.format_header
        format_dtype = self.format_dtype
        can_display_data = self.can_display_data
        output = list()
        offset = 0

        if raw_data is not None:
            raw_data_len = len(raw_data)
            field_info = FieldInfo(record)

            if raw_data_len < field_info.size:
                pad = b"\x00" * (field_info.size - raw_data_len)
            else:
                pad = b""
            # end if

            record_data = b"".join([raw_data, pad])
            record_data = record._ctype_.from_buffer_copy(record_data)
        else:
            raw_data_len = 0
            record_data = None
        # end if

        self.raw_data_len = raw_data_len

        for (name, dtype) in record._fields_:
            field_info = FieldInfo(dtype)

            if can_display_data(dtype, offset):
                if field_info.is_bittype:
                    field_data = record_data
                else:
                    field_data = getattr(record_data, name)
                # end if
            else:
                field_data = None
            # end if

            output.extend(format_header(
                dtype, offset, 0, name, field_data
            ))
            output.extend(self.format_dtype(
                dtype, offset, 0, name, field_data
            ))
            offset += FieldInfo(dtype).size
        # end for

        return output
    # end def format

    def can_display_data(self, dtype, offset):
        """Returns True if there are raw bytes remaining to display data"""

        raw_data_len = self.raw_data_len
        can_display = False

        if (offset < raw_data_len):
            field_info = RecordFormatter.FieldInfo(dtype)
            bytes_needed = field_info.size + offset

            if field_info.is_native:
                if bytes_needed <= raw_data_len:
                    can_display = True
                # end if
            elif field_info.is_raw:
                can_display = True
            else:
                can_display = True
            # end if
        # end if

        return can_display
    # end def get_data

    def format_header(self, dtype, offset, depth, name=None, data=None):
        """Creates the 'header line' for a data type"""

        FieldInfo = RecordFormatter.FieldInfo
        line_info = RecordFormatter.LineInfo()
        field_info = FieldInfo(dtype)
        output = list()

        if (field_info.is_bittype) or (name is None):
            return output
        # end if

        if data is not None:
            if field_info.is_native:
                line_info.data = data
            elif field_info.is_native:
                line_info.data = bytes(data)
            # end if
        # end if

        line_info.name = name
        line_info.offset = offset
        line_info.size = field_info.size
        line_info.count = field_info.count
        line_info.spacing = depth * 2
        line_info.type_name = field_info.type_name
        output.append(self.format_line(line_info))

        return output
    # end def format_header

    def format_dtype(self, dtype, offset, depth, name=None, data=None):
        """Formats a data type for output"""

        field_info = RecordFormatter.FieldInfo(dtype)
        output = list()

        if field_info.is_native or field_info.is_raw:
            return output
        elif field_info.is_bittype:
            output.extend(self.format_bittype(dtype, offset, depth, data))
            return output
        # end if

        max_depth = self.max_depth
        if (depth >= max_depth) and (max_depth >= 0):
            return output
        # end if

        if field_info.is_record:
            format_func = self.format_record
        elif field_info.is_array:
            format_func = self.format_array
        else:
            raise TypeError("Unknown data type {0}".format(dtype))
        # end if

        output.extend(format_func(dtype, offset, depth + 1, name, data))

        return output
    # end def format_dtype

    def format_bittype(self, dtype, offset, depth, data=None):
        """Formats a BitType data type for output"""

        LineInfo = RecordFormatter.LineInfo
        can_display_data = self.can_display_data
        raw_data_len = self.raw_data_len
        output = list()
        bit_offset = 0

        for (bit_field_name, bit_dtype) in dtype._fields_:
            line_info = LineInfo()
            line_info.offset = offset
            line_info.bit_offset = bit_offset
            line_info.name = bit_field_name
            line_info.size = bit_dtype._size_
            line_info.spacing = depth * 2

            bits_sum = bit_offset + bit_dtype._size_
            full_offset = offset + (bits_sum // 8)
            if (bits_sum % 8):
                full_offset += 1
            # end if

            if full_offset <= raw_data_len:
                line_info.data = getattr(data, bit_field_name)
            # end if

            if isclass(bit_dtype):
                line_info.type_name = bit_dtype.__name__
            else:
                line_info.type_name = bit_dtype.__class__.__name__
            # end if

            output.append(self.format_line(line_info))

            bit_offset += line_info.size
            offset += bit_offset // 8
            bit_offset = bit_offset % 8
        # end for

        return output
    # end def format_bittype

    def format_record(self, dtype, offset, depth, name=None, data=None):
        """Formats a Record data type for output"""

        LineInfo = RecordFormatter.LineInfo
        FieldInfo = RecordFormatter.FieldInfo
        format_header = self.format_header
        format_dtype = self.format_dtype
        can_display_data = self.can_display_data
        output = list()

        for (field_name, field_dtype) in dtype._fields_:
            field_info = FieldInfo(field_dtype)

            if can_display_data(field_dtype, offset):
                if field_info.is_bittype:
                    field_data = data
                else:
                    field_data = getattr(data, field_name)
                # end if
            else:
                field_data = None
            # end if

            output.extend(format_header(
                field_dtype, offset, depth, field_name, field_data
            ))
            output.extend(format_dtype(
                field_dtype, offset, depth, field_name, field_data
            ))

            offset += field_info.size
         # end for

        return output
    # end def format_record

    def format_array(self, dtype, offset, depth, name=None, data=None):
        """Formats an array data type for output"""

        LineInfo = RecordFormatter.LineInfo
        FieldInfo = RecordFormatter.FieldInfo
        can_display_data = self.can_display_data
        format_header = self.format_header
        format_dtype = self.format_dtype
        format_bittype = self.format_bittype
        format_record = self.format_record
        raw_data_len = self.raw_data_len
        output = list()

        line_info = LineInfo()
        field_info = FieldInfo(dtype)
        element_info = FieldInfo(dtype[0])

        if element_info.is_native or element_info.is_raw:
            for counter in range(field_info.count):

                if can_display_data(dtype[0], offset):
                    field_data = data[counter]
                else:
                    field_data = None
                # end if

                field_name = "{0}[{1}]".format(
                    name, self.format_index(counter)
                )
                output.extend(format_header(
                    dtype[0], offset, depth, field_name, field_data
                ))

                offset += element_info.size
            # end for
        else:
            for counter in range(field_info.count):
                line_info = LineInfo()
                line_info.offset = offset
                line_info.spacing = (depth * 2) - 1
                line_info.name = "[{0}]".format(self.format_index(counter))
                line_info.show_plus = False

                output.append(self.format_line(line_info))

                if can_display_data(dtype[0], offset):
                    field_data = data[counter]
                else:
                    field_data = None
                # end if

                if element_info.is_bittype:
                    output.extend(format_bittype(
                        dtype[0], offset, depth, name, field_data
                    ))
                elif element_info.is_record:
                    output.extend(format_record(
                        dtype[0], offset, depth, name, field_data
                    ))
                elif element_info.is_array:
                    output.extend(format_dtype(
                        dtype[0], offset, depth, name, field_data
                    ))
                else:
                    raise TypeError("Unknown data type {0}".format(dtype[0]))
                # end if

                offset += element_info.size
            # end for
        # end if

        return output
    # end def format_array

    def format_line(self, line_info):
        """Formats a line of output"""

        offset_str = self.format_offset(line_info.offset, line_info.bit_offset)
        offset_str = "{0:{1}}".format(offset_str, self.offset_width)

        if line_info.spacing and line_info.show_plus:
            name = "".join([" " * line_info.spacing, "+ ", line_info.name])
        else:
            name = "".join([" " * line_info.spacing, line_info.name])
        # end if

        if (not line_info.type_name) or (not line_info.size):
            name_str = name
            comment_str = ""
        else:
            name_str = "{0:{1}}".format(name, self.name_width)

            if line_info.count:
                index_str = "[{0}]".format(self.format_index(line_info.count))
            else:
                index_str = ""
            # end if

            size_str = self.format_size(line_info.size)

            comment_str = " ; {typename}{index_str} ({size_str})".format(
                typename=line_info.type_name,
                index_str=index_str,
                size_str=size_str
            )
        # end if

        if line_info.data is not None:
            data_str = ", data = {0}".format(self.format_data(line_info.data))
        else:
            data_str = ""
        # end if

        output = "{offset_str}{name_str}{comment_str}{data_str}".format(
            offset_str=offset_str,
            name_str=name_str,
            comment_str=comment_str,
            data_str=data_str
        )

        return output
    # end def format_line

    def format_size(self, size):
        """Formats the size parameter"""

        format_str = self.size_format_strs[self.size_base]
        return format_str.format(size=size)
    # end def format_size

    def format_offset(self, byte_offset, bit_offset=None):
        """Formats the offset parameter"""

        format_strs = self.offset_format_strs[self.offset_base]

        if bit_offset is None:
            output_str = format_strs[0].format(byte_offset=byte_offset)
        else:
            output_str = format_strs[1].format(
                byte_offset=byte_offset, bit_offset=bit_offset
            )
        # end if

        return output_str
    # end def format_offset

    def format_index(self, index):
        """Formats the index parameter"""

        format_str = self.index_format_strs[self.index_base]
        return format_str.format(index=index)
    # end def format_index

    def format_data(self, data):
        """Formats the data parmeter"""

        if isinstance(data, int):
            data_format_str = self.data_format_strs[self.data_base]
            output = data_format_str.format(data=data)
        elif isinstance(data, bytes):
            output = "{0}".format(data)
            output = output[1:]
        else:
            output = "{0}".format(data)
        # end if

        return output
    # end def format_data
# end class RecordFormatter

def get_record(module, name, absolute_import, module_is_file):
    """Retrieves a record object."""

    __import__(module_name)
    module = sys.modules[module_name]

    record = getattr(module, record_name)

    if not issubclass(record, Extractable):
        raise TypeError("{0} is not a record".format(record))
    # end if

    return record("")
# end def get_record

def main():
    usage = "%prog [options] RECORD [file]"
    description = \
        "Dumps information about record data types (data structures). " \
        "By specifying a file (or '-' for stdin) data from the file (or " \
        "stdin) is extracted and printed inline with the data structure"

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    format_group = OptionGroup(parser, "Formatting Options",
        "The options are used for formatting output of numbers.  Valid values "
        "for BASE are: [b]inary, [d]ecial, [o]ctal, and he[x|X]."
    )

    format_group.add_option(
        "-o",
        action="store",
        type="choice",
        dest="offset_base",
        default="X",
        help="The base for offsets (default: %default)",
        choices=("b", "d", "o", "x", "X"),
        metavar="BASE"
    )

    format_group.add_option(
        "-d",
        action="store",
        type="choice",
        dest="data_base",
        default="X",
        metavar="BASE",
        help="The base for data (default: %default)",
        choices=("b", "d", "o", "x", "X")
    )

    format_group.add_option(
        "-s",
        action="store",
        type="choice",
        dest="size_base",
        default="d",
        metavar="BASE",
        help="The base for sizes (default: %default)",
        choices=("b", "d", "o", "x", "X")
    )

    format_group.add_option(
        "-i",
        action="store",
        type="choice",
        dest="index_base",
        default="d",
        metavar="BASE",
        help="The base for indices (default: %default)",
        choices=("b", "d", "o", "x", "X")
    )

    parser.add_option(
        "-r",
        dest="max_depth",
        action="store",
        type="int",
        default=0,
        help="Maximum depth for recursion (-1 is unlimited)"
    )

    parser.add_option(
        "-f",
        "--file",
        action="store",
        dest="module_file",
        nargs=2,
        metavar="FILE MODNAME",
        help="Load RECORD from FILE using MODNAME as the module name"
    )

    parser.add_option_group(format_group)

    (options, args) = parser.parse_args()

    data_name = None
    data = None
    input_file_name = None
    module_name = None

    obase = options.offset_base
    dbase = options.data_base
    sbase = options.size_base
    ibase = options.index_base
    max_depth = options.max_depth

    if len(args) < 1:
        parser.error("you must specify a RECORD to dump")
    elif len(args) > 1:
        if args[1] == "-":
            data = sys.stdin.buffer.read()
            data_name = "--stdin--"
        else:
            data = RawIStream(args[1]).read()
            data_name = args[1]
        # end if
    # end if

    if options.module_file:
        (input_file_name, module_name) = options.module_file
        module = imp.load_source(module_name, input_file_name)
        record_name = args[0]
    else:
        (module_name, record_name) = args[0].rsplit(".", 1)
        __import__(module_name)
        module = sys.modules[module_name]
    # end if

    record = getattr(module, record_name)
    if not issubclass(record, Record):
        parser.error("Only record data types are supported")
    # end if

    output = list()
    if input_file_name:
        output.append("File: {0}".format(input_file_name))
    else:
        output.append("File: n/a")
    # end if

    output.append("Module: {0}".format(module_name))
    output.append("Record: {0}".format(record_name))
    output.append("Size of record: {0} bytes".format(record._size_))

    if data_name:
        output.append("Data: {0} bytes from {1}".format(len(data), data_name))
    else:
        output.append("Data: n/a")
    # end if

    output.append("")
    formatter = RecordFormatter(obase, ibase, sbase, dbase, max_depth)
    output.extend(formatter.format(record, data))

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
