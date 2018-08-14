#coding:utf-8
import numpy as np
def load_data():
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 +1  和  -1
    """

    # TODO: 你的代码
    from sklearn.datasets import load_iris
    data, target = load_iris(return_X_y=True)
    target = (target == 0).astype(int) * 2 - 1
    return data, target
def sigmoid(x):

    return 1.0/(1+np.exp(-x))