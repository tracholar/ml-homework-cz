# !/usr/bin/env python
# encoding=utf8
'''
  Author: zldeng hitdzl@gmail.com
  create@2017-11-24 10:29:56
'''
import sys
from multiprocessing import Pool
from functools import partial
import pandas as pd
import numpy as np
import copy_reg
import types
import traceback

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split



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


# def _pickle_method(m):
#     if m.im_self is None:
#         return getattr, (m.im_class, m.im_func.func_name)
#     else:
#         return getattr, (m.im_self, m.im_func.func_name)
#
#
# copy_reg.pickle(types.MethodType, _pickle_method)


class TreeNode(object):
    def __init__(self, is_leaf=False, leaf_score=None, split_feature=None, \
                 split_threshold=None, left_child=None,
                 right_child=None, direction=0):
        '''
        is_leaf: if True, only need to initialize leaf_score. other params are not used
        leaf_score: prediction score of the leaf node
        split_feature: split feature of the intermediate node
        split_threshold: split threshold of the intermediate node
        left_child: left child node
        right_child: right child node
        direction: if 0, those NAN sample goes to left child, else goes to right child.
        '''
        self.is_leaf = is_leaf
        self.leaf_score = leaf_score
        self.split_feature = split_feature
        self.split_threshold = split_threshold
        self.left_child = left_child
        self.right_child = right_child
        self.direction = direction


