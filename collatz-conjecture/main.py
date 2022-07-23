# coding:utf-8


def simulate(num):
    def _next(n):
        if n % 2 == 0:
            return n // 2
        return n * 3 + 1

    while num > 1:
        yield num
        num = _next(num)
    yield num

for k, n in enumerate(simulate(int(1e100))):
    if (k + 1) % 10 == 0:
        print("\n")
    print(n, end="\t")

