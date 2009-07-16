# Prints and extracts data structures (Data Structure Print and Extract)

import sys
import imp
from optparse import OptionParser
from itertools import count

from lf.datastruct import Extractor
from lf.datastruct.field import (
    bit, Bits, DataStruct, Composite, array, Primitive
)
from lf.io import raw

class StructureFormatter():
    """
    Formats a data structure for human consumption.

    .. attribute:: offset_base

        The format character for the offset column.

    .. attribute:: size_base

        The format character for the size column.

    .. attribute:: value_base

        The format character for the value column.

    .. attribute:: datastruct

        The data structure to format.

    .. attribute:: data

        If not None, binary data to extract values from.
    """

    def __init__(self, datastruct, bases, data=None):
        """
        Initializes a StructureFormatter object.

        :parameters:
            datastruct
                The data structure to format.

            bases
                A tuple of (offset_base, size_base_, value_base)

            data
                A bytes object of data to extract.
        """

        self.datastruct = datastruct
        self.offset_base = bases[0]
        self.size_base = bases[1]
        self.value_base = bases[2]
        self.data = data
    # end def __init__

    def format_structure(self):
        """
        Formats a structure for printing.

        :rtype: list
        :returns: A list of strings, suitable for printing
        """

        datastruct = self.datastruct
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
    # end def format_structure

    def get_offsets_sizes(self):
        """Wrapper function to get formatted offset and size column values"""

        offset = 0
        offsets = list()
        sizes = list()

        for field in self.datastruct.fields:
            (offset, new_offsets, new_sizes) = \
                self.build_offsets_sizes(offset, field)

            offsets.extend(new_offsets)
            sizes.extend(new_sizes)
        # end for

        return (offsets, sizes)
    # end def get_offsets_sizes

    def build_offsets_sizes(self, offset, field):
        """Recursive function to build formatted offset and size columns"""

        offsets = list()
        sizes = list()
        offset_base = self.offset_base

        offset_str = "{{0:{0}}}".format(offset_base)
        bit_offset_str = "{{0:{0}}}:{{1:{0}}}".format(offset_base, offset_base)
        size_str = "{{0:{0}}}".format(self.size_base)

        if not isinstance(field, Bits):
            offsets.append(offset_str.format(offset))
            sizes.append(size_str.format(field.size))
        # end if

        if isinstance(field, Primitive):
            if isinstance(field, Bits):
                bit_offset = 0
                for bit in field.bits:
                    offsets.append(bit_offset_str.format(offset, bit_offset))
                    sizes.append(bit.size)

                    bit_offset += bit.size
                # end for
            # end if

            offset += field.size
        else:
            for nested_field in field.fields:
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

        for field in self.datastruct.fields:
            (new_datatypes, new_names) = self.build_datatypes_names("", field)

            datatypes.extend(new_datatypes)
            names.extend(new_names)
        # end for

        return (datatypes, names)
    # end def get_datatypes_names

    def build_datatypes_names(self, parent_name, field):
        """Recursive function to build formatted data types and field names"""

        datatypes = list()
        names = list()
        get_field_name = self.get_field_name
        get_field_datatype = self.get_field_datatype

        if not isinstance(field, Bits):
            name = get_field_name(parent_name, field)
            names.append(name)
            datatypes.append(get_field_datatype(field))
        # end if

        if isinstance(field, Primitive):
            if isinstance(field, Bits):
                for bit in field.bits:
                    datatypes.append("bit")
                    names.append(get_field_name(parent_name, bit))
                # end for
            # end if
        else:
            if isinstance(field, array):
                for (index, array_field) in enumerate(field.fields):
                    parent_name = "{0}[{1}]".format(name, index)

                    (new_datatypes, new_names) = \
                        self.build_datatypes_names(parent_name, array_field)

                    datatypes.extend(new_datatypes)
                    names.extend(new_names)
                # end for
            else:
                for struct_field in field.fields:
                    (new_datatypes, new_names) = \
                        self.build_datatypes_names(name, struct_field)

                    datatypes.extend(new_datatypes)
                    names.extend(new_names)
                # end for
            # end if
        # end if

        return (datatypes, names)
    # end def build_datatypes_names

    def get_field_name(self, parent_name, field):
        """Function to format a field name"""

        field_name = field.name

        if parent_name and field_name:
            return ".".join([parent_name, field_name])
        elif field_name:
            return field_name
        else:
            return parent_name
        # end if
    # end def get_field_name

    def get_field_datatype(self, field):
        """Function to format a field datatype"""

        datatype = "(no datatype)"

        if isinstance(field, Primitive):
            if isinstance(field, Bits):
                datatype = "(bit field, {0} fields)".format(len(field.bits))
            else:
                datatype = field.__class__.__name__
            # end if
        elif isinstance(field, array):
            datatype = "(array, {0} elements)".format(len(field.fields))
        else:
            datatype = "{0} (struct)".format(field.__class__.__name__)
        # end if

        return datatype
    # end def get_field_datatype

    def get_formatted_values(self):
        """Wrapper function to get a formatted list of extracted values"""

        formatted_values = list()

        extractor = Extractor(self.datastruct)
        values = list(extractor.extract_partial(data))
        value_count = len(values)

        field_count = self.calc_field_count(self.datastruct)

        if value_count < field_count:
            values.extend(["(NULL)"] * (field_count - value_count))
        # end if

        values_iter = iter(values)

        for field in self.datastruct.fields:
            new_formatted_values = \
                self.build_formatted_values(field, values_iter)

            formatted_values.extend(new_formatted_values)
        # end for

        return (field_count, value_count, formatted_values)
    # end def get_formatted_values

    def calc_field_count(self, field):
        """Recursive function to calculate total number of fields"""

        if isinstance(field, Primitive):
            if isinstance(field, Bits):
                return len(field.bits)
            # end if

            return 1
        else:
            field_count = 0

            for nested_field in field.fields:
                new_field_count = self.calc_field_count(nested_field)
                field_count += new_field_count
            # end for

            return field_count
        # end if
    # end def build_field_count

    def build_formatted_values(self, field, values_iter):
        """Recursive function to build a formatted list of values"""

        formatted_values = list()

        if isinstance(field, Primitive):
            if isinstance(field, Bits):
                for bit in field.bits:
                    value = values_iter.__next__()
                    formatted_values.append(self.format_value(value))
                # end for
            else:
                value = values_iter.__next__()
                formatted_values.append(self.format_value(value))
            # end if
        else:
            formatted_values.append("")

            for nested_field in field.fields:
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
# end class StructureFormatter

