from rpython.rlib import jit, debug, unroll
from util import bail

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]
STACKSIZE = 1024

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


unrolling_reg_range = unroll.unrolling_iterable(range(NUM_REGS))

class VMState(object):
    _immutable_fields_ = ["instrs[*]", "label_map"]

    def __init__(self, instrs, labels):
        self.instrs = instrs
        self.label_map = labels
        self.stack = None
        #self.regs = [0 for x in range(NUM_REGS)] # r0 is the PC

        # because the register accesses are constant for a give pc value,
        # if the registers are individual fields, then the tracer can
        # optimise, as fields may not affect each other.
        for i in unrolling_reg_range:
            setattr(self, "r%s" % i, 0)

    def init_stack(self, initstack):
        self.stack = initstack + [0] * (STACKSIZE - len(initstack))
        debug.make_sure_not_resized(self.stack)
        self.sp = len(initstack)

    def pop(self):
        if self.sp == 0:
            bail("stack underflow")
        self.sp -= 1
        result = self.stack[self.sp]
        #self.stack[self.sp] = 0
        return result

    def push(self, x):
        if self.sp >= STACKSIZE:
            bail("stack overflow")
        self.stack[self.sp] = x
        self.sp += 1

    def pick(self, x):
        index = self.sp - x - 1
        if not (0 <= index < self.sp):
            bail("stack underflow")
        return self.stack[index]

    def advance_pc(self): self.r0 += 1
    def set_pc(self, x): self.r0 = x
    def get_pc(self): return self.r0
    def set_reg(self, r, v):
        for i in unrolling_reg_range:
            if r == i:
                setattr(self, "r%s" % i, v)
                break
        else:
            bail("unknown register %s" % r)

    def get_reg(self, x):
        for i in unrolling_reg_range:
            if x == i:
                return getattr(self, "r%s" % i)
        bail("unknown register %s" % x)

    def get_stack(self):
        sp = self.sp
        assert(sp >= 0)
        return self.stack[:sp]

    def get_label(self, x):
        label = self._get_label(x)
        if label == -1:
            bail("undefined label: %s" % x)
        return label

    @jit.elidable
    def _get_label(self, key): return self.label_map.get(key, -1)

    def get_regs(self):
        rs = []
        for i in unrolling_reg_range:
            rs.append(getattr(self, "r%s" % i))

        return rs

    def run(self, initstack):
        self.init_stack(initstack)

        # XXX pc local still needed?
        pc = self.r0

        # setup interpreter state
        # main interpreter loop
        while True:
            jd.jit_merge_point(pc=pc, self=self)

            # fetch the instr
            if pc >= len(self.instrs): break # end program
            instr = self.instrs[pc]
        
            instr.execute(self)
            pc = self.r0

        return self.get_regs()

    def dump_vm_state(self):
        print("stack: " + str(self.get_stack()))
        print("regs: " + str(self.get_regs()))
