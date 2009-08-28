# Prints and extracts records (Data Structure Print and Extract)

import sys
import imp
from optparse import OptionParser
from itertools import count
from inspect import isclass

from lf.datatype.base import Basic
from lf.datatype import Extractor
from lf.datatype import (
    BitType, Record, array
)
from lf.datatype.composite import Extractable
from lf.io import raw

class RecordFormatter():
    """
    Formats a record for human consumption.

    .. attribute:: offset_base

        The format character for the offset column.

    .. attribute:: size_base

        The format character for the size column.

    .. attribute:: value_base

        The format character for the value column.

    .. attribute:: record

        The record to format.

    .. attribute:: data

        If not None, binary data to extract values from.
    """

    def __init__(self, record, bases, data=None):
        """
        Initializes a RecordFormatter object.

        :parameters:
            record
                The record to format.

            bases
                A tuple of (offset_base, size_base_, value_base)

            data
                A bytes object of data to extract.
        """

        self.record = record
        self.offset_base = bases[0]
        self.size_base = bases[1]
        self.value_base = bases[2]
        self.data = data
    # end def __init__

    def format_record(self):
        """
        Formats a record for printing.

        :rtype: list
        :returns: A list of strings, suitable for printing
        """

        record = self.record
        (offsets, sizes) = self.get_offsets_sizes()
        (datatypes, names) = self.get_datatypes_names()

        output = list()

        if data:
            (field_count, value_count, values) = self.get_formatted_values()

            output.append("Extracted {0} of {1} total fields".format(
                value_count, field_count
                )
            )

            column_names = (
                "Item", "Offset", "Size", "Type", "Field", "Value"
            )

            format_str = "{0: <4} {1: <7} {2: <4} {3: <25} {4: <25} {5: <5}"
            separator_format_str = \
                "{0:-<4} {0:-<7} {0:-<4} {0:-<25} {0:-<25} {0:-<5}"

            rows_of_data = zip(
                count(), offsets, sizes, datatypes, names, values
            )
        else:
            column_names = ("Item", "Offset", "Size", "Type", "Field")

            format_str = "{0: <4} {1: <7} {2: <4} {3: <25} {4: <25}"
            separator_format_str = \
                "{0:-<4} {0:-<7} {0:-<4} {0:-<25} {0:-<25}"

            rows_of_data = zip(count(), offsets, sizes, datatypes, names)
        # end if

        output.append("")
        output.append(format_str.format(*column_names))
        output.append(separator_format_str.format("-"))

        for row_of_data in rows_of_data:
            output.append(format_str.format(*row_of_data))
        # end for

        return output
    # end def format_record

    def get_offsets_sizes(self):
        """Wrapper function to get formatted offset and size column values"""

        offset = 0
        offsets = list()
        sizes = list()

        for field in self.record._fields_:
            (offset, new_offsets, new_sizes) = \
                self.build_offsets_sizes(offset, field)

            offsets.extend(new_offsets)
            sizes.extend(new_sizes)
        # end for

        return (offsets, sizes)
    # end def get_offsets_sizes

    def build_offsets_sizes(self, offset, field):
        """Recursive function to build formatted offset and size columns"""

        (fname, field) = field

        offsets = list()
        sizes = list()
        offset_base = self.offset_base

        offset_str = "{{0:{0}}}".format(offset_base)
        bit_offset_str = "{{0:{0}}}:{{1:{0}}}".format(offset_base, offset_base)
        size_str = "{{0:{0}}}".format(self.size_base)

        if not hasattr(field, "_decoder_"):  # If it's not a BitType...
            offsets.append(offset_str.format(offset))
            sizes.append(size_str.format(field._size_))
        # end if

        if hasattr(field, "_format_"):  # If it is a Basic...
            if hasattr(field, "_decoder_"):
                bit_offset = 0
                for (bname, bit) in field._fields_:
                    offsets.append(bit_offset_str.format(offset, bit_offset))
                    sizes.append(bit._size_)

                    bit_offset += bit._size_
                # end for
            # end if

            offset += field._size_
        else:
            for nested_field in field._fields_:
                (offset, new_offsets, new_sizes) = \
                    self.build_offsets_sizes(offset, nested_field)

                offsets.extend(new_offsets)
                sizes.extend(new_sizes)
            # end for
        # end if

        return (offset, offsets, sizes)
    # end def build_offsets_sizes

    def get_datatypes_names(self):
        """Wrapper function to get formatted datatypes and field names"""

        datatypes = list()
        names = list()

        for field in self.record._fields_:
            (new_datatypes, new_names) = self.build_datatypes_names("", field)

            datatypes.extend(new_datatypes)
            names.extend(new_names)
        # end for

        return (datatypes, names)
    # end def get_datatypes_names

    def build_datatypes_names(self, parent_name, field):
        """Recursive function to build formatted data types and field names"""

        (fname, field) = field

        datatypes = list()
        names = list()
        format_field_name = self.format_field_name
        get_field_datatype = self.get_field_datatype

        if not hasattr(field, "_decoder_"): 
            name = format_field_name(parent_name, fname, field)
            names.append(name)
            datatypes.append(get_field_datatype(field))
        # end if

        if hasattr(field, "_format_"):  # If it is a Basic
            if hasattr(field, "_decoder_"):  # If it is a BitType
                for (bname, bit) in field._fields_:
                    datatypes.append("bit")
                    names.append(format_field_name(parent_name, bname, bit))
                # end for
            # end if
        else:
            if isinstance(field, array):
                for (index, array_field) in enumerate(field._fields_):
                    parent_name = "{0}[{1}]".format(name, index)

                    (new_datatypes, new_names) = \
                        self.build_datatypes_names(parent_name, array_field)

                    datatypes.extend(new_datatypes)
                    names.extend(new_names)
                # end for
            else:
                for record_field in field._fields_:
                    (new_datatypes, new_names) = \
                        self.build_datatypes_names(name, record_field)

                    datatypes.extend(new_datatypes)
                    names.extend(new_names)
                # end for
            # end if
        # end if

        return (datatypes, names)
    # end def build_datatypes_names

    def format_field_name(self, parent_name, field_name, field):
        """Function to format a field name"""

        if parent_name and field_name:
            return ".".join([parent_name, field_name])
        elif field_name:
            return field_name
        else:
            return parent_name
        # end if
    # end def format_field_name

    def get_field_datatype(self, field):
        """Function to format a field datatype"""

        datatype = "(no datatype)"

        if hasattr(field, "_format_"):  # If it is a Basic
            if hasattr(field, "_decoder_"):  # If it is a BitType
                datatype = "(bit field, {0} fields)".format(
                    len(field._fields_)
                )
            else:
                if isclass(field):
                    datatype = field.__name__
                else:
                    datatype = field.__class__.__name__
                # end if
            # end if
        elif isinstance(field, array):
            datatype = "(array, {0} elements)".format(len(field._fields_))
        else:
            if isclass(field):
                datatype = "{0} (record)".format(field.__name__)
            else:
                datatype = "{0} (record)".format(field.__class__.__name__)
            # end if
        # end if

        return datatype
    # end def get_field_datatype

    def get_formatted_values(self):
        """Wrapper function to get a formatted list of extracted values"""

        formatted_values = list()

        extractor = Extractor(self.record)
        values = list(extractor.extract_partial(data))
        value_count = len(values)

        if hasattr(self.record, "_fields_"):
            field_count = self.calc_field_count(self.record)
        else:
            field_count = 1
        # end if

        if value_count < field_count:
            values.extend(["(NULL)"] * (field_count - value_count))
        # end if

        values_iter = iter(values)

        for field in self.record._fields_:
            new_formatted_values = \
                self.build_formatted_values(field, values_iter)

            formatted_values.extend(new_formatted_values)
        # end for

        return (field_count, value_count, formatted_values)
    # end def get_formatted_values

    def calc_field_count(self, field):
        """Recursive function to calculate total number of fields"""

        if hasattr(field, "_format_"):  # If it is a Basic
            if hasattr(field, "_decoder_"):  # If it is a BitType
                return len(field._fields_)
            # end if

            return 1
        else:
            field_count = 0

            for (fname, nested_field) in field._fields_:
                new_field_count = self.calc_field_count(nested_field)
                field_count += new_field_count
            # end for

            return field_count
        # end if
    # end def build_field_count

    def build_formatted_values(self, field, values_iter):
        """Recursive function to build a formatted list of values"""

        formatted_values = list()

        (fname, field) = field

        if hasattr(field, "_format_"):  # If it is a Basic
            if hasattr(field, "_decoder_"):  # If it is a BitType
                for bit in field._fields_:
                    value = values_iter.__next__()
                    formatted_values.append(self.format_value(value))
                # end for
            else:
                value = values_iter.__next__()
                formatted_values.append(self.format_value(value))
            # end if
        else:
            formatted_values.append("")

            for nested_field in field._fields_:
                new_formatted_values = \
                    self.build_formatted_values(nested_field, values_iter)

                formatted_values.extend(new_formatted_values)
            # end for
        # end if

        return formatted_values
    # end def build_formatted_values

    def format_value(self, value):
        """Formats a value as a string"""

        if isinstance(value, int):
            value_str = "{{0:{0}}}".format(self.value_base)
            return value_str.format(value)
        else:
            return str(value)
        # end if
    # end def format_value
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

