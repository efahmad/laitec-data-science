import re
import itertools


def solve(formula):
    for f in fill_in(formula):
        if is_valid(f):
            return f


def fill_in(formula):
    letters = set(re.findall('[A-Z]', formula))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(''.join(letters), ''.join(digits))
        yield formula.translate(table)


def is_valid(formula):
    try:
        return not re.search(r'\b0[0-9]', formula) and eval(formula)
    except ArithmeticError:
        return False


def test():
    assert solve("SEND + MORE == MONEY") == '9567 + 1085 == 10652'
    assert solve("CRACK + HACK == ERROR") == '42641 + 9641 == 52282'
    assert solve("ODD + ODD == EVEN") == '655 + 655 == 1310' or '855 + 855 == 1710'

    return 'tests passes'

print(test())