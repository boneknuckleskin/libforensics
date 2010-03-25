These are a series of small tools I wrote to demonstrate some of the
functionality within the framework.  The coding isn't the best, but gets the
job done.

All of the tools will read from standard in if you specify '-' as the file
name.  On Microsoft Windows systems, you must run python with the -u option, to
force stdin to be unbuffered.  Each file has it's own readme with more
information and examples.

Feel free to use the tools, and report and bugs you find to the issue tracker
at libforensics.com.

- datedecoder.py: decodes various timestamp formats
- info2ls.py: Lists the contents of INFO2 (recycle bin) files
- info2stat.py: Prints statistics about a specific entry in an INFO2 file 
- olels.py: Lists the directory entries in an OLE compound file
- olestat.py: Prints statistics about a directory entry in an OLE compound file
- olecat.py: Extracts the contents of a stream in an OLE compound file
- oleps.py: Displays property sets from a stream in an OLE compound file
- tdbls.py: Lists entries in a thumbs.db file
- tdbstat.py: Displays statistics about a specific entry in a thumbs.db file
- tdbcat.py: Extracts thumbnail images from thumbs.db files
- wmg.py: extracts metadata from Microsoft Word documents
- dspe.py: prints and extracts data structures
- lnkinfo.py: Dumps information from shell link (.lnk, shortcut) files