parser = OptionParser()
parser.set_usage("%prog [options] MODULE RECORD [file]")

parser.add_option(
    "-o", "--offset-base", action="store", dest="offset_base", default="d",
    help="Specify the numeric base for the offset column "
    "([b]inary, [d]ecimal, [o]ctal, or he[x|X]) (def: %default)",
    choices=("b", "d", "o", "x", "X"), metavar="BASE"
)

parser.add_option(
    "-v", "--value-base", action="store", dest="value_base", default="d",
    help="Specify the numeric base for the values column "
    "([b]inary, [d]ecimal, [o]ctal, or he[x|X]) (def: %default)",
    choices=("b", "d", "o", "x", "X"), metavar="BASE"
)

parser.add_option(
    "-s", "--size-base", action="store", dest="size_base", default="d",
    help="Specify numeric base for the size column "
    "([b]inary, [d]ecimal, [o]ctal, or he[x|X]) (def: %default)",
    choices=("b", "d", "o", "x", "X"), metavar="BASE"
)

parser.add_option(
    "-e", "--extract", action="store_true", dest="extract", default=False,
    help="Extract values from [file]"
)

parser.add_option(
    "-a", "--absolute-import", action="store_true", dest="absolute_import",
    default=False, help="Imports MODULE as an absolute import (def: %default)"
)

