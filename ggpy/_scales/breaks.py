
import numpy as np


def wilkinson_breaks(dmin, dmax, n=5, **kwargs):
    return _wilkinson(dmin, dmax, n, **kwargs)


def _wilkinson(dmin, dmax, m, Q=(1,5,2,2.5,3,4,1.5,7,6,8,9), mincoverage=0.8, mrange=None):
    if mrange is None:
        mrange = list(range(int(max(np.floor(m/2),2)), int(np.ceil(6*m))))
    best = None
    for k in mrange:
        result = _wilkinson_nice_scale(min=dmin, max=dmax, k=k, Q=Q, mincoverage=mincoverage, m=m)
        if best is None:
            best = result
        elif result is None:
            continue
        elif best is not None and result['score'] > best['score']:
            best = result

    return None if best is None else np.arange(best['lmin'], best['lmax']+best['lstep'], best['lstep'])


def _wilkinson_nice_scale(min, max, k, Q=(1,5,2,2.5,3,4,1.5,7,6,8,9), mincoverage=0.8, m=None):
    if m is None:
        m = k
    Q = np.concatenate((Q, (10,)))
    range_ = max - min
    intervals = k-1
    granularity = 1-abs(k-m)/m
    delta = range_ / intervals
    base = int(np.log10(delta))
    best = None

    for b in (base-1, base):
        dbase = 10 ** b
        for i in range(len(Q)):
            tdelta = Q[i] * dbase
            tmin = np.floor(min/tdelta) * tdelta
            tmax = tmin + intervals * tdelta
            if (tmin <= min) and (tmax >= max):
                rn = 1 if tmin <= 0 <= tmax else 0
                roundness = 1 - (i - rn) / len(Q)
                coverage = (max-min)/(tmax-tmin)
                if coverage > mincoverage:
                    tnice = granularity + roundness + coverage
                    if best is None or tnice > best['score']:
                        best = {'lmin': tmin, 'lmax': tmax, 'lstep': tdelta, 'score': tnice}
    return best


def log_breaks(dmin, dmax, n=5, base=10):
    f = np.log10 if base == 10 else np.log2 if base == 2 else None
    if f is None:
        raise ValueError("Cannot perform log transformation on base %s" % base)
    lmin = np.floor(f(dmin))
    lmax = np.ceil(f(dmax))
    if lmax == lmin:
        return base ** lmin
    by = np.floor((lmax - lmin) / n) + 1
    return base ** np.arange(lmin, lmax+by, by)

# test
if __name__ == '__main__':
    print(wilkinson_breaks(-0.12, 0.91, 3))
    print(wilkinson_breaks(0, 11, 3))
    print(wilkinson_breaks(0, 11, 5))
    print(wilkinson_breaks(-2e5, -1e5, 5))
    print(log_breaks(0.1, 1e7, 3))