import re
import itertools


def faster_solve(formula):
    letters, f = compile_formula(formula)
    for digits in itertools.permutations((9, 8, 7, 6, 5, 4, 3, 2, 1, 0), len(letters)):
        try:
            if f(*digits):
                table = str.maketrans("".join(letters), "".join(map(str, digits)))
                res = formula.translate(table)
                if not re.search(r"\b0[0-9]", res):
                    return res
        except ArithmeticError:
            pass


def compile_word(word):
    if word.isupper():
        items = ["(" + w + " * (10 ** " + str(i) + "))" for i, w in enumerate(word[::-1])]
        return "(" + " + ".join(items) + ")"
    return word


def compile_formula(formula):
    letters = set(re.findall(r"[A-Z]", formula))
    params = ", ".join(letters)
    words = re.split(r"([A-Z]+)", formula)
    body = ''.join(map(compile_word, words))
    f = "lambda {params}: {body}".format(params=params, body=body)
    return letters, eval(f)


def test():
    assert faster_solve("ODD + ODD == EVEN") == '655 + 655 == 1310' or '855 + 855 == 1710'
    assert faster_solve("CRACK + HACK == ERROR") == '42641 + 9641 == 52282'
    assert faster_solve("SEND + MORE == MONEY") == '9567 + 1085 == 10652'

    print('Tests were passed')

test()
