import sys

def bail(x):
    sys.stderr.write("error: %s\n" % x)
    sys.exit(1)
