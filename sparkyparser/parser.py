from .unparse.combinators import (many0,  pure,  seq,  alt,
                                  error,  zero,  bind,
                                  seq2L,  position,  not0,  many1)
from .unparse.cst import (node, cut)

(item, literal) = (position.item, position.literal)
(oneOf, not1) = (position.oneOf, position.not1)


#### some preliminaries

space         = oneOf(' \t')
not_in_string = oneOf('\n\r\f\t\v <>')
end           = not0(item)


#### tokens -- can be followed by spaces

def munch(tok):
    return seq2L(tok, many0(space))

newline, lt, gt = map(munch, [oneOf('\n\r\f'), literal('<'), literal('>')])

string = node('string',
               ('text', munch(many1(not1(not_in_string)))))

def string_c(value):
    """
    A string of `value`
    """
    return check(lambda s: s['text'] == value, string)


#### hierarchical forms

def tag(*ps):
    children = [('open', lt)] + ps + [('close', gt), ('end', alt(newline, end))]
    return node('tag', *children)

line = node('line',
             ('strings', many1(string)),
             ('newline', newline      ))

block = error('forward declaration for mutual recursion -- replace')

datum = alt(block, line)

_block = node('block',
               ('open' , tag(('name', string))     ),
               ('body' , many0(datum)              ),
               ('close', tag(('en', string_c('end')), 
                             ('name', string))))

def block_check(e):
    if e['open']['name'] == e['close']['name']:
        return pure(e)
    return cut('mismatched open/close names', zero)

block.parse = bind(_block, block_check).parse

version = tag(('ve', string_c('version')),
              ('version', string        ))

type_ = tag(('sp'  , string_c('sparky')),
            ('type', string            ),
            ('fi'  , string_c('file')  ))

project = node('project',
                ('type'   , type_       ),
                ('version', version     ),
                ('blocks' , many0(block)),
                ('end'    , end         ))

