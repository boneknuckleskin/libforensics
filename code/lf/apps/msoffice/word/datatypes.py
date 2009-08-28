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
Structures for Microsoft Word documents.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "FcLcb", "FcPgdOld", "FcPgd", "FibHeader", "FibShorts", "FibLongs",
    "Fib", "FibFcLcb97", "FibFcLcb2000", "FibFcLcb2002", "FibFcLcb2003",
    "FibFcLcb2007", "FibCswNewData2000", "FibCswNewData2007",

    "FNIF"
]

from lf.datatype import raw, LERecord, BitTypeU16, BitTypeU8, bit, bits
from lf.windows.datatypes import (
    LONG, ULONG, USHORT, UINT8, UINT16, UINT32, UINT64, INT32, FILETIME
)

class FcLcb(LERecord):
    fc = ULONG
    lcb = ULONG
# end class FIBFCLCB

class FcPgdOld(LERecord):
    pgd = FcLcb
    bkd = FcLcb
# end class FcPgdOld

class FcPgd(LERecord):
    pgd = FcLcb
    bkd = FcLcb
    afd = FcLcb
# end class FcPgd

class FibFlags1(BitTypeU16):
    dot = bit
    glsy = bit
    complex = bit
    hasPic = bit
    quickSaves = bit

    encrypted = bit
    whichTblStm = bit
    readOnlyRecommended = bit
    writeReservation = bit
    extChar = bit
    loadOverride = bit
    farEast = bit
    crypto = bit
# end class FibFlags1

class FibFlags2(BitTypeU8):
    mac = bit
    emptySpecial = bit
    loadOverridePage = bit
    futureSavedUndo = bit
    word97Saved = bit
    spare0 = bits(3)
# end class FibFlags2

class FibHeader(LERecord):
    wIdent = UINT16
    nFib = UINT16
    nProduct = UINT16
    lid = UINT16
    pnNext = UINT16
    flags1 = FibFlags1()
    nFibBack = UINT16
    lKey = UINT32
    envr = UINT8
    flags2 = FibFlags2()
    chs = UINT16
    chsTables = UINT16
    fcMin = ULONG
    fcMac = ULONG
# end class FibHeader

class FibShorts(LERecord):
    wMagicCreated = USHORT
    wMagicRevised = USHORT
    wMagicCreatedPrivate = USHORT
    mMagicRevisedPrivate = USHORT
    pnFbpChpFirst_W6 = USHORT
    pnChpFirst_W6 = USHORT
    cpBteChp_W6 = USHORT
    pnFbpPapFirst_W6 = USHORT
    pnPapFirst_W6 = USHORT
    cpnBtePap_W6 = USHORT
    pnFbpLvcFirst_W6 = USHORT
    pnLvcFirst_W6 = USHORT
    cpnBteLvc_W6 = USHORT
    lidFE = USHORT
# end class FibShorts

class FibLongs(LERecord):
    cbMac = LONG
    lProductCreated = ULONG
    lProductRevised = ULONG
    ccpText = LONG
    ccpFtn = LONG
    ccpHdd = LONG
    ccpMcr = LONG
    ccpAtn = LONG
    ccpEdn = LONG
    ccpTxbx = LONG
    ccpHdrTxbx = LONG
    pnFbpChpFirst = LONG
    pnChpFirst = LONG
    cpnBteChp = LONG
    pnFbpBapFirst = LONG
    pnPapFirst = LONG
    cpnBtePap = LONG
    pnFbpLvcFirst = LONG
    pnLvcFirst = LONG
    cpnBteLvc = LONG
    fcIslandFirst = LONG
    fcIslandLim = LONG
# end class FibLongs

class Fib(LERecord):
    header = FibHeader
    csw = UINT16
# end class Fib