parser.add_option(
    "-f", "--module-is-file", action="store_true", dest="module_is_file",
    default=False, help="Treats MODULE as a file (instead of a package) "
    "(def: %default)"
)

(options, args) = parser.parse_args()

if len(args) < 2:
    parser.error("you must specify both MODULE and RECORD")
# end if

if options.module_is_file and options.absolute_import:
    parser.error("you can't specify both -f and -a")
# end if

offset_base = options.offset_base
value_base = options.value_base
size_base = options.size_base

if options.extract:
    if len(args) == 2:
        filename = "--stdin--"
        data = sys.stdin.buffer.read()
    else:
        filename = args[2]
        data = raw.open(filename).read()
    # end if
else:
    data = None
# end if

(module_name, record_name) = args[0:2]

if options.module_is_file:
    module = imp.load_source("module", module_name)
else:
    if not options.absolute_import:
        module_name = ".".join(["lf", module_name, "datatypes"])
    # end if

    __import__(module_name)
    module = sys.modules[module_name]
# end if

record = getattr(module, record_name)
if not issubclass(record, Extractable):
    parser.error("Only extractable classes can be printed/extracted")
# end if

output = list()
output.append("Data Structure Print and Extract")
output.append("")
output.append("Module: {0}".format(module_name))
output.append("Record: {0}".format(record_name))
output.append("Size of record: {0} bytes".format(record._size_))

if options.extract:
    output.append("Read {0} bytes from {1}".format(len(data), filename))
# end if

bases = (offset_base, size_base, value_base)
formatter = RecordFormatter(record, bases, data)

output.extend(formatter.format_record())

print("\n".join(output))
