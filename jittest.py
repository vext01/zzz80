# This is the driver for graphical trace examination.
#
# It is a little slow, but at least allows you # to examine the traces
# that are being generated in an intuitive fashion.
#
# During testing in this way, execution is paused and a graphical
# CFG is shown. From here you can zoom in and inspect, search, etc.
# Press q or esc to continue execution until the next pause.
# When the pausing occurs is controlled by the option class.

import rpython.conftest

class option:
    view = False
    viewloops = True
    
rpython.conftest.option = option

from rpython.jit.metainterp.test.test_ajit import LLJitMixin
from parse import parse

SRC = """
POP r1
loop:
    PUSH r1
    CALL dosub
    DROP
    JE end, r1, 0
    JMP loop
end:
    DUMP
    HALT

dosub:
    PICK r1, 1
    ADD r2, 1
    SUB r1, 1
    RET
"""

def main(ct):
    pgm = parse(SRC)
    pgm.run([ct])

class TestJit(LLJitMixin):
    def test_zzz80(self):
        main(1000)
        self.meta_interp(main, [1000], listcomp=True, backendopt=True, listops=True)
