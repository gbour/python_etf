# -*- coding: utf8 -*-

class Atom(str):
    def __eq__(self, other):
        return isinstance(other, Atom) and super(Atom, self).__eq__(other)

    def __repr__(self):
        return "a'{0}'".format(str(self))

#
#TODO: use collections.defaultdict instead of dict so we can store multiple values for one key
#      (possible in proplists)
class Proplist(dict):
    def __eq__(self, other):
        return isinstance(other, Proplist) and super(Proplist, self).__eq__(other)

    # do a search for key as atom
    def __getattr__(self, key):
        return self.get(Atom(key), None)

    # set value (key as atom)
    def __setattr__(self, key, value):
        self[Atom(key)] = value

