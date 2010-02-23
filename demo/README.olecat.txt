Displays the contents of an OLE stream to standard out.


Usage:
------
$ python3.1 olecat.py -h
Usage: olecat.py [options] olefile sid

Displays the contents of an OLE stream to standard out. If file is '-', then
stdin is read.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -s          Include slack space


Examples:
---------
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

1) Extract the contents of stream 2

$ python3.1 olecat.py -i 2 blair.doc > blair.doc.2


2) Extract the contents of stream 2, including slack

$ cat blair.doc | python3.1 olecat.py  -s - 2 > blair.doc.2.slack
