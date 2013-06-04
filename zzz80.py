#!/usr/bin/env python2.7

import os, sys
from util import bail, print_vm_state
from parse import suck_in

#def interp_loop(prog, stack): return prog.run(stack)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: zzz80.py <infile>")
        sys.exit(1)

    program = suck_in(sys.argv[1])

    # command line args start on the stack
    try:
        stack = [ int(x) for x in sys.argv[2:] ]
    except ValueError:
        bail("bad argv")

    program.run(stack)
