
from ._scales.ranges import train_continuous, train_discrete
from ._na import NA


class Range(object):

    def __init__(self):
        self.range = None

    def reset(self):
        self.range = None

    def train(self, x, drop=False):
        raise NotImplementedError()


class RangeDiscrete(Range):

    def __init__(self):
        Range.__init__(self)
        self.range = ()

    def reset(self):
        self.range = ()

    def train(self, x, drop=False):
        self.range = train_discrete(x, self.range, drop=drop)


class RangeContinuous(Range):

    def __init__(self):
        Range.__init__(self)
        self.range = (NA, NA)

    def reset(self):
        self.range = (NA, NA)

    def train(self, x, drop=False):
        self.range = train_continuous(x, self.range)
