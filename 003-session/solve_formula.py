import re
from itertools import permutations


def solve(formula):
    for item in fill_in(formula):
        if validate(item):
            return item


def fill_in(formula):
    letters = set(re.findall(r"[A-z]", formula))
    for digits in permutations("1234567890", len(letters)):
        table = str.maketrans("".join(letters), "".join(digits))
        yield formula.translate(table)


def validate(formula):
    try:
        return not re.findall(r"\b0", formula) and eval(formula)
    except ArithmeticError:
        return False


def test():
    assert solve("ODD + ODD == EVEN") == '655 + 655 == 1310'
    assert solve("CRACK + HACK == ERROR") == '42641 + 9641 == 52282'
    assert solve("SEND + MORE == MONEY") == '9567 + 1085 == 10652'

    return 'Tests were passed'


# print(solve("ODD + ODD == EVEN"))
# print(solve("CRACK + HACK == ERROR"))
# print(solve("SEND + MORE == MONEY"))

print(test())
