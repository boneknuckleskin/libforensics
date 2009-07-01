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
Extractors for Microsoft Word.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "fc_lcb", "fc_pgd_old", "fc_pgd", "fib_header", "fib_shorts", "fib_longs",
    "fib", "fib_fc_lcb_97", "fib_fc_lcb_2000", "fib_fc_lcb_2002",
    "fib_fc_lcb_2003", "fib_fc_lcb_2007", "fib_csw_new_data_2000",
    "fib_csw_new_data_2007"
]

from lf.struct.extract import extractor_factory as factory
from lf.apps.msoffice.word.structs import (
    FcLcb, FcPgdOld, FcPgd, FibHeader, FibShorts, FibLongs, Fib, FibFcLcb97,
    FibFcLcb2000, FibFcLcb2002, FibFcLcb2003, FibFcLcb2007, FibCswNewData2000,
    FibCswNewData2007
)

fc_lcb = factory.make(FcLcb())
fc_pgd_old = factory.make(FcPgdOld())
fc_pgd = factory.make(FcPgd())
fib_header = factory.make(FibHeader())
fib_shorts = factory.make(FibShorts())
fib_longs = factory.make(FibLongs())
fib = factory.make(Fib())
fib_fc_lcb_97 = factory.make(FibFcLcb97())
fib_fc_lcb_2000 = factory.make(FibFcLcb2000())
fib_fc_lcb_2002 = factory.make(FibFcLcb2002())
fib_fc_lcb_2003 = factory.make(FibFcLcb2003())
fib_fc_lcb_2007 = factory.make(FibFcLcb2007())
fib_csw_new_data_2000 = factory.make(FibCswNewData2000())
fib_csw_new_data_2007 = factory.make(FibCswNewData2007())
