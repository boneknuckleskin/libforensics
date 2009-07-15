Grabs metadata from Microsoft Word (.doc) files.

$ python3.1 wmg.py -h
Usage: wmg.py <word file>

Options:
  -h, --help  show this help message and exit

Note: If you don't specify a word file, stdin is used.  Output is written to
stdout.

Examples:

1) Dump metadata on blair.doc
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)

$ python3.1 wmg.py blair.doc
ompound File Information
-------------------------
File: blair.doc
Root directory creation time: Mon Feb  3 11:08:06 2003 UTC
Root directory modification time: Mon Feb  3 11:18:31 2003 UTC

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

Word Information
----------------
Magic: Word 8.0 (0xA5EC)
Version: 0xC1
Language: United States English
Encryption key: 0
Created in: Windows
Created by: Word 97 (Build date: Fri Aug 21 1998)
Last revised by: Word 97 (Build date: Fri Aug 21 1998)

 Miscellaneous Properties
 ------------------------
 Is a template: no
 Is a glossary: no
 Is in complex format: no
 Has pictures: no
 Is encrypted: no
 Is Far East encoded: no
 Last saved on a Mac: no

 Last Authors / Locations
 ------------------------
 10: MKhan: C:\WINNT\Profiles\mkhan\Desktop\Iraq.doc
 9: MKhan: C:\TEMP\Iraq - security.doc
 8: ablackshaw: A:\Iraq - security.doc
 7: ablackshaw: C:\ABlackshaw\A;Iraq - security.doc
 6: ablackshaw: C:\ABlackshaw\Iraq - security.doc
 5: JPratt: A:\Iraq - security.doc
 4: JPratt: C:\TEMP\Iraq - security.doc
 3: cic22: C:\DOCUME~1\phamill\LOCALS~1\Temp\AutoRecovery save of Iraq -
security.asd
 2: cic22: C:\DOCUME~1\phamill\LOCALS~1\Temp\AutoRecovery save of Iraq -
security.asd
 1: cic22: C:\DOCUME~1\phamill\LOCALS~1\Temp\AutoRecovery save of Iraq -
security.asd

 Associated Strings
 ------------------
 Template used: 
 Title: Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND INTIMIDATION
 Subject: 
 Keywords: 
 Comments: 
 Author: default
 Last revised by: MKhan

 Users / Roles
 -------------
 No users / roles in document


2) Dump metadata from _IMMYJ~1.DOC
(image from SOTM24 http://old.honeynet.org/scans/scan24/)

$ icat -r image 5 | python3.1 wmg.py
Compound File Information
-------------------------
File: --stdin--
Root directory creation time: Mon Jan  1 00:00:00 1601 UTC
Root directory modification time: Mon Apr 15 21:42:29 2002 UTC

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

Document Summary Information
----------------------------
Category: (not in file)
Presentation format: (not in file)
Slide count: (not in file)
Manager: (not in file)
Company: OOOO
Major version: 10
Minor version: 65
Content type: (not in file)
Content status: (not in file)
Language: (not in file)
Document version: (not in file)

 User Defined Properties
 -----------------------
 (not in file)

Word Information
----------------
Magic: Word 8.0 (0xA5EC)
Version: 0xC1
Language: United States English
Encryption key: 0
Created in: Windows
Created by: Word 97 (Build date: Wed Feb 27 1901)
Last revised by: Word 97 (Build date: Wed Feb 27 1901)

 Miscellaneous Properties
 ------------------------
 Is a template: no
 Is a glossary: no
 Is in complex format: no
 Has pictures: no
 Is encrypted: no
 Is Far East encoded: no
 Last saved on a Mac: no

 Last Authors / Locations
 ------------------------
 1: CSTC: 

 Associated Strings
 ------------------
 Template used: 
 Title: Jimmy Jungle
 Subject: 
 Keywords: 
 Comments: 
 Author: CSTC
 Last revised by: CSTC

 Users / Roles
 -------------
 No users / roles in document
