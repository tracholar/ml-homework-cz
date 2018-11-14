
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 21:23:02 2018
@author: wenshiqi
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


def getPoissonData():
    n_samples = 100
    n_features = 4

    np.random.seed(2018)
    w = np.random.rand(n_features) * 0.3
    b = np.random.rand() * 0.1

    X = np.random.rand(n_samples, n_features)
    lamb = np.exp(np.dot(X, w) + b)
    return X,np.random.poisson(lamb), w, b

def poisson(z):
    return np.exp(z)


def forward(X,w,b):
    '''
    计算模型输出
    '''
    z=np.dot(X,w)+b
    # hx=poisson(z)
    return z
    

def logloss(y, hx):
    # print hx
    j = (1.0/y.shape[0])*(-1. * np.sum(y*hx) + np.sum(poisson(hx)))
    # j=-np.mean(-hx+y*np.log(hx+1e-5))
    return j

def backward(y,X,hx,w,b,lr):
    '''
    更新参数
    '''
    # print "debug_info:", np.dot(X.T,y),  np.dot(X.T, poisson(hx)),X.T*y,X.T*poisson(hx)
    w = w + (np.sum(-X.T*y + X.T*poisson(hx),axis=1))*lr
    # w = w + (-np.dot(X.T,y) + np.dot(X.T, poisson(hx)))*lr
    I=np.ones(shape=(X.shape[0],1))
    b = b + (np.sum(-I.T*y + I.T* poisson(hx),axis=1))*lr

    # print "current weight and bias:", w, b
    return w,b

def train(X,y,w,b,lr):
    '''
    模型训练
    '''
    max_iter = 1000
    for i in range(0, max_iter):
        hx=forward(X,w,b)
        loss=logloss(y,hx)
        print '当前迭代次数：',i,'loss为：',loss
        w,b=backward(y,X,hx,w,b,lr)
    return w,b



if __name__ == '__main__':
    X, Y, w, b = getPoissonData()
    # print X
    # print w,b
    
    w = np.random.normal(size=(4,))
    b = np.random.normal()

    print "label:", Y
    w,b=train(X,Y,w,b,1e-5)
    print "current weight and bias:", w, b
    # hx=forward(test_X,w,b)
    # print '测试集acc为：',accuracy(test_target,hx)