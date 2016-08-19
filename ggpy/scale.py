
from .aes import aes
from ._na import NA, is_nan, NA_character_
from .range import Range, RangeContinuous, RangeDiscrete
from .utilities import Waiver
from ._scales.ranges import rescale, censor, expand_range, zero_range
from ._scales.trans import TransIdentity
from ._scales.palette import PaletteDiscrete
import numpy as np
import copy


class Scale(object):

    def __init__(self, aesthetics=None, scale_name=None, range=None, limits=None, na_value=NA, expand=Waiver(),
                 name=Waiver(), breaks=Waiver(), labels=Waiver(), guide="legend", trans=None):
        self.aesthetics = aes() if aesthetics is None else aesthetics
        self.scale_name = scale_name
        self.range = Range() if range is None else range
        self.limits = limits
        self.na_value = na_value
        self.expand = expand
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.guide = guide
        self.trans = trans

    def palette(self, x=np.array((0,))):
        raise NotImplementedError()

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

    def __init__(self, range=None, na_value=NA, trans=TransIdentity(), rescaler=rescale, oob=censor,
                 minor_breaks=Waiver()):
        range = RangeContinuous() if range is None else range
        Scale.__init__(self, range=range, na_value=na_value, trans=trans)
        self.rescaler = rescaler
        self.oob = oob
        self.minor_breaks = minor_breaks

    def is_emtpy(self):
        return all(np.isnan(self.range.range)) or (self.limits is not None and all(np.isnan(self.limits)))

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
        scaled = [pal[int(np.argwhere(v == uniq))] for v in x]
        scaled[is_nan(x)] = self.na_value
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
        if type(self.labels) == Waiver:
            return self.trans.format(breaks)
        elif callable(self.labels):
            return np.array(self.labels(breaks))
        else:
            labels = np.array(self.labels)

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
        if labels is not None and len(labels) > 0:
            labels = labels[~is_nan(labels)]
        minor = self.get_breaks_minor(b=major, limits=range)
        major_n = rescale(major, from_=range)
        minor_n = rescale(minor, from_=range)
        return {'range': range, 'labels': labels, 'major': major_n, 'minor': minor_n,
                'major_source': major, 'minor_source': minor}

    def __repr__(self):  # is 'print' in ggproto
        return "<%s>\n  Range: %.3f -- %.3f\n  Limits: %.3f -- %.3f\n  Breaks: %s" % \
               (type(self), self.range.range[0], self.range.range[1],
                self.dimension()[0], self.dimension()[1],
                self.break_info())


class ScaleDiscrete(Scale):

    def __init__(self, drop=True, range=None, na_value=NA_character_, name=Waiver(), breaks=Waiver(),
                 labels=Waiver(), limits=None, expand=Waiver(), guide="legend"):
        range = RangeDiscrete() if range is None else range
        Scale.__init__(self, na_value=na_value, name=name, breaks=breaks, labels=labels, limits=limits,
                       expand=expand, guide=guide, range=range)
        self.drop = drop

    def palette(self, x=0):
        return PaletteDiscrete(n=x, na_value=self.na_value)

    def is_emtpy(self):
        return len(self.range.range) == 0 and self.limits is not None and len(self.limits) == 0

    def is_discrete(self):
        return True

    def train(self, x):
        if len(x) == 0:
            return
        self.range.train(x, drop=self.drop)

    def transform(self, x):
        return x

    def map(self, x, limits=None):
        if limits is None:
            limits = self.get_limits()
        limits = np.array(limits)
        n = np.sum(~is_nan(limits))
        pal = self.palette(n)
        pal_match = np.array([pal[int(np.argwhere(v == limits))] for v in x])
        return pal_match

    def dimension(self, expand=(0, 0)):
        return expand_range(len(self.get_limits()), expand[0], expand[1])

    def get_breaks(self, limits=None):
        if self.is_emtpy():
            return np.array(())
        if limits is None:
            limits = self.get_limits()
        if self.breaks is None:
            return np.array(())
        elif type(self.breaks) == Waiver:
            breaks = limits
        elif callable(self.breaks):
            breaks = self.breaks(limits)
        else:
            breaks = self.breaks

        return np.array([b for b in breaks if b in limits])

    def get_breaks_minor(self, **kwargs):
        return np.array(())

    def get_labels(self, breaks=None):
        if self.labels is None:
            return np.array(())
        if breaks is None:
            breaks = self.get_breaks()
        if type(self.labels) == Waiver:
            return np.array([('%s' % label).strip() for label in breaks])
        elif callable(self.labels):
            return np.array(self.labels(breaks))
        elif type(self.labels) == dict:
            return np.array([self.labels[b] for b in breaks])
        else:
            labels = np.array(self.labels)

        if len(labels) != len(breaks):
            raise ValueError("Length of labels is different than length of breaks")
        return labels

    def clone(self):
        return copy.deepcopy(self)

    def break_info(self, range=None):
        limits = self.get_limits()
        major = self.get_breaks(limits)
        if len(major) == 0:
            labels = major_n = np.array(())
        else:
            labels = self.get_labels(major)
            major = self.map(major)
            major_n = np.repeat(NA, len(major)) if range is None else rescale(major, from_=range)

        return {'range': range, 'labels': labels, 'major': major_n,
                'major_source': major}

    def __repr__(self):  # is 'print' in ggproto
        return "<%s>\n  Range: %s\n  Limits: %s\n  Breaks: %s" % \
               (type(self), self.range.range, self.get_limits(), self.break_info())



