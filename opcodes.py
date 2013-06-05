import sys
from util import bail

# --- Opcode Handlers
def nop(operands, vm_state):
    vm_state.advance_pc()

def mov(args, vm_state):
    (o0, o1) = args

    regno = o0.evaluate(vm_state)
    rhs = o1.evaluate(vm_state)
    o0.set(vm_state, rhs)

    vm_state.advance_pc()

def add(args, vm_state):
    (o0, o1) = args
    o0.set(vm_state, o0.evaluate(vm_state) + o1.evaluate(vm_state))
    vm_state.advance_pc()

def sub(args, vm_state):
    (o0, o1) = args
    o0.set(vm_state, o0.evaluate(vm_state) - o1.evaluate(vm_state))
    vm_state.advance_pc()

def push(args, vm_state):
    (o0,) = args
    vm_state.push(o0.evaluate(vm_state))
    vm_state.advance_pc()

def pop(args, vm_state):
    (o0,) = args
    o0.set(vm_state, vm_state.pop())
    vm_state.advance_pc()

def jmp(args, vm_state):
    (o0,) = args
    o0.dispatch(vm_state)

# Jump to o0 if o1 = o2
def je(args, vm_state):
    (o0, o1, o2) = args

    v1 = o1.evaluate(vm_state)
    v2 = o2.evaluate(vm_state)

    if v1 == v2: # jump is taken
        o0.dispatch(vm_state)
    else:
        vm_state.advance_pc()

def halt(args, vm_state): vm_state.set_pc(sys.maxint) # XXX hacky

def pt(args, vm_state):
    (o0,) = args
    print(o0.evaluate(vm_state))
    vm_state.advance_pc()

def pick(args, vm_state):
    (o0, o1) = args
    stack = vm_state.get_stack()

    try:
        o0.set(vm_state, stack[-(o1.evaluate(vm_state) + 1)])
    except IndexError:
        bail("PICK: stack underflow")

    vm_state.advance_pc()

# discards top of stack
def drop(args, vm_state):
    vm_state.pop() # ignore ret
    vm_state.advance_pc()

def call(args, vm_state):
    (o0,) = args
    vm_state.push(vm_state.get_pc() + 1) # push return addr
    o0.dispatch(vm_state)

def ret(args, vm_state):
    vm_state.set_reg(0, vm_state.pop())

# for debugging purposes - prints the state of the interpreter
def dump(args, vm_state):
    vm_state.dump_vm_state()
    vm_state.advance_pc()
