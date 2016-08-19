
import numpy as np
from .breaks import wilkinson_breaks, log_breaks


class Trans(object):

    def __init__(self):
        self.domain = (-np.inf, np.inf)

    def format(self, x):
        return np.array(['%s' % e for e in x])

    def breaks(self, x, **kwargs):
        return wilkinson_breaks(np.nanmin(x), np.nanmax(x), **kwargs)

    def transform(self, x):
        raise NotImplementedError()

    def inverse(self, x):
        raise NotImplementedError()


class TransIdentity(Trans):

    def __init__(self):
        Trans.__init__(self)

    def transform(self, x):
        return x

    def inverse(self, x):
        return x


class TransLog10(Trans):

    def __init__(self):
        Trans.__init__(self)
        self.domain = (0, np.inf)

    def transform(self, x):
        return np.log10(x)

    def inverse(self, x):
        return 10 ** np.array(x)

    def breaks(self, x, **kwargs):
        return log_breaks(np.nanmin(x), np.nanmax(x), **kwargs)