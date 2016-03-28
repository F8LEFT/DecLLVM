########################################################################
#                         DecLLVM for ida v1.2                         #
#                                  Author F8LEFT                       #
#                                  2015.12.7                           #
########################################################################

用来和OLLVM对抗的脚本。需要自己编写寻找真实指令的代码，写法可以参考360LLVM或者AliLLVM。
主要是继承 InstructionHelp 类，重写get_next_instruction方法。
get_next_instruction 返回0，调试器将会直接把当前pc，reg数据输出到文件中
返回地址，将会运行到相应的地址，然后进行输出。

程序会不断地调用get_next_instruction函数，好好弄好这个函数，应该可以弄成不错的结果，当然，效率方面就不清楚了
main函数如下
if __name__ == "__main__":
    print("============360LLVMStart=================")
    ins = C360LLVM()
    reg = ArmReg()
    dbgEng = DbgEngine(reg, ins)
    fd = open("F:/trace.log", "w+")
    dbgEng.start_run(GetRegValue("PC"), 400, fd)
    fd.close()
    del dbgEng
    del reg
    del ins
    print("============360LLVMEnd=================")

初始化DbgEngine类，传递ins类，Reg(x86,arm)类信息,同时打开log文件，就可以完成自动运行跟踪。
程序将会执行指定次数的指令，然后退出。

当然，只是个试作品，功能可能还不完善，大家将就着用着好了。
