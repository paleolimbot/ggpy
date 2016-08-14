
from .aes import aes
from ._na import NA
from .range import Range, RangeContinuous, RangeDiscrete
from .utilities import Waiver
from ._scales.ranges import rescale, censor

class Scale(object):

    def __init__(self):
        self.aesthetics = aes()
        self.scale_name = None
        self.range = Range()
        self.limits = None
        self.na_value = NA
        self.expand = Waiver()
        self.name = Waiver()
        self.breaks = Waiver()
        self.labels = Waiver()
        self.guide = "legend"

    def palette(self):
        raise NotImplementedError("Not implemented")

    def is_discrete(self):
        raise NotImplementedError()

    def train_df(self, df):
        pass

    def train(self, x):
        pass

    def reset(self):
        self.range.reset()

    def transform_df(self, df):
        pass

    def transform(self, x):
        raise NotImplementedError()

    def map_df(self, df):
        pass

    def map(self, x):
        raise NotImplementedError()

    def get_limits(self):
        pass

    def dimension(self, expand=(0,0)):
        raise NotImplementedError()

    def get_breaks(self, limits=None):
        raise NotImplementedError()

    def break_positions(self, range=None):
        raise NotImplementedError()

    def get_breaks_minor(self, n=2, b=None, limits=None):
        raise NotImplementedError()

    def get_labels(self, breaks=None):
        raise NotImplementedError()

    def clone(self):
        raise NotImplementedError()

    def break_info(self, range=None):
        raise NotImplementedError()


class ScaleContinuous(Scale):

    def __init__(self):
        Scale.__init__(self)
        self.range = RangeContinuous()
        self.na_value = NA  # numeric
        self.rescaler = rescale
        self.oob = censor
        self.minor_breaks = Waiver()

    def is_discrete(self):
        return False

    def dimension(self, expand=(0,0)):
        pass

    def get_breaks(self, limits=None):
        pass

    def get_breaks_minor(self, n=2, b=None, limits=None):
        pass

    def get_labels(self, breaks=None):
        pass

    def clone(self):
        pass

    def break_info(self, range=None):
        pass

    def __repr__(self):  # is 'print' in ggproto
        pass


class ScaleDiscrete(Scale):

    def __init__(self):
        Scale.__init__(self)
        self.drop = True
        self.range = RangeContinuous()
        self.na_value = NA  # non-numeric?
        self.rescaler = rescale
        self.oob = censor
        self.minor_breaks = Waiver()

    def is_discrete(self):
        return True

    def train(self, x):
        pass

    def transform(self, x):
        return x

    def map(self, x):
        pass

    def dimension(self, expand=(0,0)):
        pass

    def get_breaks(self, limits=None):
        pass

    def get_breaks_minor(self, n=2, b=None, limits=None):
        pass

    def get_labels(self, breaks=None):
        pass

    def clone(self):
        pass

    def break_info(self, range=None):
        pass

    def __repr__(self):  # is 'print' in ggproto
        pass