
from .aes import aes_to_scale


class Position(object):
    pass
    # TODO: need to define position object


def transform_position(df, rescale_x=None, rescale_y=None):
    cols = df.columns
    scales = aes_to_scale(df.columns)
    out = df.copy(deep=True)
    if rescale_x is not None:
        for i in range(len(scales)):
            if scales[i] == 'x':
                out[cols[i]] = rescale_x(df[cols[i]])

    if rescale_y is not None:
        for i in range(len(scales)):
            if scales[i] == 'y':
                out[cols[i]] = rescale_y(df[cols[i]])

    return out
