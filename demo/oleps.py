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

"""Tool to demonstrate some of the capabilities in LibForensics"""

# stdlib imports
import sys
from optparse import OptionParser
from datetime import datetime

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.objects import HRESULT
from lf.win.codepage import add_codecs
from lf.win.ole import varenum
from lf.win.ole.cfb import CompoundFile
from lf.win.ole.ps import (
    VT_EMPTY, VT_NULL, VT_I2, VT_I4, VT_R4, VT_R8, VT_CY, VT_DATE, VT_LPSTR,
    VT_ERROR, VT_BOOL, VT_UI2, VT_DECIMAL, VT_I1, VT_UI1, VT_UI4, VT_I8,
    VT_UI8, VT_INT, VT_UINT, VT_BSTR, VT_LPWSTR, VT_FILETIME, VT_BLOB,
    VT_STREAM, VT_STORAGE, VT_STREAMED_OBJECT, VT_STORED_OBJECT,
    VT_BLOB_OBJECT, VT_CF, VT_CLSID, VT_VERSIONED_STREAM, VT_ARRAY, VT_VECTOR,

    Dictionary, PropertySetMetadata, PropertiesMetadata, Builder, Array,
    Vector, TypedPropertyValue, CURRENCY, CodePageString, DECIMAL, DATE,
    UnicodeString, BLOB, IndirectPropertyName, GUID, VersionedStream, FILETIME,
    ClipboardData, Packet
)
from lf.win.ole.ps.consts import DICTIONARY_PROPERTY_IDENTIFIER

# module globals
STATIC_NAMES = {  # Stuff that has a static name
    Dictionary: "Dictionary",
    VT_EMPTY: "VT_EMPTY",
    VT_NULL: "VT_NULL",
    VT_I2: "VT_I2",
    VT_I4: "VT_I4",
    VT_R4: "VT_R4",
    VT_R8: "VT_R8",
    VT_CY: "VT_CY",
    VT_DATE: "VT_DATE",
    VT_LPSTR: "VT_LPSTR",
    VT_ERROR: "VT_ERROR",
    VT_BOOL: "VT_BOOL",
    VT_UI2: "VT_UI2",
    VT_DECIMAL: "VT_DECIMAL",
    VT_I1: "VT_I1",
    VT_UI1: "VT_UI1",
    VT_UI4: "VT_UI4",
    VT_I8: "VT_I8",
    VT_UI8: "VT_UI8",
    VT_INT: "VT_INT",
    VT_UINT: "VT_UINT",
    VT_BSTR: "VT_BSTR",
    VT_LPWSTR: "VT_LPWSTR",
    VT_FILETIME: "VT_FILETIME",
    VT_BLOB: "VT_BLOB",
    VT_STREAM: "VT_STREAM",
    VT_STORAGE: "VT_STORAGE",
    VT_STREAMED_OBJECT: "VT_STREAMED_OBJECT",
    VT_STORED_OBJECT: "VT_STORED_OBJECT",
    VT_BLOB_OBJECT: "VT_BLOB_OBJECT",
    VT_CF: "VT_CF",
    VT_CLSID: "VT_CLSID",
    VT_VERSIONED_STREAM: "VT_VERSIONED_STREAM",
    CURRENCY: "CURRENCY",
    DATE: "DATE",
    CodePageString: "CodePageString",
    DECIMAL: "DECIMAL",
    IndirectPropertyName: "IndirectPropertyName",
    UnicodeString: "UnicodeString",
    FILETIME: "FILETIME",
    BLOB: "BLOB",
    ClipboardData: "ClipboardData",
    GUID: "GUID",
    VersionedStream: "VersionedStream",
    HRESULT: "HRESULT"
}

SIMPLE_TYPES = [  # Stuff we can process easily
    CURRENCY, CodePageString, DECIMAL, UnicodeString, BLOB,
    IndirectPropertyName, GUID, VersionedStream
]

TPV_TYPES = {
    varenum.VT_EMPTY: VT_EMPTY,
    varenum.VT_NULL: VT_NULL,
    varenum.VT_I2: VT_I2,
    varenum.VT_I4: VT_I4,
    varenum.VT_R4: VT_R4,
    varenum.VT_R8: VT_R8,
    varenum.VT_CY: VT_CY,
    varenum.VT_DATE: VT_DATE,
    varenum.VT_BSTR: VT_BSTR,
    varenum.VT_ERROR: VT_ERROR,
    varenum.VT_BOOL: VT_BOOL,
    varenum.VT_DECIMAL: VT_DECIMAL,
    varenum.VT_I1: VT_I1,
    varenum.VT_UI1: VT_UI1,
    varenum.VT_UI2: VT_UI2,
    varenum.VT_UI4: VT_UI4,
    varenum.VT_I8: VT_I8,
    varenum.VT_UI8: VT_UI8,
    varenum.VT_INT: VT_INT,
    varenum.VT_UINT: VT_UINT,
    varenum.VT_LPSTR: VT_LPSTR,
    varenum.VT_LPWSTR: VT_LPWSTR,
    varenum.VT_FILETIME: VT_FILETIME,
    varenum.VT_BLOB: VT_BLOB,
    varenum.VT_STREAM: VT_STREAM,
    varenum.VT_STORAGE: VT_STORAGE,
    varenum.VT_STREAMED_OBJECT: VT_STREAMED_OBJECT,
    varenum.VT_STORED_OBJECT: VT_STORED_OBJECT,
    varenum.VT_BLOB_OBJECT: VT_BLOB_OBJECT,
    varenum.VT_CF: VT_CF,
    varenum.VT_CLSID: VT_CLSID,
    varenum.VT_VERSIONED_STREAM: VT_VERSIONED_STREAM
}


# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)

__docformat__ = "restructuredtext en"
__all__ = [
    "VER_MAJOR", "VER_MINOR", "main", "format_output", "format_property_info",
    "format_value", "format_sequence"
]

add_codecs()

def format_packet_type(packet):
    """Formats the packet type"""

    if packet.__class__ in STATIC_NAMES:
        return STATIC_NAMES[packet.__class__]
    elif isinstance(packet, VT_ARRAY):
        scalar_type = packet.type & (~varenum.VT_ARRAY)
        if scalar_type in TPV_TYPES:
            type_str = STATIC_NAMES[TPV_TYPES[scalar_type]]
        elif scalar_type == varenum.VT_VARIANT:
            type_str = "VT_VARIANT"
        else:
            type_str = "Unknown"
        # end if

        return "VT_ARRAY | {0}".format(type_str)
    elif isinstance(packet, VT_VECTOR):
        scalar_type = packet.type & (~varenum.VT_VECTOR)
        if scalar_type in TPV_TYPES:
            type_str = STATIC_NAMES[TPV_TYPES[scalar_type]]
        elif scalar_type == varenum.VT_VARIANT:
            type_str = "VT_VARIANT"
        else:
            type_str = "Unknown"
        # end if

        return "VT_VECTOR | {0}".format(type_str)
    else:
        return "Unknown"
    # end if
# end def format_packet_type

def format_property_info(property, depth=1):
    """Formats any property specific information"""

    output = list()
    spacer = " " * (depth * 2)

    if isinstance(property, VT_ARRAY):
        value = property.value
        output.append("{0}Scalar type: {1}".format(spacer, value.scalar_type))
        output.append("{0}Number of dimensions: {1}".format(
            spacer, value.dimension_count
        ))
        for (index, dim) in enumerate(value.dimensions):
            output.append(
                "{0}Dimension {1}:  Size: {2},  IndexOffset: {3}".format(
                    spacer, index, dim[0], dim[1]
                )
            )
        # end for
    elif isinstance(property, VT_VECTOR):
        output.append("{0}Scalar count: {1}".format(
            spacer, property.value.scalar_count
        ))
    # end if

    return output
# end def format_property_info

def format_sequence(sequence, depth=2):
    """Formats a sequence (list) for output"""

    spacer = " " * (depth * 2)
    output = list()

    if isinstance(sequence[0], Packet):
        for element in sequence:
            type_str = format_packet_type(element)

            if isinstance(element, TypedPropertyValue):
                output.append("{0}Type: {1} (0x{2:X})".format(
                    spacer, type_str, element.type
                ))
            else:
                output.append("{0}Type: {1}".format(spacer, type_str))
            # end if

            value_output = format_value(element.value, depth+1)

            output.append("{0}Size: {1} bytes".format(spacer, element.size))

            if len(value_output) == 1:
                output.append("{0}Value: {1}".format(spacer, value_output[0]))
            else:
                output.append("{0}Value:".format(spacer))
                output.extend(value_output)
            # end if

            output.append("")
        # end for
    else:
        output = [str(element) for element in sequence]
        output = ", ".join(output)
    # end if

    return output
# end def format_sequence

def format_value(value, depth=2):
    """Formats a value for output"""

    output = list()
    spacer = " " * (depth * 2)

    if value.__class__ in SIMPLE_TYPES:
        output.append(str(value.value))
    elif isinstance(value, HRESULT):
        spacer = "".join([spacer, "  "])
        output.append("{0}Severity bit: {1}".format(spacer, value.s))
        output.append("{0}Reserved bit: {1}".format(spacer, value.r))
        output.append("{0}Customer bit: {1}".format(spacer, value.c))
        output.append("{0}NTSTATUS bit: {1}".format(spacer, value.n))
        output.append("{0}X bit: {1}".format(spacer, value.x))
        output.append("{0}Facility: {1}".format(spacer, value.facility))
        output.append("{0}Code: {1}".format(spacer, value.code))
    elif isinstance(value, Array) or isinstance(value, Vector):
        output.extend(format_sequence(value.value, depth))
    elif isinstance(value, DATE):
        if isinstance(value.value, datetime):
            output.append(str(value.value.isoformat(" ")))
        else:
            output.append(str(value.value))
        # end if
    elif isinstance(value, ClipboardData):
        output.append("{0}Format: {1}".format(spacer, value.format))
        output.append("{0}Data: {1}".format(spacer, value.data))
    elif isinstance(value, datetime):
        output.append(str(value.isoformat(" ")))
    elif isinstance(value, dict):
        for (pid, name) in value.items():
            output.append("{0}{1}: {2}".format(spacer, pid, name))
        # end for
    elif (value is None):
        output.append("<no value>")
    else:
        output.append(str(value))
    # end if

    return output
