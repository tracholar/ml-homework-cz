#coding:utf-8
from __future__ import division
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from numpy import *
from random import normalvariate#正态分布
from datetime import datetime

def loadDataSet():

    # Load dataset
    wine_data = load_wine()
    X = wine_data['data']
    y = (wine_data['target'] == 1)

    X_train,X_val,y_train,y_val = train_test_split(X, y, test_size=0.2, random_state=0)

    # Standardize input
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    return  X_train,X_val,y_train,y_val

def sigmoid(z):
    return 1.0 / (1 + exp(-z))

def train(X_train,X_label,k,iter):
    alpha = 0.01

    #m,n分别为训练数据的样本数和特征数
    m,n=shape(X_train)

    #初始化参数
    w=zeros((n,1))#w为线性部分的权重矩阵
    w0=0.
    v=normalvariate(0.,0.2)*ones((n,k))#k为隐向量维度，v为隐向量

    for it in xrange(iter):
        loss_value=0
        for x in xrange(m):#对每个样本而言进行优化
            inter1=X_train[x]*v
            inter2= multiply(X_train,X_train)*multiply(v,v)
            #交叉项部分计算
            interaction =sum(multiply(inter1,inter1)-inter2)/2.

            p = w0 + X_train[x]*w + interaction #计算预测的输出
            pre = sigmoid(p[0,0])
            loss_value+=(X_label[x]-pre)*(X_label[x]-pre)

        
            loss = sigmoid(X_label[x]*p[0,0]) - 1


            #更新w0
            w0=w0-alpha*loss*X_label[x]

            for i in xrange(n):
                if X_train[x, i] != 0:
                    w[i, 0] = w[i, 0] - alpha * loss * X_label[x] * X_train[x, i]
                    for j in xrange(k):
                        v[i, j] = v[i, j] - alpha * loss * X_label[x] * (
                                X_train[x, i] * inter1[0, j] - v[i, j] * X_train[x, i] * X_train[x, i])
        print "迭代轮数:{},损失值{}".format(it, loss_value)



    return w0,w,v



def getAccuracy(X_train,X_label,w0,w,v):
    m,n =shape(X_train)
    error=0

    for x in xrange(m):
        inter1=X_train[x]*v
        inter2=multiply(X_train,X_train)*multiply(v,v)
        #交叉项计算
        interaction = sum(multiply(inter1,inter1)-inter2)/2.
        p= w0 + X_train[x]*w +interaction

        pre=sigmoid(p[0,0])

        if pre<0.5 and X_label[x]==1.0:
            error+=1
        elif pre>=0.5 and X_label[x]==0.0:
            error+=1
        else:
            continue

    return 1.*(m-error)/m



if __name__ == '__main__':
    X_train, X_val, y_train, y_val=loadDataSet()
    date_startTrain = datetime.now()
    print "开始训练"
    w_0, w, v = train(mat(X_train), y_train, 10, 15)
    print "训练准确性为：%f" %  getAccuracy(mat(X_train), y_train, w_0, w, v)
    date_endTrain = datetime.now()
    print "训练时间为：%s" % (date_endTrain - date_startTrain)
    print "开始测试"
    print "测试准确性为：%f" % getAccuracy(mat(X_val), y_val, w_0, w, v)
