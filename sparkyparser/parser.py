from .unparse.combinators import (many0,  optional,  pure,
                                  seq,       alt,   error,
                                  seq2L,  position,  not0,  many1, bind,
                                  zero)
from .unparse.cst import (node, cut)


(item, literal, satisfy) = (position.item, position.literal, position.satisfy)
(oneOf, not1, string) = (position.oneOf, position.not1, position.string)

space = oneOf(' \t')
not_in_string = oneOf('\n\r\f\t\v <>')
newline = oneOf('\n\r\f')
end = not0(item)

def munch(tok):
    return seq2L(tok, optional(space))

def tag(p):
    return node('tag',
                 ('open' , literal('<')     ),
                 ('value', p                ),
                 ('close', literal('>')     ),
                 ('end'  , alt(newline, end)))

str_ = node('string',
            ('text', munch(many1(not1(not_in_string)))))

line = node('line',
             ('strings', many1(str_)),
             ('newline', newline))

block = error('forward declaration for mutual recursion -- replace')

datum = alt(block, line)

_block = node('block',
               ('open', tag(str_)),
               ('body', many0(datum)),
               ('close', tag([munch(string('end')), str_]))) # TODO should this be a node?  so that `block_check` can get the data easily

def block_check(e):
    if e['open']['name'] == e['close']['name']:
        return pure(e)
    return cut('mismatched open/close names', zero)

block.parse = bind(_block, block_check).parse

version = tag([munch(string('version')), str_])

type_ = tag(seq(munch(string('sparky')), 
                str_, 
                munch(string('file'))))

project = node('project',
                ('type'   , type_       ),
                ('version', version     ),
                ('blocks' , many0(block)),
                ('end'    , end         ))

