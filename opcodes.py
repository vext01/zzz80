import sys
from util import bail, print_vm_state

# --- Utility Funcs
def _is_reg(x):
    return True if x[0] == 'r' else False

def _is_const(x):
    return True if x[0] == 'c' else False

def _is_label(x):
    return True if x[0] == 'l' else False

def _advance_pc(regs):
    regs[0] += 1

def _val(x): return x[1]

def _label_target(lab_map, lbl):
    try:
        return lab_map[lbl]
    except KeyError:
        bail("Bad label: %s" % lbl)

def _stk_pop(stack):
    try:
        return stack.pop()
    except IndexError:
        bail("stack underflow")

# --- Opcode Handlers
def nop(operands, stack, regs, lab_map):
    _advance_pc(regs)

def mov(args, stack, regs, lab_map):
    (o0, o1) = args

    if not _is_reg(o0): bail("MOV: type error: %s" % args)

    if _is_const(o1):
        regs[_val(o0)] = _val(o1)
    elif _is_reg(o1):
        regs[_val(o0)] = regs[_val(o1)]
    else:
        bail("MOV: unmatched case: %s" % args)

    _advance_pc(regs)

def add(args, stack, regs, lab_map):
    (o0, o1) = args

    if not _is_reg(o0): bail("ADD: type error: %s" % args)

    if _is_const(o1):
        regs[_val(o0)] += _val(o1)
    elif _is_reg(o1):
        regs[_val(o0)] += regs[_val(o1)]
    else:
        bail("ADD: unmatched case: %s" % args)

    _advance_pc(regs)

def sub(args, stack, regs, lab_map):
    (o0, o1) = args

    if not _is_reg(o0): bail("SUB: type error: %s" % args)

    if _is_const(o1):
        regs[_val(o0)] -= _val(o1)
    elif _is_reg(o1):
        regs[_val(o0)] -= regs[_val(o1)]
    else:
        bail("SUB: unmatched case: %s" % args)

    _advance_pc(regs)

def push(args, stack, regs, lab_map):
    (o0,) = args

    if _is_const(o0):
        stack.append(_val(o0))
    elif _is_reg(o0):
        stack.append(regs[_val(o0)])
    else:
        bail("PUSH: unmatched case: %s" % args)

    _advance_pc(regs)

def pop(args, stack, regs, lab_map):
    (o0,) = args
    if not _is_reg(o0): bail("POP: type error: %s" % args)

    regs[_val(o0)] = _stk_pop(stack)
    _advance_pc(regs)

def jmp(args, stack, regs, lab_map):
    (o0,) = args
    if not _is_label(o0): bail("JMP: type error: %s" % args)

    regs[0] = _label_target(lab_map, _val(o0))

def je(args, stack, regs, lab_map):
    (o0, o1, o2) = args

    if not _is_label(o0): bail("JE: type error: %s" % args)
    if (not _is_reg(o1)) and (not _is_const(o1)): bail("JE: type error: %s" % args)
    if (not _is_reg(o2)) and (not _is_const(o2)): bail("JE: type error: %s" % args)

    # Slipped a lambda in to see what pypy makes of it...
    cval = lambda x: _val(x) if _is_const(x) else regs[_val(x)]
    vals = [ cval(x) for x in [o1, o2] ]

    if vals[0] == vals[1]:
        # jump is taken
        regs[0] = _label_target(lab_map, _val(o0))
    else:
        _advance_pc(regs)

def halt(args, stack, regs, lab_map): sys.exit(0)

def pt(args, stack, regs, lab_map):
    (o0,) = args
    if not _is_reg(o0): bail("PRINT: type error: %s" % args)

    print(regs[_val(o0)])
    _advance_pc(regs)

def pick(args, stack, regs, lab_map):
    (o0,o1) = args
    if not _is_reg(o0) or not _is_const(o1): bail("PICK: type error: %s" % args)

    try:
        regs[_val(o0)] = stack[-_val(o1)]
    except IndexError:
        bail("PICK: stack underflow")

    _advance_pc(regs)

# discards top of stack
def drop(args, stack, regs, lab_map):
    _stk_pop(stack)
    _advance_pc(regs)

def call(args, stack, regs, lab_map):
    (o0,) = args
    if not _is_label(o0): bail("CALL: type error: %s" % args)

    stack.append(regs[0] + 1) # push return addr
    regs[0] = _label_target(lab_map, _val(o0))

def ret(args, stack, regs, lab_map):
    regs[0] = _stk_pop(stack)

# for debugging purposes - prints the state of the interpreter
def dump(args, stack, regs, lab_map):
    print_vm_state(regs, stack)
    _advance_pc(regs)
