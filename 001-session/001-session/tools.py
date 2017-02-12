import time


def time_it(n):
    def time_it_dec(f):
        def _f(*args):
            t0 = time.clock()
            for _ in range(n):
                f(*args)
            print("{f}: {t}".format(f=f.__name__, t=time.clock() - t0))
        return _f
    return time_it_dec
