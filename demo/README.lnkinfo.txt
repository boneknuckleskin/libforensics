Dumps information from a .lnk (shortcut) files

$ python3.1 lnkinfo.py -h
Usage: lnkinfo.py [lnk file]

Options:
  -h, --help  show this help message and exit

Note: If you don't specify an lnk file, input si read from stdin.  Output is
written to stdout.

Examples:

1) Dump the values from an lnk file
("Temp on m1200 (4.12.220.254).lnk" from CFReDS hacking case http://www.cfreds.nist.gov/Hacking_Case.html)

$ python3.1 lnkinfo.py Temp\ on\ m1200\ \(4.12.220.254\).lnk 
Header Information
------------------
Filename: Temp on m1200 (4.12.220.254).lnk
CLSID: 00021401-0000-0000-c000-000000000046
Show command: 0x1 (SW_SHOWNORMAL)
Hotkey: 00:00 

 Flags
 -----
 Has item id list: Yes
 Has link information: Yes
 Has NAME_STRING: No
 Has RELATIVE_PATH: No
 Has WORKING_DIR: No
 Has COMMAND_LINE_ARGUMENTS: No
 Has ICON_LOCATION: No
 Has Unicode encoded strings: Yes
 Ignore LinkInfo structure: No
 Has EnvironmentVariableDataBlock structure: No
 Run in separate vm: No
 Has logo3 id (unused): No
 Has DarwinDataBlock structure: No
 Run as a different user: No
 Has IconEnvironmentDataBlock structure: No
 In shell namespace: No
 Force UNC name: No
 Run with shim layer: No
 Object ID distributed tracking disabled: No
 Cache target metadata: No
 Shell link tracking disabled: No
 Known folder tracking disabled: No
 Known folder alias mapping disabled: No
 Can point to other shell link files: No
 Remove alias when saving item id list: No
 Recalculate item id list from path: No
 Keep local copy of item id list (if on UNC): No

 Target Metadata
 ---------------
 Creation time: 08/02/2004 06:51:49
 Access time: 08/26/2004 15:07:06
 Modification time: 08/26/2004 13:49:28
 File size: 0
 Icon index: 0

  Attributes
  ----------
  Read only: No
  Hidden: No
  System: No
  Directory: Yes
  Archive: No
  Normal: No
  Temporary: No
  Sparse: No
  Reparse point: No
  Compressed: No
  Offline: No
  Contents need indexing: No
  Encrypted: No

Item ID List
------------
0: b'\x1fX`,\x8d \xea:i\x10\xa2\xd7\x08\x00+00\x9d'
1: b'G\x00\x02Entire Network\x00'
2: b'F\x00\x82Microsoft Windows Network\x00Microsoft Network\x00\x02\x00'
3: b'A\x00\x821a\x00Microsoft Network\x00\x02\x00'
4: b'B\x00\xc2\\\\4.12.220.254\x00Microsoft Network\x00m1200\x00\x02\x00'
5: b'\xc3\x01\xc1\\\\4.12.220.254\\Temp\x00Microsoft Network\x00\x00\x02\x00'

Link Info
---------
Local base path: Not in file
Local base path (unicode): Not in file
Path suffix: b''
Path suffix (unicode): Not in file

 Volume ID
 ---------
 Not in file

 Common Network Relative Link
 ----------------------------
 Device name valid: No
 Device name: Not in file
 Device name (unicode): Not in file
 Net name: b'\\\\4.12.220.254\\TEMP'
 Net name (unicode): Not in file
 Net type valid: Yes
 Net type: 0x20000 (WNNC_NET_LANMAN)

String Data
-----------
NAME_STRING: Not in file
RELATIVE_PATH: Not in file
WORKING_DIR: Not in file
COMMAND_LINE_ARGS: Not in file
ICON_LOCATION: Not in file

Extra Data
----------
 Tracker Data Block
 ------------------
 Version: 0x0
 Machine ID: b''
 Droid (volume): 09b7eb60-3056-483a-afb8-4ccac688960b
 Droid (object): 0a009e41-e49a-11d8-8ba3-00023fb3e570
 Droid birth (volume): 09b7eb60-3056-483a-afb8-4ccac688960b
 Droid birth (object): 0a009e41-e49a-11d8-8ba3-00023fb3e570

 Terminal Data Block
 -------------------
 Size: 0


2) Dump the values from an lnk file from Windows Vista
(shortcut_to_local_executable.lnk from unittest/tests/windows/shell/link/data)

