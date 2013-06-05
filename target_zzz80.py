import sys
import os
import parse, zzz80
from util import bail

from rpython.rlib.streamio import open_file_as_stream

def main(argv):

    if len(argv) < 2:
        bail("bad usage")

    hndl = open_file_as_stream(argv[1])
    prog = parse.parse(hndl.readall())
    hndl.close()
    prog.run([int(x) for x in argv[2:]])

    return 0

def target(*args):
    return main, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

if __name__ == "__main__":
    main(sys.argv)

