#coding:utf-8
"""评估推荐效果, 每个函数都只算一个user的score,多个user需要将每个user的score平均"""
from math import log

def log2(x):
    return log(x)/log(2)

def precision_at_n(pred_list, pos_list, n):
    p = sum(1 for i in pred_list[:n] if i in pos_list)
    return 1.0*p/n

def recall_at_n(pred_list, pos_list, n):
    p = sum(1 for i in pred_list[:n] if i in pos_list)
    return 1.0*p/len(pos_list)

def f1_at_n(pred_list, pos_list, n):
    p = precision_at_n(pred_list, pos_list, n)
    r = recall_at_n(pred_list, pos_list, n)
    return 2*p*r/(p+r)

def _idcg_at_n(pos_list, n):
    return sum(1.0/log2(i+2) for i in range(min(n, len(pos_list))))

def ndcg_at_n(pred_list, pos_list, n):
    ndcg = sum(1.0/log2(i+2) for i, item in enumerate(pred_list) if item in pos_list and i < n)
    idcg = _idcg_at_n(pos_list, n)
    return ndcg / idcg

def mrr(pred_list, pos_list, n):
    pass

if __name__ == '__main__':
    pred_list = [2, 3,7,1,0]
    pos_list = [2,3]
    n = 3
    print 'P@N:', precision_at_n(pred_list, pos_list, n)
    print 'R@N:', recall_at_n(pred_list, pos_list, n)
    print 'F1@N:', f1_at_n(pred_list, pos_list, n)
    print 'ndcg@N:', ndcg_at_n(pred_list, pos_list, n)