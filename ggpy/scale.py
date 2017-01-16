
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
                 name=Waiver(), breaks=Waiver(), labels=Waiver(), guide="legend", trans=None, palette=None,
                 position="left"):
        self.aesthetics = () if aesthetics is None else aesthetics
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
        self.palette = self.default_palette() if palette is None else palette
        self.position = position

    def expand_default(self, discrete=(0, 0.6), continuous=(0.05, 0)):
        raise NotImplementedError()

    def default_palette(self):
        raise NotImplementedError()

    def is_discrete(self):
        raise NotImplementedError()

    def train_df(self, df):
        if len(df) == 0:
            return
        aesthetics = set(self.aesthetics).intersection(set(df.columns))
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
            return df
        aesthetics = set(self.aesthetics).intersection(set(df.columns))
        # modify df in place
        for col in aesthetics:
            df[col] = self.transform(df[col])
        return df

    def transform(self, x):
        raise NotImplementedError()

    def map_df(self, df, i=None):
        if len(df) == 0:
            return df
        aesthetics = set(self.aesthetics).intersection(set(df.columns))
        if i is not None:
            df = df.iloc[i]  # subset the data frame
        # if the data frame is not subsetted it is modified in place
        for col in aesthetics:
            df[col] = self.map(df[col])
        return df

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
        return self.map(self.get_breaks(range))

    def get_breaks_minor(self, n=2, b=None, limits=None):
        raise NotImplementedError()

    def get_labels(self, breaks=None):
        raise NotImplementedError()

    def clone(self):
        raise NotImplementedError()

    def break_info(self, range=None):
        raise NotImplementedError()

    def axis_order(self):
        if self.position in ("bottom", "right"):
            return "secondary", "primary"
        else:
            return "primary", "secondary"

    def make_title(self, title):
        return title

    def make_sec_title(self, title):
        return title


class ScaleContinuous(Scale):

    def __init__(self, aesthetics=None, scale_name=None, range=None, limits=None, na_value=NA,
                 expand=Waiver(), name=Waiver(), breaks=Waiver(), labels=Waiver(), guide="legend",
                 trans=TransIdentity(), rescaler=rescale, oob=censor, palette=None,
                 minor_breaks=Waiver()):
        range = RangeContinuous() if range is None else range
        Scale.__init__(self, aesthetics=aesthetics, range=range, na_value=na_value, trans=trans, limits=limits,
                       expand=expand, name=name, breaks=breaks, labels=labels, guide=guide, scale_name=scale_name,
                       palette=palette)
        self.rescaler = rescaler
        self.oob = oob
        self.minor_breaks = minor_breaks

    def expand_default(self, discrete=(0, 0.6), continuous=(0.05, 0)):
        return continuous

    def default_palette(self):
        return None

    def is_emtpy(self):
        return all(np.isnan(self.range.range)) or (self.limits is not None and all(np.isnan(self.limits)))

    def is_discrete(self):
        return False

    def train(self, x):
        if len(x) != 0:
            self.range.train(x)

    def transform(self, x):
        return self.trans.transform(x)

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
            raise ValueError("Zero breaks for %s" % "/".join(self.aesthetics))
        return breaks

    def get_breaks_minor(self, n=2, b=None, limits=None):
        if b is None:
            b = self.break_positions()
        if limits is None:
            limits = self.get_limits()
        if zero_range(limits):
            return np.array(())

        if self.minor_breaks is None:
            return np.array(())
        elif isinstance(self.minor_breaks, Waiver):
            if b is None:
                return np.array(())
            b = b[~is_nan(b)]
            if len(b) < 2:
                return np.array(())
            bd = np.diff(b)[0]
            if np.min(limits) < np.min(b):
                b = np.concatenate([[b[0] - bd, ], b])
            if np.max(limits) > np.max(b):
                b = np.concatenate([b, [b[len(b)-1] + bd,]])
            breaks = [(b[i-1]+b[i])/2 for i in range(1, len(b))]
        elif callable(self.minor_breaks):
            breaks = self.minor_breaks(self.trans.inverse(limits))
            breaks = self.trans.transform(breaks)
        elif is_nan(self.minor_breaks):
            raise ValueError("Use None to specify no minor breaks")
        else:
            breaks = self.trans.transform(self.minor_breaks)

        return np.array([br for br in breaks if limits[0] <= br <= limits[1]])

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

    def __init__(self, aesthetics=None, scale_name=None, drop=True, range=None, limits=None, na_value=NA_character_,
                 expand=Waiver(), name=Waiver(), breaks=Waiver(), palette=None,
                 labels=Waiver(), guide="legend"):
        range = RangeDiscrete() if range is None else range
        Scale.__init__(self, na_value=na_value, name=name, breaks=breaks, labels=labels, limits=limits,
                       expand=expand, guide=guide, range=range, aesthetics=aesthetics, scale_name=scale_name,
                       palette=palette)
        self.drop = drop

    def expand_default(self, discrete=(0, 0.6), continuous=(0.05, 0)):
        return discrete

    def default_palette(self, x=0):
        return lambda n: PaletteDiscrete(n=n, na_value=self.na_value)

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
        limits = list(limits)
        n = np.sum(~is_nan(np.array(limits)))
        pal = self.palette(n)
        # NA may have to be numeric here (or may not), but if it is __NA_character it
        # forces the type of pal_match to all strings, which when passed to rescale()
        # forces all major_n to be nan
        pal_match = np.array([pal[limits.index(v)] if v in limits else NA for v in x])
        return pal_match

    def dimension(self, expand=(0, 0)):
        return expand_range((0, len(self.get_limits())-1), expand[0], expand[1])

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
            if len(major) > 0:
                mask = ~is_nan(major)
                major = major[mask]
                labels = labels[mask]
            major_n = np.repeat(NA, len(major)) if range is None else rescale(major, from_=range)

        return {'range': range, 'labels': labels, 'major': major_n,
                'major_source': major}

    def __repr__(self):  # is 'print' in ggproto
        return "<%s>\n  Range: %s\n  Limits: %s\n  Breaks: %s" % \
               (type(self), self.range.range, self.get_limits(), self.break_info())

# these aesthetics get used in a few places
aesthetics_x = ("x", "xmin", "xmax", "xend", "xintercept", "xmin_final", "xmax_final", "xlower", "xmiddle", "xupper")
aesthetics_y = ("y", "ymin", "ymax", "yend", "yintercept", "ymin_final", "ymax_final", "lower", "middle", "upper")
