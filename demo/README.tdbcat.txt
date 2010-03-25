Extracts a thumbnail from a thumbs.db file

$ python3.1 tdbcat.py -h
Usage: tdbcat.py [options] thumbsdb id

Extracts raw thumbnail data from a thumbs.db file. If thumbsdb is '-', then
stdin is read.

Options:
  --version        show program's version number and exit
  -h, --help       show this help message and exit
  -c CATALOG_NAME  The name of the catalog stream (def: Catalog)



Examples:

1) Extract the image with id 4.
(thumbs.db from unittests/data/thumbsdb)

$ python3.1 tdbcat.py thumbs.db 4 > thumb.jpg


2) Extract the thumbnail with id 4 from the same thumbs.db file.  Send the
output to imagemagic to identify image metadata.

$ cat thumbs.db | python3.1 tdbcat.py - 4 | identify -verbose -
Image: /tmp/magick-XXZPK0Vw
  Base filename: -
  Format: JPEG (Joint Photographic Experts Group JFIF format)
  Class: DirectClass
  Geometry: 96x96+0+0
  Resolution: 96x96
  Print size: 1x1
  Units: PixelsPerInch
  Type: TrueColor
  Endianess: Undefined
  Colorspace: RGB
  Depth: 8-bit
[... output truncated ...]
