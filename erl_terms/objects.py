
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
