#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

def psd(L):
    """
    TODO 将对称矩阵L变为半正定矩阵
    :param L: 输入对称矩阵
    :return: PSD(L)
    """
    raise NotImplementedError()

def calc_sim(emb):
    """
    计算每个向量间的相似度
    :param emb:
    :return:
    """
    return np.dot(emb, emb.T)

def calc_L(q, emb, alpha=0.1, sigma = 1):
    """
    TODO 计算L矩阵，参考 Practical Diversified Recommendations
    on YouTube with Determinantal Point Processes
    :param q: array 每个item的质量分
    :param emb: 2d array 每个item的embedding向量
    :return: L nxn 矩阵,要求矩阵是半正定的
    """
    assert type(q) is np.ndarray and type(emb) is np.ndarray
    assert q.ndim == 1 and emb.ndim == 2
    assert q.shape[0] == emb.shape[0]

    raise NotImplementedError()

def gready_approx_max(L, idx, k = 10):
    """
    寻找最大概率的k维子序列
    :param L: L矩阵
    :param idx: 身下的下标序列
    :param k: 子序列大小，即窗口大小，默认为10
    :return: Y 最大概率的下标集合
    """
    Y = []
    remain_idx = [i for i in idx]
    for _ in range(min(k, len(remain_idx))):
        ## TODO 贪心搜索最优的k个下标
        raise NotImplementedError()

    return Y

def rank_via_dpp(L):
    """
    用行列式点过程排序，假设是已经排好序的。
    注意这里的实现跟论文中有所差异
    :param L:
    :return: R 最终的顺序
    """
    k = 10
    W = range(len(L)) # 剩下的下标
    R = [] # 排好序的item 下标
    while len(W) > 0:
        ## TODO 实现DPP排序过程
        raise NotImplementedError()
    return R



if __name__ == '__main__':
    n = 100 # item总数目
    d = 4   # item embedding向量长度
    q = np.array(sorted(np.random.rand(n), reverse=True))
    emb = np.random.rand(n, d)
    L = calc_L(q, emb, 1.)
    R = rank_via_dpp(L)
    print R

    plt.subplot(121)
    plt.imshow(calc_sim(emb), interpolation='nearest', cmap=plt.cm.hot)
    plt.colorbar()

    plt.subplot(122)
    plt.imshow(calc_sim(emb[R]), interpolation='nearest', cmap=plt.cm.hot)
    plt.colorbar()
    plt.show()


