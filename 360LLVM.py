__author__ = 'F8LEFT'

from dbgEngine import *
from regHelper import ArmReg
# '''
from idaapi import *
from idautils import *
from idc import *
# '''
# from python import *

vReg = 'R0'
# vReg = 'R7'
# for 360 Android Crackme
#for arm
# find mov R0,xxxxxxxx, mov R0,xxxxxxxx, B xxxxxxxx
# mov R1,same as R0
class C360LLVM(InstructionHelp):

    def __init__(self):
        InstructionHelp.__init__(self)


    def __del__(self):
        InstructionHelp.__del__(self)

    def get_next_instruction(self,  regObj):
        Mnem = GetMnem(regObj.insAddr)
        if Mnem == "":                      #Err code just get lr and return
            RunTo(GetRegValue('LR') & 0xfffffffe)
            GetDebuggerEvent(WFNE_SUSP, -1)
            return 0
        inss = regObj.insAddr
        while True:
            regObj.dumpReg()
            isVm, addr = self.isVMStart(regObj)
            if isVm:
                print("isVMStart %x" %reg.insAddr)
                RunTo(addr)
                GetDebuggerEvent(WFNE_SUSP, -1)
                StepOver()
                GetDebuggerEvent(WFNE_SUSP, -1)
            regObj.dumpReg()
            isBody = self.isVMBody(regObj)
            skipBody = isBody
            while skipBody:
                StepOver()
                GetDebuggerEvent(WFNE_SUSP, -1)
                regObj.dumpReg()
                skipBody = self.isVMBody(regObj)
        # while isBody:
            #     print("isVMBody %x" %reg.insAddr)
            #     regObj.dumpReg()
            #     isBodyEnd, addr = self.isVMBodyEnd(regObj)
            #     if isBodyEnd:
            #         RunTo(addr)
            #         GetDebuggerEvent(WFNE_SUSP, -1)
            #         StepOver()
            #         GetDebuggerEvent(WFNE_SUSP, -1)
            #         break
            #     StepOver()
            #     GetDebuggerEvent(WFNE_SUSP, -1)
            if isVm == False and isBody == False:
                break

        regObj.dumpReg()
        if inss == regObj.insAddr:
            StepOver()
            GetDebuggerEvent(WFNE_SUSP, -1)
        return 0



#mov R0, #0x00000000
    #mov R0, #0x00000000
    #B 0x00000000
    def isVMStart(self, regObj):
        instructionAddr = regObj.insAddr
        Mnem = GetMnem(instructionAddr)
        if Mnem.find('MOV') > -1:           #
            Opnd = GetOpnd(instructionAddr, 0)
            if (Opnd == vReg):              #mov R0, #0x00000000
                bFind = False
                iNext = 2
                nextAddr = instructionAddr
                while iNext > 0:
                    nextAddr = nextAddr + ItemSize(nextAddr)
                    Mnem = GetMnem(nextAddr)
                    Opnd = GetOpnd(nextAddr, 0)
                    if Mnem.find('MOV') > -1 and Opnd == vReg:
                        pass
                    elif Mnem.find('B') > -1:
                        bFind = True
                        break
                    iNext = iNext - 1
                return bFind, nextAddr
        return False, 0

    #mov R1, 0x00000000
    #cmp R0,R1
    #BNE
    def isVMBodyEnd(self, regObj):
        instructionAddr = regObj.insAddr
        ads = '#0x%X' %regObj.reg[vReg]
        Mnem = GetMnem(instructionAddr)
        if Mnem.find('MOV') > -1:           #
            Opnd = GetOpnd(instructionAddr, 0)
            Opnd2 = GetOpnd(instructionAddr, 1)
            if Opnd == 'R1' and ads == Opnd2:              #mov R1, #0x00000000
                bFind = False
                iNext = 2
                nextAddr = instructionAddr
                while iNext > 0:
                    nextAddr = nextAddr + ItemSize(nextAddr)
                    Mnem = GetMnem(nextAddr)
                    if Mnem.find('B') > -1:
                        bFind = True
                        break
                    iNext = iNext - 1
                return bFind, nextAddr
        return False, 0

    # cmp R0,xxxxxxxx
    # B xxxxxxxx
    def isVMBody(self, regObj):
        instructionAddr = regObj.insAddr
        nextAddr = instructionAddr
        Mnem = GetMnem(nextAddr)
        Opnd = GetOpnd(nextAddr, 0)

        nextAddr = nextAddr + ItemSize(nextAddr)
        Mnem2 = GetMnem(nextAddr)
        Opnd2 = GetOpnd(nextAddr, 0)

        nextAddr = nextAddr + ItemSize(nextAddr)
        Mnem3 = GetMnem(nextAddr)
        Opnd3 = GetOpnd(nextAddr, 0)
        if Mnem.find('B') > -1:
            return True
        if Mnem.find('CMP') > -1 and Opnd == vReg:
            if Mnem2.find("B") > -1:
                return True
        if Mnem2.find('CMP') > -1 and Opnd2 == vReg:
            if Mnem3.find('B') > -1:
                return True
        return False




if __name__ == "__main__":
    print("============360LLVMStart=================")
    ins = C360LLVM()
    reg = ArmReg()
    dbgEng = DbgEngine(reg, ins)
    fd = open("F:/trace.log", "w+")
    dbgEng.start_run(GetRegValue("PC"), 1000, fd)
    fd.close()
    del dbgEng
    del reg
    del ins
    print("============360LLVMEnd=================")

