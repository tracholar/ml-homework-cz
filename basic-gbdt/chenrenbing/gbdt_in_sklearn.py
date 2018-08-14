#coding:utf-8

import abc
from abc import abstractmethod
from abc import ABCMeta
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from util import *


"""
挑战自己，提高能力。
1.正 负 1 的 对齐问题。
2.多分类问题
3.接口统一
"""


class loss():
    __metaclass__ = ABCMeta

    @abstractmethod
    def negative_gradient(self,y,pred):
        pass

class logloss(loss):

    def negative_gradient(self,y,pred):
        return y/(1+np.exp(y*pred))
class squareloss(loss):

    def negative_gradient(self,y,pred):

        return y-pred

lossFunction={'logloss':logloss,'mse':squareloss}

class gbdtClassifier:

    def __init__(self,max_depth=3,itr=3,learning_rate=0.1,loss='logloss'):

        self.depth=max_depth
        self.learning_rate=learning_rate
        self.itr=itr
        self.tree=[]
        self.loss=lossFunction[loss]()

    def fit(self,X,y):
        print(np.shape(y))
        pre_y=np.random.rand(np.shape(y)[0],np.shape(y)[1])
        for i in range(self.itr):
            tree_=DecisionTreeRegressor('mse',max_depth=3)

            hat_y=self.loss.negative_gradient(y,pre_y)

            tree_.fit(X,hat_y)
            tmp_pre=tree_.predict(X)
            pre_y+=self.learning_rate*np.reshape(tree_.predict(X),np.shape(pre_y))
            self.tree.append(tree_)
    def predict_proba(self,X):

        pre_y=np.zeros((np.shape(X)[0],1))
        for i in range(self.itr):
            pre_y+=self.learning_rate*np.reshape(self.tree[i].predict(X),np.shape(pre_y))
        return sigmoid(pre_y)

    def predict(self,X):

        proba_=self.predict_proba(X)
        proba_[proba_>=0.5]=1
        proba_[proba_<0.5]=-1
        return proba_

class gbdtRegression:

    def __init__(self,itr=10,max_depth=3,loss='mse',learing_rate=0.1):
        self.itr=itr
        self.depth=max_depth
        self.loss=lossFunction[loss]()
        self.learning_rate=learing_rate
    def fit(self,X,y):
        pass


if __name__=="__main__":

    X,y=load_data()
    y=y[:,np.newaxis]
    model=gbdtClassifier(itr=10,loss='logloss')

    model.fit(X,y)

    print(model.predict_proba(X))


