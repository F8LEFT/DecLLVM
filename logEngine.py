__author__ = 'F8LEFT'

#for ida trace instruction
#only for arm
# from python import *

from collections import OrderedDict
from regHelper import *

from idaapi import *
from idautils import *
from idc import *

class LogEngine:
    def __init__(self):
        self.reg = OrderedDict()

    def log_start(self, saveReg, fd):
        fd.write("%-8s  %-32s  %s" % ("Address", "Instruction", "RegValue(Changed)\n"))
        for register in saveReg.reg:
            regValue = saveReg.reg[register]
            fd.write("%s=%X " % (register, regValue))
            self.reg[register] = saveReg.reg[register]
        fd.write('\n')

    def log_trace(self, curReg ,fd):
        # Address Instructions Result
        insAddr = curReg.insAddr
        fd.write("%08X  %-32s  " % (insAddr, GetDisasm(insAddr)))

        for register in curReg.reg:
            regValue = curReg.reg[register]
            if self.reg[register] != regValue:
                fd.write("%s=%X " % (register, regValue))
                self.reg[register] = regValue
        fd.write("\n")


if __name__ == "__main__":
    fd = open("F:/trace.log", "w+")
    r1 = ArmReg()
    r1.dumpReg()
    te = LogEngine()
    te.log_start(r1, fd)
    te.log_trace(r1, fd)
    StepInto()
    GetDebuggerEvent(WFNE_SUSP, -1)
    r2 = ArmReg()
    r2.dumpReg()
    te.log_trace(r2, fd)
    StepInto()
    GetDebuggerEvent(WFNE_SUSP, -1)
    r3 = ArmReg()
    r3.dumpReg()
    te.log_trace(r3, fd)
    fd.close()




