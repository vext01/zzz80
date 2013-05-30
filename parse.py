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

# returns a tuple (x, v) where x \in {'r', 'c', 'l'} for reg/const/label
# v is then either a numeric constant, a register number or a label name
def parse_operand(x):

    # is it a register name?
    if x in REG_NAMES:
        return ('r', int(x[1:]))

    # is it an integer constant?
    try:
        return ('c', int(x))
    except ValueError:
        pass

    # a label name?
    if re.match('^[\w-]+$', x) is not None:
        return ('l', x)

    bail("Bad operand: %s" % x)

def parse_instr(s):
    """ Parses a simple OP [ARG1 [, ... ,ARGN]] """

    words = s.split(" ")
    opcode = words[0]
    args_raw = string.join(words[1:], "").split(",") if len(words) > 1 else []

    optab_rec = OPTAB.get(opcode)
    if optab_rec is None: bail("unknown opcode: %s" % opcode)
    (f, nargs) = optab_rec

    # check number of args is good
    if len(args_raw) != nargs: bail("wrong arg count: %s" % opcode)

    args = [ parse_operand(x) for x in args_raw ]
    return [f] + args

def suck_in():
    """ Reads in the program from stdin and returns a map:
    Z -> str (instruction address to instr strings)
    """

    src = sys.stdin.read()
    lines = src.split("\n")
    
    # strip cruft
    lines = [ x.strip() for x in lines]
    lines = [ x.upper() for x in lines if len(x) > 0 and not x.startswith("#") ]

    prog = []
    labmap = dict() # str -> Z for labels.

    # generate a .text-a-like mapping
    for line in lines:

        # special handling of labels
        if(line.endswith(":")):
            labmap[line[0:-1]] = len(prog)
            continue

        prog.append(parse_instr(line))

    return (prog, labmap)
