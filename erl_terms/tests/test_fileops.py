# -*- coding: utf8 -*-

from unittest import TestCase

from nose.tools import eq_, ok_

import tempfile

#from erl_terms.erl_terms_core import encode
from erl_terms.objects import Atom, Proplist
from erl_terms.fileops import from_file, to_file

class FileOpsTests(TestCase):
    """Tests for file reading/writing"""

    def test_from_file(self):
        [conf] = from_file('./erl_terms/tests/boss.simple.config')

        ok_(isinstance(conf, Proplist))
        eq_(conf.boss.session_adapter, Atom('mock'))
        eq_(conf.lager.handlers.lager_file_backend[0][3], "$D0")

    def test_to_file(self):
        conf = Proplist({
            Atom('timer'): {
                Atom('name')  : 'atomic clock',
                Atom('start') : (2000, 01, 01, 13, 37, 00),
                Atom('each')  : 15,
                Atom('active'): True
            },

            Atom('defaults'): [1,8,12]
        })

        (fh, fname) = tempfile.mkstemp(prefix="pyetf-")
        to_file([conf], fname)

        with open(fname, 'r') as f:
            eq_(f.read(),
"""[
  {defaults, [1, 8, 12]},
  {timer, #{active => true, each => 15, name => "atomic clock", start => {
      2000,
      1,
      1,
      13,
      37,
      0
    }}}
].
""")

