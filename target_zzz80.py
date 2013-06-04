import sys
import parse, zzz80

SRC = """
POP r1
MOV r2, 0
loop:
    SUB r1, 1
    ADD r2, 1
    JE end, r1, 0
    JMP loop

end:
    DUMP
"""

def main(argv):

    stmts, lbls = parse.parse(SRC)
    regs = zzz80.interp_loop(stmts, lbls, [int(argv[1])])

    return 0

def target(*args):
    return main, None

if __name__ == "__main__":
    main(sys.argv)

