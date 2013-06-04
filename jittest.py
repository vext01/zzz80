# /home/edd/source/pypy/pytest.py jittest.py -s --pdb -s
import rpython.conftest

class option:
    view = False
    viewloops = True
    
rpython.conftest.option = option

from rpython.jit.metainterp.test.test_ajit import LLJitMixin
from target_zzz80 import SRC
from parse import parse

def main(ct):
    pgm = parse(SRC)
    pgm.run([ct])

class TestJit(LLJitMixin):
    def test_zzz80(self):

        self.meta_interp(main, [1000], listcomp=True, backendopt=True, listops=True)
