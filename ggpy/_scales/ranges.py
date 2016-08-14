
import numpy as np
from .._na import NA


def expand_range(range, mul=0, add=0, zero_width=1):
    c = np.mean(range)
    spread = range[1] - range[0]
    if spread == 0:
        spread = zero_width
    spread *= 1 + mul*2
    return c-spread/2-add, c+spread/2+add


def zero_range(range, tol=2.220446e-13):
    return (np.nanmax(range) - np.nanmin(range)) < tol


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


def train_continuous(new, existing=tuple()):
    if new is None:
        return existing
    both = np.concatenate((new, existing))
    return np.nanmin(both), np.nanmax(both)


def train_discrete(new, old, drop=False):
    return list(sorted(set(np.concatenate((new, old)))))  # not great for factors but works for now
