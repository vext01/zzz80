import zzz80, parse

def test_mov():
    p = "MOV r1, 666"
    pgm = parse.parse(p)
    regs = pgm.run([])
    print(regs)

    assert regs[0] == 1 and regs[1] == 666

def test_strip_empty():
    assert parse._strip("    ") == ""
    assert parse._strip(" ") == ""
    assert parse._strip("  ") == ""
    assert parse._strip("\t") == ""

def test_tab_comment_parsing():

    line = "\t# we will be trashing these"
    prog = parse.parse(line)

    assert prog.instrs == []
