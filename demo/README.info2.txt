Dumps information from INFO2 (recycle bin) files.

$ python3.1 info2.py -h
Usage: info2.py <INFO2 file>

Options:
  -h, --help  show this help message and exit

Note: If you don't specify an info2 file, input is read from stdin.  Output is
written to stdout.

Examples:

1) Dump the values in an INFO2 file
(INFO2 from CFReDS hacking case http://www.cfreds.nist.gov/Hacking_Case.html)

$ python3.1 info2.py INFO2 
File: INFO2
Note: times are in UTC

Deleted name    Deleted time           Size         Original name
------------    ------------           ----         ------------
Dc1.exe         08/25/2004 16:18:25    2160128      C:\Documents and Settings\Mr. Evil\Desktop\lalsetup250.exe
Dc2.exe         08/27/2004 15:12:30    1325056      C:\Documents and Settings\Mr. Evil\Desktop\netstumblerinstaller_0_4_0.exe
Dc3.exe         08/27/2004 15:15:26    442880       C:\Documents and Settings\Mr. Evil\Desktop\WinPcap_3_01_a.exe
Dc4.exe         08/27/2004 15:29:58    8460800      C:\Documents and Settings\Mr. Evil\Desktop\ethereal-setup-0.10.6.exe


2) Decoding the same file, but using The Sleuthkit, and not creating an intermediate file first.

$ icat -o 63 CFReDS/SCHARDT.00* 11850 | python3.1 info2.py 
File: stdin
Note: times are in UTC

Deleted name    Deleted time           Size         Original name
------------    ------------           ----         ------------
Dc1.exe         08/25/2004 16:18:25    2160128      C:\Documents and Settings\Mr. Evil\Desktop\lalsetup250.exe
Dc2.exe         08/27/2004 15:12:30    1325056      C:\Documents and Settings\Mr. Evil\Desktop\netstumblerinstaller_0_4_0.exe
Dc3.exe         08/27/2004 15:15:26    442880       C:\Documents and Settings\Mr. Evil\Desktop\WinPcap_3_01_a.exe
Dc4.exe         08/27/2004 15:29:58    8460800      C:\Documents and Settings\Mr. Evil\Desktop\ethereal-setup-0.10.6.exe
