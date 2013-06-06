RPYTHON=rpython
PYTEST=/home/edd/source/pypy/pytest.py

all:
	-echo "targets are 'trans', 'jit', 'tracegui', 'world'"

world: trans jit

trans:
	${RPYTHON} --output bin/nojit target_zzz80.py

jit:
	${RPYTHON} --output bin/jit -Ojit target_zzz80.py

test:
	${PYTEST}

tracegui:
	${PYTEST} jittest.py -s --pdb
