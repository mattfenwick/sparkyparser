from . import parser
from .unparse.cst import cut
from .unparse.combinators import run
from .unparse.maybeerror import MaybeError
import sys


def project(string):
    '''
    Parse a string according to the Sparky project file syntax.
    '''
    out = run(parser.project, string, (1, 1))
    if out.status == 'error':
        print 'error while parsing:'
        for (message, (line, col)) in out.value:
            print '  at line %s, column %s: %s' % (line, col, message)
    else:
        print 'success: ', out
#    return run(parser.tag(('a', parser.string), 
#                          ('b', cut('oops', parser.string_c('def')))), 
#               string, 
#               (1, 1))


def save(string):
    raise ValueError('unimplemented')


if __name__ == "__main__":
    print sys.argv
    path = sys.argv[1]
    contents = open(path, 'r').read()
    # contents = sys.stdin.read()
    print project(contents)

