#coding:utf-8
import numpy as np

n_samples = 10000
n_features = 10

np.random.seed(2018)
w = np.random.rand(n_features) * 0.3
b = np.random.rand() * 0.1

X = np.random.rand(n_samples, n_features)
lamb = np.exp(np.dot(X, w) + b)
for i in range(n_samples):
    n = np.random.poisson(lamb[i])
    print(n)
    fstr = ' '.join('{0}:{1:.3g}'.format(k, v) for k,v in zip(range(n_features), X[i]))
    print('{0} {1}'.format(n, fstr))