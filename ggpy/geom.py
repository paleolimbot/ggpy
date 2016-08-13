
from .aes import aes


class Geom(object):

    def __init__(self):
        self.required_aes = ()
        self.non_missing_aes = ()
        self.default_aes = aes()
        self.extra_params = "na.rm"

    def draw_key(self):
        pass

    def handle_na(self, data, params):
        pass

    def draw_layer(self, data, params, panel, coord):
        pass

    def draw_panel(self, data, panel_scales, coord, **kwargs):
        pass

    def draw_group(self, data, panel_scales, coord):
        pass

    def setup_data(self, data, params):
        return data

    def use_defaults(self, data, params={}):
        pass

    def parameters(self):
        pass

    def aesthetics(self):
        return tuple(set(self.default_aes.keys()).union(set(self.required_aes)))

