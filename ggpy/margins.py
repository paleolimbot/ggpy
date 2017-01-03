
from ggpy._grob.unit import Unit


class Margin(object):

    def __init__(self, t=0, r=0, b=0, l=0, unit="pt"):
        self.t = Unit(t, unit)
        self.r = Unit(r, unit)
        self.b = Unit(b, unit)
        self.l = Unit(l, unit)
        self.unit = unit

    def __mul__(self, other):
        val = [val*other for val in (self.t, self.r, self.b, self.l)]
        return Margin(val[0], val[1], val[2], val[3], self.unit)

    def __rmul__(self, other):
        val = [other * val for val in (self.t, self.r, self.b, self.l)]
        return Margin(val[0], val[1], val[2], val[3], self.unit)

    def __repr__(self):
        return "Margin(t=%s, r=%s, b=%s, l=%s, unit='%s')" % (self.t, self.r, self.b, self.l, self.unit)