# end def format_value

def format_property(pid, property, property_offset, dictionary):
    """Formats a property for output"""

    output = list()

    type_str = format_packet_type(property)

    if pid in dictionary:
        name_str = dictionary[pid]
    else:
        name_str = "<not found>"
    # end if

    output.append("Property: {0}".format(pid))
    if pid != DICTIONARY_PROPERTY_IDENTIFIER:
        output.append("  Type: {0} (0x{1:X})".format(type_str, property.type))
    else:
        output.append("  Type: Dictionary")
    # end if
    output.append("  Offset: {0}".format(property_offset))
    output.append("  Size: {0} bytes".format(property.size))
    output.append("  Name: {0}".format(name_str))
    output.extend(format_property_info(property, 1))

    value_output = format_value(property.value, 2)

    if len(value_output) == 1:
        output.append("  Value: {0}".format(value_output[0]))
    else:
        output.append("  Value:")
        output.extend(value_output)
    # end if

    return output
# end def format_property

def format_output(stream, options):
    """Formats the output"""

    output = list()

    pss = Builder.build(stream)

    output.append("Property Set Stream Header")
    output.append("--------------------------")
    output.append("Byte order: 0x{0:X}".format(pss.byte_order))
    output.append("Version: {0}".format(pss.version))
    output.append("Sys. id: {0}".format(pss.sys_id))
    output.append("CLSID: {0}".format(pss.clsid))
    output.append("Number of property sets: {0}".format(
        pss.property_set_count
    ))
    output.append("Property set 0 FMTID: {0}".format(pss.fmtid0))
    output.append("Property set 0 offset: {0}".format(pss.offset0))
    if (pss.fmtid1 is not None) and (pss.offset1 is not None):
        output.append("Property set 1 FMTID: {0}".format(pss.fmtid1))
        output.append("Property set 1 offset: {0}".format(pss.offset1))
    # end if

    # First property set
    ps = pss.property_set_0
    offset = pss.offset0
    output.append("")
    output.append("Property Set 0")
    output.append("--------------")
    output.append("Header size: {0} bytes".format(ps.size))
    output.append("Number of pid/offset pairs: {0}".format(ps.pair_count))
    output.append("")

    if DICTIONARY_PROPERTY_IDENTIFIER in ps.properties:
        dictionary = ps.properties[DICTIONARY_PROPERTY_IDENTIFIER].value
    else:
        dictionary = dict()
    # end if

    for (pid, property) in ps.properties.items():
        property_offset = offset + ps.pids_offsets[pid]
        output.extend(format_property(
            pid, property, property_offset, dictionary
        ))
        output.append("")
    # end for

    if (pss.fmtid1 is None) or (pss.offset1 is None):
        return output
    # end if

    # Second property set
    ps = pss.property_set_1
    offset = pss.offset1
    output.append("")
    output.append("Property Set 1")
    output.append("--------------")
    output.append("Header size: {0} bytes".format(ps.size))
    output.append("Number of pid/offset pairs: {0}".format(ps.pair_count))
    output.append("")

    if DICTIONARY_PROPERTY_IDENTIFIER in ps.properties:
        dictionary = ps.properties[DICTIONARY_PROPERTY_IDENTIFIER].value
    else:
        dictionary = dict()
    # end if

    for (pid, property) in ps.properties.items():
        property_offset = offset + ps.pids_offsets[pid]
        output.extend(format_property(
            pid, property, property_offset, dictionary
        ))
        output.append("")
    # end for

    return output
# end def format_output

def main():
    usage = "%prog [options] -i sid olefile"
    description = "\n".join([
        "Displays OLE property sets from a stream in an OLE compound file.",
        "",
        "If file is '-' then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-r",
        action="store_true",
        dest="raw_stream",
        help="Input is just a stream (not an OLE compound file)",
        default=False
    )

    parser.add_option(
        "-i",
        action="store",
        dest="sid",
        help="Stream to analyze",
    )

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("You must specify an olefile (or '-' for stdin)")
    # end if

    if (not options.raw_stream) and (not options.sid):
        parser.error("You must specify either -i or -r")
    # end if

    if args[0] == "-":
        input_stream = ByteIStream(sys.stdin.buffer.read())
    else:
        input_stream = RawIStream(args[0])
    # end if

    if options.raw_stream:
        output = format_output(input_stream, options)
    else:
        cfb = CompoundFile(input_stream)
        sid = int(options.sid)

        if sid not in cfb.dir_entries:
            print("Can't find sid {0}".format(sid), file=sys.stderr)
            sys.exit(-2)
        # end if

        output = format_output(cfb.get_stream(sid), options)
    # end if

    print("\n".join(output))
# end def main

if __name__ == "__main__":
    main()
# end if
