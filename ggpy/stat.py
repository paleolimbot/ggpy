
from .aes import aes
import numpy as np
from .utilities import check_required_aesthetics


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
        check_required_aesthetics(self.required_aes,
                                  np.concatenate((params.keys(), data.columns)),
                                  type(self).__name__)


    def compute_panel(self, data, scales):
        pass

    def compute_group(self, data, scales):
        raise NotImplementedError("Not implemented")

    def parameters(self):
        return ()