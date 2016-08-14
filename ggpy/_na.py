
import numpy as np

NA = float("nan")
NA_character_ = "__NA_character_"


def is_nan(x):
    return np.array([e == NA_character_ or e is NA for e in x])