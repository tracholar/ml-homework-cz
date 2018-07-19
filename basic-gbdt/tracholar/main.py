#coding:utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor

def load_data():
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 0  和  1
    """

    #TODO 二分类数据
    raise NotImplementedError()

def sigmoid(x):
    """
    请实现 sigmoid 函数
    :param x:
    :return:
    """
    raise NotImplementedError()

def logloss(z, y):
    """
    请实现logloss的计算和梯度的计算
    :return: 返回二元组 (loss, gradient)
    """

    loss = 0.0
    gradient = np.zeros(y.shape)

    # TODO: 你的代码


    return loss, gradient

def predict(X, trees):
    """
    实现预测逻辑
    :param X:
    :param trees: 回归树列表
    :return: y
    """
    raise NotImplementedError()

def train(X, y, ntrees = 10, alpha = 0.5):
    """
    训练模型
    :return: 返回参数 trees 返回回归树列表
    """

    trees = []
    z = 0.5
    for i in range(0, ntrees):
        # TODO: 你的代码
        raise NotImplementedError()

    return trees

if __name__ == '__main__':
    X, y = load_data()
    trees = train(X, y)
    yhat = predict(X, trees)
    print('ACC:{0}'.format(np.mean(yhat == y)))