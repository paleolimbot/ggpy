
from .aes import aes
import numpy as np
import pandas as pd
from .utilities import check_required_aesthetics, remove_missing, warning_wrap


class Stat(object):

    def __init__(self):
        self.retransform = True
        self.default_aes = aes()
        self.required_aes = ()
        self.non_missing_aes = ()
        self.extra_params = ("na_rm", )

    def setup_params(self, data, params):
        return params

    def setup_data(self, data, params):
        return data

    def compute_layer(self, data, params, panels):
        check_required_aesthetics(self.required_aes,
                                  np.concatenate((tuple(params.keys()), data.columns)),
                                  type(self).__name__)
        data = remove_missing(data, params['na_rm'], np.concatenate((self.required_aes, self.non_missing_aes)),
                              type(self).__name__, finite=True)
        newpars = {}
        parnames = [p for p in self.parameters() if p in params]
        for p in parnames:
            newpars[p] = params[p]

        def f(paneldata):
            scales = panels.scales(paneldata.PANEL[0])
            try:
                return self.compute_panel(paneldata, scales, params)
            except Exception as e:
                warning_wrap('Computation failed in %s: %s %s' % type(self).__name__, type(e).__name__, str(e))
                return pd.DataFrame()

        return data.groupby('PANEL').apply(f)

    def compute_panel(self, data, scales, params=None):
        if len(data) == 0:
            return pd.DataFrame()
        # missing some of https://github.com/hadley/ggplot2/blob/master/R/stat-.r#L104
        return data.groupby('group').apply(lambda group: self.compute_group(group, scales, params))

    def compute_group(self, data, scales, params=None):
        raise NotImplementedError("Not implemented")

    def parameters(self):
        return ()


class StatIdentity(Stat):

    def __init__(self):
        Stat.__init__(self)

    def compute_group(self, data, scales, params=None):
        return data