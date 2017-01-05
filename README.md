
# ggpy

Ok, so there already exists a [ggplot package for Python](https://github.com/yhat/ggplot), but this package is almost entirely based on the [matplotlib](http://matplotlib.org/) framework. There is greatness in this framework, but a true implementation of the grammar of graphics (after [Wilkinson 2005](http://www.springer.com/gp/book/9780387245447)) does not depend on a plotting backend. This package is closely structured after the [ggplot2 package for R](https://github.com/tidyverse/ggplot2/) because this framework has seen much use and any port to Python would be remiss to ignore the success of that framework.

The similarities to the R framework are intended to be purely internal, since there are many things that are possible in R that are not possible in Python (`uneval` objects and so on), and Python users have a different expectation of syntax (notably that in-place modification of objects in R is almost unheard of whereas in Python this is the norm). As such, the interface for ggpy is based on the dot modifier instead of the `+` symbol (although the `+` symbol will still work in the same way it does in R).

```Python
from ggpy import ggplot, aes
df = {'varone': [1, 2, 3], 'vartwo': ['one', 'two', 'three']}
p = ggplot(df, aes('varone', 'vartwo').layer_point()
```

Everything else is a work in progress...

