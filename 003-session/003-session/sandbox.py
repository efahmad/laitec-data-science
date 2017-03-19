# RE
# TT
# ITERTOOLS
# TRY ... EXCEPT ... FINAL

# from itertools import permutations
#
# print(list(permutations([1, 2, 3, 4], 2)))

# table = str.maketrans('ABC', '123')
# s = 'A + B == C'
# print(s.translate(table))

# a = 10
# b = 0
# import sys
#
# sys.exit(100)
# LBYL
# if b == 0:
#     print("B 0 nabayad bashad")
# else:
#     print(a / b)

# it's easier to ask for forgiveness than permission
# try:
#     print(a / b)
# except ArithmeticError:
#     print("B 0 nabayad bashad")
# finally:
#     print("DONE")

# class MyException(Exception):
#     pass

# input("Enter a number")
# raise MyException("Harchi")

# falsy values:  0, 0.0, 0j, Fasle, None, '', "", [], {}, set(), __len__, __bool__

# import re

# m = re.match('a.i', 'ali kalan')
# m = re.match('a.i', 'kalan ali')
# m = re.search('\Aa.i', 'kalan ali')
# print(m)
# m = re.findall("[A-Z]", "ODD + ODD == EVEN")
# m = re.split('([A-Z]+)', "ODD + ODD == EVEN")
# print(m)

# m = re.search('ع.ی', 'علی')
# print(m)


def my_range(*args):
    l = len(args)
    if l == 3:
        start, stop, step = args
    elif l == 2:
        start, stop = args
        step = 1
    elif l == 1:
        start, step = 0, 1
        stop = args[0]

    while start < stop:
        yield start
        start += step

# g = my_range(4)
# for i in g:
#     print(i)
# from dis import dis, show_code
# dis(my_range)
# show_code(dis)

# for i in range(5, 10, 3):
#     print(i)
