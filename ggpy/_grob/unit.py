
from .._na import NA_character_
import numpy as np


class Unit(object):

    def __init__(self, val, unit=NA_character_):
        self.val = np.array(val)
        # TODO check if val is numeric
        try:
            self.unit = np.array(unit)
            if len(self.unit) != len(self.val):
                raise ValueError("Value and unit must be of same dimensions")
        except TypeError:
            self.unit = np.repeat(unit, len(self.val))

    def __mul__(self, other):
        return Unit(self.val*other, self.unit)

    def __rmul__(self, other):
        return Unit(other * self.val, self.unit)

    def __getitem__(self, item):
        return self.val[item]

    def __repr__(self):
        return "Unit(%s, '%s')" % (self.val, self.unit)


def concatenate_units(*units):
    return Unit(np.concatenate([u.val for u in units]), [np.concatenate(u.unit) for u in units])
