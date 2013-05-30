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

def mov(args, stack, regs, pc):
    (o0, o1) = args

    if not is_reg(o0): bail("MOV: type error: %s" % args)

    if is_const(o1):
        regs[val(o0)] = val(o1)
    elif is_reg(o1):
        regs[val(o0)] = regs[val(o1)]
    else:
        bail("MOV: unmatched case: %s" % args)

def add(args, stack, regs, pc):
    (o0, o1) = args

    if not is_reg(o0): bail("ADD: type error: %s" % args)

    if is_const(o1):
        regs[val(o0)] += val(o1)
    elif is_reg(o1):
        regs[val(o0)] += regs[val(o1)]
    else:
        bail("ADD: unmatched case: %s" % args)

def sub(args, stack, regs, pc):
    (o0, o1) = args

    if not is_reg(o0): bail("SUB: type error: %s" % args)

    if is_const(o1):
        regs[val(o0)] += val(o1)
    elif is_reg(o1):
        regs[val(o0)] += regs[val(o1)]
    else:
        bail("SUB: unmatched case: %s" % args)

def push(args, stack, regs, pc):
    (o0,) = args

    if is_const(o0):
        stack.append(val(o0))
    elif is_reg(o0):
        stack.append(regs[val(o0)])
    else:
        bail("PUSH: unmatched case: %s" % args)

def pop(args, stack, regs, pc):
    (o0,) = args

    if not is_reg(o0): bail("POP: type error: %s" % args)

    regs[val(o0)] = stack.pop()

# for debugging purposes - prints the state of the interpreter
def dump(args, stack, regs, pc):
    s = sys.stderr.write
    s("--- DUMP ---\n")
    s("Registers: %s\n" % regs)
    s("Stack: %s\n" % stack)
    s("PC: %d\n" % pc)
    s("------------\n")
