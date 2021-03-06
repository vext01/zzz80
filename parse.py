import sys, string, re
import opcodes
from util import bail
from vmstate import Instr, ConstOperand, LabelOperand
from vmstate import RegOperand, VMState, REG_NAMES

# Opcode Table
# str -> [F', Z], where [F', Z] is an opcode handler fn and the # of operands
OPTAB = {
    "NOP" : (opcodes.nop, 0),
    "MOV" : (opcodes.mov, 2),
    "DUMP" : (opcodes.dump, 0),
    "ADD" : (opcodes.add, 2),
    "SUB" : (opcodes.sub, 2),
    "PUSH": (opcodes.push, 1),
    "POP": (opcodes.pop, 1),
    "JMP" : (opcodes.jmp, 1),
    "JE" : (opcodes.je, 3),
    "HALT" : (opcodes.halt, 0),
    "PT" : (opcodes.pt, 1),
    "PICK" : (opcodes.pick, 2),
    "DROP" : (opcodes.drop, 0),
    "CALL" : (opcodes.call, 1),
    "RET" : (opcodes.ret, 0),
}

# returns a tuple (x, v) where x \in {'r', 'c', 'l'} for reg/const/label
# v is then either a numeric constant, a register number or a label name
def parse_operand(x):

    # is it a register name?
    if x in REG_NAMES:
        return RegOperand(int(x[1:]))

    # is it an integer constant?
    try:
        return ConstOperand(int(x))
    except ValueError:
        pass

    return LabelOperand(x)

def parse_instr(s):
    """ Parses a simple OP [ARG1 [, ... ,ARGN]] """

    words = s.split(" ")
    opcode = words[0]
    args_raw = string.join(words[1:], "").split(",") if len(words) > 1 else []

    f, nargs = OPTAB.get(opcode, (None, -1))
    if nargs == -1: bail("unknown opcode: '%s'" % opcode)

    # check number of args is good
    num_args = len(args_raw)
    if len(args_raw) != nargs: bail("wrong arg count: %s" % opcode)

    args = [ parse_operand(x) for x in args_raw ]

    # Note that you cant reflect on functions in rpython, so we
    # have to pass the name of the opcode in aswell as the function
    # itself. Ideally we would have done: f.function_name, however,
    # this is not RPython
    return Instr(f, opcode, args)

def _strip(s):
    start, stop = 0, 0

    for start, ch in enumerate(s):
        if not ch.isspace(): break
    else:
        return ""

    for stop in range(len(s) - 1, -1, -1):
        if not s[stop].isspace(): break

    return s[start:stop + 1]

def parse(src):
    lines = src.split("\n")

    # strip cruft
    lines_p = []
    for l in lines:
        l = l.upper()

        # strip comments
        com_idx = l.find('#')

        if com_idx < 0:
            com_idx = len(l)

        #assert(com_idx >= 0)

        l = l[0:com_idx]

        # strip whitespace
        l = _strip(l)

        # no blank lines
        if len(l) == 0: continue

        lines_p.append(l)

    prog = []
    labmap = {} # str -> Z for labels.

    # generate a .text-a-like mapping
    for line in lines_p:

        # special handling of labels
        if(line.endswith(":")):
            labmap[line[0:-1]] = len(prog)
            continue

        prog.append(parse_instr(line))

    return VMState(prog[:], labmap)
