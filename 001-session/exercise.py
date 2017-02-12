from datetime import datetime
from itertools import product
from string import ascii_lowercase


def time_it(func):
    def my_func(*args, **kwargs):
        t0 = datetime.now()
        func(*args, **kwargs)
        t1 = datetime.now()
        print("{f} finished in: {t}".format(f=func.__name__, t=t1 - t0))

    return my_func


def get_generator(alphabet, length):
    alphabet_list = list(alphabet)
    for i in range(length):
        # Calc cartesian product for each length
        for prod in product(alphabet_list, repeat=i + 1):
            yield prod


@time_it
def execute_generator(alphabet, length):
    all_combinations = get_generator(alphabet, length)
    # Print items
    for item in all_combinations:
        print(''.join(item))
    # Calc count
    # n + n ** 2 + n ** 3 + ... + n ** m = (n ** (m + 1) - n) / (n - 1)
    n = len(alphabet)
    all_count = (n ** (length + 1) - n) / (n - 1)
    print("Count: " + str(all_count))


execute_generator(ascii_lowercase, 3)
