import zzz80, parse

def test_mov():
    p = "MOV r1, 666"
    pgm = parse.parse(p)
    regs = pgm.run([])
    print(regs)

    assert regs[0] == 1 and regs[1] == 666
