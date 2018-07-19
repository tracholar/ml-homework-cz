#coding:utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor

def load_data():
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 +1  和  -1
    """

    from sklearn.datasets import load_iris
    data, target = load_iris(return_X_y=True)
    target = (target == 0).astype(int)
    return data, target

def sigmoid(x):
    """
    请实现 sigmoid 函数
    :param x:
    :return:
    """
    return 1/(1+np.exp(-x))

def logloss(z, y):
    """
    请实现logloss的计算和梯度的计算
    :return: 返回二元组 (loss, gradient)
    """

    loss = 0.0
    gradient = np.zeros(y.shape)

    # TODO: 你的代码
    loss = np.sum(- y * np.log(sigmoid(z)) - (1 - y) * np.log(1 - sigmoid(z)))
    gradient = sigmoid(z) - y

    return loss, gradient

def predict(X, trees):
    """
    实现预测逻辑
    :param X:
    :param theta: 回归树列表
    :return: y
    """
    z = 0.5
    for t in trees:
        z += t.predict(X)
    return (sigmoid(z) > 0.5).astype(int)

def train(X, y, ntrees = 10, alpha = 0.5):
    """
    训练模型
    :return: 返回参数 trees 返回回归树列表
    """

    trees = []
    z = 0.5
    for i in range(0, ntrees):
        # TODO: 你的代码
        loss, gradient = logloss(z, y)
        clf = DecisionTreeRegressor(max_depth=3)
        clf.fit(X, - alpha * gradient)
        z += clf.predict(X)
        trees.append(clf)

        print i, loss

    return trees

if __name__ == '__main__':
    X, y = load_data()
    trees = train(X, y)
    yhat = predict(X, trees)
    print('ACC:{0}'.format(np.mean(yhat == y)))