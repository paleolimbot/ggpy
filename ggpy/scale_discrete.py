
from .range import RangeContinuous
from .scale import ScaleDiscrete, aesthetics_x, aesthetics_y


def scale_x_continuous(**kwargs):
    return ScaleDiscrete(aesthetics=aesthetics_x, scale_name="position_d", guide="none", **kwargs)


def scale_y_continuous(**kwargs):
    return ScaleDiscrete(aesthetics=aesthetics_y, scale_name="position_d", guide="none", **kwargs)


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
        # todo: stub
        pass

    def reset(self):
        # todo: stub
        pass

    def map(self, x, limits=None):
        if limits is None:
            limits = self.get_limits()
        # todo: stub
        pass

    def dimension(self, expand=(0, 0)):
        # todo: stub
        pass

    def get_breaks(self, limits=None):
        if limits is None:
            limits = self.get_limits()
        # todo: stub
        pass

    def clone(self):
        # todo: stub
        pass

