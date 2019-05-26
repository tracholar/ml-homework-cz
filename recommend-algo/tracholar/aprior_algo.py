#coding:utf-8
"""频繁项集挖掘 Aprior 算法"""

from movielens_dataset import MovieLens
import pandas as pd

dataset = MovieLens()
df = dataset.get_user_like_list()

def gen_set_list(arr, Ck):
    res = []
    arr_set = set(arr)
    for c in Ck:
        if c not in arr_set:
            return []
    for c in arr:
        if c not in Ck:
            res.append(frozenset([c] + list(Ck)))
    return res


print gen_set_list(df[1], [])
