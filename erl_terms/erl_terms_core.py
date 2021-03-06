import re, os
import cStringIO
from parsimonious.grammar import Grammar
import parsimonious.exceptions

from objects import Atom, Proplist
from serializer import serialize

class ParseError(Exception):
    pass

def readint(text):
    if "#" in text:
        (a, b) = text.split("#", 2)
        return int(b, int(a))
    else:
        return int(text)

def transform(ast):
    if ast.expr_name == "number":
        return [float(ast.text)] if "." in ast.text else [readint(ast.text)]
    elif ast.expr_name == "boolean":
        return [ast.text=="true"]
    elif ast.expr_name == "string":
        return [ast.text[1:-1].replace(r'\"', '"')] # "something"
    elif ast.expr_name == "binary":
        return [ast.text[3:-3].replace(r'\"', '"')] # <<"something">>
    elif ast.expr_name == "atom":
        text = ast.text[1:-1] if ast.text.startswith("'") else ast.text
        return [Atom(text)]
    else:
        lis = reduce(lambda a, x: a + transform(x), ast.children, [])
        if ast.expr_name == "list":
            # if list only contains tuples with at least 2 values, we transform it to a proplist
            # (kind of dictionary)
            # TODO: allow single atoms (equivalent of {atom, true}
            #
            notuples = [elt for elt in lis if not isinstance(elt,tuple) or len(elt) != 2]
            if len(lis) > 0 and len(notuples) == 0:
                return [Proplist(lis)]

            return [lis]
        elif ast.expr_name == "map":
            return [dict(lis)]
        elif ast.expr_name in ["tuple", "keyvalue"]:
            return [tuple(lis)]
        return lis


def lex(text):
    grammar = Grammar("""\
    entry = (term _ "." _)* _
    term = boolean / atom / list / tuple / map / string / binary / number
    atom = ~"[a-z][0-9a-zA-Z_]*" / ("'" ~"[^']*" "'")
    _ = ~"\s*"
    list = ( _ "[" _ term (_ "," _ term)* _ "]" ) / ( _ "[" _ "]")
    tuple = ( _ "{" _ term (_ "," _ term)* _ "}" ) / ( _ "{" _ "}")
    map   = ( _ "#{" _ keyvalue (_ "," _ keyvalue)* _ "}" ) / ( _ "#{" _ "}")
    keyvalue = term _ "=>" _ term _
    string = '"' ~r'(\\\\"|[^"])*' '"'
    binary = "<<" string ">>"
    boolean = "true" / "false"
    number = ~"[0-9]+\#[0-9a-zA-Z]+" / ~"[0-9]+(\.[0-9]+)?(e\-?[0-9]+)?"
    """)
    nocomments = re.sub("(?m)%.*?$", "", text)
    try:
        return grammar.parse(nocomments)
    except parsimonious.exceptions.ParseError as e:
        raise ParseError(e)


def decode(text):
    return transform(lex(text))


def encode(vals, pretty=False):
    out = cStringIO.StringIO()

    cr = sp = ''
    csp = ' '
    if pretty:
        cr  = '\n'  # carriage return
        sp  = '  '  # alignment space
        csp = ''    # after-comma space

    for elt in vals:
        serialize(elt, out=out, pretty=pretty, cr=cr, sp=sp, csp=csp, depth=0)
        out.writelines(['.',csp,cr])

    if not pretty:
        # removing last space
        out.seek(-1, os.SEEK_END); out.truncate()
    return out.getvalue()


