#coding:utf-8

import numpy as np
from sklearn.tree import DecisionTreeRegressor

def load_data():
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 0  和  1
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
    loss = np.sum(- y * np.log(sigmoid(z)) - (1 - y) * np.log(1 - sigmoid(z)))
    gradient = sigmoid(z) - y


    return loss, gradient

def predict(X, trees):
    """
    实现预测逻辑
    :param X:
    :param trees: 回归树列表
    :return: y
    """
    z = 0.5
    for t in trees:
        z += t.predict(X)
    return (sigmoid(z) > 0.5).astype(int)

def predict_score(X, trees):
    """
    预测得分
    :param X:
    :param trees:
    :return: score
    """
    score = np.zeros(X.shape[0])
    #TODO 你的代码

    return score
def train(X, y, ntrees = 10, alpha = 0.5, mode='gbdt'):
    """
    训练模型
    :param X: 特征
    :param y: 标签
    :param ntrees: 树的棵树
    :param alpha: 学习率
    :param mode: 学习模式, gbdt 一阶算法, xgboost 二阶算法
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

def auc(y, score):
    """
    计算AUC
    :param y: 真实标签
    :param score: 预测的概率或者得分
    :return: auc
    """

    # TODO 你的代码

    raise NotImplementedError

def kfold(X, y, k=3):
    """
    kfold 交叉验证
    :param X:
    :param y:
    :param k:
    :return: n_trees 树的棵树最佳参数
    """

    # TODO 你的代码
    raise NotImplementedError

if __name__ == '__main__':
    X, y = load_data()
    n_trees = kfold(X, y, k=3) #3折叠交叉验证选出最佳树的棵树
    trees = train(X, y, ntrees=n_trees) #以最佳参数重新训练模型
    yhat = predict(X, trees)
    print('ACC:{0}'.format(np.mean(yhat == y)))

    score = predict_score(X, trees)
    print('AUC:{0}'.format(auc(y, score)))

    # 二阶算法
    trees = train(X, y, ntrees=n_trees, mode='xgboost')
    yhat = predict(X, trees)
    print('ACC:{0}'.format(np.mean(yhat == y)))

    score = predict_score(X, trees)
    print('AUC:{0}'.format(auc(y, score)))