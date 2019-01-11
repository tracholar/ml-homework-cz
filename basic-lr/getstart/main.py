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
    pass

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

def gradient_check(f, x0, epsilon=1e-4):
    x1 = np.zeros(x0.shape)
    x2 = np.zeros(x0.shape)


    g = np.zeros(x0.shape)
    for i in range(x0.shape[0]):
        x1[:] = x0
        x2[:] = x0

        x1[i] += epsilon
        x2[i] -= epsilon
        y1 = f(x1)
        y2 = f(x2)
        g[i] = (y1 - y2)/2/epsilon
    return g

def predict(X, theta):
    """
    实现预测逻辑
    :param X:
    :param theta:
    :return: y
    """
    b = theta[0]
    w = theta[1:]
    margin = np.dot(X, w) + b
    return (margin > 0).astype(int) * 2 - 1

def train(X, y):
    """
    训练模型
    :return: 返回参数 theta
    """

    theta = np.random.rand(X.shape[1]+1)
    max_iter = 100000

    loss0 = 0
    for i in range(0, max_iter):
        # TODO: 你的代码
        pass

    return theta


if __name__ == '__main__':
    X, y = load_data()

    theta = np.random.rand(X.shape[1]+1)
    _, g = logloss(X, y, theta)
    print 'gradient diff:', np.linalg.norm(gradient_check(lambda x: logloss(X, y, x)[0], theta) - g)
    print g
    print gradient_check(lambda x: logloss(X, y, x)[0], theta)


    theta = train(X, y)

    yhat = predict(X, theta)
    print('ACC:{0}'.format(np.mean(yhat == y)))
    print('theta:', theta)

    from sklearn.linear_model import  LogisticRegression
    clf = LogisticRegression(C=1)
    clf.fit(X, y)
    print('sklearn theta:',clf.intercept_, clf.coef_[0])