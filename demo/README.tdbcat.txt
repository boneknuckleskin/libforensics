Extracts thumbnails from thumbs.db files

$ python3.1 tdbcat.py -h
Usage: tdbcat.py [options] <thumbs.db file>

Options:
  -h, --help            show this help message and exit
  -i INDEX, --index=INDEX
                        Thumbnail index to extract
  -a, --all             Extract all thumbnails (to files named BASE.#)
  -b BASE, --base=BASE  Create files BASE.1, BASE.2, ... (def: <thumbs.db
                        file>)
  -o DIR, --output-dir=DIR
                        Save files to DIR

Note: If you don't specify a thumbs.db file, input is read from stdin.  If
you're extracting a single image, output is written to stdout.  If extracting
all images, the ".jpg" extension is added automatically.

Also, unlike vinetto, we don't try to re-create jpg's from older version of
thumbs.db (without headers, quantization tables, etc.)

Examples:

1) Extract all images to directory "out" with base img:
(Thumbs.db from
http://mozmill.googlecode.com/svn/!svn/bc/414/trunk/mozmill/extension/content/editarea/edit_area/images/)

$ python3.1 tdbcat.py -a -b img -o out Thumbs.db
$ ls out
img.1.jpg	img.13.jpg	img.17.jpg	img.4.jpg	img.8.jpg
img.10.jpg	img.14.jpg	img.18.jpg	img.5.jpg	img.9.jpg
img.11.jpg	img.15.jpg	img.2.jpg	img.6.jpg
img.12.jpg	img.16.jpg	img.3.jpg	img.7.jpg


2) Extract just the third image and send it to ImageMagic to get metadata

$ cat Thumbs.db | python3.1 tdbcat.py -i 3 | identify -verbose -
Image: /tmp/magick-XXMQ5L6b
  Base filename: -
  Format: JPEG (Joint Photographic Experts Group JFIF format)
  Class: DirectClass
  Geometry: 96x72+0+0
  Resolution: 96x96
  Print size: 1x0.75
  Units: PixelsPerInch
  Type: TrueColor
  Endianess: Undefined
  Colorspace: RGB
  Depth: 8-bit
[... output truncated ...]
