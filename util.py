import sys

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]

def bail(x):
    sys.stderr.write("error: %s\n" % x)
    sys.exit(1)

def print_vm_state(regs, stack):
    s = sys.stderr.write
    s("Registers: %s\n" % regs)
    s("Stack: %s\n" % stack)
