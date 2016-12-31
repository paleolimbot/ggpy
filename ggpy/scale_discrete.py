

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

# todo: implement other position scale thinger for jittering
