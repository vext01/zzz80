import sys
from util import bail, print_vm_state

# --- Utility Funcs
def _advance_pc(regs):
    regs[0] += 1

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
    o0.dispatch(regs, lab_map)

# Jump to o0 if o1 = o2
def je(args, stack, regs, lab_map):
    (o0, o1, o2) = args

    v1 = o1.evaluate(regs)
    v2 = o2.evaluate(regs)

    if v1 == v2: # jump is taken
        o0.dispatch(regs, lab_map)
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

def call(args, stack, regs, lab_map):
    (o0,) = args
    stack.append(regs[0] + 1) # push return addr
    o0.dispatch(regs, lab_map)

def ret(args, stack, regs, lab_map):
    regs[0] = _stk_pop(stack)

# for debugging purposes - prints the state of the interpreter
def dump(args, stack, regs, lab_map):
    print_vm_state(regs, stack)
    _advance_pc(regs)
