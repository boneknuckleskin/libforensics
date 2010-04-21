Dumps information about record data types (data structures).


Usage:
------

$ python3.1 recdump.py -h
Usage: recdump.py [options] RECORD [file]

Dumps information about record data types (data structures). By specifying a
file (or '-' for stdin) data from the file (or stdin) is extracted and printed
inline with the data structure

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -r MAX_DEPTH          Maximum depth for recursion (-1 is unlimited)
  -f FILE MODNAME, --file=FILE MODNAME
                        Load RECORD from FILE using MODNAME as the module name

  Formatting Options:
    The options are used for formatting output of numbers.  Valid values
    for BASE are: [b]inary, [d]ecial, [o]ctal, and he[x|X].

    -o BASE             The base for offsets (default: X)
    -d BASE             The base for data (default: X)
    -s BASE             The base for sizes (default: d)
    -i BASE             The base for indices (default: d)


Examples:
---------

1) Display the structure of an INFO2 deleted file entry.

$ python3.1 recdump.py lf.win.shell.recyclebin.dtypes.INFO2Item
File: n/a
Module: lf.win.shell.recyclebin.dtypes
Record: INFO2Item
Size of record: 800 bytes
Data: n/a

0000:     name_asc                   ; raw (260)
0104:     id                         ; DWORD (4)
0108:     drive_num                  ; DWORD (4)
010C:     dtime                      ; FILETIME_LE (8)
0114:     file_size                  ; DWORD (4)
0118:     name_uni                   ; raw (520)


2) Display the structure, and extract values for a PropertySetStreamHeader in
an OLE compound file.
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

$ python3.1 olecat.py blair.doc 3 | python3.1 recdump.py -r 2 \
lf.win.ole.ps.dtypes.PropertySetStreamHeader -
File: n/a
Module: lf.win.ole.ps.dtypes
Record: PropertySetStreamHeader
Size of record: 48 bytes
Data: 4096 bytes from --stdin--

0000:     byte_order                 ; WORD (2), data = 0xFFFE
0002:     version                    ; WORD (2), data = 0x0
0004:     sys_id                     ; raw (4)
0008:     clsid                      ; CLSID_LE (16)
0008:       + data1                  ; DWORD (4), data = 0x0
000C:       + data2                  ; WORD (2), data = 0x0
000E:       + data3                  ; WORD (2), data = 0x0
0010:       + data4                  ; BYTE[8] (8)
0010:         + data4[0]             ; BYTE (1), data = 0x0
0011:         + data4[1]             ; BYTE (1), data = 0x0
0012:         + data4[2]             ; BYTE (1), data = 0x0
0013:         + data4[3]             ; BYTE (1), data = 0x0
0014:         + data4[4]             ; BYTE (1), data = 0x0
0015:         + data4[5]             ; BYTE (1), data = 0x0
0016:         + data4[6]             ; BYTE (1), data = 0x0
0017:         + data4[7]             ; BYTE (1), data = 0x0
0018:     property_set_count         ; DWORD (4), data = 0x1
001C:     fmtid0                     ; FMTID (16)
001C:       + data1                  ; DWORD (4), data = 0xF29F85E0
0020:       + data2                  ; WORD (2), data = 0x4FF9
0022:       + data3                  ; WORD (2), data = 0x1068
0024:       + data4                  ; BYTE[8] (8)
0024:         + data4[0]             ; BYTE (1), data = 0xAB
0025:         + data4[1]             ; BYTE (1), data = 0x91
0026:         + data4[2]             ; BYTE (1), data = 0x8
0027:         + data4[3]             ; BYTE (1), data = 0x0
0028:         + data4[4]             ; BYTE (1), data = 0x2B
0029:         + data4[5]             ; BYTE (1), data = 0x27
002A:         + data4[6]             ; BYTE (1), data = 0xB3
002B:         + data4[7]             ; BYTE (1), data = 0xD9
002C:     offset0                    ; DWORD (4), data = 0x30


3) Display and extract values for an HRESULT data type (little endian)

$ echo -ne "\x64\x53\x64\x53" | python3.1 recdump.py lf.win.dtypes.HRESULT_LE -
File: n/a
Module: lf.win.dtypes
Record: HRESULT_LE
Size of record: 4 bytes
Data: 4 bytes from --stdin--

0000:00:  code                       ; bits (16), data = 0x5364
0002:00:  facility                   ; bits (11), data = 0x364
0003:03:  x                          ; bit (1), data = 0x0
0003:04:  n                          ; bit (1), data = 0x1
0003:05:  c                          ; bit (1), data = 0x0
0003:06:  r                          ; bit (1), data = 0x1
0003:07:  s                          ; bit (1), data = 0x0
