# coding:utf-8


def print_tree(n = 10):
    x = list(range(n))
    space = [n - i for i in x]
    black = [(i + 1)*2 for i in x]

    for s, b in zip(space, black):
        print(' '*s, end='')
        print('△'*b, end='')
        print()
    for _ in x:
        print(' '*n, end='')
        print('△'*2)

print_tree(5)