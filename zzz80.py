#!/usr/bin/env python2.7

import os, sys
from util import bail, print_vm_state, NUM_REGS, REG_NAMES
from parse import suck_in
from rpython.rlib import jit

# each arg is one green var
def get_printable_location(pc):
    return str(pc)

jd = jit.JitDriver(
        greens = [ "pc" ],
        reds = ["regs", "prog", "lab_map", "stack"],
        get_printable_location = get_printable_location,
        )

def interp_loop(prog, lab_map, stack):

    # setup interpreter state
    regs = [0 for x in range(NUM_REGS)] # r0 is the PC
    pc = regs[0]

    # main interpreter loop
    while True:
        jd.jit_merge_point(pc=pc, regs=regs, prog=prog, lab_map=lab_map, stack=stack)

        # fetch the instr
        if pc >= len(prog): break # end program
        instr = prog[pc]
    
        instr.execute(stack, regs, lab_map)
        pc = regs[0]

    return regs

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
