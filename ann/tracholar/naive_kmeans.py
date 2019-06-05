#coding:utf-8
"""实现基本的基于K-Means聚类的矢量量化算法,从而实现基于矢量量化的快速索引
参考论文: “Video google: A text retrieval approach to object matching in videos.”
"""

import numpy as np
from gendata import gendata
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import time

class VQ(object):
    def __init__(self, D, K = 10):
        """
        :param D: 向量的维度
        :param K: 聚类的数目
        """
        self.D = D
        self.K = K

    def index(self, data):
        """
        :param data: n_sample x D 维矩阵
        :return:
        """
        clf = KMeans(n_clusters=self.K, verbose=False)
        clf.fit(data)
        self.clf = clf
        self.data = data

        data_cluster = clf.predict(data)
        self.data_index = {}
        for cluster, i in zip(data_cluster, range(len(data_cluster))):
            if cluster not in self.data_index:
                self.data_index[cluster] = []
            self.data_index[cluster].append(i)

        return self

    def query(self, q, n = 1):
        q = q.reshape((1, self.D))
        cluster = self.clf.predict(q)[0]
        ids = self.data_index[cluster]
        distance = np.sum((self.data[ids, :] - q)**2, axis=1)
        i = np.argmin(distance)
        return ids[i], self.data[ids[i]]


D = 10
n = 100000

def experiment(D=10, n=1000, K = 10):
    data = gendata(n_sample=n, dim=D, K=50)
    #plt.plot(data[:, 0], data[:, 1], '.')
    #plt.show()

    print data.shape
    vq = VQ(D=D, K=K)
    vq.index(data)
    q = np.random.randn(D)
    print 'q:', q

    t1 = time.time()
    i, v = vq.query(q)
    t2 = time.time()
    cost_vq = t2 - t1
    print 'query: i', i, 'v:', v, 'd=', np.sum((v - q)**2), 'cost:', cost_vq

    t1 = time.time()
    y = np.argmin(np.sum((data - q)**2, axis=1))
    t2 = time.time()
    cost_bf = t2 - t1
    print 'ground truth:', y, data[y, :], 'd=', np.sum((data[y] - q)**2), 'cost:', cost_bf

    return cost_vq, cost_bf

x = [10000, 100000, 1000000]
y_vq = []
y_bf = []
for n in x:
    vq, bf = experiment(n=n)
    y_vq.append(vq)
    y_bf.append(bf)
plt.semilogx(x, y_vq, '.-')
plt.semilogx(x, y_bf, '.-')

y_vq = []
y_bf = []
for n in x:
    vq, bf = experiment(n=n, K=50)
    y_vq.append(vq)
    y_bf.append(bf)
plt.semilogx(x, y_vq, '.-')
plt.semilogx(x, y_bf, '.-')


plt.legend(['vq-10', 'bf-10', 'vq-50', 'bf-50'])
plt.show()
