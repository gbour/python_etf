# -*- coding: utf8 -*-

from unittest import TestCase

from nose.tools import eq_

from erl_terms.erl_terms_core import decode, encode
from erl_terms.objects import Atom, Proplist

class AccessorsTests(TestCase):
    """Tests for r/w accessors"""

    def test_read(self):
        [props] = decode('[{foo, bar}, {"foo", 42}, {1, true}].')
        eq_(props[Atom('foo')], Atom('bar'))
        eq_(props["foo"], 42)
        eq_(props[1], True)

        eq_(props.foo, Atom('bar'))

    def test_write(self):
        [props] = decode('[{foo, bar}, {"foo", 42}, {1, true}].')
        props.foo = Atom('baz')

        eq_(encode([props]), '[{1, true}, {foo, baz}, {"foo", 42}].')

