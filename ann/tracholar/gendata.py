#coding:utf-8
import numpy as np



def gendata(n_sample = 1000, dim = 16, K = 10):
    np.random.seed(2019)
    data = []
    for i in range(K):
        mu = np.random.randn(dim)*10
        sigma = np.random.rand(dim)
        data.append(np.random.randn(int(n_sample/K), dim) * sigma + mu)
    return np.concatenate(data, axis=0)
