# -*- coding: utf8 -*-

from unittest import TestCase

from nose.tools import eq_

from erl_terms.erl_terms_core import encode
from erl_terms.objects import Atom, Proplist

class EncodeEverythingTests(TestCase):
    """Tests for atoms, strings, lists and so on"""

    def test_simple_types(self):
        eq_(encode([18]), '18.')
        eq_(encode([18, 19, 21]), '18. 19. 21.')
        eq_(encode([18.88]), '18.88.')
        eq_(encode([0.015]), '0.015.')
        eq_(encode([True]), 'true.')
        eq_(encode([False]), 'false.')
        eq_(encode([Atom('atom')]), 'atom.')
        eq_(encode([Atom('this is an atôm')]), '\'this is an atôm\'.')
        eq_(encode(['String']), '"String".')
        # NOT SUPPORTED FOR NOW
        #eq_(encode(['Binary']), '<<"Binary">>')

    def test_list(self):
        eq_(encode([[]]), '[].')
        eq_(encode([[1]]), '[1].')
        eq_(encode([[18,4,9]]), '[18, 4, 9].')
        eq_(encode([[[18, 4], 9]]), '[[18, 4], 9].')
        eq_(encode([range(0,11)]), '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].')

        # pretty formatting
        eq_(encode([[]], pretty=True), '[].\n')
        eq_(encode([[[18, 4], 9]], pretty=True), '[[18, 4], 9].\n')
        eq_(encode([range(0,11)], pretty=True),
"""[
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10
].
""")

    def test_tuple(self):
        eq_(encode([()]), '{}.')
        eq_(encode([(1,)]), '{1}.')
        eq_(encode([(18, 4, 9)]), '{18, 4, 9}.')
        eq_(encode([((18, 4), 9)]), '{{18, 4}, 9}.')

        # pretty formatting
        eq_(encode([()], pretty=True), '{}.\n')
        eq_(encode([((18, 4), 9)], pretty=True), '{{18, 4}, 9}.\n')
        eq_(encode([tuple(range(0,11))], pretty=True),
"""{
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10
}.
""")

    def test_proplist(self):
        eq_(encode([Proplist({Atom('foo'): Atom('bar'), "foo": 42})]), '[{foo, bar}, {"foo", 42}].')

        # pretty formatting
        eq_(encode([Proplist({0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10})], pretty=True),
"""[
  {0, 0},
  {1, 1},
  {2, 2},
  {3, 3},
  {4, 4},
  {5, 5},
  {6, 6},
  {7, 7},
  {8, 8},
  {9, 9},
  {10, 10}
].
""")

    def test_string(self):
        eq_(encode(['ohai']), '"ohai".')
        eq_(encode(['password: "123"']), '"password: \"123\"".')
        eq_(encode(['ascii code \e[1;34m']), '"ascii code \\e[1;34m".')
        eq_(encode([]), '')

    def test_map(self):
        eq_(encode([{}]), '#{}.')
        eq_(encode([{Atom('a'): 1}]), '#{a => 1}.')
        eq_(encode([{Atom('a'): 1, Atom('b'): 2, Atom('c'): 3}]), '#{a => 1, b => 2, c => 3}.')
        eq_(encode([{Atom('a'):{Atom('a'):1, Atom('b'):2}, Atom('b'):2}]), '#{a => #{a => 1, b => 2}, b => 2}.')

        # pretty
        eq_(encode([dict([(x,x) for x in range(0,6)])], pretty=True),
"""#{
  0 => 0,
  1 => 1,
  2 => 2,
  3 => 3,
  4 => 4,
  5 => 5
}.
""")

    def test_complex(self):
        eq_(encode([Proplist({Atom('outer_key'): {'inner_key': [Atom('whatever')]},
            "another_outer_key":  False}), Atom('punchline')], pretty=True),
"""[
  {"another_outer_key", false},
  {'outer_key', #{"inner_key" => [whatever]}}
].
punchline.
""")

    # binary type not supported yet
#    def test_complex2(self):
#        eq_(decode('["foo", <<"bar">>].'),
#            [['foo', 'bar']])
#
     #TODO: add comments
#    def test_comment(self):
#        eq_(decode("% comment"), [])
#        eq_(decode("% comment\n"), [])
#        eq_(decode("% comment\n\n"), []) # check multi-line
#        eq_(decode("true. % comment\n true."), [True, True])
#        eq_(decode("true. % comment\n"), [True])
