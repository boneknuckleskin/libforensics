Prints data structures to the screen, and extracts values

$ python3.1 dspe.py -h
Usage: dspe.py [options] MODULE RECORD [file]

Options:
  -h, --help            show this help message and exit
  -o OFFSET_BASE, --offset-base=BASE
                        Specify the numeric base for the offset column
                        ([b]inary, [d]ecimal, [o]ctal, or he[x|X]) (def: X)
  -v VALUE_BASE, --value-base=BASE
                        Specify the numeric base for the values column
                        ([b]inary, [d]ecimal, [o]ctal, or he[x|X]) (def: X)
  -s SIZE_BASE, --size-base=BASE
                        Specify numeric base for the size column ([b]inary,
                        [d]ecimal, [o]ctal, or he[x|X]) (def: X)
  -e, --extract         Extract values from [file]
  -a, --absolute-import
                        Imports MODULE as an absolute import (def: False)
  -f, --module-is-file  Treats MODULE as a file (instead of a package) (def:
                        False)

In the framework, all data structures are defined in the file structs.py (in
the various package directories).  For example, the module that contains the
data structures for Microsoft Word would be: lf.apps.msoffice.word.structs.  If
you don't specify -a, the leading "lf" and trailing "structs" are implied (so
you can just type apps.msoffice.word).

Note: If you specify extract (-e) and don't specify an input file, input is
read from stdin.  Output is written to stdout.

Examples:

1) Display the structure of an INFO2 deleted file entry.

$ python3.1 dspe.py windows.shell.recyclebin Item
Data Structure Print and Extract

Module: lf.windows.shell.recyclebin.structs
Data structure: Item
Size of data structure: 800 bytes

Item Offset  Size Type                      Field                    
---- ------- ---- ------------------------- -------------------------
0    0       260  raw                       name_asc                 
1    260     4    DWORD                     index                    
2    264     4    DWORD                     drive_num                
3    268     8    FILETIME                  dtime                    
4    276     4    DWORD                     phys_size                
5    280     520  raw                       name_uni                 


2) Display the structure (and extract values for) the header structure in a
an OLE compound file (structured storage).
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

$ python3.1 dspe.py -e -o X -s X -v X windows.ole.compoundfile Header blair.doc
Data Structure Print and Extract

Module: lf.windows.ole.compoundfile.structs
Data structure: Header
Size of data structure: 512 bytes
Read 65024 bytes from blair.doc
Extracted 136 of 136 total fields

Item Offset  Size Type                      Field                     Value
---- ------- ---- ------------------------- ------------------------- -----
0    0       8    raw                       sig                       b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
1    8       10   CLSID (struct)            clsid                          
2    8       4    DWORD                     clsid.data1               0    
3    C       2    WORD                      clsid.data2               0    
4    E       2    WORD                      clsid.data3               0    
5    10      8    (array, 8 elements)       clsid.data4                    
6    10      1    BYTE                      clsid.data4[0]            0    
7    11      1    BYTE                      clsid.data4[1]            0    
8    12      1    BYTE                      clsid.data4[2]            0    
9    13      1    BYTE                      clsid.data4[3]            0    
10   14      1    BYTE                      clsid.data4[4]            0    
11   15      1    BYTE                      clsid.data4[5]            0    
12   16      1    BYTE                      clsid.data4[6]            0    
13   17      1    BYTE                      clsid.data4[7]            0    
14   18      2    USHORT                    ver_minor                 3E   
15   1A      2    USHORT                    ver_major                 3    
[... output truncated ...]


3) Display the header structure, and extract values, for the File Info Block
from a Microsoft Word document. (the values are in hex)
(image from SOTM24 http://old.honeynet.org/scans/scan24/)

$ icat -r image 5 | dd bs=512 skip=1 count=2 | python3.1 dspe.py -e -v X apps.msoffice.word FibHeader
Data Structure Print and Extract

Module: lf.apps.msoffice.word.structs
Data structure: FibHeader
Size of data structure: 32 bytes
Read 1024 bytes from --stdin--
Extracted 31 of 31 total fields

Item Offset  Size Type                      Field                     Value
---- ------- ---- ------------------------- ------------------------- -----
0    0       2    UINT16                    wIdent                    A5EC 
1    2       2    UINT16                    nFib                      C1   
2    4       2    UINT16                    nProduct                  4035 
3    6       2    UINT16                    lid                       409  
4    8       2    UINT16                    pnNext                    0    
5    10:0    1    bit                       dot                       0    
6    10:1    1    bit                       glsy                      0    
7    10:2    1    bit                       complex                   0    
8    10:3    1    bit                       hasPic                    0    
9    10:4    4    bit                       quickSaves                F    
10   10:8    1    bit                       encrypted                 0    
11   10:9    1    bit                       whichTblStm               1    
[... output truncated ...]
