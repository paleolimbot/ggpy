
from .._na import NA_character_
import numpy as np


class Unit(object):

    def __init__(self, val, unit=NA_character_):
        self.val = val
        self.unit = unit
        if len(np.shape(self.val)) != 0:
            raise TypeError("Cannot use more than one value in a unit object")
        if len(np.shape(self.unit)) != 0:
            raise TypeError("Cannot use more than one unit in a unit object")

    def __float__(self):
        return float(self.val)

    def __mul__(self, other):
        return Unit(self.val*other, self.unit)

    def __rmul__(self, other):
        return Unit(other * self.val, self.unit)

    def __repr__(self):
        return "Unit(%s, '%s')" % (self.val, self.unit)


def concatenate_units(*units):
    return list(units)
