#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

def psd(L):
    """
    将对称矩阵L变为半正定矩阵
    :param L: 输入对称矩阵
    :return: PSD(L)
    """
    w, v = np.linalg.eig(L)
    w = w * np.sign(w)
    L2 = v * w
    L2 = np.matmul(L2, v.T)
    return L2

def calc_sim(emb):
    """
    计算每个向量间的相似度
    :param emb:
    :return:
    """
    return np.dot(emb, emb.T)

def calc_L(q, emb, alpha=0.1, sigma = 1):
    """
    计算L矩阵，参考 Practical Diversified Recommendations
    on YouTube with Determinantal Point Processes
    :param q: array 每个item的质量分
    :param emb: 2d array 每个item的embedding向量
    :return: L nxn 矩阵,要求矩阵是半正定的
    """
    assert type(q) is np.ndarray and type(emb) is np.ndarray
    assert q.ndim == 1 and emb.ndim == 2
    assert q.shape[0] == emb.shape[0]

    n = q.shape[0]
    L = np.diag(q*q)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            L[i, j] = alpha * q[i] * q[j] * np.exp(-np.dot(emb[i], emb[j])/2/sigma/sigma)

    ## 将L变成PSD
    L2 = psd(L)
    return L, L2

def gready_approx_max(L):
    pass

def rank_via_dpp(L):
    """
    用行列式点过程排序，假设是已经排好序的
    :param L:
    :return: R 最终的顺序
    """

if __name__ == '__main__':
    n = 10
    d = 4
    q = np.array(sorted(np.random.rand(n), reverse=True))
    emb = np.random.rand(n, d)
    print calc_L(q, emb, 1.)

    plt.imshow(calc_sim(emb), interpolation='nearest', cmap=plt.cm.hot)
    plt.colorbar()
    plt.show()


