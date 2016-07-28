# -*- coding: utf8 -*-

from erl_terms_core import encode, decode

def from_file(fname):
    with open(fname, 'r') as f:
        return decode(f.read())

def to_file(data, fname, pretty=True):
    with open(fname, 'w') as f:
        f.write(encode(data, pretty=pretty))


