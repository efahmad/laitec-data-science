import random
from collections import defaultdict


def trivial(p):
    n = len(p)
    swapped = [False] * n
    while not all(swapped):
        i, j = random.randrange(n), random.randrange(n)
        swap(p, i, j)
        swapped[i] = swapped[j] = True


def knuth(p):
    n = len(p)
    for i in range(n - 1):
        swap(p, i, random.randrange(i, n))


def swap(p, i, j):
    p[i], p[j] = p[j], p[i]


def test_shuffle(shuffler, deck='abcd', n=10000):
    counts = defaultdict(int)
    for _ in range(n):
        input_deck = list(deck)
        shuffler(input_deck)
        counts[''.join(input_deck)] += 1
    e = n * 1./factorial(len(deck))
    ok = all((0.9 <= counts[item]/e <= 1.1) for item in counts)
    name = shuffler.__name__
    print('%s(%s) %s' % (name,  deck, ('ok' if ok else '*** BAD ***')))
    for item, count in sorted(counts.items()):
        print("%s:%4.1f" % (item, count * 100. / n),)
    print('   ',)


def test_shufflers(shufflers=[knuth, trivial], decks=['abc', 'ab']):
    for deck in decks:
        print
        for f in shufflers:
            test_shuffle(f, deck)


def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

test_shufflers()