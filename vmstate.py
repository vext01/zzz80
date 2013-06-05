from rpython.rlib import jit
from util import bail

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]

# each arg is one green var
def get_printable_location(pc, pgm):
    return "%s:%s" % (str(pc), pgm.instrs[pc])

jd = jit.JitDriver(
        greens = [ "pc", "self" ], # stuff at a jit merge
        #reds = ["regs", "stack"], # don't try to optimise on these
        reds = [],
        get_printable_location = get_printable_location,
        )

# -- Instructions
class Instr:
    _immutable_fields_ = ["handler", "operands[*]"]

    def __init__(self, f, opers):
        self.handler = f
        self.operands = opers

    def execute(self, program):
        self.handler(self.operands, program)

    def __str__(self):
        arg_str = ", ".join([ str(x) for x in self.operands ])
        return (self.handler.func_name + " " + arg_str)

# -- Operands
class Operand(object):
    def set(self, program, v):
        raise TypeError("Cannot set %s to a %s" % (self, v))

class RegOperand(Operand):
    _immutable_fields_ = ["register"]

    def __init__(self, v):
        self.register = v

    def __str__(self): return "reg(%s)" % self.register
    def evaluate(self, program): return program.get_reg(self.register)
    def set(self, program, v): program.set_reg(self.register, v)

class LabelOperand(Operand):
    _immutable_fields_ = ["label"]

    def __init__(self, v):
        self.label = v

    def __str__(self): return "label(%s)" % self.label
    def dispatch(self, program): program.set_pc(program.get_label(self.label))

class ConstOperand(Operand):
    _immutable_fields_ = ["value"]

    def __init__(self, v):
        self.value = v

    def __str__(self): return "const(%s)" % self.value
    def evaluate(self, program): return self.value

class VMState(object):
    _immutable_fields_ = ["instrs[*]", "label_map"]

    def __init__(self, instrs, labels):
        self.instrs = instrs
        self.label_map = labels
        self.stack = None
        self.regs = [0 for x in range(NUM_REGS)] # r0 is the PC

    @jit.elidable
    def lookup_label(self, key): return self.label_map.get(key, -1)

    def pop(self):
        try:
            return self.stack.pop()
        except ValueError:
            bail("stack underflow")

    def push(self, x): self.stack.append(x)
    def advance_pc(self): self.regs[0] += 1
    def set_pc(self, x): self.regs[0] = x
    def get_pc(self): return self.regs[0]
    def set_reg(self, r, v): self.regs[r] = v
    def get_reg(self, x): return self.regs[x]
    def get_stack(self): return self.stack

    def get_label(self, x):
        try:
            return self.label_map[x]
        except KeyError:
            bail("undefined label: %s" % x)

    def run(self, stack):
        pc = self.regs[0]
        self.stack = stack

        # setup interpreter state
        # main interpreter loop
        while True:
            jd.jit_merge_point(pc=pc, self=self)

            # fetch the instr
            if pc >= len(self.instrs): break # end program
            instr = self.instrs[pc]
        
            instr.execute(self)
            pc = self.regs[0]

        return self.regs

    def dump_vm_state(self):
        print("stack: " + str(self.stack))
        print("regs: " + str(self.regs))
