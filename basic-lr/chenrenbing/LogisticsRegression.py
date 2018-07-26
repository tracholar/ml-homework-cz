#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 20:31:28 2018

@author: bing
"""

import sys
import __future__
import numpy as np

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression as LR

def score_sup(p,y):
    correct=np.sum(p==y)
    score_=correct*1.0/np.shape(y)[0]
    return score_

class LogisticRegression:
     
     def __init__(self,learning_rate=0.01,itr=1000,batch_size=16,verbose=False):
         self.learning_rate=learning_rate
         self.itr=itr
         self.batch_size=batch_size
         self.verbose=verbose
     def fit(self,X,y):
         
        X=np.array(X)
        row_x,col_x=np.shape(X)
        row_y,col_y=np.shape(y)
                 
        if(np.shape(y[y==0])[0]!=0):
            y[y==0]=-1
        if self.batch_size>row_x:
           self.batch_size=row_x
        self.weights=np.random.rand(col_x+1,1)
        #print(" init : ",self.weights.ravel())
        X_=np.insert(X,np.shape(X)[1],values=np.ones(np.shape(X)[0]),axis=1)

        for i in range(self.itr):
            count=0
            grad=np.zeros(np.shape(self.weights))*1.0
            for j in range(row_x):
                
                tmp_x=np.reshape(X_[j],np.shape(self.weights))
                """
                y_w_x=np.exp(-y * W^T * x)
                """
                y_w_x=np.exp(-y[j]*np.dot(self.weights.T,tmp_x))
                """
                grad=(y_w_x)*(-y*x)/(1+y_w_x)
                """
                grad+=y_w_x*(-y[j]*tmp_x)/(1+y_w_x)
                
                count=count+1
                if count==self.batch_size:
                   self.weights=self.weights-self.learning_rate*grad/self.batch_size
                   grad=np.zeros(np.shape(self.weights))*1.0
                   count=0
            if(self.verbose):
                if(i%2==0):
                    #print(" grad : ",grad)
                    label_=self.predict(X)
                    label_[label_==0]=-1
                    
                    print("itr : ",i," accuracy : ",score_sup(label_,y))
     """           
     def sgd(self,batch_data_x,batch_data_y):
         有问题，想实现多种梯度计算(BGD,SGD,MBGD)方式
         grad=np.zeros(np.shape(self.weights))       
         for i in range(self.batch_size):            
             tmp_x=np.reshape(batch_data_x[i],np.shape(self.weights))             
             #y_w_x=np.exp(-y * W^T * x)                          
             y_w_x=np.exp(-batch_data_y[i]*np.dot(self.weights.T,tmp_x))                         
             #grad=(1+y_w_x)*(-y*x)/(1+y_w_x)
             grad+=y_w_x*(-batch_data_y[i]*tmp_x)/(1+y_w_x)                         
         grad=grad/self.batch_size
         #print("grad : ",grad)
         return grad
     """
     def proba(self,x):
        tmp_x=np.dot(x,self.weights[:-1])+self.weights[-1]
        
        """
        proba=1/(1+np.exp(-w^T*x))
        """
        proba_=1.0/(1+np.exp(-tmp_x))
                      
        return proba_
            
    
     def predict(self,x):
         
         proba_=self.proba(x)        
         label_=np.zeros(np.shape(proba_))
         label_[proba_>0.5]=1         
         return label_
     
     def score(self,x,y):
         
         label_=self.predict(x)
         score_=score_sup(label_,y)
         return score_

         
data=load_iris() 
X=data.data
y=data.target
y[y>1]=1
y=y[:,np.newaxis] 
"""
选取部分作为测试集
"""
flag_choose=np.arange(np.shape(y)[0])
flag_train=(flag_choose%8!=0)
flag_test=(flag_choose%8==0)

for i in range(5):
    model=LogisticRegression(learning_rate=0.15,itr=2000,batch_size=1,verbose=False)
    model.fit(X[flag_train],y[flag_train])  
    print(i,"model's weights: ",model.weights.ravel())
    print(i,"model's precision : ",model.score(X[flag_test],y[flag_test])) 
    
model_sklearn=LR(C=100000000000)
model_sklearn.fit(X[flag_train],y[flag_train].ravel())
print("sklearn weights: ",model_sklearn.coef_,model_sklearn.intercept_)
      
print("sklearn's precision :",model_sklearn.score(X[flag_test],y[flag_test].ravel()))         
     
    