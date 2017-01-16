

# define interface for plot renderer
class PlotRenderer(object):

    def render(self, built_plot):
        raise NotImplementedError()


