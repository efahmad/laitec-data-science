import re
import itertools


def faster_solve(formula):
    letters, f = compile_formula(formula)
    for digits in itertools.permutations((9, 8, 7, 6, 5, 4, 3, 2, 1, 0), len(letters)):
        try:
            if f(*digits):
                table = str.maketrans(''.join(letters), ''.join(map(str, digits)))
                res = formula.translate(table)
                if not re.search(r'\b0[0-9]', res):
                    return res
        except ArithmeticError:
            pass


def compile_word(word):
    if word.isupper():
        items = ["(%s * (10 ** %s))" % (w, i) for i, w in enumerate(word[::-1])]
        return "(" + " + ".join(items) + ")"
    return word


def compile_formula(formula, verbose=False):
    letters = set(re.findall('[A-Z]', formula))
    params = ', '.join(letters)
    body = ''.join(map(compile_word, re.split('([A-Z]+)', formula)))
    f = "lambda %s: %s" % (params, body)
    if verbose:
        print(f)
    return letters, eval(f)


def test():
    assert faster_solve("SEND + MORE == MONEY") == '9567 + 1085 == 10652'
    assert faster_solve("CRACK + HACK == ERROR") == '42641 + 9641 == 52282'
    assert faster_solve("ODD + ODD == EVEN") == '655 + 655 == 1310' or '855 + 855 == 1710'

    return 'tests passes'

test()