
from .aes import aes


class Stat(object):

    def __init__(self):
        self.retransform = True
        self.default_aes = aes()
        self.required_aes = ()
        self.non_missing_aes = ()
        self.extra_params = ("na.rm", )

    def setup_params(self, data, params):
        return params

    def setup_data(self, data, params):
        return data

    def compute_layer(self, data, params, panels):
        pass

    def compute_panel(self, data, scales):
        pass

    def compute_group(self, data, scales):
        raise NotImplementedError("Not implemented")

    def parameters(self):
        return ()