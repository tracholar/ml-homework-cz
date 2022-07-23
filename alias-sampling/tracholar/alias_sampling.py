# coding:utf-8
from random import random, randint

class AliasSampler(object):
    def __init__(self, p_arr):
        assert isinstance(p_arr, list)
        self.p_arr = p_arr
        self._build_alias_table()

    def _build_alias_table(self):
        p = []   # 命中概率
        alias = [] # 没有命中的情况下，应该采样的下标
        p = [x * len(self.p_arr) for x in  self.p_arr]
        alias = [None] * len(p)
        for i in range(len(p)):
            if p[i] < 1:
                for j in range(len(p)):
                    if p[j] > 1:
                        break
                alias[i] = j
                p[j] = p[j] - (1 - p[i])
            else:
                pass
        self.p = p
        self.alias = alias

    def sample(self):
        n = randint(0, len(self.p))
        if random() < self.p[n]:
            return n
        else:
            return self.alias[n]

print(randint(0, 10))
s = AliasSampler([0.1,0.2,0.3,0.4])

print(s.sample())