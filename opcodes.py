import sys
from util import bail

# Utility Funcs
def is_reg(x):
    return True if x[0] == 'r' else False

def is_const(x):
    return not is_reg(x)

def val(x): return x[1]

# Opcode Handlers
def nop(operands, stack, regs, pc): pass

def mov((o0, o1), stack, regs, pc):
    if not is_reg(o0): bail("MOV: type error: %s" % operands)

    if is_const(o1):
        regs[val(o0)] = val(o1)
    elif is_reg(o1):
        regs[val(o0)] = regs[val(o1)]
    else:
        bail("MOV: unmatched casei: %s" % operands)

def add(operands, stack, regs, pc):
    pass

# for debugging purposes - prints the state of the interpreter
def dump(operands, stack, regs, pc):
    s = sys.stderr.write
    s("--- DUMP ---\n")
    s("Registers: %s\n" % regs)
    s("Stack: %s\n" % stack)
    s("PC: %d\n" % pc)
    s("------------\n")
