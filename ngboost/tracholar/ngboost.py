#coding:utf-8
from __future__ import print_function
import numpy as np


def gen_regression_data(n_sample=1000, n_dim=10):
    """
    生成测试的回归数据
    :param n_sample: 样本数目
    :param n_dim:    特征维度
    :return: (X, y, mu, sigma, w_mu, w_sigma)
    """
    X = np.random.rand(n_sample, n_dim)
    w_mu = np.random.rand(n_dim)
    w_sigma = np.random.rand(n_dim)
    mu = np.dot(X, w_mu)
    sigma = np.exp(np.dot(X, w_sigma)) # 对数正态分布
    y = np.random.rand(n_sample) * sigma + mu
    return X, y, mu, sigma, w_mu, w_sigma

class NGBoost(object):
    _mu_trees = []
    _sigma_triees = []
    def __init__(self):
        pass

    def calc_nature_gradient(self, y, mu, sigma, **kwargs):
        """
        计算梯度
        :param yhat:
        :param y:
        :param kwargs:
        :return: (d_mu, d_sigma)
        """
        d_mu = mu - y
        d_sigma = np.zeros(sigma.shape)
        return d_mu, d_sigma

    def boost(self, X, g):
        from sklearn.tree import DecisionTreeRegressor
        tree = DecisionTreeRegressor(max_depth=3)
        tree.fit(X, g)
        return tree

    def predict(self, X):
        """
        预测期望和方差
        :param X:
        :return:
        """
        mu = np.zeros(X.shape[0])
        for t in self._mu_trees:
            mu += t.predict(X)

        sigma = np.zeros(X.shape[0])
        for t in self._sigma_triees:
            sigma += t.predict(X)


        return mu, np.exp(sigma)

    def fit(self, X, y, max_iter = 10):
        for _ in range(max_iter):
            mu, sigma = self.predict(X)
            d_mu, d_sigma = self.calc_nature_gradient(y, mu, sigma)
            mu_tree = self.boost(X, -d_mu)
            sigma_tree= self.boost(X, -d_sigma)
            self._mu_trees.append(mu_tree)
            self._sigma_triees.append(sigma_tree)
        return self

if __name__ == '__main__':
    X, y, mu, sigma, w_mu, w_sigma = gen_regression_data()

    boost = NGBoost()
    boost.fit(X, y)
    mu_, sigma_ = boost.predict(X)
    print("mu:diff")
    print(zip(mu, mu_))
    print("sigma:diff")
    print(zip(sigma, sigma_))

