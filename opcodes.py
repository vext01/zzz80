import sys
from util import bail

# --- Opcode Handlers
def nop(operands, program):
    program.advance_pc()

def mov(args, program):
    (o0, o1) = args

    regno = o0.evaluate(program)
    rhs = o1.evaluate(program)
    o0.set(program, rhs)

    program.advance_pc()

def add(args, program):
    (o0, o1) = args
    o0.set(program, o0.evaluate(program) + o1.evaluate(program))
    program.advance_pc()

def sub(args, program):
    (o0, o1) = args
    o0.set(program, o0.evaluate(program) - o1.evaluate(program))
    program.advance_pc()

def push(args, program):
    (o0,) = args
    program.push(o0.evaluate(program))
    program.advance_pc()

def pop(args, program):
    (o0,) = args
    o0.set(program, program.pop())
    program.advance_pc()

def jmp(args, program):
    (o0,) = args
    o0.dispatch(program)

# Jump to o0 if o1 = o2
def je(args, program):
    (o0, o1, o2) = args

    v1 = o1.evaluate(program)
    v2 = o2.evaluate(program)

    if v1 == v2: # jump is taken
        o0.dispatch(program)
    else:
        program.advance_pc()

def halt(args, program): program.set_pc(sys.maxint) # XXX hacky

def pt(args, program):
    (o0,) = args
    print(o0.evaluate(program))
    program.advance_pc()

def pick(args, program):
    (o0, o1) = args
    stack = program.get_stack()

    try:
        o0.set(program, stack[-(o1.evaluate(program) + 1)])
    except IndexError:
        bail("PICK: stack underflow")

    program.advance_pc()

# discards top of stack
def drop(args, program):
    program.pop() # ignore ret
    program.advance_pc()

def call(args, program):
    (o0,) = args
    program.push(program.get_pc() + 1) # push return addr
    o0.dispatch(program)

def ret(args, program):
    program.set_reg(0, program.pop())

# for debugging purposes - prints the state of the interpreter
def dump(args, program):
    program.dump_vm_state()
    program.advance_pc()
