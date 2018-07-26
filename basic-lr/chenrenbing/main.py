#coding:utf-8
'''
It is just a example, no solution here!
'''

import numpy as np

def load_data():
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 +1  和  -1
    """

    # TODO: 你的代码
    raise NotImplementedError()

def logloss(X, y, theta):
    """
    请实现logloss的计算和梯度的计算
    :param X: 特征 np.array (n_samples, n_feature)
    :param y: 标签 np.array (n_samples,)
    :param theta: 参数,类型 np.array, 其中 theta[0] 表示 b, theta[1:] 表示w
    :return: 返回二元组 (loss, gradient)
    """
    b = theta[0]
    w = theta[1:]

    loss = 0.0
    gradient = np.zeros(theta.shape)

    # TODO: 你的代码

    return loss, gradient

def predict(X, theta):
    """
    实现预测逻辑
    :param X:
    :param theta:
    :return: y
    """
    raise NotImplementedError()

def train(X, y):
    """
    训练模型
    :return: 返回参数 theta
    """

    theta = np.zeros(X.shape[1]+1)
    max_iter = 100
    for i in range(0, max_iter):
        # TODO: 你的代码
        pass

    return theta


if __name__ == '__main__':
    X, y = load_data()
    theta = train(X, y)
    yhat = predict(X, theta)
    print('ACC:{0}'.format(np.mean(yhat == y)))