class Tree(object):
    def __init__(self):
        self.root = None
        # self.min_sample_split = None
        # self.colsample_bylevel = None
        self.eta = None
        # self.gamma = None
        self.num_thread = None
        # self.min_child_weight = None
        self.feature_importance = {}

    def calculateLeafScore(self, Y):
        '''
        计算叶子节点的值
        '''

        score = -Y.grad.sum() / (Y.hess.sum() + self.eta + 1e-5)

        return score

    def calculateSplitGain(self, left_Y, right_Y):
        '''
        gain = 0.5*(GL^2/(HL+lambda) + GR^2/(HR+lambda) - (GL+GR)^2/(HL+HR+lambda)) - gamma
        G_nan,Hnan is gain from NAN feature value data
        '''
        GL = left_Y.grad.sum()
        HL = left_Y.hess.sum()

        GR = right_Y.grad.sum()
        HR = right_Y.grad.sum()

        gain = 0.5 * (GL ** 2 / (HL + self.eta + 1e-5) + GR ** 2 / (HR + self.eta + 1e-5) \
                      - (GL + GR) ** 2 / (HL + HR + self.eta + 1e-5)) - self.gamma

        return gain

    def findBestThreshold(self, data, col):
        '''
        find best threshold for the given col feature
        data: the column of data: col,'label','grad','hess''
        '''
        best_threshold = None
        best_gain = -np.inf
        direction = 0
        try:
            tmp_data = data[[col, 'label', 'grad', 'hess']]

            
            # sort data by the selected feature
            tmp_data.reset_index(inplace=True)
            tmp_data.is_copy = False
            tmp_data[str(col) + '_idx'] = tmp_data[col].argsort()
            tmp_data = tmp_data.ix[tmp_data[str(col) + '_idx']]

            # 线性搜索找到最佳阈值
            for i in xrange(tmp_data.shape[0] - 1):
                # don't need to split at those same value
                cur_value, nxt_value = tmp_data[col].iloc[i], tmp_data[col].iloc[i + 1]
                if cur_value == nxt_value:
                    continue

                # split at this value
                this_threshold = (cur_value + nxt_value) / 2.0
                this_gain = None
                left_Y = tmp_data.iloc[:(i + 1)]
                right_Y = tmp_data.iloc[(i + 1):]

                # let the NAN data go to left and right, and chose the way which gets the max gain
                left_gain = self.calculateSplitGain(left_Y, right_Y)

                right_gain = self.calculateSplitGain(left_Y, right_Y)

                if left_gain < right_gain:
                    cur_direction = 1
                    this_gain = right_gain
                else:
                    cur_direction = 0
                    this_gain = left_gain

                if this_gain > best_gain:
                    best_gain = this_gain
                    best_threshold = this_threshold
                    direction = cur_direction
        except Exception, e:
            traceback.print_exc()
            sys.exit(1)

        return col, best_threshold, best_gain, direction

    def findBestFeatureAndThreshold(self, X, Y):
        """
        para:
            X [selected_n_samples,selected_feature_samples]
            Y [selected_n_samples,5] column is [label,y_pred,grad,hess,sample_weight]
        find the (feature,threshold) with the largest gain
        if there are NAN in the feature, find its best direction to go
        """
        direction = 0
        best_gain = - np.inf
        best_feature, best_threshold = None, None
        rsts = None

        # for each feature, find its best_threshold and best_gain
        # finally select the largest gain
        cols = list(X.columns)
        data = pd.concat([X, Y], axis=1)
        
        for col in cols:
            rst=self.findBestThreshold(data,col)
            if rst[2] > best_gain:
                best_gain = rst[2]
                best_threshold = rst[1]
                best_feature = rst[0]
                direction = rst[3] 

        return best_feature, best_threshold, best_gain, direction

    def splitData(self, X, Y, feature, threshold, direction):
        """
            split the dataset according to (feature,threshold), direction
            faeture_value < feature_threshold : left
            faeture_value >= feature_threshold : right
        """
        X_cols, Y_cols = list(X.columns), list(Y.columns)
        data = pd.concat([X, Y], axis=1)
        right_data = None
        left_data = None


        mask = data[feature] >= threshold
        right_data = data[mask]
        left_data = data[~mask]


        return left_data[X_cols], left_data[Y_cols], right_data[X_cols], right_data[Y_cols]

    def buildTree(self, X, Y, max_depth):
        '''
        build a tree recursively
        '''
        if max_depth == 0:
            is_leaf = True
            leaf_score = self.calculateLeafScore(Y)

            leaf_node = TreeNode(is_leaf=is_leaf, leaf_score=leaf_score)

            return leaf_node

    

        best_feature, best_threshold, best_gain, direction = self.findBestFeatureAndThreshold(X, Y)

        if best_gain <= 0:
            is_leaf = True
            leaf_score = self.calculateLeafScore(Y)
            leaf_node = TreeNode(is_leaf=is_leaf, leaf_score=leaf_score)

            return leaf_node

        # split data according to (best_feature,best_threshold,direction)
        left_X, left_Y, right_X, right_Y = self.splitData(X, Y, best_feature, best_threshold, direction)

        # creat left tree and right tree
        left_tree = self.buildTree(left_X, left_Y, max_depth - 1)
        right_tree = self.buildTree(right_X, right_Y, max_depth - 1)

        # update feature importance
        if self.feature_importance.has_key(best_feature):
            self.feature_importance[best_feature] += 1
        else:
            self.feature_importance[best_feature] = 1

        # merge left child and right child to get a sub-tree
        sub_tree = TreeNode(is_leaf=False, leaf_score=None,
                            split_feature=best_feature,
                            split_threshold=best_threshold,
                            left_child=left_tree, \
                            right_child=right_tree,
                            direction=direction)

        return sub_tree

    def fit(self, X, Y, max_depth=5, min_child_weight=1,
            colsample_bylevel=1.0, min_sample_split=10, \
            eta=1.0, gamma=0.0, num_thread=-1):
        '''
        X:pd.DataFram [n_sampels,n_features]
        Y:pd.DataFram [n_samples,5],column is [label,y_pred,grad,hess,sample_weight]
        '''
        # self.min_child_weight = min_child_weight
        # self.colsample_bylevel = colsample_bylevel
        # self.min_sample_split = min_sample_split
        self.eta = eta
        self.gamma = gamma
        # self.num_thread = num_thread

        self.root = self.buildTree(X, Y, max_depth)

    def _predict(self, tree_node, X):
        '''
        predict a single sample
        note that X is a tupe(index,pandas.core.series.Series) from df.iterrows()
        '''
        if tree_node.is_leaf:
            return tree_node.leaf_score

        elif pd.isnull(X[1][tree_node.split_feature]):
            if tree_node.direction == 0:
                return self._predict(tree_node.left_child, X)
            else:
                return self._predict(tree_node.right_child, X)
        elif X[1][tree_node.split_feature] < tree_node.split_threshold:
            return self._predict(tree_node.left_child, X)
        else:
            return self._predict(tree_node.right_child, X)

    def predict(self, X):
        '''
        predict multi samples
        X is DataFrame
        '''
        preds = []
        samples = X.iterrows()
        for sample in samples:
            pred = self._predict(self.root, sample)
            preds.append(pred)
        # func = partial(self._predict, self.root)
        #
        # if self.num_thread == -1:
        #     pool = Pool()
        #     preds = pool.map(func, samples)
        #     pool.close()
        #     pool.join()
        # else:
        #     pool = Pool(self.num_thread)
        #     preds = pool.map(func, samples)
        #     pool.close()
        #     pool.join()

        return np.array(preds)




if __name__ == '__main__':
    train_x, test_x, train_y, test_y= load_data()
    # print len(train_x), len(train_y)
    # TODO: 实现迭代版本的gbdt
    X = pd.DataFrame(train_x)
    y = pd.Series(train_y)

    Y = pd.DataFrame(y.values, columns=['label'])
    Y['y_pred'] = y
    Y['grad'] = y
    Y['hess'] = y

    tree=Tree()
    tree.fit(X,Y)
    # trees = train(train_x, train_y)  # 以最佳参数重新训练模型
    # predict_score(test_x,test_y,trees,0.5)


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

