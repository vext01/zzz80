import sys
from util import bail

# Utility Funcs
def is_reg(x):
    return True if x[0] == 'r' else False

def is_const(x):
    return not is_reg(x)

# Opcode Handlers
def nop(operands, stack, regs, pc): pass

def mov(operands, stack, regs, pc):
    if not is_reg(operands[0]): bail("MOV: type error: %s" % operands)

    if is_const(operands[1]):
        regs[operands[0][1]] = operands[1][1]
    elif is_reg(operands[1]):
        regs[operands[0][1]] = regs[operands[1][1]]
    else:
        bail("MOV: unmatched casei: %s" % operands)

# for debugging purposes - prints the state of the interpreter
def dump(operands, stack, regs, pc):
    s = sys.stderr.write
    s("--- DUMP ---\n")
    s("Registers: %s\n" % regs)
    s("Stack: %s\n" % stack)
    s("PC: %d\n" % pc)
    s("------------\n")
