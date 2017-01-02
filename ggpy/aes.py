
from ._component import Component
from .aes_calculated import is_calculated_aes
from .scale import aesthetics_y, aesthetics_x
import pandas as pd
import numpy as np
import re

_all_aesthetics = ("adj", "alpha", "angle", "bg", "cex", "col", "color",
  "colour", "fg", "fill", "group", "hjust", "label", "linetype", "lower",
  "lty", "lwd", "max", "middle", "min", "pch", "radius", "sample", "shape",
  "size", "srt", "upper", "vjust", "weight", "width", "x", "xend", "xmax",
  "xmin", "xintercept", "y", "yend", "ymax", "ymin", "yintercept", "z")

_base_to_ggplot = {
  "col": "colour",
  "color": "colour",
  "pch": "shape",
  "cex": "size",
  "lty": "linetype",
  "lwd": "size",
  "srt": "angle",
  "adj": "hjust",
  "bg": "fill",
  "fg": "colour",
  "min": "ymin",
  "max": "ymax"
}

match_function_aes = re.compile("^[a-zA-Z._]*?\(([a-zA-Z_]+)\)$")


def _rename_aes(dct):
    nd = {}
    for key, value in dct.items():
        nd[_base_to_ggplot[key] if key in _base_to_ggplot else key] = value
    return Mapping(**nd)


class Mapping(Component):

    def __init__(self, **kwargs):
        super(Mapping, self).__init__(**kwargs)

    def map(self, data, key, global_vars=None, local_vars=None):
        val = self[key]
        try:
            funmatch = match_function_aes.match(val)
        except TypeError:
            funmatch = False
        if val in data.columns:
            return data[val]
        elif funmatch:
            if global_vars is None:
                global_vars = globals()
            if local_vars is None:
                local_vars = {}
            else:
                local_vars = local_vars.copy()
            local_vars['__data__'] = data
            for col in data.columns:
                val = val.replace("(" + col + ")", "(__data__['%s'])" % col)
            return eval(val, global_vars, local_vars)
        else:
            return val

    def map_df(self, data, global_vars=None, local_vars=None):
        # copies data frame and returns a dict
        d = {}
        for key, value in self.items():
            # replace columns
            d[key] = self.map(data, key, global_vars, local_vars)
        return d


def aes(x=None, y=None, **kwargs):
    kwargs["x"] = x
    kwargs["y"] = y
    return _rename_aes(kwargs)


def aes_to_scale(var):
    return ["x" if v in aesthetics_x else "y" if v in aesthetics_y else v for v in var]


def is_position_aes(vars):
    scales = aes_to_scale(vars)
    return [s in ("x", "y") for s in scales]


def check_aesthetics(df_like, n):
    lens = [np.shape(df_like[col]) for col in df_like]
    if all(l == 1 or l == n for l in lens):
        return
    else:
        raise ValueError("Aesthetics must be scalar or same length as data")


def check_required_aesthetics(required, existing, classname):
    missing = [r for r in required if r not in existing]
    if missing:
        raise ValueError("%s is missing the following aesthetics: %s" % (classname, ", ".join(missing)))
