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

    regno = o0.evaluate(regs)
    rhs = o1.evaluate(regs)
    o0.set(regs, rhs)

    _advance_pc(regs)

def add(args, stack, regs, lab_map):
    (o0, o1) = args
    o0.set(regs, o0.evaluate(regs) + o1.evaluate(regs))
    _advance_pc(regs)

def sub(args, stack, regs, lab_map):
    (o0, o1) = args
    o0.set(regs, o0.evaluate(regs) - o1.evaluate(regs))
    _advance_pc(regs)

def push(args, stack, regs, lab_map):
    (o0,) = args
    stack.append(o0.evaluate(regs))
    _advance_pc(regs)

def pop(args, stack, regs, lab_map):
    (o0,) = args
    o0.set(regs, _stk_pop(stack))
    _advance_pc(regs)

def jmp(args, stack, regs, lab_map):
    (o0,) = args
    if not _is_label(o0): bail("JMP: type error: %s" % args)

    regs[0] = _label_target(lab_map, _val(o0))

# XXX Tomorrow
def je(args, stack, regs, lab_map):
    (o0, o1, o2) = args

    if not _is_label(o0): bail("JE: type error: %s" % args)
    if (not _is_reg(o1)) and (not _is_const(o1)): bail("JE: type error: %s" % args)
    if (not _is_reg(o2)) and (not _is_const(o2)): bail("JE: type error: %s" % args)

    # Slipped a lambda in to see what pypy makes of it...
    # XXX inline body of lambda
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
    print(o0.evaluate(regs))
    _advance_pc(regs)

def pick(args, stack, regs, lab_map):
    (o0, o1) = args
    #if not _is_reg(o0) or not _is_const(o1): bail("PICK: type error: %s" % args)

    try:
        o0.set(regs, stack[-(o1.evaluate(regs) + 1)])
    except IndexError:
        bail("PICK: stack underflow")

    _advance_pc(regs)

# discards top of stack
def drop(args, stack, regs, lab_map):
    _stk_pop(stack)
    _advance_pc(regs)

# XXX tomorrow
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
