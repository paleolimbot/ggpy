
from .aes import aes_to_scale
import pandas as pd


class Position(object):

    def __init__(self, required_aes=()):
        self.required_aes = required_aes

    def setup_params(self, data):
        return {}

    def setup_data(self, data, params):
        return data

    def compute_layer(self, data, params, layout):
        def f(data):
            if len(data) == 0:
                return pd.DataFrame()
            scales = layout.get_scales(data["PANEL"][0])
            self.compute_panel(data=data, params=params, scales=scales)
        return data.groupby("PANEL").apply(f)

    def compute_panel(self, data, params, layout, scales):
        raise NotImplementedError()


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
