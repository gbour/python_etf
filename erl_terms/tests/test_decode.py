# -*- coding: utf8 -*-

from unittest import TestCase

from nose.tools import eq_

from erl_terms.erl_terms_core import decode
from erl_terms.objects import Atom

class DecodeEverythingTests(TestCase):
    """Tests for atoms, strings, lists and so on"""

    def test_simple_types(self):
        eq_(decode('18.'), [18])
        eq_(decode('18 .'), [18])
        eq_(decode('18.  19  . 21.'), [18, 19, 21])
        eq_(decode('18.88.'), [18.88])
        eq_(decode('1.5e-2.'), [0.015])
        eq_(decode('2#10.'), [2])
        eq_(decode('true.'), [True])
        eq_(decode('false.'), [False])
        eq_(decode('16#FF.'), [255])
        eq_(decode('atom.'), [Atom('atom')])
        eq_(decode('\'this is an atôm\'.'), [Atom('this is an atôm')])
        eq_(decode('"String".'), ['String'])
        eq_(decode('<<"Binary">>.'), ['Binary'])

    def test_list(self):
        eq_(decode('[].'), [[]])
        eq_(decode('[1].'), [[1]])
        eq_(decode('[18, 4, 9].'), [[18, 4, 9]])
        eq_(decode('[[18, 4], 9].'), [[[18, 4], 9]])

    def test_tuple(self):
        eq_(decode('{}.'), [()])
        eq_(decode('{1}.'), [(1,)])
        eq_(decode('{18, 4, 9}.'), [(18, 4, 9)])
        eq_(decode('{{18, 4}, 9}.'), [((18, 4), 9)])

    def test_string(self):
        eq_(decode('"ohai".'), [('ohai')])
        eq_(decode(r'"password:\"123\"".'), [('password:"123"')])
        eq_(decode('"ascii code \e[1;34m".'), [('ascii code \e[1;34m')])

    def test_map(self):
        eq_(decode('#{}.'), [{}])
        eq_(decode('#{ a=>1}.'), [{Atom('a'):1}])
        eq_(decode('#{a =>1, b=>2, c=>3}.'), [{Atom('a'):1, Atom('b'):2, Atom('c'):3}])
        eq_(decode('#{a=> #{a=>1, b => 2}, b=>2}.'), [{Atom('a'):{Atom('a'):1, Atom('b'):2}, Atom('b'):2}])

    def test_complex(self):
        eq_(decode('[{outer_key, #{"inner_key" => [whatever]}}, {<<"another_outer_key">>, false}]. punchline.'),
            [[(Atom('outer_key'), {'inner_key': [Atom('whatever')]}),
              ("another_outer_key",  False)],
             Atom('punchline')])

    def test_complex2(self):
        eq_(decode('["foo", <<"bar">>].'),
            [['foo', 'bar']])

    def test_comment(self):
        eq_(decode("% comment"), [])
        eq_(decode("% comment\n"), [])
        eq_(decode("% comment\n\n"), []) # check multi-line
        eq_(decode("true. % comment\n true."), [True, True])
        eq_(decode("true. % comment\n"), [True])
