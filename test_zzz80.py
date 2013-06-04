import zzz80, parse

def test_mov():
    p = "MOV r1, 666"
    stmts, lbls = parse.parse(p)
    regs = zzz80.interp_loop(stmts, lbls, [])
    print(regs)

    assert regs[0] == 1 and regs[1] == 666
