Displays OLE property sets from a stream in an OLE compound file.


Usage:
------

$ python3.1 oleps.py -h
Usage: oleps.py [options] -i sid olefile

Displays OLE property sets from a stream in an OLE compound file.  If file is
'-' then stdin is read.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -r          Input is just a stream (not an OLE compound file)
  -i SID      Stream to analyze


Examples:
---------

(sample.doc is found under the unittests/data/doc directory)

1) Extract the property set(s) from the SummaryInformation stream.

$ python3.1 oleps.py -i 39 sample.doc
Property Set Stream Header
--------------------------
Byte order: 0xFFFE
Version: 0
Sys. id: b'\x05\x01\x02\x00'
CLSID: 00000000-0000-0000-0000-000000000000
Number of property sets: 1
Property set 0 FMTID: f29f85e0-4ff9-1068-ab91-08002b27b3d9
Property set 0 offset: 48

Property Set 0
--------------
Header size: 153200 bytes
Number of pid/offset pairs: 18

Property: 1
  Type: VT_I2 (0x2)
  Offset: 200
  Size: 8 bytes
  Name: <not found>
  Value: 1252
[... output truncated ...]


2) Use olecat.py to extract the DocumentSummaryInformation stream and then
extract the property set(s).

$ python3.1 olecat.py sample.doc 40 | python3.1 oleps.py -r -
Property Set Stream Header
--------------------------
Byte order: 0xFFFE
Version: 0
Sys. id: b'\x05\x01\x02\x00'
CLSID: 00000000-0000-0000-0000-000000000000
Number of property sets: 2
Property set 0 FMTID: d5cdd502-2e9c-101b-9397-08002b2cf9ae
Property set 0 offset: 68
Property set 1 FMTID: d5cdd505-2e9c-101b-9397-08002b2cf9ae
Property set 1 offset: 504

Property Set 0
--------------
Header size: 436 bytes
Number of pid/offset pairs: 15

Property: 1
  Type: VT_I2 (0x2)
  Offset: 196
  Size: 8 bytes
  Name: <not found>
  Value: 1252
[... output truncated ...]
