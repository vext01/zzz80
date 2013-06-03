import sys, string, re
import opcodes
from util import bail, REG_NAMES

# Opcode Table
# str -> [F', Z], where [F', Z] is an opcode handler fn and the # of operands
OPTAB = {
    "NOP" : [opcodes.nop, 0],
    "MOV" : [opcodes.mov, 2],
    "DUMP" : [opcodes.dump, 0],
    "ADD" : [opcodes.add, 2],
    "SUB" : [opcodes.sub, 2],
    "PUSH": [opcodes.push, 1],
    "POP": [opcodes.pop, 1],
    "JMP" : [opcodes.jmp, 1],
    "JE" : [opcodes.je, 3],
    "HALT" : [opcodes.halt, 0],
    "PT" : [opcodes.pt, 1],
    "PICK" : [opcodes.pick, 2],
    "DROP" : [opcodes.drop, 0],
    "CALL" : [opcodes.call, 1],
    "RET" : [opcodes.ret, 0],
}

# -- Instructions
class Instr:
    def __init__(self, f, opers):
        self.handler = f
        self.operands = opers
        #operand1 = o1
        #operand2 = o2
        #operand3 = o3

    def execute(self, stack, regs, lab_map):
        self.handler(self.operands, stack, regs, lab_map)

    def __str__(self):
        arg_str = ", ".join([ str(x) for x in self.operands ])
        return (self.handler.func_name + " " + arg_str)

# -- Operands
class Operand(object):
    pass

class RegOperand(Operand):
    def __init__(self, v):
        self.register = v

    def __str__(self): return "reg(%s)" % self.register

class LabelOperand(Operand):
    def __init__(self, v):
        self.label = v

    def __str__(self): return "label(%s)" % self.label

class ConstOperand(Operand):
    def __init__(self, v):
        self.value = v

    def __str__(self): return "const(%s)" % self.value

# returns a tuple (x, v) where x \in {'r', 'c', 'l'} for reg/const/label
# v is then either a numeric constant, a register number or a label name
# XXX Use objects for instrs and operands
def parse_operand(x):

    # is it a register name?
    if x in REG_NAMES:
        return RegOperand(int(x[1:]))

    # is it an integer constant?
    try:
        return ConstOperand(int(x))
    except ValueError:
        pass

    # a label name?
    # XXX regex needs to go
    #if re.match('^[\w-]+$', x) is not None:
    #    return ('l', x)
    return LabelOperand(x)

    #bail("Bad operand: %s" % x)

def parse_instr(s):
    """ Parses a simple OP [ARG1 [, ... ,ARGN]] """

    words = s.split(" ")
    opcode = words[0]
    args_raw = string.join(words[1:], "").split(",") if len(words) > 1 else []

    optab_rec = OPTAB.get(opcode)
    if optab_rec is None: bail("unknown opcode: %s" % opcode)
    (f, nargs) = optab_rec

    # check number of args is good
    num_args = len(args_raw)
    if len(args_raw) != nargs: bail("wrong arg count: %s" % opcode)

    args = [ parse_operand(x) for x in args_raw ] #+ [ None for x in range(3 - num_args) ]
    #for i in range(3 - len(args_raw)):
    #    args.extend([None])

    return Instr(f, args)
    #return [f] + args

def suck_in():
    """ Reads in the program from stdin and returns a map:
    Z -> str (instruction address to instr strings)
    """

    src = sys.stdin.read()
    lines = src.split("\n")
    
    # strip cruft
    lines_p = []
    for l in lines:
        l = l.upper()

        # strip comments
        try:
            com_idx = l.index('#')
        except ValueError:
            com_idx = len(l)

        l = l[0:com_idx]

        # strip whitespace
        l = l.strip()

        # no blank lines
        if len(l) == 0: continue

        lines_p.append(l)

    prog = []
    labmap = dict() # str -> Z for labels.

    # generate a .text-a-like mapping
    for line in lines_p:

        # special handling of labels
        if(line.endswith(":")):
            labmap[line[0:-1]] = len(prog)
            continue

        prog.append(parse_instr(line))

    #for i in prog:
    #    print(i)
    #sys.exit(1)

    return (prog, labmap)