class FibFcLcb97(LERecord):
    stshOrig = FcLcb
    stshF = FcLcb
    plcfFndRef = FcLcb
    plcfFndTxt = FcLcb
    plcfAndRef = FcLcb
    plcfAndTxt = FcLcb
    plcfSed = FcLcb
    plcPad = FcLcb
    plcfPhe = FcLcb
    sttbfGlsy = FcLcb
    plcfGlsy = FcLcb
    plcfHdd = FcLcb
    plcfBteChpx = FcLcb
    plcfBtePapx = FcLcb
    plcfSea = FcLcb
    sttbfFfn = FcLcb
    plcfFldMom = FcLcb
    plcfFldHdr = FcLcb
    plcfFldFtn = FcLcb
    plcfFldAtn = FcLcb
    plcfFldMcr = FcLcb
    sttbfBkmk = FcLcb
    plcfBkf = FcLcb
    plcfBkl = FcLcb
    cmds = FcLcb
    plcMcr = FcLcb
    sttbfMcr = FcLcb
    prDrvr = FcLcb
    prEnvPort = FcLcb
    prEnvLand = FcLcb
    wss = FcLcb
    dop = FcLcb
    sttbfAssoc = FcLcb
    clx = FcLcb
    plcfPgdFtn = FcLcb
    autosaveSource = FcLcb
    GrpXstAtnOwner = FcLcb
    sttbfAtnBkmk = FcLcb
    plcDoaMom = FcLcb
    plcDoaHdr = FcLcb
    plcSpaMom = FcLcb
    plcSpaHdr = FcLcb
    plcfAtnBkf = FcLcb
    plcfAtnBkl = FcLcb
    pms = FcLcb
    formFldSttbs = FcLcb
    plcfEndRef = FcLcb
    plcfEndTxt = FcLcb
    plcfFldEdn = FcLcb
    plcfPgdEdn = FcLcb
    dggInfo = FcLcb
    sttbfRMark = FcLcb
    sttbCaption = FcLcb
    sttbAutoCaption = FcLcb
    plcfWkb = FcLcb
    plcfSpl = FcLcb
    plcfTxbxTxt = FcLcb
    plcfFldTxbx = FcLcb
    plcfHdrTxbxTxt = FcLcb
    plcfFldHdrTxbx = FcLcb
    stwUser = FcLcb
    sttbTtmbd = FcLcb
    cookieData = FcLcb
    pgdMotherOldOld = FcPgdOld
    pgdFtnOldOld = FcPgdOld
    pgdEndOldOld = FcPgdOld
    sttbfIntlFld = FcLcb
    routeSlip = FcLcb
    sttbSavedBy = FcLcb
    sttbFnm = FcLcb
    plcfLst = FcLcb
    plcfLfo = FcLcb
    plcfTxbxBkd = FcLcb
    plcfTxbxHdrBkd = FcLcb
    docUndoWord9 = FcLcb
    rgbUse = FcLcb
    usp = FcLcb
    uskf = FcLcb
    plcupcRgbUse = FcLcb
    plcupcUsp = FcLcb
    sttbGlsyStyle = FcLcb
    plgOsl = FcLcb
    plcOcx = FcLcb
    plcfBteLvc = FcLcb
    modified = FILETIME
    plcfLvcPre10 = FcLcb
    plcAsumy = FcLcb
    plcfGram = FcLcb
    sttbListNames = FcLcb
    sttbfUssr = FcLcb
# end class FibFcLcb97

class FibFcLcb2000(FibFcLcb97):
    plcfTch = FcLcb
    rmdfThreading = FcLcb
    mid = FcLcb
    sttbRgtplc = FcLcb
    msoEnvelope = FcLcb
    plcfLad = FcLcb
    rgDofr = FcLcb
    plcosl = FcLcb
    plcfCookieOld = FcLcb
    pgdMotherOld = FcPgdOld
    pgdFtnOld = FcPgdOld
    pgdEdnOld = FcPgdOld
# end class FibFcLcb2000

