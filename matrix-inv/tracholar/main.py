#coding:utf-8
"""海森矩阵求逆的随机估计
参考论文: Understanding Black-box Predictions via Influence Functions
"""

import numpy as np

np.random.seed(2019)

n = 10
M = np.random.randn(n, n)
H = np.matmul(M.T, M)
H = H / np.linalg.norm(H) #归一化,构造谱半径小于1的对称方阵

v = np.random.randn(n)  # v向量,正真需要的不是 H^-1, 而是 H^-1 v
Hinv_gt = np.linalg.inv(H)
Hv_gt = np.dot(Hinv_gt, v)

Sk = np.eye(n)
Hv = v
for i in range(1, 100000):
    Sk = np.eye(n) + np.matmul(np.eye(n) - H, Sk)
    Hv = v + np.dot(np.eye(n) - H, Hv)
    if i % 1000 == 0:
        print('{0} error H^-1:{1}, error H^-1 v:{2}'.format(i,
                                                        np.linalg.norm(Hinv_gt - Sk),
                                                        np.linalg.norm(Hv_gt - Hv)))