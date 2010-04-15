Decodes various timestamp formats.

$ python3.1 datedecoder.py  -h
Usage: datedecoder.py [options] timestamp

Decodes various timestamp formats.  If timestamp is '-' then stdin is read.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -b BASE, --base=BASE  The numeric base for the input (def: 16).  This only
                        applies when the input type is int.
  -m INPUT_MODE, --input-mode=INPUT_MODE
                        Set input to (binary, text) (def: text).  Binary is
                        only available when reading from stdin.
  -i TYPE, --input-type=TYPE
                        The data type of timestamp (int, float).  The default
                        for variant timestamps is float.  For all other
                        timestamps the default is int.
  -t TIMESTAMP_TYPE, --timestamp-type=TIMESTAMP_TYPE
                        The type of timestamp (filetime, unix|posix, dosdate,
                        dostime, variant).
  -e ENDIAN, --endian=ENDIAN
                        The byte order to use (big, little). (def: little).
                        This only applies when the input type is int.
  -s FORMAT, --format-str=FORMAT
                        The format string to print the decoded timestamp.  If
                        this is not specified ISO 8601 format is used.
  -f, --filetime        Implies -t filetime
  -u, --unix            Implies -t unix
  -p, --posix           Implies -t posix
  -d, --decimal         Implies -b 10
  -x, --hex             Implies -b 16


Examples:

1) Decoding a Windows FILETIME timestamp in little endian:

$ python3.1 datedecoder.py -f -e little 0x0008f4eb6f04ca01
2009-07-14 10:43:28


2) Decoding the same timestamp, as a decimal, in big endian, using a custom
format string:

$ python3.1 datedecoder.py -f -e big -d 128920418080000000 \
-s "%m/%d/%Y %H:%M:%S"
07/14/2009 10:43:28


3) Decoding a variant timestamp:
$ python3.1 datedecoder.py -t variant 3.25
1900-01-02 06:00:00


4) Decoding the same timestamp, this time it is a little endian decimal value:
$ python3.1 datedecoder.py -t variant -i int -d -e little 2624
1900-01-02 06:00:00


5) Decoding a binary timestamp, little endian embedded in a word document
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

$ dd if=blair.doc bs=512 skip=1 count=2 | dd bs=1 skip=850 count=8 | \
python3.1 datedecoder.py -f -m binary -
2+0 records in
[... output truncated ...]
2003-02-03 11:18:31.234000


6) Decoding the same timestamp, but with output copy/pasted from a hex editor
(text instead of binary)

$ dd if=blair.doc bs=512 skip=1 count=2 | dd bs=1 skip=850 count=8 | \
xxd -g 1 -u
2+0 records in
[... output truncated ...]
0000000: 20 52 96 FB 75 CB C2 01                           R..u...

$ python3.1 datedecoder.py -e little -f 20 52 96 FB 75 CB C2 01
2003-02-03 11:18:31.234000
