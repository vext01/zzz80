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

    prog = parse.parse(SRC)
    prog.run([int(argv[1])])

    return 0

def target(*args):
    return main, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

if __name__ == "__main__":
    main(sys.argv)

