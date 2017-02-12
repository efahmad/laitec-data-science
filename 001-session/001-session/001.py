import numpy as np
from tools import time_it
X = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

Y = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# print(list(zip(*Y)))
# print(list(zip([1, 2], [3, 4], [5, 6])))


@time_it(10000)
def py_mul(X, Y):
    return [
        [sum(x * y for x, y in zip(y_col, x_row)) for y_col in zip(*Y)] for x_row in X
    ]


@time_it(10000)
def np_mul(X, Y):
    return np.dot(X, Y)

py_mul(X, Y)
np_mul(X, Y)