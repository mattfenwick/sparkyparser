from .. import parser as p
from ..unparse import maybeerror as me
from ..unparse import combinators
import unittest as u


m = me.MaybeError
l = combinators.ConsList

def good(rest, state, result):
    return m.pure({'rest': rest, 'state': state, 'result': result})

def bad(message, position):
    return m.error({'message': message, 'position': position})

def run(parser, i):
    return combinators.run(parser, i, 1)

def node(name, count, **kwargs):
    kwargs['_name'] = name
    kwargs['_state'] = count
    return kwargs

class TestCombinations(u.TestCase):

    def testLoop(self):
        self.assertEqual(1, 2)

