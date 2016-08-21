
import numpy as np


class Unit(object):

    def __init__(self, val, unit):
        self.val = np.array(val)
        # TODO check if val is numeric
        self.unit = unit

    def __mul__(self, other):
        return Unit(self.val*other, self.unit)

    def __rmul__(self, other):
        return Unit(other * self.val, self.unit)

    def __getitem__(self, item):
        return self.val[item]

    def __repr__(self):
        return "Unit(%s, '%s')" % (self.val, self.unit)