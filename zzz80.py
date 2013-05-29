#!/usr/bin/env python2.7

import os, sys, string

def parse_instr(s):
    """ Parses a simple OP [ARG1 [, ... ,ARGN]] """

    words = s.split(" ")

    oper = words[0]
    args = string.join(words[1:], "").split(",") if len(words) > 1 else []

    return [oper] + args

def suck_in():
    """ Reads in the program from stdin and returns a map:
    Z -> str (instruction address to instr strings)
    """

    src = sys.stdin.read()
    lines = src.split("\n")
    
    # strip cruft
    lines = [ x.strip() for x in lines]
    lines = [ x for x in lines if len(x) > 0 and not x.startswith("#") ]

    # In a real language you would replace the instruction mnems with
    # integer identifiers so that interp_loop could do integer comparisons.
    # Let's see if pypy can optimise the string comparisons ;)

    # generate a .text-a-like mapping
    prog = dict((addr, parse_instr(lines[addr])) for addr in range(len(lines)))
    print(prog)


def interp_loop():
    pass

if __name__ == "__main__":
    instr_map = suck_in()
