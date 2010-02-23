Displays statistics about a directory entry in an OLE compound file.


Usage:
------
$ python3.1 olestat.py -h
Usage: olestat.py olefile sid

Displays statistics about entries in an OLE compound file.  If file is '-'
then stdin is read.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit


Examples:
---------
(sample.doc is found under the unittests/data/doc directory)

1) Display statistics on the root entry

$ python3.1 olestat.py sample.doc 0
Stream id: 0
Name size: 22
Name: Root Entry
Type: STGTY_ROOT (0x5)
Color: Black (0x1)
Left stream id: STREAM_ID_NONE (0xFFFFFFFF)
Right stream id: STREAM_ID_NONE (0xFFFFFFFF)
Child stream id: 2
CLSID: 00020906-0000-0000-c000-000000000046
State: 0x0
Size: 20288

Timestamps:
Stream creation time: 1601-01-01 00:00:00
Stream modification time: 2010-02-02 06:46:38.627000

Normal sector(s):
13366, 13393, 16879, 16880, 16881, 16882, 16883, 16908
16909, 16910, 16911, 16912, 16913, 16915, 16916, 16918
16920, 16921, 16922, 16924, 16925, 16926, 16927, 16928
16929, 16930, 16931, 16932, 16933, 16934, 16935, 16936
16939, 17244, 17245, 17246, 17247, 17248, 17249, 17251


2) Display statistics about stream 40

$ python3.1 olestat.py sample.doc 40
Stream id: 40
Name size: 56
Name: \x05DocumentSummaryInformation
Type: STGTY_STREAM (0x2)
Color: Red (0x0)
Left stream id: STREAM_ID_NONE (0xFFFFFFFF)
Right stream id: STREAM_ID_NONE (0xFFFFFFFF)
Child stream id: STREAM_ID_NONE (0xFFFFFFFF)
CLSID: 00000000-0000-0000-0000-000000000000
State: 0x0
Size: 2572

Timestamps:
Stream creation time: 1601-01-01 00:00:00
Stream modification time: 1601-01-01 00:00:00

Mini stream sector(s):
264, 265, 266, 267, 268, 269, 270, 271
272, 273, 274, 275, 276, 277, 278, 279
280, 281, 282, 283, 284, 285, 286, 287
288, 289, 290, 291, 292, 293, 294, 295
296, 297, 298, 299, 300, 301, 302, 303
304


2) Display statistics about the OLE compound file header

$ cat sample.doc | python3.1 olestat.py - 48
Signature: b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
CLSID: 00000000-0000-0000-0000-000000000000
Major version: 3
Minor version: 62
Transaction signature #: 0
Byte order: 0xFFFE
Sector size: 512 bytes
Mini sector size: 64 bytes
Mini stream cutoff: 4096 bytes
Number of dir. sectors: 0
Dir. sector offset: 13363
Reserved value: b'\x00\x00\x00\x00\x00\x00'

FATs:
DI FAT sector offset: 13911
Number of DI FAT sectors: 1
Number of FAT sectors: 135
Mini FAT sector offset: 13365
Number of Mini FAT sectors: 3



3) Display statistics about the double indirect FAT (DI FAT)

$ python3.1 olestat.py sample.doc 49
Double Indirect FAT:

0: 13258
1: 13259
2: 13260
3: 13261
4: 13262
5: 13263
[... output truncated ...]


4) Display statistics about the FAT

$ python3.1 olestat.py sample.doc 50
FAT:

0-20 (21) -> EOC
21-13257 (13237) -> 13395
13258: 0xFFFFFFFD (FAT sector)
13259: 0xFFFFFFFD (FAT sector)
13260: 0xFFFFFFFD (FAT sector)
13261: 0xFFFFFFFD (FAT sector)
13262: 0xFFFFFFFD (FAT sector)
[... output truncated ...]



5) Displays statistics about the mini FAT

$ python3.1 olestat.py sample.doc 51
Mini FAT:

0-0 (1) -> EOC
1-2 (2) -> EOC
3-3 (1) -> EOC
4-7 (4) -> EOC
8-11 (4) -> EOC
[... output truncated ...]