$ python3.1 lnkinfo.py shortcut_to_local_executable.lnk
Header Information
------------------
Filename: shortcut_to_local_executable.lnk
CLSID: 00021401-0000-0000-c000-000000000046
Show command: 0x3 (SW_SHOWMAXIMIZED)
Hotkey: 53:06 (Ctrl + Alt + S)

 Flags
 -----
 Has item id list: Yes
 Has link information: Yes
 Has NAME_STRING: Yes
 Has RELATIVE_PATH: Yes
 Has WORKING_DIR: Yes
 Has COMMAND_LINE_ARGUMENTS: Yes
 Has ICON_LOCATION: Yes
 Has Unicode encoded strings: Yes
 Ignore LinkInfo structure: No
 Has EnvironmentVariableDataBlock structure: No
 Run in separate vm: No
 Has logo3 id (unused): No
 Has DarwinDataBlock structure: No
 Run as a different user: Yes
 Has IconEnvironmentDataBlock structure: Yes
 In shell namespace: No
 Force UNC name: No
 Run with shim layer: No
 Object ID distributed tracking disabled: No
 Cache target metadata: Yes
 Shell link tracking disabled: No
 Known folder tracking disabled: No
 Known folder alias mapping disabled: No
 Can point to other shell link files: No
 Remove alias when saving item id list: No
 Recalculate item id list from path: No
 Keep local copy of item id list (if on UNC): No

 Target Metadata
 ---------------
 Creation time: 11/02/2006 12:35:01
 Access time: 11/02/2006 12:35:01
 Modification time: 11/02/2006 12:35:01
 File size: 151040
 Icon index: 0

  Attributes
  ----------
  Read only: No
  Hidden: No
  System: No
  Directory: No
  Archive: Yes
  Normal: No
  Temporary: No
  Sparse: No
  Reparse point: No
  Compressed: No
  Offline: No
  Contents need indexing: No
  Encrypted: No

Item ID List
------------
0: b'\x1fP\xe0O\xd0 \xea:i\x10\xa2\xd8\x08\x00+00\x9d'
1: b'/C:\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
2: b'1\x00\x00\x00\x00\x00\xfb:T\xba\x10\x00Windows\x008\x00\x07\x00\x04\x00\xef\xbeb5RZ\xfb:T\xba&\x00\x00\x00\xc5\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00W\x00i\x00n\x00d\x00o\x00w\x00s\x00\x00\x00\x16\x00'
3: b'2\x00\x00N\x02\x00b5ad \x00notepad.exe\x00@\x00\x07\x00\x04\x00\xef\xbeb5adb5ad&\x00\x00\x00L!\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n\x00o\x00t\x00e\x00p\x00a\x00d\x00.\x00e\x00x\x00e\x00\x00\x00\x1a\x00'

Link Info
---------
Local base path: b'C:\\'
Local base path (unicode): Not in file
Path suffix: b'Windows\\notepad.exe'
Path suffix (unicode): Not in file

 Volume ID
 ---------
 Drive type: 3 (Fixed)
 Drive serial num: 0x900FF081
 Volume label: b''

 Common Network Relative Link
 ----------------------------
 Device name valid: No
 Device name: Not in file
 Device name (unicode): Not in file
 Net name: b'\\\\TESTUSER-PC\\C'
 Net name (unicode): Not in file
 Net type valid: Yes
 Net type: 0x20000 (WNNC_NET_LANMAN)

String Data
-----------
NAME_STRING: this is a comment
RELATIVE_PATH: ..\..\..\Windows\notepad.exe
WORKING_DIR: C:\Windows
COMMAND_LINE_ARGS: c:\arg1.txt
ICON_LOCATION: C:\Windows\twunk_32.exe

Extra Data
----------
 Special Folder Data Block
 -------------------------
 Special folder ID: 0x24 (CSIDL_WINDOWS, "WINDOWS")
 Offset: 0x7B

 Known Folder Data Block
 -----------------------
 Known folder ID: f38bf404-1d43-42f2-9305-67de0b28fc23 (FOLDERID_Windows, "Windows")
 Offset: 0x7B

 Tracker Data Block
 ------------------
 Version: 0x0
 Machine ID: b'testuser-pc'
 Droid (volume): e0d619cc-7a40-4399-b848-29fafe3bdbac
 Droid (object): c9b4b50f-7b03-11de-b10a-000c291b5cb3
 Droid birth (volume): e0d619cc-7a40-4399-b848-29fafe3bdbac
 Droid birth (object): c9b4b50f-7b03-11de-b10a-000c291b5cb3

 Icon Environment Data Block
 ---------------------------
 Target (ansi): b'%SystemRoot%\\twunk_32.exe'
 Target (unicode): %SystemRoot%\twunk_32.exe

 Terminal Data Block
 -------------------
 Size: 0
