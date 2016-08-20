
import warnings
import numpy as np

from ._na import is_nan, is_finite

class Waiver(object):
    def __init__(self):
        pass


def check_required_aesthetics(required, present, name):
    missing = set(required).difference(set(present))
    if len(missing) > 0:
        raise ValueError('%s requires the following aesthetics: %s' % (name, ", ".join(missing)))


def remove_missing(df, na_rm=False, vars=None, name="", finite=False):
    if vars is None:
        vars = df.columns
    vars = list(set(vars).intersection(set(df.columns)))
    if finite:
        missing = ~finite_cases(df[vars])
        string = 'non-finite'
    else:
        missing = ~complete_cases(df[vars])
        string = 'missing'

    if any(missing):
        df = df.iloc[~missing,]
        if not na_rm:
            warning_wrap('Removed %d %s cases (%s)' % (np.sum(missing), string, name))
    return df


def finite_cases(df):
    return np.array([all(is_finite(df.iloc[i, ])) for i in range(len(df))], dtype=bool)


def complete_cases(df):
    return np.array([all(~is_nan(df.iloc[i, ])) for i in range(len(df))], dtype=bool)


def warning_wrap(*args):
    msg = "".join([str(arg) for arg in args])
    warnings.warn(msg)


