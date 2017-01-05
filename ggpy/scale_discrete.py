
from .range import RangeContinuous
from .scale import ScaleDiscrete, aesthetics_x, aesthetics_y
from ._scales.ranges import expand_range
import numpy as np


def scale_x_continuous(**kwargs):
    return ScaleDiscretePosition(aesthetics=aesthetics_x, scale_name="position_d", guide="none", **kwargs)


def scale_y_continuous(**kwargs):
    return ScaleDiscretePosition(aesthetics=aesthetics_y, scale_name="position_d", guide="none", **kwargs)


def discrete_scale(aes_name, **kwargs):
    if aes_name == "x":
        return scale_x_continuous(**kwargs)
    elif aes_name == "y":
        return scale_y_continuous(**kwargs)
    else:
        return None


def is_discrete(x):
    dtype = str(x.dtype)
    if dtype in ("object", "category"):
        return True
    elif dtype.startswith("<U"):
        return True
    else:
        return False


class ScaleDiscretePosition(ScaleDiscrete):

    def __init__(self, **kwargs):
        ScaleDiscrete.__init__(self, **kwargs)
        self.range_c = RangeContinuous()

    def train(self, x):
        if is_discrete(x):
            self.range.train(x, drop=self.drop)
        else:
            self.range_c.train(x)

    def get_limits(self):
        if self.is_emtpy():
            return 0, 1
        if self.limits is not None:
            return self.limits
        elif self.range.range is not None:
            return self.range.range
        else:
            return ()

    def is_emtpy(self):
        return self.range.range is None and self.limits is None and self.range_c.range is None

    def reset(self):
        # Can't reset discrete scale because no way to recover values
        self.range_c.reset()

    def map(self, x, limits=None):
        if limits is None:
            limits = self.get_limits()
        if is_discrete(x):
            limits = list(limits)
            na = self.na_value
            return np.array([limits.index(e) if e in limits else na for e in x])
        else:
            return x

    def dimension(self, expand=(0, 0)):
        c_range = self.range_c.range
        d_range = self.get_limits()

        if self.is_emtpy():
            return 0, 1
        elif self.range.range is None:
            # only continuous
            return expand_range(c_range, expand[0], expand[1], 1)
        elif c_range is None:
            # only discrete
            return expand_range((1, len(d_range)), expand[0], expand[1], 1)
        else:
            # both
            both = np.concatenate([expand_range(c_range, expand[0], 0, 1),
                                   expand_range((0, len(d_range)-1), 0, expand[1], 1)])
            return np.nanmin(both), np.nanmax(both)

    def get_breaks(self, limits=None):
        if limits is None:
            limits = self.get_limits()
        # this is identical to the super method, not sure why it is 'overridden' in scale_discrete.R
        return ScaleDiscrete.get_breaks(self, limits)

    def clone(self):
        # this is the same as the super method, which uses deepcopy to copy the scale
        # this should be sufficient to the implementation in scale_discrete.R
        return ScaleDiscrete.clone(self)
