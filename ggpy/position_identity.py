
from .position import Position


class PositionIdentity(Position):

    def compute_layer(self, data, params, layout):
        return data

    def compute_panel(self, data, params, layout, scales):
        raise NotImplementedError() # not needed in this case
