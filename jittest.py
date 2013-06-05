# /home/edd/source/pypy/pytest.py jittest.py -s --pdb -s
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
