Lists information from INFO2 (recycle bin) files.

$ python3.1 info2.py -h
Usage: info2ls.py [options] info2file

Lists the entries in an INFO2 file.  If info2file is '-', then stdin is read.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -R          Display details in Rifiuti-style format
  -l          Display details in long format
  -m          Display details in mactime format


Examples:

1) List the entries in the INFO2 file under unittests/data/INFO2/INFO2_1.bin

$ python3.1 info2ls.py INFO2
r/r * 3 C:\Documents and Settings\lftest1\Desktop\file2.bmp
r/r * 4 C:\Documents and Settings\lftest1\Desktop\folder3.lnk
r/r 5 C:\Documents and Settings\lftest1\Desktop\file1.txt
r/r 6 C:\Documents and Settings\lftest1\Desktop\file2.bmp
v/v 7 $HEADER


2) List the entries in the INFO2 file in rifiuti-style output.
(INFO2 from CFReDS hacking case http://www.cfreds.nist.gov/Hacking_Case.html)

$ python3.1 info2ls.py -R INFO2
INDEX  Deleted time         Drive number  Size        Deleted  Original name
1      2004-08-25 16:18:25  2             2160128     No       C:\Documents and
2      2004-08-27 15:12:30  2             1325056     No       C:\Documents and
[... output truncated ...]


3) Listing entries from the same INFO2 file in mactime format, using icat
instead to send the file to stdout, and read from stdin.  Use mactime to
generate a timeline based on the deleted timestamps (shown as metadata change
time).

$ icat -o 63 CFReDS/SCHARDT.00* 11850 | python3.1 info2ls.py -m - > bodyfile
$ mactime -b bodyfile
Wed Aug 25 2004 09:18:25  2160128 ..c. 1 C:\Documents and Settings\Mr. Evil\...
Fri Aug 27 2004 08:12:30  1325056 ..c. 2 C:\Documents and Settings\Mr. Evil\...
Fri Aug 27 2004 08:15:26   442880 ..c. 3 C:\Documents and Settings\Mr. Evil\...
Fri Aug 27 2004 08:29:58  8460800 ..c. 4 C:\Documents and Settings\Mr. Evil\...
[... output truncated ...]
