import sys
from util import bail

# Utility Funcs
def is_reg(x):
    return True if x[0] == 'r' else False

def is_const(x):
    return True if x[0] == 'c' else False

def is_label(x):
    return True if x[0] == 'l' else False

def advance_pc(regs):
    regs[0] += 1

def val(x): return x[1]

# Opcode Handlers
def nop(operands, stack, regs, lab_map):
    advance_pc(regs)

def mov(args, stack, regs, lab_map):
    (o0, o1) = args

    if not is_reg(o0): bail("MOV: type error: %s" % args)

    if is_const(o1):
        regs[val(o0)] = val(o1)
    elif is_reg(o1):
        regs[val(o0)] = regs[val(o1)]
    else:
        bail("MOV: unmatched case: %s" % args)

    advance_pc(regs)

def add(args, stack, regs, lab_map):
    (o0, o1) = args

    if not is_reg(o0): bail("ADD: type error: %s" % args)

    if is_const(o1):
        regs[val(o0)] += val(o1)
    elif is_reg(o1):
        regs[val(o0)] += regs[val(o1)]
    else:
        bail("ADD: unmatched case: %s" % args)

    advance_pc(regs)

def sub(args, stack, regs, lab_map):
    (o0, o1) = args

    if not is_reg(o0): bail("SUB: type error: %s" % args)

    if is_const(o1):
        regs[val(o0)] += val(o1)
    elif is_reg(o1):
        regs[val(o0)] += regs[val(o1)]
    else:
        bail("SUB: unmatched case: %s" % args)

    advance_pc(regs)

def push(args, stack, regs, lab_map):
    (o0,) = args

    if is_const(o0):
        stack.append(val(o0))
    elif is_reg(o0):
        stack.append(regs[val(o0)])
    else:
        bail("PUSH: unmatched case: %s" % args)

    advance_pc(regs)

def pop(args, stack, regs, lab_map):
    (o0,) = args

    if not is_reg(o0): bail("POP: type error: %s" % args)

    regs[val(o0)] = stack.pop()
    advance_pc(regs)

def jmp(args, stack, regs, lab_map):
    (o0,) = args

    if not is_label(o0): bail("JMP: type error: %s" % args)

    regs[0] = lab_map[val(o0)]

# for debugging purposes - prints the state of the interpreter
def dump(args, stack, regs, lab_map):
    s = sys.stderr.write
    s("--- DUMP ---\n")
    s("Registers: %s\n" % regs)
    s("Stack: %s\n" % stack)
    s("------------\n")
    advance_pc(regs)
