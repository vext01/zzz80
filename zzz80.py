#!/usr/bin/env python2.7

import os, sys
from util import bail, print_vm_state, NUM_REGS, REG_NAMES
from parse import suck_in

def interp_loop(prog, lab_map, stack):

    # setup interpreter state
    regs = [0 for x in range(NUM_REGS)] # r0 is the PC

    # main interpreter loop
    while True:

        # fetch the instr
        if regs[0] >= len(prog): break # end program
        instr = prog[regs[0]]

        handler = instr[0]
        operands = instr[1:]

        # dispatch the instr
        handler(operands, stack, regs, lab_map)

        # debug
        #sys.stderr.write(str(instr) + "\n")
        #print_vm_state(regs, stack)
        #sys.stderr.write("\n\n")

if __name__ == "__main__":
    (program, label_map) = suck_in()

    # command line args start on the stack
    try:
        stack = [ int(x) for x in sys.argv[1:] ]
    except ValueError:
        bail("bad argv")

    interp_loop(program, label_map, stack)
