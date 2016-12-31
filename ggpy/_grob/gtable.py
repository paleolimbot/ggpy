
import numpy as np


class GTable(object):

    def __init__(self, widths=None, heights=None, respect=False, name="layout"):
        self.name = name
        self.els = {}
        self.widths = [] if widths is None else widths
        self.heights = [] if heights is None else heights
        self.respect = respect

    def add_row(self, height, pos=-1):
        if pos != -1:
            self.heights.insert(height, pos)
        else:
            self.heights.append(height)

    def add_col(self, width, pos=-1):
        if pos != -1:
            self.widths.insert(width, pos)
        else:
            self.widths.append(width)

    def add_grob(self, grob, t, l, b=None, r=None, z=9999, clip="on", name=None):
        if b is None:
            b = t
        if r is None:
            r = l
        if name is None:
            name = self.name
        zs = [el["z"] for el in self.els.values()]
        if len(zs) == 0:
            z = 0
        elif z >= max(zs):
            z = max(zs) + 1
        elif z <= min(zs):
            z = min(zs) - 1
        else:
            z = 0
        self.els[(t, l)] = {"t": t, "l": l, "b": b, "r": r, "z": z,
                            "grob": grob, "name": name, "clip": clip}

    def __iter__(self):
        if len(self.els) == 0:
            return
        # deliver in row/col order
        for t in range(max(el["b"] for el in self.els.values()) + 1):
            for l in range(max(el["l"] for el in self.els.values()) + 1):
                key = (t, l)
                if key in self.els:
                    yield self.els[key]
                else:
                    yield {"t": t, "l": l, "b": None, "r": None, "z": None,
                           "grob": None, "name": None, "clip": None}

    @staticmethod
    def matrix(name, grobs, names=None, widths=None, heights=None, respect=False, clip="on", z=9999):
        shp = np.shape(grobs)
        if len(shp) != 2:
            raise ValueError("input grobs must be a 2-dimensional matrix")
        if widths is None:
            widths = np.repeat(None, shp[1])
        elif len(widths) != shp[1]:
            raise ValueError("length of widths must be identical to columns in grobs")
        if heights is None:
            heights = np.repeat(None, shp[0])
        elif len(heights) != shp[0]:
            raise ValueError("length of heights must be identical to rows in grobs")
        if len(np.shape(names)) == 0:
            names = np.reshape(np.repeat(names, shp[0]*shp[1]), shp)
        elif np.shape(names) != shp:
            raise ValueError("Shape of grobs and names must be identical")
        if len(np.shape(clip)) == 0:
            clip = np.reshape(np.repeat(clip, shp[0]*shp[1]), shp)
        elif np.shape(clip) != shp:
            raise ValueError("Shape of grobs and clip must be identical")
        tbl = GTable(widths=widths, heights=heights, respect=respect, name=name)
        for t in range(shp[0]):
            for l in range(shp[1]):
                tbl.add_grob(grobs[t, l], t, l, z=z[t, l], clip=clip[t, l], name=names[t, l])
        return tbl

    # todo: need to create the GTree and do all the calculations regarding placement
    # it's possible this should be done using the renderer and not the grob interface?
