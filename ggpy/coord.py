
class Coord(object):

    def __init__(self):
        pass

    def aspect(self, ranges):
        return None

    def labels(self, scale_details):
        return scale_details

    def render_fg(self, scale_details, theme):
        return theme.render_element('panel_border')

    def render_bg(self, scale_details, theme):
        pass  # TODO need guide_grid() first

    def render_axis_h(self, scale_details, theme):
        pass  # TODO need guide_axis() first

    def render_axis_v(self, scale_details, theme):
        pass  # TODO need guide_axis() first

    def range(self, scale_details):
        return {'x': scale_details['x_range'], 'y': scale_details['y_range']}

    def train(self, scale_details):
        pass

    def transform(self, data, range):
        pass

    def distance(self, x, y, scale_details):
        pass

    def is_linear(self):
        return False