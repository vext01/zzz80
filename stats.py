import time, os, sys
#import matplotlib.pyplot as plt

NUM_TESTS = 10

def time_exec(cmd):
    t0 = time.time()
    os.system(cmd)
    t1 = time.time()
    return t1 - t0

if __name__ == "__main__":
    times_nojit = [0 for x in range(NUM_TESTS) ]
    times_jit = []
    for tno in xrange(NUM_TESTS):
        print("running test #%s" % tno)
        #nojit = time_exec("./bin/nojit %s" % 10**tno)
        jit = time_exec("./bin/jit %s" % 10**tno)

        #times_nojit.append(nojit)
        times_jit.append(jit)

    print("Done:")
    print(times_nojit)
    print(times_jit)

    from prettytable import PrettyTable
    t = PrettyTable(["Iterations", "No Jit (s)", "Jit (s)"])
    t.align[1] = "r"
    t.align[2] = "r"

    for i in xrange(NUM_TESTS):
        t.add_row(["10^%s" % i, times_nojit[i], times_jit[i]])

    print(t)


    #plt.plot([10**x for x in xrange(NUM_TESTS)], times_nojit, "ro")
    #plt.plot([10**x for x in xrange(NUM_TESTS)], times_jit, "go")
    #plt.xlabel("loop iterations")
    #plt.ylabel("time (s)")
    #plt.show()


