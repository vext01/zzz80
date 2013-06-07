# This is the entry point for rpython to begin its analysis and
# translation; the so-called 'target'.
#
# The function "target" should return a function at which rpython
# should begins it's analysis.
#
# A function 'jitpolicy' should return a JitPolicy. The default one
# is fine in this instance.
#
# This can also be run by normal cpython or pypy for testing purposes,
# just so long as the rpython libs are available.

import sys
import os
import parse
from util import bail

from rpython.rlib.streamio import open_file_as_stream

def main(argv):

    if len(argv) < 2: bail("bad usage")

    hndl = open_file_as_stream(argv[1])
    prog = parse.parse(hndl.readall())
    hndl.close()

    args = [ int(x) for x in argv[2:] ]
    prog.run(args)

    return 0

def target(*args):
    return main, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

if __name__ == "__main__":
    main(sys.argv)
