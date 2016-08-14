
from .aes import aes
from ._na import NA, is_nan
from .range import Range, RangeContinuous, RangeDiscrete
from .utilities import Waiver
from ._scales.ranges import rescale, censor, expand_range, zero_range
import numpy as np
import copy


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
        self.trans = None

    def palette(self, x=()):
        raise NotImplementedError("")

    def is_discrete(self):
        raise NotImplementedError()

    def train_df(self, df):
        if len(df) == 0:
            return
        aesthetics = set(self.aesthetics.values()).intersection(set(df.columns))
        for col in aesthetics:
            self.train(df[col])

    def train(self, x):
        raise NotImplementedError()

    def reset(self):
        self.range.reset()

    def is_emtpy(self):
        return self.range is None and self.limits is None

    def transform_df(self, df):
        if len(df) == 0:
            return []
        aesthetics = set(self.aesthetics.values()).intersection(set(df.columns))
        return [self.transform(df[col]) for col in aesthetics]

    def transform(self, x):
        raise NotImplementedError()

    def map_df(self, df, i=None):
        if len(df) == 0:
            return []
        aesthetics = set(self.aesthetics.values()).intersection(set(df.columns))
        if i is None:
            return [self.map(df[col]) for col in aesthetics]
        else:
            return [self.map(df[col][i]) for col in aesthetics]

    def map(self, x):
        raise NotImplementedError()

    def get_limits(self):
        if self.is_emtpy():
            return 0, 1
        if self.limits is not None:
            return self.range.range if NA in self.limits else self.limits
        else:
            return self.range.range

    def dimension(self, expand=(0, 0)):
        raise NotImplementedError()

    def get_breaks(self, limits=None):
        raise NotImplementedError()

    def break_positions(self, range=None):
        if range is None:
            range = self.get_limits()
        self.map(self.get_breaks(range))

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

    def train(self, x):
        if len(x) != 0:
            self.range.train(x)

    def transform(self, x):
        self.trans.transform(x)

    def map(self, x, limits=None):
        if limits is None:
            limits = self.get_limits()
        x = self.oob(self.rescaler(x, from_=limits))
        uniq = np.unique(x)
        pal = self.palette(uniq)
        scaled = pal[[int(np.argwhere(v == uniq)) for v in x]]
        scaled[scaled == NA] = self.na_value
        return scaled

    def dimension(self, expand=(0, 0)):
        return expand_range(self.get_limits(), expand[0], expand[1])

    def get_breaks(self, limits=None):
        if self.is_emtpy():
            return np.array(())
        if limits is None:
            limits = self.get_limits()
        limits = self.trans.inverse(limits)
        if self.breaks is None:
            return np.array(())
        elif zero_range(limits):
            breaks = limits[0]
        elif type(self.breaks) == Waiver:
            breaks = self.trans.breaks(limits)
        elif callable(self.breaks):
            breaks = self.breaks(limits)
        else:
            breaks = self.breaks

        breaks = censor(self.trans.transform(breaks), self.trans.transform(limits), only_finite=False)
        if len(breaks) == 0:
            raise ValueError("Zero breaks for %s" % "/".join(self.aesthetics.values()))
        return breaks

    def get_breaks_minor(self, n=2, b=None, limits=None):
        # TODO not dealing with this yet
        return np.array(())

    def get_labels(self, breaks=None):
        if self.labels is None:
            return np.array(())
        if breaks is None:
            breaks = self.get_breaks()
        elif type(self.labels) == Waiver:
            return self.trans.format(breaks)
        elif callable(self.labels):
            return self.labels(breaks)
        else:
            labels = self.labels

        if len(labels) != len(breaks):
            raise ValueError("Length of labels is different than length of breaks")
        return labels

    def clone(self):
        return copy.deepcopy(self)

    def break_info(self, range=None):
        if range is None:
            range = self.dimension()

        major = self.get_breaks(range)
        labels = self.get_labels(major)
        if major is not None:
            major = major[~np.isnan(major)]
        if labels is not None:
            labels = labels[~is_nan(labels)]
        minor = self.get_breaks_minor(b=major, limits=range)
        major_n = rescale(major, from_=range)
        minor_n = rescale(minor, from_=range)
        return {'range': range, 'labels': labels, 'major': major_n, 'minor': minor_n,
                'major_source': major, 'minor_source': minor}

    def __repr__(self):  # is 'print' in ggproto
        return "<%s>\n  Range: %.3d -- %.3d\n  Limits: %.3d -- %.3d" % \
               (type(self), self.range.range[0], self.range.range[1],
                self.dimension()[1], self.dimension()[2])


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