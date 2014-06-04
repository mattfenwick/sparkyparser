from .unparse.combinators  import (many0,  seq2L,  count,  not0)
from .unparse.cst          import (node, cut)
from .unparse.combinators import (many0,  optional,  app,   pure,  check,
                                  seq2R,  seq,       alt,   error,
                                  seq2L,  position,  not0,  many1, bind,
                                  zero,   getState)
from .unparse.cst import (node, sepBy0, cut, addError)


(item, literal, satisfy) = (position.item, position.literal, position.satisfy)
(oneOf, not1, string) = (position.oneOf, position.not1, position.string)


space = node('space',
             ('value', many1(oneOf(' \t'))))

def munch(tok):
    return seq2L(tok, optional(space))

val = node('val',
            ('text', many1(not1(oneOf('\n\r\f\t\v ')))))

tag = node('tag',
            ('open', literal('<')),
            ('values', munch(many1(val))),
            ('close', literal('>')))


