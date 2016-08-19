
import numpy as np

NA = float("nan")
NA_character_ = "__NA_character_"


def is_nan(x):
    if type(x) in (float, int, bool, str, np.float64, np.float32, np.float16):
        return x == NA_character_ or (type(x) == float and np.isnan(x))
    else:
        return np.array([e == NA_character_ or (type(e) == float and np.isnan(e)) for e in x], dtype=bool)