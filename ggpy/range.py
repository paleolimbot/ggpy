
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

    def train(self, x, drop=False):
        pass


class RangeContinuous(Range):

    def __init__(self):
        Range.__init__(self)

    def train(self, x, drop=False):
        pass
