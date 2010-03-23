Prints information about a specific entry in an INFO2 file.

$ python3.1 info2stat.py -h
y -h
Usage: info2stat.py info2file index

Displays statistics about a specific entry in an INFO2 file. If info2file is
'-', then stdin is read.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit



Examples:

1) Print statistics about the entry with index 3 in an INFO2 ifle.
(INFO2 from CFReDS hacking case http://www.cfreds.nist.gov/Hacking_Case.html)

$ python3.1 info2stat.py INFO2 3
Deleted name: Dc3.exe
Index: 3
Drive number: 2 (C:)
ASCII name: C:\\Documents and Settings\\Mr. Evil\\Desktop\\WinPcap_3_01_a.exe
Unicode name: C:\Documents and Settings\Mr. Evil\Desktop\WinPcap_3_01_a.exe
File size: 442880 bytes
Deleted time: 2004-08-27 15:15:26
Exists on disk: Yes


2) Print statistics about the header (index 5) of the same INFO2 file.

$ icat -o 63 CFReDS/SCHARDT.00* 11850 | python3.1 info2stat.py - 5
Version: 5
Item size: 800
