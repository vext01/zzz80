import time, os, sys
import matplotlib.pyplot as plt

ENV = "PYTHONPATH=/home/edd/source/pypy"

def time_exec(cmd):
    t0 = time.time()
    os.system(cmd)
    t1 = time.time()
    return t1 - t0

if __name__ == "__main__":
    #times_cpy = []
    #times_pypy = []

    if len(sys.argv) < 2:
        print("specify num tests")
        sys.exit(1)

    NUM_TESTS = int(sys.argv[1])
    times_nojit = []
    times_jit = []
    for tno in xrange(NUM_TESTS):
        print("running test #%s" % tno)
        #cpy = time_exec("%s python target_zzz80.py examples/fib.zzz %s" % (ENV, tno))
        #pypy = time_exec("%s pypy target_zzz80.py examples/fib.zzz %s" % (ENV, tno))
        nojit = time_exec("./bin/nojit examples/fib.zzz %s" % tno)
        jit = time_exec("./bin/jit examples/fib.zzz %s" % tno)

        #times_cpy.append(cpy)
        #times_pypy.append(pypy)
        times_nojit.append(nojit)
        times_jit.append(jit)

    print("Done:")
    print(times_nojit)
    print(times_jit)

    from prettytable import PrettyTable
    #t = PrettyTable(["FIB #", "CPython", "PyPy", "No Jit", "Jit"])
    t = PrettyTable(["FIB #", "No Jit", "Jit"])
    t.align[1] = "r"
    t.align[2] = "r"
    #t.align[3] = "r"
    #t.align[4] = "r"

    for i in xrange(NUM_TESTS):
        #t.add_row([i, times_cpy[i], times_pypy[i], times_nojit[i], times_jit[i]])
        t.add_row([i, times_nojit[i], times_jit[i]])

    print(t)

    #plt.plot([x for x in xrange(NUM_TESTS)], times_cpy)
    #plt.plot([x for x in xrange(NUM_TESTS)], times_pypy)
    plt.plot([x for x in xrange(NUM_TESTS)], times_nojit, label="No JIT", marker="x", linestyle="-")
    plt.plot([x for x in xrange(NUM_TESTS)], times_jit, label="JIT", marker="x", linestyle="-")
    plt.xlabel("FIB Number")
    plt.ylabel("time (s)")
    plt.legend()
    plt.show()


