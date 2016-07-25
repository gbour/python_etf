
class Atom(str):
    def __eq__(self, other):
        return isinstance(other, Atom) and super(Atom, self).__eq__(other)

    def __repr__(self):
        return "a'{0}'".format(str(self))

