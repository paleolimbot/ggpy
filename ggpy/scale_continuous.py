
import numpy as np

from ._na import is_nan
from .scale import ScaleContinuous, aesthetics_x, aesthetics_y
from .utilities import Waiver


def scale_x_continuous(**kwargs):
    return ScaleContinuousPosition(aesthetics=aesthetics_x, scale_name="position_c", guide="none", **kwargs)


def scale_y_continuous(**kwargs):
    return ScaleContinuousPosition(aesthetics=aesthetics_y, scale_name="position_c", guide="none", **kwargs)


def continuous_scale(aes_name, **kwargs):
    if aes_name == "x":
        return scale_x_continuous(**kwargs)
    elif aes_name == "y":
        return scale_y_continuous(**kwargs)
    else:
        # todo: need to add default colour/other aesthetic scales
        return ScaleContinuous(aesthetics=(aes_name,), **kwargs)


class ScaleContinuousPosition(ScaleContinuous):

    def __init__(self, secondary_axis=Waiver(), **kwargs):
        ScaleContinuous.__init__(self, **kwargs)
        self.secondary_axis = secondary_axis

    def map(self, x, limits=None):
        if limits is None:
            limits = self.get_limits()
        scaled = self.oob(x, limits)  # censor() returns dtype of float (amenable to NAs) but other oob funcs might not
        scaled = np.array(scaled, dtype=float)
        scaled[is_nan(scaled)] = self.na_value
        return scaled

    def break_info(self, range=None):
        breaks = ScaleContinuous.break_info(self, range)
        if not isinstance(self.secondary_axis, Waiver) and self.secondary_axis.empty():
            self.secondary_axis.init(self)
            for key, value in self.secondary_axis.break_info(breaks["range"], self):
                breaks[key] = value
        return breaks

    def sec_name(self):
        if isinstance(self.secondary_axis, Waiver):
            return Waiver()
        else:
            return self.secondary_axis.name

    def make_sec_title(self, title):
        if isinstance(self.secondary_axis, Waiver):
            ScaleContinuous.make_sec_title(self, title)
        else:
            self.secondary_axis.make_title(title)


