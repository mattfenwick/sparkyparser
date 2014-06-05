from .unparse.combinators import (many0,  pure,  seq,  alt, fmap,
                                  error,  zero,  bind, check, get,
                                  seq2L,  position,  not0,  many1)
from .unparse.cst import (node, cut)

(item, literal) = (position.item, position.literal)
(oneOf, not1) = (position.oneOf, position.not1)


#### some preliminaries

ws            = oneOf('\n\r\f\t\v ')
space         = oneOf(' \t')
not_in_string = oneOf('\n\r\f\t\v <>')
end           = not0(item)


#### tokens -- can be followed by spaces

def munch(tok):
    return seq2L(tok, many0(space))

newline, lt, gt = map(munch, [oneOf('\n\r\f'), literal('<'), literal('>')])

string = node('string',
               ('text', fmap(''.join, munch(many1(not1(not_in_string))))))

def string_c(value):
    """
    A string of `value`
    """
    return check(lambda s: s['text'] == value, string)


#### hierarchical forms

def tag(*ps):
    children = [('open', lt)]
    children.extend(ps)
    children.append(('close', cut('>', gt)))
    children.append(('end', cut('newline or end', alt(newline, end))))
    return node('tag', *children)

line = node('line',
             ('strings', many1(string)),
             ('newline', newline      ))

block = error('forward declaration for mutual recursion -- replace')

datum = alt(block, line)

_not_end = check(lambda x: x['text'] != 'end', string)

_block = node('block',
               ('open' , tag(('name', many1(_not_end)))),
               ('body' , many0(datum)                  ),
               ('close', tag(('en', string_c('end')    ), 
                             ('name', many1(string)))  ))

def block_check(e):
    n1s = [n['text'] for n in e['open']['name']] 
    n2s = [n['text'] for n in e['close']['name']]
    if n1s == n2s:
        return pure(e)
    return cut('mismatched open/close names -- %s and %s' % (n1s, n2s), zero)

block.parse = bind(_block, block_check).parse

version = tag(('ve', string_c('version')),
              ('version', string        ))

type_ = tag(('sp'  , string_c('sparky')),
            ('type', string            ),
            ('fi'  , string_c('file')  ))

project = node('project',
                ('open-ws', many0(ws)               ),
                ('type'   , cut('type', type_)      ),
                ('version', cut('version', version) ),
                ('blocks' , many0(block)            ),
                ('end-ws' , many0(ws)               ),
                ('end'    , cut('end of input', end)))

