__author__ = 'F8LEFT'

from dbgEngine import *
from regHelper import ArmReg
# '''
from idaapi import *
from idautils import *
from idc import *
# '''
# from python import *


# for 360 encrypt
# for arm
# shell
# STMFD   SP!, {R0}
# ADRL    R0, sub_7551FA34  ; next address
# SUB     R0, R0, #4
# BX      R0 ; loc_7551FA3
# LDMFD   SP!, {R0}

class S360Shell(InstructionHelp):
    def __init__(self):
        InstructionHelp.__init__(self)

    def __del__(self):
        InstructionHelp.__del__(self)

    def get_next_instruction(self, regObj):
        StepOver()
        GetDebuggerEvent(WFNE_SUSP, -1)
        regObj.dumpReg()

        isVm, addr = self.isVMStart(regObj)
        if isVm:
            return addr
        else:
            return 0

            # STMFD   SP!, {R0}
            # ADRL    R0, sub_7551FA34  ; next address
            # SUB     R0, R0, #4
            # BX      R0 ; loc_7551FA3#

    def isVMStart(self, regObj):
        insAddr1 = regObj.insAddr
        disAsm1 = GetDisasmEx(insAddr1, GENDSM_FORCE_CODE)
        if disAsm1 == "STMFD   SP!, {R0}":
            insAddr2 = insAddr1 + ItemSize(insAddr1)
            disAsm2 = GetDisasmEx(insAddr2, GENDSM_FORCE_CODE)
            if disAsm2.find("ADRL    R0") > -1:
                nextAddr = LocByName(GetOpnd(insAddr2, 1))
                return True, nextAddr
        return False, 0




if __name__ == "__main__":
    print("============360LLVMStart=================")
    ins = S360Shell()
    reg = ArmReg()
    dbgEng = DbgEngine(reg, ins)
    fd = open("F:/trace.log", "w+")
    dbgEng.start_run(GetRegValue("PC"), 50, fd)
    fd.close()
    del dbgEng
    del reg
    del ins
    print("============360LLVMEnd=================")
