import os

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]

def bail(x):
    os.write(2, "error: %s\n" % x)
    raise Exception()

def print_vm_state(regs, stack):
    s = os.write
    s(2, "Registers: %s\n" % regs)
    s(2, "Stack: %s\n" % stack)
