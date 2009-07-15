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

from lf.datastruct import Extractor
from lf.apps.msoffice.word.structs import (
    FcLcb, FcPgdOld, FcPgd, FibHeader, FibShorts, FibLongs, Fib, FibFcLcb97,
    FibFcLcb2000, FibFcLcb2002, FibFcLcb2003, FibFcLcb2007, FibCswNewData2000,
    FibCswNewData2007
)

fc_lcb = Extractor(FcLcb())
fc_pgd_old = Extractor(FcPgdOld())
fc_pgd = Extractor(FcPgd())
fib_header = Extractor(FibHeader())
fib_shorts = Extractor(FibShorts())
fib_longs = Extractor(FibLongs())
fib = Extractor(Fib())
fib_fc_lcb_97 = Extractor(FibFcLcb97())
fib_fc_lcb_2000 = Extractor(FibFcLcb2000())
fib_fc_lcb_2002 = Extractor(FibFcLcb2002())
fib_fc_lcb_2003 = Extractor(FibFcLcb2003())
fib_fc_lcb_2007 = Extractor(FibFcLcb2007())
fib_csw_new_data_2000 = Extractor(FibCswNewData2000())
fib_csw_new_data_2007 = Extractor(FibCswNewData2007())
