#coding:utf-8
import numpy as np

def Reward(w):
    assert type(w) is np.ndarray and len(w) == 2
    w0 = np.array([0.2, 0.4])
    return np.exp(- np.linalg.norm(w - w0))

def CEM():

    n = 100
    k = 25
    mu = np.zeros(2)
    sigma = np.eye(2,2)

    for itr in range(100):
        w = np.random.multivariate_normal(mu, sigma, n)
        R = [Reward(w[i]) for i in range(n)]
        inds = np.argsort(R)[-k:]

        mu = np.mean(w[inds], axis=0)
        z = np.eye(2, 2) * max(0, 1 - 1.0*itr/40.0) # 随时间递减至0，才能收敛
        sigma = np.diag(np.var(w[inds], axis=0)) + z

        print 'Iter {}, max Reward {}, min Reward {}, mean Reward {}, std Reward {}, w=[{}, {}]'.format(itr, np.max(R), np.min(R), np.mean(R), np.std(R), mu[0], mu[1])


if __name__ == '__main__':
    CEM()
