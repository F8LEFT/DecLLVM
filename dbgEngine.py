__author__ = 'F8LEFT'

#for ida debug loop
#collect breakpoint

# from python import *


from idaapi import *
from idautils import *
from idc import *


from logEngine import *
from regHelper import ArmReg


class InstructionHelp:
    def __init__(self):
        self.saveBp = {}
        for i in range(0, GetBptQty()):
            bptea = GetBptEA(i)
            self.saveBp[bptea] = GetBptAttr(bptea, BPTATTR_FLAGS)
        for bp in self.saveBp:
            EnableBpt(bp, 0)

    def __del__(self):
        for bp in self.saveBp:
            SetBptAttr(bp, BPTATTR_FLAGS, self.saveBp[bp])

    def get_next_instruction(self, regObj):
        StepInto()
        return 0



class DbgEngine:
    def __init__(self, regHelper, insObj):
        self.addr = 0
        regHelper.dumpReg()
        self.tracer = LogEngine()
        self.ins = insObj
        self.regis = regHelper

    def start_run(self, startAddr, count, logfd):
        GetDebuggerEvent(WFNE_SUSP, -1)
        pc = GetRegValue("PC")
        if pc != startAddr:
            RunTo(startAddr)
        GetDebuggerEvent(WFNE_SUSP, -1)

        self.regis.dumpReg()
        self.tracer.log_start(self.regis, logfd)
        self.tracer.log_trace(self.regis, logfd)
        while count > 0:
            nextReg = self.ins.get_next_instruction(self.regis)
            if nextReg != 0:
                RunTo(nextReg)
            GetDebuggerEvent(WFNE_SUSP, -1)
            if not isCode(getFlags(nextReg)):
                MakeCode(nextReg)
            self.regis.dumpReg()
            self.tracer.log_trace(self.regis, logfd)
            count -= 1
        return True


if __name__ == "__main__":
    ins = InstructionHelp()
    reg = ArmReg()
    dbgEng = DbgEngine(reg, ins)
    fd = open("F:/trace.log", "w+")
    dbgEng.start_run(GetRegValue("PC"), 2, fd)
    fd.close()
