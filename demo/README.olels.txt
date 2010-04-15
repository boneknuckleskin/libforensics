Lists entries in an OLE compound file.


Usage:
------

$ python3.1 olels.py -h
Usage: olels.py [options] olefile [dir. entry #]

Lists entries in an OLE compound file.  If file is '-', then stdin is read. If
a directory entry number is not specified, root is assumed.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -D          Display only directories (storages)
  -F          Display only files (streams)
  -l          Display details in long format
  -m PATH     Display details in mactime format (prefixed by PATH)
  -p          Display full path when recursing
  -r          Recurse into sub-directories


Examples:
---------

(sample.doc is found under the unittests/data/doc directory)

1) List the streams at the root directory (storage)

$ python3.1 olels.py sample.doc
r/r 2 WordDocument
d/d 16 Macros
r/r 1 Data
r/r 38 1Table
d/d 3 ObjectPool
r/r 45 \x01CompObj
d/d 41 MsoDataStore
r/r 39 \x05SummaryInformation
r/r 40 \x05DocumentSummaryInformation
v/v 48 $Header
v/v 49 $DIFAT
v/v 50 $FAT
v/v 51 $MiniFAT

(Note: the last 4 entries are virtual and don't actually exist in the file.)


2) Recursively list the streams

$ cat sample.doc | python3.1 olels.py -r -
r/r 2 WordDocument
d/d 16 Macros
r/r 31 +PROJECT
d/d 17 +VBA
r/r 21 ++__SRP_2
r/r 19 ++__SRP_0
r/r 18 ++dir
r/r 20 ++__SRP_1
[... output truncated ...]


3) Recursively list the streams, showing the full path

$ python3.1 olels.py -r -p sample.doc
r/r 2 WordDocument
d/d 16 Macros
r/r 31 Macros/PROJECT
d/d 17 Macros/VBA
r/r 21 Macros/VBA/__SRP_2
r/r 19 Macros/VBA/__SRP_0
r/r 18 Macros/VBA/dir
r/r 20 Macros/VBA/__SRP_1
[... output truncated ...]


4) List the entries under the ObjectPool directory (storage)

$ python3.1 olels.py sample.doc 3
d/d 4 _1326562448
d/d 11 _1326567708


5) Recursively list the entries under the ObjectPool directory (storage)
showing the full path

$ python3.1 olels.py -rp sample.doc 3
d/d 4 _1326562448
r/r 6 _1326562448/\x01CompObj
r/r 5 _1326562448/\x01Ole
r/r 8 _1326562448/Workbook
r/r 7 _1326562448/\x03ObjInfo
r/r 9 _1326562448/\x05SummaryInformation
r/r 10 _1326562448/\x05DocumentSummaryInformation
d/d 11 _1326567708
r/r 13 _1326567708/\x03ObjInfo
r/r 12 _1326567708/\x01Ole
r/r 14 _1326567708/\x03LinkInfo
r/r 15 _1326567708/\x02OlePres000


6) Recursively list (showing full path) just the files (streams)

$ python3.1 olels.py -rpF sample.doc
r/r 2 WordDocument
r/r 31 Macros/PROJECT
r/r 21 Macros/VBA/__SRP_2
r/r 19 Macros/VBA/__SRP_0
r/r 18 Macros/VBA/dir
r/r 20 Macros/VBA/__SRP_1
r/r 25 Macros/VBA/__SRP_6
[... output truncated ...]


7) Generate mactime output for all entries, saving the output to bodyfile.
Then run mactime against bodyfile to generate a timeline

$ python3.1 olels.py -rm "c:\\sample.doc" sample.doc > bodyfile
$ mactime -b bodyfile
Wed Dec 31 1969 16:00:00 20288 .acb d/d 0  c:\sample.doc/Root Entry
                             0 .ac. d/d 11 c:\sample.doc/ObjectPool/_1326567708
                             0 .ac. d/d 16 c:\sample.doc/Macros
                             0 .ac. d/d 17 c:\sample.doc/Macros/VBA
                             0 .ac. d/d 3  c:\sample.doc/ObjectPool
                             0 .ac. d/d 33 c:\sample.doc/Macros/UserForm1
                             0 .ac. d/d 4  c:\sample.doc/ObjectPool/_1326562448
                             0 .ac. d/d 41 c:\sample.doc/MsoDataStore
[... output truncated ...]

(Note: Some of the columns and spacing have been removed for display purposes)
