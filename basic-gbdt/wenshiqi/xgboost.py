
# encoding=utf8

import sys
from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

from tree import Tree
import pickle

import abc
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from kfold import Kfold

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

    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 0  和  1
    """
    return train_x, test_x, train_y, test_y


class BaseLoss(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, reg_lambda):
        self.reg_lambda = reg_lambda

    @abc.abstractmethod
    def grad(self, preds, labels):
        pass

    @abc.abstractmethod
    def hess(self, preds, labels):
        pass

    @abc.abstractmethod
    def transform(self, preds):
        pass


class LogisticLoss(BaseLoss):
    '''
    label is {0,1}
    '''

    def transform(self, preds):
        return 1.0 / (1.0 + np.exp(-preds))

    def grad(self, preds, labels):
        preds = self.transform(preds)

        return (1 - labels) / (1 - preds + 1e-5) - labels / (preds + 1e-5)

    def hess(self, preds, labels):
        preds = self.transform(preds)

        return labels / (np.square(preds) + 1e-5) + (1 - labels) / (np.square(1 - preds) + 1e-5)


class binary_classification_loss(BaseLoss):
    """
    loss = \log(1 + \exp^{f(x) * y})
    """

    def transform(self, preds):
        return 1.0 / (1.0 + np.exp(-preds))

    def grad(self, preds, labels):
        preds = self.transform(preds)
        return -1. * labels / (1. + np.exp(preds * labels) + 1e-5)

    def hess(self, preds, labels):
        preds = self.transform(preds)
        return 1. * labels ** 2 / ((np.exp(preds * labels) + 1. + 1e-5) * (np.exp(-preds * labels) + 1. + 1e-5))

    def value(self, preds, labels):
        preds = self.transform(preds)
        return np.mean(np.log(1. + np.exp(-preds * labels)))

class xgboost(object):
    '''
    simple xgboost
    '''

    def __init__(self):
        self.trees = []
        self.eta = None
        self.num_boost_round = None
        self.first_round_pred = None
        self.loss = None
        self.subsample = None
        self.max_depth = None
        self.colsample_bylevel = None
        self.colsample_bytree = None
        self.reg_lambda = None
        self.min_sample_split = None
        self.gamma = None
        self.num_thread = None
        self.min_child_weight = None
        self.scale_pos_weight = None
        self.feature_importance = defaultdict(lambda: 0)
        self.pred_cutoff = 0.5
        self.epoches = None

        self.attr_need_save = ['eta', 'first_round_pred', 'reg_lambda', 'gamma', 'pred_cutoff', 'loss']

    def fit(self, X, y, epoches=10, eta=0.3,
            num_boost_round=1000, max_depth=5, scale_pos_weight=1,
            subsample=0.8, colsample_bytree=0.8, colsample_bylevel=0.8,
            min_child_weight=1, min_sample_split=10, reg_lambda=1.0, gamma=0,
            num_thread=-1, pred_cutoff=0.5):
        '''
        X:pandas.core.frame.DataFrame
        y:pandas.core.series.Series
        early_stopping_rounds: early_stop when eval rsult become worse more the early_stopping_rounds times
        maximize:the target is to make loss as large as possible
        eval_metric: evaluate method
        loss : loss function for optionmize
        num_boost_round : number of boosting
        max_depth: max_depth for a tree
        scale_pos_weight: weight for samples with 1 labels
        subsample: row sample rate when build a tree
        colsample_bytree: column sample rate when building a tree
        colsample_bylevel: column sample rate when spliting each tree node. when split a tree,the number of features = total_features*colsample_bytree*colsample_bylevel
        min_sample_split: min number of samples in a leaf node
        '''
        self.eta = eta
        self.num_boost_round = num_boost_round
        self.first_round_pred = 0.0
        self.subsample = subsample
        self.max_depth = max_depth
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.reg_lambda = reg_lambda
        self.min_sample_split = min_sample_split
        self.gamma = gamma
        self.num_thread = num_thread
        self.min_child_weight = min_child_weight
        self.scale_pos_weight = scale_pos_weight
        self.pred_cutoff = pred_cutoff
        self.epoches = epoches

        # 将X,y修改为能通过int下标（从0开始）进行索引的FramData
        X.reset_index(drop=True, inplace=True)
        y.reset_index(drop=True, inplace=True)

        self.loss = binary_classification_loss(self.eta)

        Y = pd.DataFrame(y.values, columns=['label'])
        Y['y_pred'] = self.first_round_pred
        Y['grad'] = self.loss.grad(Y.y_pred.values, Y.label.values)
        Y['hess'] = self.loss.hess(Y.y_pred.values, Y.label.values)

        Y['sample_weight'] = 1.0
        # 调整正样本权重
        Y.loc[Y.label == 1, 'sample_weight'] = self.scale_pos_weight
        for epoch in xrange(epoches):
            loss = []
            for i in range(self.num_boost_round):
                # row and column sample before training the current tree
                data = X.sample(frac=self.colsample_bytree, axis=1)  # column sample
                data = pd.concat([data, Y], axis=1)
                data = data.sample(frac=self.subsample, axis=0)  # row sample

                Y_selected = data[['label', 'y_pred', 'grad', 'hess']]
                X_selected = data.drop(['label', 'y_pred', 'grad', 'hess', 'sample_weight'], axis=1)

                # fit a tree
                if epoch==0:
                    tree = Tree()
                else:
                    tree = self.trees[i]
                tree.fit(X_selected, Y_selected, max_depth=self.max_depth,
                         min_child_weight=self.min_child_weight,
                         colsample_bylevel=self.colsample_bylevel,
                         min_sample_split=self.min_sample_split,
                         eta=self.eta,
                         gamma=self.gamma,
                         num_thread=self.num_thread)

                # predict the whole trainset and update y_pred,grad,hess
                preds = tree.predict(X)
                Y['y_pred'] += self.eta * preds

                Y['grad'] = self.loss.grad(Y.y_pred.values, Y.label.values) * Y.sample_weight
                Y['hess'] = self.loss.hess(Y.y_pred.values, Y.label.values) * Y.sample_weight

                loss.append(self.loss.value(Y.y_pred.values, Y.label.values))
                # update feature importance
                for k in tree.feature_importance.iterkeys():
                    self.feature_importance[k] += tree.feature_importance[k]
                if epoch==0:
                    self.trees.append(tree)
            print "epoch:{} loss:{}".format(epoch, np.mean(loss))

    def predict(self, X):
        assert len(self.trees) > 0

        preds = np.zeros(X.shape[0])

        preds += self.first_round_pred
        for tree in self.trees:
            preds += self.eta * tree.predict(X)

        res = self.loss.transform(preds)

        return (res > self.pred_cutoff).astype(int)

def _rank(x):
    sorted_x = sorted(zip(x, range(len(x))))
    r = [0 for k in x]
    cur_val = sorted_x[0][0]
    last_rank = 0
    for i in range(len(sorted_x)):
        if cur_val != sorted_x[i][0]:
            cur_val = sorted_x[i][0]
            for j in range(last_rank, i):
                r[sorted_x[j][1]] = float(last_rank + 1 + i) / 2.0
            last_rank = i
        if i == len(sorted_x) - 1:
            for j in range(last_rank, i + 1):
                r[sorted_x[j][1]] = float(last_rank + i + 2) / 2.0
    return r


def auc(preds, labels):
    r = _rank(preds)
    num_positive = len([0 for x in labels if x == 1])
    num_negative = len(labels) - num_positive
    sum_positive = sum([r[i] for i in range(len(r)) if labels[i] == 1])
    auc = ((sum_positive - num_positive * (num_positive + 1) / 2.0) /
           (num_negative * num_positive))
    return auc



if __name__ == '__main__':

    train_x, test_x, train_y, test_y = load_data()

    train_X = pd.DataFrame(train_x)
    train_Y = pd.Series(train_y)

    test_X = pd.DataFrame(test_x)
    test_Y = pd.Series(test_y)

    params = {'eta': 0.1,
              'max_depth': 5,
              'num_boost_round': 10,
              'scale_pos_weight': 1.0,
              'subsample': 0.7,
              'colsample_bytree': 0.7,
              'colsample_bylevel': 1.0,
              'min_sample_split': 10,
              'min_child_weight': 2,
              'reg_lambda': 10,
              'gamma': 0,
              'num_thread': 16}
    kf = Kfold(n_splits=1, shuffle=False, random_state=2018)

    # kfold to choose best 'eta', 'max_depth'
    cv_params = zip((0.02, 0.02, 0.02), (4, 5, 6))
    tgb = xgboost()
    max_auc = -np.inf
    best_eta = 0.1
    best_depth = 3

    tmp_auc = []
    print "start to select eta and depth..."
    for cvp in cv_params:
        print "*****************************"
        eta, max_depth = cvp
        params['eta'] = eta
        params['max_depth'] = max_depth
        for train_idx, test_idx in kf.split(train_x, train_y):
            train_label = train_y[train_idx]
            train_data = train_x[train_idx]

            test_label = train_y[test_idx]
            test_data = train_x[test_idx]

            train_label = pd.Series(train_label)
            train_data = pd.DataFrame(train_data)

            test_data = pd.DataFrame(test_data)
            test_label = pd.Series(test_label)

            tgb.fit(train_data, train_label, **params)
            pred_res = tgb.predict(test_data)
            tmp_auc.append(auc(pred_res, test_label))
            print "auc:", auc(pred_res, test_label)
        if np.mean(tmp_auc) > max_auc:
            max_auc = np.mean(tmp_auc)
            best_eta = eta
            best_depth = max_depth
    print "best eta:{}, best max_depth:{}".format(best_eta, best_depth)

    params = {'eta': eta,
              'max_depth': max_depth,
              'num_boost_round': 10,
              'scale_pos_weight': 1.0,
              'subsample': 0.7,
              'colsample_bytree': 0.7,
              'colsample_bylevel': 1.0,
              'min_sample_split': 10,
              'min_child_weight': 2,
              'reg_lambda': 10,
              'gamma': 0,
              'num_thread': 16}

    # tgb = xgboost()
    tgb.fit(train_X, train_Y, **params)

    pred_res = tgb.predict(test_X)
    print "AUC:{}".format(auc(pred_res, test_Y))