class FibFcLcb2002(FibFcLcb2000):
    unused = FcLcb
    plcfPgp = FcLcb
    plcfUim = FcLcb
    plfGuidUim = FcLcb
    attrdExtra = FcLcb
    plrsid = FcLcb
    sttbfBkmkFactoid = FcLcb
    plcfBkfFactoid = FcLcb
    plcfCookie = FcLcb
    plcfBklFactoid = FcLcb
    factoidData = FcLcb
    docUndo = FcLcb
    sttbfBkmkFcc = FcLcb
    plcfBkfFcc = FcLcb
    plcfBklFcc = FcLcb
    sttbfBkmkBPRepairs = FcLcb
    plcfBkfBPRepairs = FcLcb
    plcfBklBPRepairs = FcLcb
    pmsNew = FcLcb
    odso = FcLcb
    plcfPmiOldXP = FcLcb
    plcfPmiNewXP = FcLcb
    plcfPmiMixedXp = FcLcb
    encryptedProps = FcLcb
    plcfFactoid = FcLcb
    plcfLvcOldXP = FcLcb
    plcfLvcNewXP = FcLcb
    plcfLvcMixedXP = FcLcb
# end class FibFcLcb2002

class FibFcLcb2003(FibFcLcb2002):
    hplXsdr = FcLcb
    sttbBkmkSdt = FcLcb
    plcfBkfSdt = FcLcb
    plcfBklSdt = FcLcb
    customXForm = FcLcb
    sttbfBkmkProt = FcLcb
    plcfBkfProt = FcLcb
    plcfBklProt = FcLcb
    sttbProtUser = FcLcb
    plcftpc = FcLcb
    plcfPmiOld = FcLcb
    plcfPmiOldInline = FcLcb
    plcfPmiNew = FcLcb
    plcfPnewNewInline = FcLcb
    plcfLvcOld = FcLcb
    plcfLvcOldInline = FcLcb
    plcfLvcNew = FcLcb
    plcfLvcNewInline = FcLcb
    pgdMother = FcPgd
    pgdFtn = FcPgd
    pgdEdn = FcPgd
    afd = FcLcb
# end class FibFcLcb2003

class FibFcLcb2007(FibFcLcb2003):
    plcfMthd = FcLcb
    sttbfBkmkMoveFrom = FcLcb
    plcfBkfMoveFrom = FcLcb
    plcfBklMoveFrom = FcLcb
    sttbfBkmkMoveTo = FcLcb
    plcfBkfMoveTo = FcLcb
    plcfBklMoveTo = FcLcb
    unused1 = FcLcb
    unused2 = FcLcb
    unused3 = FcLcb
    sttbfBkmkArto = FcLcb
    plcfBkfArto = FcLcb
    plcfBklArto = FcLcb
    artoData = FcLcb
    unused4 = FcLcb
    unused5 = FcLcb
    unused6 = FcLcb
    ossTheme = FcLcb
    colorSchemeMapping = FcLcb
# end class FibFcLcb2007

class FibCswNewData2000(LERecord):
    quickSavesNew = UINT16
# end class FibCswNewData2000

class FibCswNewData2007(FibCswNewData2000):
    lidThemeOther = UINT16
    lidThemeFE = UINT16
    lidThemeCS = UINT16
# end class FibCswNewData2007

class FNPIBits(BitTypeU16):
    fnpt = bits(4)
    fnpd = bits(12)
# end class FNPIBits

class FNPI(LERecord):
    bit_field = FNPIBits
# end class FNPI

class FNFBBits(BitTypeU16):
    fat = bit
    unused1 = bit
    unused2 = bit
    ntfs = bit
    nonfileSys = bit
    unused3 = bits(2)
    unused4 = bit
# end class FNFBBits

class FNFB(LERecord):
    bit_field = FNFBBits
# end class FNFB

class FNIF(LERecord):
    fnpi = FNPI
    ichRelative = UINT8
    fnfb = FNFB
    unused = raw(4)
# end class FNIF
