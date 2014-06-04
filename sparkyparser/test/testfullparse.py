from .. import fullparse
from ..unparse import maybeerror
import unittest as u


parse = fullparse.parse
good = maybeerror.MaybeError.pure
bad = maybeerror.MaybeError.error


class TestFullParse(u.TestCase):
    
    def testFailing(self):
        self.assertEqual(1, 2)

