These are a series of small tools I wrote to demonstrate some of the
functionality within the framework.  The coding isn't the best, but gets the
job done.

All of the tools will read from standard in, if you don't give them a file
name.  If you're on a Windows system, you'll have to make sure to run python
with the -u option (to force stdin to be unbuffered.)  Each file has it's own
readme with more information and examples.

Feel free to use the tools, and report and bugs you find to the issue tracker
at libforensics.com.

- datedecoder.py: decodes various timestamp formats
- info2.py: lists the contents of INFO2 (recycle bin) files
- olecat.py: extracts streams from OLE files (Office documents, thumbs.db,
  etc.)
- oleinfo.py: dumps informatin from OLE files
- tdbcat.py: extracts thumbnail images from thumbs.db files
- tdbinfo.py: dumps information from thumbs.db files
- wmg.py: extracts metadata from Microsoft Word documents
