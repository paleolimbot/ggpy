
def scales():
    from ggpy.scale import ScaleContinuous, ScaleDiscrete
    from ggpy.aes import aes
    import pandas as pd
    from ggpy._na import NA

    sc = ScaleContinuous()
    print(sc)

    a = pd.DataFrame({'a':(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 'b':(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1)})
    sc.aesthetics = aes(x='a')
    sc.train_df(a)
    print(sc)

    scD = ScaleDiscrete()
    print(scD)
    a['c'] = pd.Series(['fish', 'in', 'sea', 'fish', 'in', 'sea', 'fish', 'in', 'sea', NA, 'in'], dtype='category')
    scD.aesthetics = aes(c='c')
    scD.train_df(a)
    print(scD)

def ggplots():
    from ggpy.plot import ggplot
    g = ggplot()
    print(ggplot())

def ggplot_builds():
    import numpy as np
    import pandas as pd
    from ggpy import ggplot, aes
    from ggpy.geom_point import GeomPoint
    df = pd.DataFrame({'a': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                       'b': (0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1),
                       'c': ("one", "one", "one", "two", "one", "two", "one", "two", "two", "one", "two"),
                       'd': ("one", ) * 11})
    # both continuous example
    p = ggplot(df, aes('a', 'b')).layer(geom=GeomPoint(), inherit_aes=True)
    pb = p.build()
    print(pb.data[0])  # see what the output data is like
    print(pb)

    # discrete example
    p2 = ggplot(df, aes('a', 'c')).layer(geom=GeomPoint(), inherit_aes=True)
    pb2 = p2.build()
    print(pb2.data[0])
    print(pb2)

    # zero-range discrete example
    p3 = ggplot(df, aes('a', 'd')).layer(geom=GeomPoint(), inherit_aes=True)
    pb3 = p3.build()
    print(pb3.data[0])
    print(pb3)

    # todo: colour mapping example with add_group(), grouping, and colour pallette
    # in tandem with scale_ function / default scale updates
    p4 = ggplot(df, aes('a', 'b', col='c')).layer(geom=GeomPoint(), inherit_aes=True)
    pb4 = p4.build()
    print(pb4.data[0])
    print(pb4)

ggplot_builds()
