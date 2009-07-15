Decodes various timestamp formats.

$ python3.1 datedecoder.py  -h
Usage: datedecoder.py [options] [timestamp]

Options:
  -h, --help            show this help message and exit
  -b BASE, --base=BASE  The numeric base for the input (def: 16)
  -m MODE, --input-mode=MODE
                        Set input to (b, binary, t, text) (def: text) NOTE:
                        binary only applies when reading from stdin
  -t TYPE, --type=TYPE  The type of timestamp (filetime, unix, dos, dosdate,
                        dostime)
  -e ENDIAN, --endian=ENDIAN
                        The byte order to use (b, big, l, little) (def:
                        little)
  -s FORMAT_STR, --format-str=FORMAT_STR
                        The format string to print the decoded timestamp
  -f, --filetime        Implies -t filetime
  -u, --unix            Implies -t unix
  -d, --decimal         Implies -b 10
  -x, --hex             Implies -b 16

Note: If you don't specify a timestamp, input is read from stdin in the mode
specified with the -m option.  Output is written to stdout.

Examples:

1) Decoding a Windows FILETIME timestamp in little endian:

$ python3.1 datedecoder.py -f -e l 0x0008f4eb6f04ca01
07/14/2009 10:43:28


2) Decoding the same timestamp, as a decimal, in big endian:

$ python3.1 datedecoder.py -f -e b -d 128920418080000000
07/14/2009 10:43:28


3) Decoding a binary timestamp, little endian embedded in a word document
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

$ dd if=blair.doc bs=512 skip=1 count=2 | dd bs=1 skip=850 count=8 |
python3.1 datedecoder.py -m b -e l -f
2+0 records in
[... output truncated ...]
02/03/2003 11:18:31


4) Decoding the same timestamp, but with output copy/pasted from a hex editor
(text instead of binary)

$ dd if=blair.doc bs=512 skip=1 count=2 | dd bs=1 skip=850 count=8 |
xxd -g 1 -u
2+0 records in
[... output truncated ...]
0000000: 20 52 96 FB 75 CB C2 01                           R..u...

$ python3.1 datedecoder.py -e l -f 20 52 96 FB 75 CB C2 01
02/03/2003 11:18:31

