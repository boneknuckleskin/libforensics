Dumps information from a Thumbs.db file

$ python3.1 tdbinfo.py -h
Usage: tdbinfo.py [thumbs.db file]

Options:
  -h, --help  show this help message and exit

Note: If you don't specify a thumbs.db file, input is read from stdin.  Output
is written to stdout.

Examples:

1) Display a list of thumbnails from Thumbs.db
(Thumbs.db from
http://mozmill.googlecode.com/svn/!svn/bc/414/trunk/mozmill/extension/content/editarea/edit_area/images/Thumbs.db)

$ python3.1 tdbinfo.py Thumbs.db
File: Thumbs.db
Note: times are in UTC

Index    Modified Time          Original Name
-----    -------------          -------------
1        03/02/2006 17:46:46    close.gif
2        03/02/2006 17:46:46    go_to_line.gif
3        03/02/2006 17:46:48    help.gif
4        03/02/2006 17:46:48    highlight.gif
5        03/07/2006 11:52:12    load.gif
6        07/02/2006 18:28:06    move.gif
[... output truncated ...]


2) Display list of thumbnails from a Thumbs.db, downloaded from the internet
(using curl) without using an intermediate file.
(The command should all be on one line)

$ curl http://mozmill.googlecode.com/svn/\!svn/bc/414/trunk/mozmill/extension/content/editarea/edit_area/images/Thumbs.db | python3.1 tdbinfo.py
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 23040  100 23040    0     0   129k      0 --:--:-- --:--:-- --:--:--  329k
File: stdin
Note: times are in UTC

Index    Modified Time          Original Name
-----    -------------          -------------
1        03/02/2006 17:46:46    close.gif
2        03/02/2006 17:46:46    go_to_line.gif
3        03/02/2006 17:46:48    help.gif
4        03/02/2006 17:46:48    highlight.gif
5        03/07/2006 11:52:12    load.gif
6        07/02/2006 18:28:06    move.gif
[... output truncated ...]