def get_data_structure(module, name, absolute_import, module_is_file):
    """Retrieves a data structure object."""

    __import__(module_name)
    module = sys.modules[module_name]

    datastruct = getattr(module, struct_name)

    if not issubclass(datastruct, DataStruct):
        raise TypeError("{0} is not a data structure".format(datastruct))
    # end if

    return datastruct("")
# end def get_data_structure

parser = OptionParser()
parser.set_usage("%prog [options] MODULE STRUCT [file]")

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
    parser.error("you must specify both MODULE and STRUCT")
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

(module_name, struct_name) = args[0:2]

if options.module_is_file:
    module = imp.load_source("module", module_name)
else:
    if not options.absolute_import:
        module_name = ".".join(["lf", module_name, "structs"])
    # end if

    __import__(module_name)
    module = sys.modules[module_name]
# end if

datastruct = getattr(module, struct_name)
if not issubclass(datastruct, DataStruct):
    parser.error("Only data structures can be printed/extracted")
# end if

datastruct = datastruct()

output = list()
output.append("Data Structure Print and Extract")
output.append("")
output.append("Module: {0}".format(module_name))
output.append("Data structure: {0}".format(struct_name))
output.append("Size of data structure: {0} bytes".format(datastruct.size))

if options.extract:
    output.append("Read {0} bytes from {1}".format(len(data), filename))
# end if

bases = (offset_base, size_base, value_base)
formatter = StructureFormatter(datastruct, bases, data)

output.extend(formatter.format_structure())

print("\n".join(output))
