# Copyright 2010 Michael Murr
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

"""Unit tests for the lf.dtypes.dal module."""

# stdlib imports
from unittest import TestCase

# local imports
from lf.dec import ByteIStream
from lf.dtypes.composite import LERecord
from lf.dtypes.native import int8, uint8
from lf.dtypes.dal import structuple, Structuple, CtypesWrapper

__docformat__ = "restructuredtext en"
__all__ = [
    "structupleTestCase", "StructupleTestCase", "CtypesWrapperTestCase"
]

class structupleTestCase(TestCase):
    def test_structuple(self):
        ae = self.assertEqual
        af = self.assertFalse
        at = self.assertTrue

        fields = ("field1", "field2")
        dup_fields = ["field1", "field2", "field1"]
        dup_fields_renamed = ("field1", "field2", "field1__2")
        aliases = {"field3": "field1", "field4": "field2"}
        st_init = [0x64, 0x53]
        st3_init = [0x64, 0x53, 0xCC]
        field_vals = {
            "field1": 0x64,
            "field3": 0x64,
            "field2": 0x53,
            "field4": 0x53,
            "field1__2": 0xCC
        }

        st1 = structuple("st1_name", fields, aliases, True, False)
        st2 = structuple("st2_name", fields, aliases, False, False)
        st3 = structuple("st3_name", dup_fields, aliases, True, True)


        # Check name and rename
        ae(st1.__name__, "st1_name")
        ae(st2.__name__, "st2_name")
        ae(st3.__name__, "st3_name")


        # Check fields
        ae(st1._fields_, fields)
        ae(st2._fields_, fields)
        ae(st3._fields_, dup_fields_renamed)

        st1_vals = st1(st_init)
        st2_vals = st2(st_init)
        st3_vals = st3(st3_init)

        for field in fields:
            ae(getattr(st1_vals, field), field_vals[field])
            ae(getattr(st2_vals, field), field_vals[field])
        # end for

        for field in dup_fields_renamed:
            ae(getattr(st3_vals, field), field_vals[field])
        # end for


        # Check aliases
        for alias in aliases.keys():
            ae(getattr(st1_vals, alias), field_vals[alias])
            ae(getattr(st2_vals, alias), field_vals[alias])
            ae(getattr(st3_vals, alias), field_vals[alias])
        # end for


        # Check auto_slots
        class AutoSlots1(st1):
            extra_field = None
        # end class
        as1 = AutoSlots1()

        class AutoSlots2(st2):
            extra_field = None
        # end class AutoSlots2
        as2 = AutoSlots2()

        af(hasattr(as1, "__dict__"))
        at(hasattr(as2, "__dict__"))
    # end def test_structuple
# end class structupleTestCase

class StructupleTestCase(TestCase):
    def test_Structuple(self):
        ae = self.assertEqual
        af = self.assertFalse
        at = self.assertTrue

        fields1 = ("field1_0", "field1_1")
        fields2 = ("field2_0", "field2_1")
        fields3 = ("field3_0", "field3_1")
        aliases = {"field1_0_A": "field1_0", "field3_0_A": "field3_0"}
        fields2_full = ("field1_0", "field1_1", "field2_0", "field2_1")
        fields3_full = ("field1_0", "field1_1", "field3_0", "field3_1")
        st_init = (0x64, 0x53)
        st2_init = (0x64, 0x53, 0xAA, 0x55)
        field_vals = {
            "field1_0": 0x64,
            "field1_0_A": 0x64,
            "field1_1": 0x53,
            "field2_0": 0xAA,
            "field3_0": 0xAA,
            "field3_0_A": 0xAA,
            "field2_1": 0x55,
            "field3_1": 0x55,
        }

        class TestStructuple1(Structuple):
            _fields_ = fields1
            _aliases_ = aliases
            _auto_slots_ = True
        # end class TestStructuple1

        class TestStructuple2(TestStructuple1):
            _fields_ = fields2
        # end class TestStructuple2

        class TestStructuple3(TestStructuple1):
            _fields_ = fields3
            _auto_slots_ = False
        # end class TestStructuple3


        # Check _fields_
        ae(TestStructuple1._fields_, fields1)
        ae(TestStructuple2._fields_, fields2_full)
        ae(TestStructuple3._fields_, fields3_full)

        st1_vals = TestStructuple1(st_init)
        st2_vals = TestStructuple2(st2_init)
        st3_vals = TestStructuple3(st2_init)

        for field in fields1:
            ae(getattr(st1_vals, field), field_vals[field])
        # end for

        for field in fields2_full:
            ae(getattr(st2_vals, field), field_vals[field])
        # end for

        for field in fields3_full:
            ae(getattr(st3_vals, field), field_vals[field])
        # end for


        # Check _aliases_
        ae(st1_vals.field1_0_A, field_vals["field1_0_A"])
        ae(st2_vals.field1_0_A, field_vals["field1_0_A"])
        ae(st3_vals.field3_0_A, field_vals["field3_0_A"])
        af(hasattr(st1_vals, "field3_0_A"))
        af(hasattr(st2_vals, "field3_0_A"))
        at(hasattr(st3_vals, "field1_0_A"))


        # Check auto_slots
        ts1 = TestStructuple1()
        ts2 = TestStructuple2()
        ts3 = TestStructuple3()

        af(hasattr(ts1, "__dict__"))
        af(hasattr(ts2, "__dict__"))
        at(hasattr(ts3, "__dict__"))
    # end def test_Structuple
# end class StructupleTestCase

class CtypesWrapperTestCase(TestCase):
    def test_CtypesWrapper(self):
        ae = self.assertEqual

        class TestDataType(LERecord):
            field1 = int8
            field2 = uint8
        # end class TestDataType
        ctype = TestDataType._ctype_

        class CtypesWrapperTest(CtypesWrapper):
            _ctype_ = ctype
            _fields_ = [x[0] for x in TestDataType._fields_]
        # end class CtypesWrapperTest

        cwt1 = CtypesWrapperTest.from_stream(ByteIStream(b"\x64\x53"))
        ctype_with_val = ctype.from_buffer_copy(b"\x64\x53")
        cwt2 = CtypesWrapperTest.from_ctype(ctype_with_val)
        cwt3 = CtypesWrapperTest.from_bytes(b"\x64\x53")

        for cwt in (cwt1, cwt2, cwt3):
            ae(cwt.field1, 0x64)
            ae(cwt.field2, 0x53)
            ae(cwt, (0x64, 0x53))
        # end for
    # end def test_CtypesWrapper
# end class CtypesWrapperTestCase
