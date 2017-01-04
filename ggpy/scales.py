
from .messaging import message_wrap
from .aes import aes_to_scale
from .scale_continuous import continuous_scale
from .scale_discrete import discrete_scale

import numpy as np


class ScalesList(object):

    def __init__(self, scales=None):
        self.scales = scales if scales is not None else []

    def find(self, aesthetic):
        if len(np.shape(aesthetic)) == 0:
            aesthetic = [aesthetic, ]
        for scale in self.scales:
            if any([a in scale.aesthetics for a in aesthetic]):
                return scale
        return None

    def has_scale(self, aesthetic):
        return self.find(aesthetic) is not None

    def add(self, scale):
        prev_scale = self.find(scale.aesthetics)
        if prev_scale is not None:
            name = prev_scale.aesthetics[0]
            message_wrap("Replacing scale for '%s'" % name)
            self.scales.remove(prev_scale)
        self.scales.append(scale)

    def __len__(self):
        return len(self.scales)

    def __iter__(self):
        return iter(self.scales)

    def __getitem__(self, item):
        scale = self.find(item)
        if scale is None:
            raise KeyError("No scale for aesthetic '%s'" % item)
        return scale

    def input(self):
        # lists all aesthetics from all scales?
        return [item for sublist in self.scales for item in sublist.aesthetics]

    def clone(self):
        return ScalesList(scales=[scale.clone() for scale in self.scales])

    def non_position_scales(self):
        # not cloning actual scales, mostly just subsetting this scales list
        scales = [scale for scale in self.scales if "x" not in scale.aesthetics and "y" not in scale.aesthetics]
        return ScalesList(scales=scales)

    def get_scales(self, output):
        return self.find(output)

    def train_df(self, df):
        if len(df) == 0 or len(self.scales) == 0:
            return
        for scale in self.scales:
            scale.train_df(df=df)

    def map_df(self, df):
        if len(df) == 0 or len(self.scales) == 0:
            return df
        # df is modified in place in Scale.map_df()
        for scale in self.scales:
            scale.map_df(df=df)
        return df

    def transform_df(self, df):
        if len(df) == 0 or len(self.scales) == 0:
            return df
        # df is modified in place
        for scale in self.scales:
            scale.transform_df(df)
        return df

    def add_defaults(self, data, aesthetics, global_vars=None, local_vars=None):
        # no concept of an 'env' in Python?
        scalekeys = aes_to_scale(aesthetics.keys())
        newkeys = set(scalekeys).difference(set(self.input()))
        if len(newkeys) == 0:
            return
        else:
            # need to pick default scales. this is done in scale-type.R
            # going to use the dtype
            # need the original aesthetic values for this
            for scale, aesname in zip(scalekeys, aesthetics.keys()):
                if scale in newkeys and not self.has_scale(scale):
                    dtype = aesthetics.map(data, aesname, global_vars, local_vars).dtype
                    defaultscale = default_scale(str(dtype), scale)
                    if defaultscale is not None:
                        self.add(defaultscale)

    def add_missing(self, aesthetics):  # don't need plot env since we are not using find_global for default scales
        aesthetics = set(aesthetics).difference(set(self.input()))
        for aes in aesthetics:
            self.add(continuous_scale(aes))


def default_scale(dtype, aes):
    # todo: need better default scale mapping strategy
    if dtype in ('object', 'category'):
        return discrete_scale(aes)
    elif dtype.startswith("<U"):
        return discrete_scale(aes)
    else:
        return continuous_scale(aes)

