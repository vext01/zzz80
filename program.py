from rpython.rlib import jit

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]

# each arg is one green var
def get_printable_location(pc, pgm):
    return "%s:%s" % (str(pc), pgm.instrs[pc])

jd = jit.JitDriver(
        greens = [ "pc", "self" ],
        reds = ["regs", "stack"],
        get_printable_location = get_printable_location,
        )

# -- Instructions
class Instr:
    _immutable_fields_ = ["handler", "operands[*]"]

    def __init__(self, f, opers):
        self.handler = f
        self.operands = opers

    def execute(self, stack, regs, program):
        self.handler(self.operands, stack, regs, program)

    def __str__(self):
        arg_str = ", ".join([ str(x) for x in self.operands ])
        return (self.handler.func_name + " " + arg_str)

# -- Operands
class Operand(object):
    def set(self, regs, v):
        raise TypeError("Cannot set %s to a %s" % (self, v))

class RegOperand(Operand):
    _immutable_fields_ = ["register"]
    def __init__(self, v):
        self.register = v

    def __str__(self): return "reg(%s)" % self.register

    def evaluate(self, regs): return regs[self.register]

    def set(self, regs, v):
        regs[self.register] = v

class LabelOperand(Operand):
    _immutable_fields_ = ["label"]
    def __init__(self, v):
        self.label = v

    def __str__(self): return "label(%s)" % self.label

    def dispatch(self, regs, program):
        # XXX resolve prior to runtime
        addr = program.lookup_label(self.label)
        if addr == -1: raise ValueError("unresolved label")

        regs[0] = addr # set pc

class ConstOperand(Operand):
    _immutable_fields_ = ["value"]
    def __init__(self, v):
        self.value = v

    def __str__(self): return "const(%s)" % self.value

    def evaluate(self, regs): return self.value # regs unused

class Program(object):
    _immutable_fields_ = ["instrs[*]", "label_map"]

    def __init__(self, instrs, labels):
        self.instrs = instrs
        self.label_map = labels

    @jit.elidable
    def lookup_label(self, key):
        return self.label_map.get(key, -1)

    def run(self, stack):

        # setup interpreter state
        regs = [0 for x in range(NUM_REGS)] # r0 is the PC
        pc = regs[0]

        # main interpreter loop
        while True:
            jd.jit_merge_point(pc=pc, regs=regs, self=self, stack=stack)

            # fetch the instr
            if pc >= len(self.instrs): break # end program
            instr = self.instrs[pc]
        
            instr.execute(stack, regs, self)
            pc = regs[0]

        return regs

