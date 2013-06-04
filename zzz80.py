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
    
        instr.execute(stack, regs, lab_map)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: zzz80.py <infile>")
        sys.exit(1)

    (program, label_map) = suck_in(sys.argv[1])

    # command line args start on the stack
    try:
        stack = [ int(x) for x in sys.argv[2:] ]
    except ValueError:
        bail("bad argv")

    interp_loop(program, label_map, stack)
