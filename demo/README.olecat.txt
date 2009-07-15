Dumps streams from an OLE compound file.

$ python3.1 olecat.py -h
Usage: olecat.py [options] <ole file>

Options:
  -h, --help            show this help message and exit
  -i ID, --id=ID        Find stream at location ID
  -n NAME, --name=NAME  Find stream called NAME
  -a, --all             Extract all streams (to files named BASE.#)
  -r, --root            Extract root stream (when extracting all streams)
  -b BASE, --base=BASE  Create files BASE.1, BASE.2, ... (def: <ole file>)
  -o DIR, --output-dir=DIR
                        Save files to DIR


Note: If you don't specify an ole file, input is read from stdin.
If you aren't specifying all stream (-a), output is written to stdout.
Otherwise output is written to files with the specified base (-b).

Examples:
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

1) Extract the 3rd stream to the file blair.doc.3

$ python3.1 olecat.py -i 3 blair.doc > blair.doc.3


2) Extract all streams to the directory "out", with the base name bld

$ python3.1 olecat.py -a -o out -b bld blair.doc
$ ls out
bld.1	bld.2	bld.3	bld.4	bld.5	bld.6


3) Extract all streams (including directory stream) to directory "out", with
base name sotm24.5, for _IMMYJ~1.DOC
(image from SOTM24 http://old.honeynet.org/scans/scan24/)

$ icat -r image 5 | python3.1 olecat.py -a -r -b sotm24.5 -o out
$ ls out
sotm24.5.0  sotm24.5.1  sotm24.5.2  sotm24.5.3  sotm24.5.4  sotm24.5.5
