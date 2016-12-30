
class GTable(object):

    def __init__(self, name, grobs, names, widths, heights, respect, clip, z):
        self.name = name
        self.grobs = grobs
        self.names = names
        self.widths = widths
        self.heights = heights
        self.respect = respect
        self.clip = clip
        self.z = z

    # todo: need to create the GTree and do all the calculations regarding placement
    # it's possible this should be done using the renderer and not the grob interface?
