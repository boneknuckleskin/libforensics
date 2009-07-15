# Copyright 2009 Michael Murr
#
# This file is part of LibForensics.
#
# LibForensics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibForensics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with LibForensics.  If not, see <http://www.gnu.org/licenses/>.

"""
Metadata from Microsoft Word documents.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"

__all__ = [
    "WordMetadata"
]

from datetime import date
from lf.apps.msoffice.word.objects import Fib, SttbShortUnicode

class WordMetadata():
    """
    Represents metadata from a Microsoft Word document.

    .. attribute:: magic

        The magic number from the FIB.

    .. attribute:: version

        The file format version from the FIB.

    .. attribute:: lang_id

        The language identifier from the FIB.

    .. attribute:: encryption_key

        The encryption key from the FIB.

    .. attribute:: is_template

        True if the document is a template.

    .. attribute:: is_glossary

        True if the document is a glossary.

    .. attribute:: is_complex

        True if the document is in complex fast-saved format.

    .. attribute:: has_pictures

        True if the document has pictures.

    .. attribute:: is_encrypted

        True if the document is encrypted.

    .. attribute:: is_far_east_encoded

        True if the document is encoded for the far east.

    .. attribute:: created_environment

        The environment the document was created in.

    .. attribute:: saved_mac

        True if the document was last saved on a Mac.

    .. attribute:: magic_created_by

        The magic number of the application that created the document.

    .. attribute:: magic_revised_by

        The magic number of the application that last revised the document.

    .. attribute:: created_build_date

        The build date of the application that created the document.

    .. attribute:: revised_build_date

        The build date of the application that last revised the document.

    .. attribute:: last_saved_by

        A list of the last authors to save the document.

    .. attribute:: last_saved_locations

        A list of the last locations the document was saved to (correspond
        with last_saved_by)

    .. attribute:: associated_strings

        Associated strings.

    .. attribute:: users_roles

        A list of (user name, role) pairs for protected content.
    """

    def __init__(self, cfb):
        """
        Initializes a WordMetadata object.

        :parameters:
            cfb
                A CompoundFile object for the word document.
        """

        for entry in cfb.dir_entries.values():
            if entry.name == "WordDocument":
                stream_id = entry.sid
            # end if
        # end for

        fib = Fib(cfb.get_stream(stream_id))

        if fib.header.whichTblStm:
            table_name = "1Table"
        else:
            table_name = "0Table"
        # end if

        for entry in cfb.dir_entries.values():
            if entry.name == table_name:
                stream_id = entry.sid
            # end if
        # end for

        table_stream = cfb.get_stream(stream_id, ignore_size=True)

        self.magic = fib.header.wIdent
        self.version = fib.header.nFib
        self.lang_id = fib.header.lid
        self.encryption_key = fib.header.lKey
        self.is_template = bool(fib.header.dot)
        self.is_glossary = bool(fib.header.glsy)
        self.is_complex = bool(fib.header.complex)
        self.has_pictures = bool(fib.header.hasPic)
        self.is_encrypted = bool(fib.header.encrypted)
        self.is_far_east_encoded = bool(fib.header.farEast)
        self.saved_mac = bool(fib.header.mac)
        self.created_environment = fib.header.envr
        self.magic_created_by = fib.shorts.wMagicCreated
        self.magic_revised_by = fib.shorts.wMagicRevised

        created_date = fib.longs.lProductCreated
        year = (created_date % 100) + 1900
        day = (created_date // 100) % 100
        month = (created_date // 10000) % 100
        self.created_build_date = date(year, month, day)

        revised_date = fib.longs.lProductRevised
        year = (revised_date % 100) + 1900
        day = (revised_date // 100) % 100
        month = (revised_date // 10000) % 100
        self.revised_build_date = date(year, month, day)

        if fib.fc_lcb.sttbSavedBy.lcb:
            saved_by = SttbShortUnicode(
                table_stream, fib.fc_lcb.sttbSavedBy.fc
            )

            last_saved_by = list(saved_by.data[::2])
            last_saved_locations = list(saved_by.data[1::2])
        else:
            last_saved_by = list()
            last_saved_locations = list()
        # end if

        if fib.fc_lcb.sttbfAssoc.lcb:
            assoc = SttbShortUnicode(table_stream, fib.fc_lcb.sttbfAssoc.fc)
            associated_strings = assoc.data
        else:
            associated_strings = list()
        # end if

        if hasattr(fib.fc_lcb, "sttbProtUser"):
            if fib.fc_lcb.sttbProtUser.lcb:
                prot_users = SttbShortUnicode(
                    table_stream, fib.fc_lcb.sttbProtUser.fc
                )

                users_roles = list(zip(prot_users.data, prot_users.extra_data))
            else:
                users_roles = list()
            # end if
        else:
            users_roles = list()
        # end if

        self.last_saved_by = last_saved_by
        self.last_saved_locations = last_saved_locations
        self.associated_strings = associated_strings
        self.users_roles = users_roles
    # end def __init__
# end class WordMetadata
