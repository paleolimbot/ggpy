
from ._component import Component

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


def _rename_aes(dct):
    nd = {}
    for key, value in dct.items():
        nd[_base_to_ggplot[key] if key in _base_to_ggplot else key] = value
    return Mapping(**nd)


class Mapping(Component):

    def __init__(self, **kwargs):
        super(Mapping, self).__init__(**kwargs)


def aes(x=None, y=None, **kwargs):
    kwargs["x"] = x
    kwargs["y"] = y
    return _rename_aes(kwargs)
