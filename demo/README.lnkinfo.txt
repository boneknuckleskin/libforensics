Displays information about shell link (.lnk) files

$ python3.1 lnkinfo.py -h
Usage: lnkinfo.py [options] lnkfile

Displays information from shell link (.lnk) files.  If file is '-' then stdin
is read.

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -f          Display full output for binary attributes


Examples:

1) Display information from shortcut_to_local_exe.lnk (in unittests/data/lnk)

$ python3.1 lnkinfo.py shortcut_to_local_exe.lnk
File: shortcut_to_local_exe.lnk

Shell Link Header
=================
 Header size: 76
 CLSID: 00021401-0000-0000-c000-000000000046
 Creation time: 2010-03-17 09:58:19.239000
 Access time: 2010-03-17 09:58:19.239000
 Modification time: 2006-11-02 09:45:32.330000
 Target size: 15360
 Icon index: 18
 Show command: SW_SHOWMAXIMIZED (0x3)
 Hotkey: 7:4B (CTRL + SHIFT + ALT + K)

 Link Flags:
 -----------
  Has link target idlist: True
  Has link info: True
  Has name: True
  Has relative path: True
  Has working directory: True
  Has arguments: True
  Has icon location: True
  Is unicode: True
  Force no link info: False
  Has exp. string: True
  Run in separate process: False
  Has logo3 id: False
  Has darwin id: False
  Run as user: True
  Has exp. icon: False
  No pidl alias: False
  Force UNC name: False
  Run with shim layer: False
  Force no link track: False
  Enable target metadata: True
  Disable link path tracking: False
  Disable known folder tracking: False
  Disable known folder alias: False
  Allow link to link: False
  Prefer environment path: False
  Keep local idlist for UNC target: False

 File Attributes:
 ----------------
  Read only: False
  Hidden: False
  System: False
  Directory: False
  Archive: True
  Normal: False
  Temp: False
  Sparse: False
  Reparse point: False
  Compressed: False
  Offline: False
  Not content indexed: False
  Encrypted: False


Link Target IDList
==================
 Byte count: 20
 Data: b'\x1fP\xe0O\xd0 \xea:i\x10\xa2\xd8\x08\x00+'

 Byte count: 25
 Data: b'/C:\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

 Byte count: 78
 Data: b'1\x00\x00\x00\x00\x00q<JO\x10\x00Win'

 Byte count: 82
 Data: b'2\x00\x00<\x00\x00b5\xb1M \x00PIN'

 Byte count: 0
 Data: Not in file


Link Info
=========
 Size: 66
 Header size: 28
 Volume ID and local base path: True
 CNRL and path suffix: False
 Volume ID offset: 28
 Local base path offset: 45
 CNRL offset: 0
 Common path suffix offset: 65
 Local base path offset (unicode): None
 Common path suffix offset (unicode): None
 Local base path: b'C:\\Windows\\PING.EXE'
 Local base path (unicode): Not in file
 Common path suffix: Not in file
 Common path suffix (unicode): Not in file

 Volume ID:
 ----------
  Size: 17
  Drive type: Fixed (0x3)
  Drive serial number: 0xA0E8D60C
  Volume label offset: 16
  Volume label offset (unicode): None
  Volume label: b''

 Common Network Relative Link:
 -----------------------------
  Not in file


String Data
===========

 Name String:
 ------------
  Character count: 7
  String: comment

 Relative Path:
 --------------
  Character count: 25
  String: ..\..\..\Windows\PING.EXE

 Working Directory:
 ------------------
  Character count: 15
  String: c:\start-in-dir

 Command Line Arguments:
 -----------------------
  Character count: 14
  String: arg1 arg2 arg3

 Icon Location:
 --------------
  Character count: 33
  String: %SystemRoot%\system32\SHELL32.dll


Extra Data
==========
 SpecialFolderDataBlock:
 -----------------------
  Size: 16
  Signature: SPECIAL_FOLDER_PROPS (0xA0000005)
  Special folder id: WINDOWS (0x24) (CSIDL_WINDOWS)
  Offset: 123

 KnownFolderDataBlock:
 ---------------------
  Size: 28
  Signature: KNOWN_FOLDER_PROPS (0xA000000B)
  Known folder ID: f38bf404-1d43-42f2-9305-67de0b28fc23
  Offset: 123

 TrackerDataBlock:
 -----------------
  Size: 96
  Signature: TRACKER_PROPS (0xA0000003)
  Length: 88
  Version: 0
  Machine ID: b'lftest-vista-pc'

  DROID:
  ------
   Volume: 1960e830-83b3-4aae-93a1-9b9319d21e50
   Object: 196f4ff5-31a1-11df-a968-000c29c44b38

  DROID Birth:
  ------------
   Volume: 1960e830-83b3-4aae-93a1-9b9319d21e50
   Object: 196f4ff5-31a1-11df-a968-000c29c44b38

 ConsoleDataBlock:
 -----------------
  Size: 204
  Signature: CONSOLE_PROPS (0xA0000002)
  Screen buffer size (horizontal): 79
  Screen buffer size (vertical): 300
  Window size (horizontal): 79
  Window size (vertical): 23
  Window origin: (5, 5)
  Font: 0
  Input buffer size: 0
  Font size: 786448
  Font family: Modern (0x30)
  Font weight: Regular (400)
  Face name: Terminal
  Cursor size: Medium (50)
  Full screen: True (1)
  Insert mode: True (1)
  Auto position window: False (0)
  History buffer size: 47
  Number of history buffers: 6
  Remove history duplicates: False (0)

  Fill Attributes:
  ----------------
   Blue (foreground): True
   Green (foreground): True
   Red (foreground): True
   Intensity (foreground): False
   Blue (background): False
   Green (background): False
   Red (background): False
   Intensity (background): False

  Popup Fill Attributes:
  ----------------------
   Blue (foreground): True
   Green (foreground): False
   Red (foreground): True
   Intensity (foreground): False
   Blue (background): True
   Green (background): True
   Red (background): False
   Intensity (background): True

  Color Table:
  ------------
   0x00000000, 0x00800000, 0x00008000, 0x00808000
   0x00000080, 0x00800080, 0x00008080, 0x00C0C0C0
   0x00808080, 0x00FF0000, 0x0000FF00, 0x00FFFF00
   0x000000FF, 0x00FF00FF, 0x0000FFFF, 0x00FFFFFF

 EnvironmentVariableDataBlock:
 ------------------------------
  Size: 788
  Signature: ENVIRONMENT_PROPS (0xA0000001)
  Target ANSI: b'%windir%\\PING.EXE'
  Target unicode: %windir%\PING.EXE



