

from itertools import permutations
p = permutations

def perm(iterable, r=None):
    items = list(iterable)
    r = len(items) if r is None else r
    answers = []
    def sub(items, k, p):
        if k == 0:
            answers.append(p)
        else:
            for i in range(k):
                # sub(list_del(items, i), k-1, p+(items[i],))
                sub(items[:i] + items[i+1:], k-1, p+(items[i],))
    sub(items, r, ())
    return answers

if __name__ == '__main__':
    tests = (list(range(3)), ['a','b','c','d'], list(range(100, 106)))
    for t in tests:
        pa = list(p(t))
        pb = perm(t)
        if set(pa) == set(pb):
            print('yes')
        else:
            print('no')
    for t in tests:
        for r in range(1, len(t)):
            pa = list(p(t))
            pb = perm(t)
            if set(pa) == set(pb):
                print('yes')
            else:
                print('no')
    