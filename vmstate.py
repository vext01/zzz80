from rpython.rlib import jit, debug, unroll
from util import bail

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]
STACKSIZE = 1024

# each arg is one green var
def get_printable_location(pc, pgm):
    return "%s:%s" % (str(pc), pgm.instrs[pc])

# The union of the red and green vars must include the live variables
# at the jit merge point.
#
# We specialise the interpreter upon the values of the green variables.
# Red variables, on the other hand, will stay variables in the trace.
jd = jit.JitDriver(
        greens = [ "pc", "self" ], # specialise.
        reds = [], # don't specialise
        get_printable_location = get_printable_location,
        )

# -- Instructions
class Instr:
    # immutable fields are, obviously, not changing after their definition.
    # The JIT can avoid superfluous lookups/reads out of constant objects.
    #
    # field[*] means that the contents of the list (which is a field) are
    # themselves constant.
    #
    # field?, means that the field is very likely to be immutable. When such
    # a field changes, an expensive invalidation of asm code occurs.
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


# This is a metaprogramming construct used below to unroll loops
# read on...
unrolling_reg_range = unroll.unrolling_iterable(range(NUM_REGS))

class VMState(object):
    _immutable_fields_ = ["instrs[*]", "label_map"]

    def __init__(self, instrs, labels):
        self.instrs = instrs
        self.label_map = labels
        self.stack = None

        # unrolls the loop via metaprogramming.
        # We resist the temptation to use a list for registers, as
        # rpython must consider the fact that mutating the list may
        # affect multiple registers (and other lists of the same type).
        # If the regsiters are separate
        # fields, then they are absolutely independent of each other and
        # of other lists of the same type.
        for i in unrolling_reg_range:
            setattr(self, "r%s" % i, 0)

    def init_stack(self, initstack):
        # The stack is a constant size list. This means that rpython
        # does not need to check if re-allocation/downsizing should
        # occur.
        self.stack = initstack + [0] * (STACKSIZE - len(initstack))
        # The next line is just an assertion of the above comment.
        debug.make_sure_not_resized(self.stack)
        self.sp = len(initstack)

    def pop(self):
        if self.sp == 0:
            bail("stack underflow")
        self.sp -= 1
        result = self.stack[self.sp]
        #self.stack[self.sp] = 0 # XXX
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
        sp = self.sp # asserting upon a field does not help type inference, use local
        assert(sp >= 0)
        return self.stack[:sp]

    def get_label(self, x):
        label = self._get_label(x)
        if label == -1:
            bail("undefined label: %s" % x)
        return label

    # An elidable function is one which behaves deterministically. The elidable
    # hint suggests that a method is elidable, even if it depends upon
    # object state. The JIT can take advantage of this.
    @jit.elidable
    def _get_label(self, key): return self.label_map.get(key, -1)

    def get_regs(self):
        rs = []
        for i in unrolling_reg_range:
            rs.append(getattr(self, "r%s" % i))

        return rs

    def run(self, initstack):
        self.init_stack(initstack)

        pc = self.r0 # green fields may not be fields

        # main interpreter loop
        while True:
            # This is the reference point for the JIT to specialise a
            # trace. For example here, if the pc is the same as a pc
            # value seen before, then we can assume the same happens as before.
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
