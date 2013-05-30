#!/usr/bin/env python2.7

import os, sys, string
import opcodes
from util import bail

NUM_REGS = 8
REG_NAMES = [ "R%d" % x for x in range(NUM_REGS) ]

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
}

# returns a tuple (x, v) where x \in {'r', 'c'} for reg/const
# v is then either a numeric constant or a register number
def parse_operand(x):
    if x in REG_NAMES:
        return ('r', int(x[1:]))

    try:
        return ('c', int(x))
    except ValueError:
        pass

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

    # In a real language you would replace the instruction mnems with
    # integer identifiers so that interp_loop could do integer comparisons.
    # Let's see if pypy can optimise the string comparisons ;)

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

def interp_loop(prog, lab_map):

    # setup interpreter state
    stack = []
    regs = [0 for x in range(NUM_REGS)]
    pc = 0

    # main interpreter loop
    print(prog)
    while True:
        print("PC: %d" % pc)

        # fetch the instr
        if pc >= len(prog): break # end program
        instr = prog[pc]

        handler = instr[0]
        operands = instr[1:]
        print("OPCODE: %s   OPERANDS: %s" % (handler, operands))

        # dispatch the instr
        handler(operands, stack, regs, pc, lab_map)

        # advance program counter
        pc += 1

if __name__ == "__main__":
    (instr_map, lab_map) = suck_in()
    interp_loop(instr_map, lab_map)
