Prints information about a specific entry in a thumbs.db file.


Usage:
------

$ python3.1 tdbstat.py -h
Usage: tdbstat.py thumbsdb id

Displays statistics about a specific entry in a thumbs.db file. If thumbsdb is
'-', then stdin is read.

Options:
  --version        show program's version number and exit
  -h, --help       show this help message and exit
  -c CATALOG_NAME  The name of the catalog stream (def: Catalog)



Examples:
---------

1) Print statistics about the entry with id 4 in thumbs.db.
(thumbs.db from unittests/data/thumbsdb)

$ python3.1 tdbstat.py thumbs.db 4
ID: 4
Catalog entry size: 84
File name: Copy (2) of Makari_the_Tiger.jpg
File size: 5238
Stream name: 4
Modification time: 2010-02-02 03:25:04


2) Print statistics about the catalog from the same thumbs.db file

$ cat thumbs.db | python3.1 tdbstat.py - 16
Thumbnail width: 96
Thumbnail height: 96
Thumbnail count: 15
