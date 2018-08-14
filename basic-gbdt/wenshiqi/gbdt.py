#coding:utf-8

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeRegressor

def load_data():
    '''
        加载数据
    '''
    dataset = load_iris()
    data = dataset.data
    target = dataset.target

    target[np.where(target != 0)] = 1
    target[np.where(target == 0)] = -1

    train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.33)
    # train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.33)
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 0  和  1
    """
    return train_x, test_x, train_y, test_y

def sigmoid(x):
    """
    请实现 sigmoid 函数
    :param x:
    :return:
    """
    return 1. / (1 + np.exp(-x))

def cal_residual( f ,y):
    # 计算loss对f的梯度(分类损失)
    res=y/(1.+np.exp(y*f))
    return res

def predict_score(X,y, trees,alpha):
    """
    预测得分
    :param X:
    :param trees:
    :return: score
    """
    #初始化f0
    f=np.log(1e-5 + (np.sum(y)/np.sum(1.0-y)))*np.ones((y.shape[0],))
    score = np.zeros(X.shape[0])

    for tree, leaf_values in trees:

        leaf_indexes = tree.apply(X)
        tmp_val = map(lambda x: leaf_values[x], leaf_indexes)
        f+=alpha*np.array(tmp_val)


    pred_prob=sigmoid(f)
    print "pred_prob:", pred_prob
    pred = np.where(pred_prob > 0.5, 1, -1)
    print "pred:", pred
    print "y:", y
    acc = np.mean(np.equal(y, pred))
    print "acc:", acc
    return score

def cal_leaf_val(res, indexes):
    res = np.array(res)
    leaf_index = set(indexes)
    all_val = {}
    for idx in leaf_index:
        r_idx = np.where(np.array(indexes)==idx)[0]
        leaf_val = np.sum(res[r_idx])/(np.sum(np.abs(res)*(2. - res)))
        all_val[idx] = leaf_val
    return all_val


def train(X, y, ntrees = 10, alpha = 0.1, mode='gbdt', epoches=20):
    """
    训练模型
    :param X: 特征
    :param y: 标签
    :param ntrees: 树的棵树
    :param alpha: 学习率
    :param mode: 学习模式, gbdt 一阶算法, xgboost 二阶算法
    :return: 返回参数 trees 返回回归树列表
    """

    #初始化f0
    f = np.log(1e-5 + (np.sum(y)/np.sum(1.0-y)))*np.ones((y.shape[0],))
    #初始化残差为样本值
    r = y
    #params保留构建好的树及叶子节点值
    params = []
    for i in range(0, ntrees):
        tmp_tree = DecisionTreeRegressor(max_depth=1)
        tmp_tree.fit(X, r)

        # 计算残差
        r = cal_residual(f, y)
        leaf_indexes = tmp_tree.apply(X)

        #计算叶子节点的值
        leaf_val = cal_leaf_val(r, leaf_indexes)
        params.append((tmp_tree, leaf_val))

        tmp_val = map(lambda x:leaf_val[x], leaf_indexes)

        #更新f值
        f += alpha * np.array(tmp_val)

        #计算loss并输出
        loss=np.log(1+np.exp(-y*f))
        print ('print res:',r,'print loss:',np.mean(np.sum(loss)))

    #返回树和叶子节点值
    return params

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
    train_x, test_x, train_y, test_y= load_data()
    # print len(train_x), len(train_y)
    # TODO: 实现迭代版本的gbdt
    trees = train(train_x, train_y)  # 以最佳参数重新训练模型
    predict_score(test_x,test_y,trees,0.5)


    # n_trees = kfold(X, y, k=3) #3折叠交叉验证选出最佳树的棵树
    # trees = train(X, y, ntrees=n_trees) #以最佳参数重新训练模型
    # yhat = predict(X, trees)
    # print('ACC:{0}'.format(np.mean(yhat == y)))
    #
    # score = predict_score(X, trees)
    # print('AUC:{0}'.format(auc(y, score)))
    #
    # # 二阶算法
    # trees = train(X, y, ntrees=n_trees, mode='xgboost')
    # yhat = predict(X, trees)
    # print('ACC:{0}'.format(np.mean(yhat == y)))
    #
    # score = predict_score(X, trees)
    # print('AUC:{0}'.format(auc(y, score)))

