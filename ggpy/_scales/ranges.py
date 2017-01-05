
import numpy as np
from .._na import NA, is_nan, NA_character_


def expand_range(range, mul=0, add=0, zero_width=1):
    if zero_range(range):
        return range[0] - zero_width / 2, range[0] + zero_width / 2
    else:
        return range + np.array((-1, 1)) * (np.ptp(range) * mul + add)


def zero_range(range, tol=2.220446e-13):
    return (np.nanmax(range) - np.nanmin(range)) < tol


def rescale(x, to=(0, 1), from_=None):
    if from_ is None:
        from_ = (np.nanmin(x), np.nanmax(x))
    return (x - from_[0]) / (from_[1]-from_[0]) * (to[1]-to[0]) + to[0]


def censor(x, range=(0, 1), only_finite=True):
    if len(x) == 0:
        return x
    x = np.array(x, dtype=float)
    if only_finite:
        x[~np.isfinite(x)] = NA
    outofrange = np.logical_or(x < range[0], x > range[1])
    x[outofrange] = NA
    return x


def squish_infinite(x, range=(0, 1)):
    x = np.array(x)
    x[np.isneginf(x)] = range[0]
    x[np.isposinf(x)] = range[1]
    return x


def train_continuous(new, existing=tuple()):
    if new is None:
        return existing
    both = np.concatenate((new, existing))
    return np.nanmin(both), np.nanmax(both)


def train_discrete(new, old, drop=False):
    try:
        hasna = any(is_nan(new))
        if drop:
            newarr = np.array(new)
            new = np.array([cat for cat in new.cat.categories if cat not in old and cat in newarr])
        else:
            new = np.array([cat for cat in new.cat.categories if cat not in old])
        if hasna:
            new = np.concatenate((new, (NA_character_, )))
    except AttributeError:
        new = np.array((sorted(set(new).difference(set(old)))))

    return new