2) Display full information (all binary data) from
  "Temp on m1200 (4.12.220.154).lnk"
  (from CFReDS hacking case at http://www.cfreds.nist.gov/Hacking_Case.html)

$ python3.1 lnkinfo.py -f Temp\ on\ m1200\ \(4.12.220.254\).lnk
File: CFReDS-hacking/Temp on m1200 (4.12.220.254).lnk

Shell Link Header
=================
 Header size: 76
 CLSID: 00021401-0000-0000-c000-000000000046
 Creation time: 2004-08-02 06:51:49.881000
 Access time: 2004-08-26 15:07:06.328000
 Modification time: 2004-08-26 13:49:28.611000
 Target size: 0
 Icon index: 0
 Show command: SW_SHOWNORMAL (0x1)
 Hotkey: 0:0 

 Link Flags:
 -----------
  Has link target idlist: True
  Has link info: True
  Has name: False
  Has relative path: False
  Has working directory: False
  Has arguments: False
  Has icon location: False
  Is unicode: True
  Force no link info: False
  Has exp. string: False
  Run in separate process: False
  Has logo3 id: False
  Has darwin id: False
  Run as user: False
  Has exp. icon: False
  No pidl alias: False
  Force UNC name: False
  Run with shim layer: False
  Force no link track: False
  Enable target metadata: False
  Disable link path tracking: False
  Disable known folder tracking: False
  Disable known folder alias: False
  Allow link to link: False
  Prefer environment path: False
  Keep local idlist for UNC target: False

 File Attributes:
 ----------------
  Read only: False
  Hidden: False
  System: False
  Directory: True
  Archive: False
  Normal: False
  Temp: False
  Sparse: False
  Reparse point: False
  Compressed: False
  Offline: False
  Not content indexed: False
  Encrypted: False


Link Target IDList
==================
 Byte count: 20
 Data:
b'\x1fX`,\x8d \xea:i\x10\xa2\xd7\x08\x00+00\x9d'

 Byte count: 20
 Data:
b'G\x00\x02Entire Network\x00'

 Byte count: 51
 Data:
b'F\x00\x82Microsoft Windows Network\x00Microsoft Network\x00\x02\x00'

 Byte count: 28
 Data:
b'A\x00\x821a\x00Microsoft Network\x00\x02\x00'

 Byte count: 46
 Data:
b'B\x00\xc2\\\\4.12.220.254\x00Microsoft Network\x00m1200\x00\x02\x00'

 Byte count: 46
 Data:
b'\xc3\x01\xc1\\\\4.12.220.254\\Temp\x00Microsoft Network\x00\x00\x02\x00'

 Byte count: 0
 Data: Not in file


Link Info
=========
 Size: 69
 Header size: 28
 Volume ID and local base path: False
 CNRL and path suffix: True
 Volume ID offset: 0
 Local base path offset: 0
 CNRL offset: 28
 Common path suffix offset: 68
 Local base path offset (unicode): None
 Common path suffix offset (unicode): None
 Local base path: Not in file
 Local base path (unicode): Not in file
 Common path suffix: Not in file
 Common path suffix (unicode): Not in file

 Volume ID:
 ----------
  Not in file

 Common Network Relative Link:
 -----------------------------
  Size: 40
  Valid device: False
  Valid net type: True
  Net name offset: 20
  Device name offset: 0
  Network provider type: WNNC_NET_LANMAN (0x20000)
  Net name offset (unicode): None
  Device name offset (unicode): None
  Net name: b'\\\\4.12.220.254\\TEMP'
  Device name: Not in file
  Net name (unicode): Not in file
  Device name (unicode): Not in file


String Data
===========

 Name String:
 ------------
  Not in file

 Relative Path:
 --------------
  Not in file

 Working Directory:
 ------------------
  Not in file

 Command Line Arguments:
 -----------------------
  Not in file

 Icon Location:
 --------------
  Not in file


Extra Data
==========
 TrackerDataBlock:
 -----------------
  Size: 96
  Signature: TRACKER_PROPS (0xA0000003)
  Length: 88
  Version: 0
  Machine ID: b''

  DROID:
  ------
   Volume: 09b7eb60-3056-483a-afb8-4ccac688960b
   Object: 0a009e41-e49a-11d8-8ba3-00023fb3e570

  DROID Birth:
  ------------
   Volume: 09b7eb60-3056-483a-afb8-4ccac688960b
   Object: 0a009e41-e49a-11d8-8ba3-00023fb3e570

