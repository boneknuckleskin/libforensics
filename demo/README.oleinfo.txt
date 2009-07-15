Dumps information from an OLE file

$ python3.1 oleinfo.py -h
Usage: oleinfo.py [options] <ole file>

Options:
  -h, --help            show this help message and exit
  -s, --summary-information
                        Show SummaryInformation stream (if it exists)
  -d, --document-summary-information
                        Show DocumentSummaryInformation stream (if it exists)

Note: If you don't specify an ole file, input is read from stdin.  Output is
written to stdout.

Examples:

1) Dump OLE information, summary information, and document summary information
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

$ python3.1 oleinfo.py -s -d blair.doc
Header Information
------------------
File name: blair.doc
Signature: b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
CLSID: 00000000-0000-0000-0000-000000000000
Version: 3.62
Byte order: FFFE
Sector size: 512
Mini sector size: 64
Transaction number: 0
Mini stream cutoff: 4096
Number of DI FAT entries: 0
First sector of DI FAT: (none)
Number of Mini FAT entries: 1
First sector of Mini FAT: 124
Number of FAT entries: 1
Number of sectors in directory: 0
First sector of directory: 122
Size of root directory: 1024

Summary Information
-------------------
Title: Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND INTIMIDATION
Subject: 
Author: default
Code page: 1252
Keywords: 
Comments: 
Template used: Normal.dot
Last author: MKhan
Revision: 4
Creator: Microsoft Word 8.0
Last printed: Thu Jan 30 21:33:00 2003
Creation time: Mon Feb  3 09:31:00 2003
Last saved: Mon Feb  3 11:18:00 2003
Total edit time: 0 days, 0 hours, 3 mins, 0 secs

Document Summary Information
----------------------------
Category: (not in file)
Presentation format: (not in file)
Slide count: (not in file)
Manager: (not in file)
Company: default
Major version: 8
Minor version: 49
Content type: (not in file)
Content status: (not in file)
Language: (not in file)
Document version: (not in file)

 User Defined Properties
 -----------------------
 Code page: 1252
 _PID_GUID: {5E2C2E6C-8A16-46F3-8843-7F739FA12901}

Directory Entries
-----------------
Directory entry: 0
Name: Root Entry
Type: 5
Color: 1
Left SID: (none)
Right SID: (none)
Child SID: 3
CLSID: 00020906-0000-0000-c000-000000000046
State: 0
Creation time: Mon Feb  3 11:08:06 2003
Modification time: Mon Feb  3 11:18:31 2003
First sector: 125
Size: 128

[... output truncated ...]


2) Dump basic OLE and summary information from _IMMYJ~1.DOC
(image from SOTM24 http://old.honeynet.org/scans/scan24/)

$ icat -r image 5 | python3.1 oleinfo.py -s
Header Information
------------------
File name: stdin
Signature: b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
CLSID: 00000000-0000-0000-0000-000000000000
Version: 3.62
Byte order: FFFE
Sector size: 512
Mini sector size: 64
Transaction number: 0
Mini stream cutoff: 4096
Number of DI FAT entries: 0
First sector of DI FAT: (none)
Number of Mini FAT entries: 1
First sector of Mini FAT: 37
Number of FAT entries: 1
Number of sectors in directory: 0
First sector of directory: 35
Size of root directory: 1024

Summary Information
-------------------
Title: Jimmy Jungle
Subject: 
Author: 0000
Code page: 1252
Keywords: 
Comments: 
Template used: Normal
Last author: 0000t
Revision: 9
Creator: Microsoft Word 10.0
Last printed: (not in file)
Creation time: Mon Apr 15 20:30:00 2002
Last saved: Mon Apr 15 21:42:00 2002
Total edit time: 0 days, 0 hours, 18 mins, 0 secs

Directory Entries
-----------------
Directory entry: 0
Name: Root Entry
Type: 5
Color: 1
Left SID: (none)
Right SID: (none)
Child SID: 3
CLSID: 00020906-0000-0000-c000-000000000046
State: 0
Creation time: Mon Jan  1 00:00:00 1601
Modification time: Mon Apr 15 21:42:29 2002
First sector: 38
Size: 128
[... output truncated ...]
