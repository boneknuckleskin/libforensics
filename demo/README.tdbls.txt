Lists information from thumbs.db files.


Usage:
------

$ python3.1 tdbls.py -h
Usage: tdbls.py [options] thumbsdb

Lists the entries in an thumbs.db file.  If thumbsdb is '-', then stdin is
read.

Options:
  --version        show program's version number and exit
  -h, --help       show this help message and exit
  -p               Display details in 'pretty-print' format
  -l               Display details in long format
  -m               Display details in mactime format
  -c CATALOG_NAME  The name of the catalog stream (def: Catalog)



Examples:
---------

1) List the entries in the thumbs.db file under unittests/data/thumbsdb.

$ python3.1 tdbls.py thumbs.db
r/r 1: zoolemur1.jpg
r/r 2: Copy (2) of danger-sign-shock.jpg
r/r 3: Copy (2) of Kookaburra_at_Marwell.jpg
r/r 4: Copy (2) of Makari_the_Tiger.jpg
r/r 5: Copy (2) of prairiedogs.jpg
r/r 6: Copy (2) of zoolemur1.jpg
r/r 7: Copy of danger-sign-shock.jpg
r/r 8: Copy of Kookaburra_at_Marwell.jpg
r/r 9: Copy of Makari_the_Tiger.jpg
r/r 10: Copy of prairiedogs.jpg
r/r 11: Copy of zoolemur1.jpg
r/r 12: danger-sign-shock.jpg
r/r 13: Kookaburra_at_Marwell.jpg
r/r 14: Makari_the_Tiger.jpg
r/r 15: prairiedogs.jpg
v/v 16: $Catalog


2) List the entries in the same thumbs.db file, with long output.

$ python3.1 tdbls.py -l thumbs.db
r/r 1:	zoolemur1.jpg	2010-02-02 03:25:06	3039
r/r 2:	Copy (2) of danger-sign-shock.jpg	2010-02-02 03:25:04	4098
r/r 3:	Copy (2) of Kookaburra_at_Marwell.jpg	2010-02-02 03:25:02	2878
r/r 4:	Copy (2) of Makari_the_Tiger.jpg	2010-02-02 03:25:04	5238
r/r 5:	Copy (2) of prairiedogs.jpg	2010-02-02 03:25:06	2963
r/r 6:	Copy (2) of zoolemur1.jpg	2010-02-02 03:25:06	3039
r/r 7:	Copy of danger-sign-shock.jpg	2010-02-02 03:25:04	4098
r/r 8:	Copy of Kookaburra_at_Marwell.jpg	2010-02-02 03:25:02	2878
r/r 9:	Copy of Makari_the_Tiger.jpg	2010-02-02 03:25:04	5238
r/r 10:	Copy of prairiedogs.jpg	2010-02-02 03:25:06	2963
r/r 11:	Copy of zoolemur1.jpg	2010-02-02 03:25:06	3039
r/r 12:	danger-sign-shock.jpg	2010-02-02 03:25:04	4098
r/r 13:	Kookaburra_at_Marwell.jpg	2010-02-02 03:25:02	2878
r/r 14:	Makari_the_Tiger.jpg	2010-02-02 03:25:04	5238
r/r 15:	prairiedogs.jpg	2010-02-02 03:25:06	2963
v/v 16:	$Catalog	0	0


3) List the entries in the same thumbs.db file, with pretty-print output.

$ python3.1 tdbls.py -p thumbs.db
ID  Modified time        Size    File name
1   2010-02-02 03:25:06  3039    zoolemur1.jpg
2   2010-02-02 03:25:04  4098    Copy (2) of danger-sign-shock.jpg
3   2010-02-02 03:25:02  2878    Copy (2) of Kookaburra_at_Marwell.jpg
4   2010-02-02 03:25:04  5238    Copy (2) of Makari_the_Tiger.jpg
5   2010-02-02 03:25:06  2963    Copy (2) of prairiedogs.jpg
6   2010-02-02 03:25:06  3039    Copy (2) of zoolemur1.jpg
7   2010-02-02 03:25:04  4098    Copy of danger-sign-shock.jpg
8   2010-02-02 03:25:02  2878    Copy of Kookaburra_at_Marwell.jpg
9   2010-02-02 03:25:04  5238    Copy of Makari_the_Tiger.jpg
10  2010-02-02 03:25:06  2963    Copy of prairiedogs.jpg
11  2010-02-02 03:25:06  3039    Copy of zoolemur1.jpg
12  2010-02-02 03:25:04  4098    danger-sign-shock.jpg
13  2010-02-02 03:25:02  2878    Kookaburra_at_Marwell.jpg
14  2010-02-02 03:25:04  5238    Makari_the_Tiger.jpg
15  2010-02-02 03:25:06  2963    prairiedogs.jpg


4) List the entries in the same thumbs.db file (read from stdin) in mactime
format.  Use mactime to generate a timeline.

$ cat tdbls.py | python3.1 - -m thumbs.db > bodyfile
$ mactime -b bodyfile
Mon Feb 01 2010 19:25:02     2878 m... 13 Kookaburra_at_Marwell.jpg
                             2878 m... 3  Copy (2) of Kookaburra_at_Marwell.jpg
                             2878 m... 8  Copy of Kookaburra_at_Marwell.jpg
Mon Feb 01 2010 19:25:04     4098 m... 12 danger-sign-shock.jpg
                             5238 m... 14 Makari_the_Tiger.jpg
[... output truncated ...]
