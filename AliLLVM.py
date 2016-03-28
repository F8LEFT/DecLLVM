__author__ = 'F8LEFT'

from dbgEngine import *
from regHelper import ArmReg
# '''
from idaapi import *
from idautils import *
from idc import *
# '''
# from python import *

#for Ali msc2, crackme3
#for arm
class AliLLVM(InstructionHelp):

    def __init__(self):
        InstructionHelp.__init__(self)
        self.base_address = SegStart(GetRegValue('PC'))

        self.thunk1_beg = self.base_address + 0x2A584
        self.thunk1_ret = self.base_address + 0x17FC
        self.thunk3_beg = self.base_address + 0x2A594
        self.thunk3_ret = self.base_address + 0x2004
        self.thunk4_beg = self.base_address + 0x2A5A4
        self.thunk4_ret = self.base_address + 0x1FAC
        self.thunk2_beg = self.base_address + 0x2A5C4
        self.thunk2_ret = self.base_address + 0x205C

        self.jmp_thunk = {self.thunk1_beg: self.thunk1_ret,      #jmp_thunk1
                          self.thunk2_beg: self.thunk2_ret,      #jmp_thunk2
                          self.thunk3_beg: self.thunk3_ret,      #jmp_thunk3
                          self.thunk4_beg: self.thunk4_ret       #jmp_thunk4
                          }                                 #just set breakpoint and call StepInto

        for bp in self.jmp_thunk:
            AddBpt(self.jmp_thunk.get(bp))

    def __del__(self):
        for bp in self.jmp_thunk:
            DelBpt(self.jmp_thunk.get(bp))
        InstructionHelp.__del__(self)

    def get_next_instruction(self,  regObj):
        Mnem = GetMnem(regObj.insAddr)
        if Mnem == "":                      #Err code just get lr and return
            RunTo(GetRegValue('LR') & 0xfffffffe)
            GetDebuggerEvent(WFNE_SUSP, -1)
            return 0
        if Mnem.find('B') > -1:             #Just skip function
            StepOver()
        else:
            StepInto()
        GetDebuggerEvent(WFNE_SUSP, -1)
        bAddr = BADADDR
        while bAddr != 0:
            regObj.dumpReg()
            bAddr = self.is_vm_thunk(regObj)
            if bAddr != 0:
                self.skip_jmp_thunk(bAddr)
        return bAddr

    def is_vm_thunk(self, regObj):
        instructionAddr = regObj.insAddr
        Mnem = GetMnem(instructionAddr)
        Opnd = GetOpnd(instructionAddr, 0)
        bAddr = 0
        if Mnem == 'BL':                            #may be jmp thunk 2
            bAddr = self.get_b_final_addr(instructionAddr)
        elif Mnem == 'PUSH' and Opnd == '{R0,R1,LR}':#maybe jmp thunk 1,3,4, find next 2 op, and get code
            iNext = 3
            nextAddr = instructionAddr
            while iNext > 0:
                nextAddr = nextAddr + ItemSize(nextAddr)
                Mnem1 = GetMnem(nextAddr)
                if Mnem1 == 'BL':
                    bAddr = self.get_b_final_addr(nextAddr)
                    break
                iNext = iNext - 1
        if self.jmp_thunk.get(bAddr) != None:
            return bAddr
        return 0

    def get_b_addr(self, inAddr):
        Mnem = GetMnem(inAddr)
        if Mnem.find('B') > -1:
            return LocByName(GetOpnd(inAddr, 0))
        return BADADDR

    def get_b_final_addr(self, inAddr):
        finalAddr = 0
        nextAddr = inAddr
        while nextAddr != BADADDR:
            finalAddr = nextAddr
            nextAddr = self.get_b_addr(finalAddr)
        return finalAddr

    def skip_jmp_thunk(self, address):
        if self.jmp_thunk.get(address) != None:
            GetDebuggerEvent(WFNE_CONT | WFNE_SUSP, -1)
            StepInto()
            GetDebuggerEvent(WFNE_SUSP, -1)
            return True
        return False


if __name__ == "__main__":
    ins = AliLLVM()
    reg = ArmReg()
    dbgEng = DbgEngine(reg, ins)
    fd = open("F:/trace.log", "w+")
    dbgEng.start_run(GetRegValue("PC"), 100, fd)
    fd.close()
    del dbgEng
    del reg
    del ins
