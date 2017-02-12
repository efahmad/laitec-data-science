

def memo(f):
    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = cache[args] = f(*args)
            return result
        except TypeError:
            return f(*args)
    return _f


@memo
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

print(fib(50))

# def sample_dec(f):
#     def _f():
#         print("BEFORE")
#         print(f.__name__)
#         print("AFTER")
#     return _f
#
#
# @sample_dec()
# def harchi():
#     print("HARCHI")
#
#
# harchi()
