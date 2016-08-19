
from .._na import is_nan, NA


class Palette(dict):

    def __init__(self, na_value=NA, **kwargs):
        dict.__init__(self, **kwargs)
        self.na_value = na_value

    def __getitem__(self, item):
        return self.na_value if is_nan(item) or item not in self else dict.__getitem__(self, item)


class PaletteDiscrete(Palette):

    def __init__(self, n=0, na_value=NA):
        Palette.__init__(self, na_value=na_value)
        for i in range(n):
            self[i] = i
