
class Coord(object):

    def __init__(self):
        pass

    def aspect(self, ranges):
        return None

    def labels(self, scale_details):
        return scale_details

    def render_fg(self, scale_details, theme):
        pass

    def render_bg(self, scale_details, theme):
        pass

    def render_axis_h(self, scale_details, theme):
        pass

    def render_axis_v(self, scale_details, theme):
        pass

    def range(self, scale_details):
        pass

    def train(self, scale_details):
        pass

    def transform(self, data, range):
        pass

    def distance(self, x, y, scale_details):
        pass

    def is_linear(self):
        return False