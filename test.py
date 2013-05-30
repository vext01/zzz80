#!/usr/bin/env python2.7

import sys
from subprocess import Popen, PIPE

PYTHON="python2.7"
NUM_TESTS=22

for tno in xrange(NUM_TESTS):
    p1 = Popen([PYTHON, "examples/fib.py", str(tno)], stdout=PIPE)
    expected = p1.stdout.readline().strip()

    with open("examples/fib.zzz") as f:
        p2 = Popen([PYTHON, "zzz80.py", str(tno)], stdin=f, stdout=PIPE)
        got = p2.stdout.readline().strip()

    print("TEST #%d: Expected %s got %s" % (tno, expected, got))
    if expected != got:
        print("TEST FAILIURE")
        sys.exit(1)
