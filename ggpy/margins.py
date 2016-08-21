
from ggpy._grob.unit import Unit


class Margin(Unit):

    def __init__(self, t=0, r=0, b=0, l=0, unit="pt"):
        Unit.__init__(self, (t, r, b, l), unit=unit)

    def __mul__(self, other):
        val = self.val*other
        return Margin(val[0], val[1], val[2], val[3], self.unit)

    def __rmul__(self, other):
        val = other*self.val
        return Margin(val[0], val[1], val[2], val[3], self.unit)

    def __repr__(self):
        return "Margin(t=%s, r=%s, b=%s, l=%s, unit='%s')" % (self[0], self[1], self[2], self[3], self.unit)