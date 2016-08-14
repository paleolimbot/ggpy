
import numpy as np
from .._na import NA


def rescale(x, to=(0, 1), from_=None):
    if from_ is None:
        from_ = (np.nanmin(x), np.nanmax(x))
    return (x - from_[0]) / (from_[1]-from_[0]) * (to[1]-to[0]) + to[0]


def censor(x, range=(0, 1), only_finite=True):
    x = np.array(x)
    if only_finite:
        x[np.logical_not(np.isfinite(x))] = NA
    x[np.logical_or(x < range[0], x > range[1])] = NA
    return x

