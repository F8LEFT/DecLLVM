from idaapi import *
from idautils import *
from idc import *

from collections import OrderedDict

class RegHelper:
    def __init__(self):
        self.reg = None
        self.insPointer = None
        self.insAddr = 0

    def dumpReg(self):
        for register in self.reg:
            self.reg[register] = GetRegValue(register)
            #if self.reg[register] != regValue:
            #    self.reg[register] = regValue
        self.insAddr = GetRegValue(self.insPointer)

class ArmReg(RegHelper):
    def __init__(self):
        RegHelper.__init__(self)
        self.reg = OrderedDict([('R0', 0), ('R1', 0), ('R2', 0), ('R3', 0), ('R4', 0), ('R5', 0),
                                ('R6', 0), ('R7', 0), ('R8', 0), ('R9', 0), ('R10', 0), ('R11', 0),
                                ('R12', 0), ('SP', 0), ('LR', 0), ('PSR', 0),
                                #flags
                                ('N', 0), ('Z', 0), ('C', 0), ('V', 0), ('Q', 0), ('F', 0), ('T', 0), ('MODE', 0)
                                ])
        self.insPointer = 'PC'

class X86Reg(RegHelper):
    def __init__(self):
        RegHelper.__init__(self)
        self.reg = OrderedDict([('EAX', 0), ('ECX', 0), ('EDX', 0), ('EBX', 0),
                                ('ESP', 0), ('EBP', 0), ('ESI', 0), ('EDI', 0)])
        self.insPointer = 'EIP'

class X64Reg(RegHelper):
    def __init__(self):
        RegHelper.__init__(self)
        self.reg = OrderedDict([('RAX', 0), ('RCX', 0), ('RDX', 0), ('RBX', 0),
                                ('RSP', 0), ('RBP', 0), ('RSI', 0), ('RDI', 0),
                                ('R8', 0), ('R9', 0), ('R10', 0), ('R11', 0),
                                ('R12', 0), ('R13', 0), ('R14', 0), ('R15', 0)])
        self.insPointer = 'RIP'
