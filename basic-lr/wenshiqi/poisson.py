#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 21:23:02 2018

@author: wenshiqi
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

def load_data():
    '''
    加载数据
    '''
    dataset=load_iris()
    data=dataset.data
    target=dataset.target
    
    target[np.where(target!=0)]=1
    target[np.where(target==0)]=0

    train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.33)

    def encode_label(target):
        '''
        将样本标签转换为one-hot形式
        '''   
        target=np.reshape(target,(target.shape[0],1))

        m=np.array([[0,1]])
        temp=np.dot(target,m)
        
        s=np.array([0])
        s=np.reshape(s,(1,1))
       
        temp[np.where(temp[:,1:]==s)]=1
        return temp

    test_y_ = encode_label(test_y)
    train_y_ = encode_label(train_y)
    return train_x, train_y_, train_y, test_x, test_y_, test_y
    

def poisson(z):
    return np.exp(z)


def forward(X,w,b):
    '''
    计算模型输出
    '''
    z=np.dot(X,w)+b
    hx=poisson(z)
    return hx
    

def logloss(y, hx):
    j=-np.mean(-hx+y*np.log(hx+1e-5))
    return j

def backward(y,X,hx,w,b,lr):
    '''
    更新参数
    '''
    w=w+1./X.shape[0]*np.dot(X.T,(y-hx))*lr
    I=np.ones(shape=(X.shape[0],1))
    b=b+1./X.shape[0]*np.dot(I.T,(y-hx))*lr
    return w,b

def train(X,y,w,b,lr,target):
    '''
    模型训练
    '''
    max_iter = 1000
    for i in range(0, max_iter):
        hx=forward(X,w,b)
        loss=logloss(y,hx)
        acc=accuracy(target,hx)
        print '当前迭代次数：',i,'loss为：',loss,'accuracy为：',acc
        w,b=backward(y,X,hx,w,b,lr)
    return w,b


def accuracy(target,pred):
    pred=np.argmax(pred,axis=1)
    acc=np.sum(target==pred)/(1.0*target.shape[0])
    return acc


if __name__ == '__main__':
    X, y, target, test_X, test_y, test_target=load_data()

    w=np.random.normal(size=(4,2))
    b=np.random.normal(size=(2,))
    
    w,b=train(X,y,w,b,0.01,target)

    hx=forward(test_X,w,b)
    print '测试集acc为：',accuracy(test_target,hx)
