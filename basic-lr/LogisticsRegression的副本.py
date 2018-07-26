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

class LogisticRegression1:
     
     def __init__(self,learning_rate=0.01,itr=1000,batch_size=16,verbose=False):
         self.learning_rate=learning_rate
         self.itr=itr
         self.batch_size=batch_size
         self.verbose=verbose
     def fit(self,X,y):
         
        X=np.array(X)
        row_x,col_x=np.shape(X)
        row_y,col_y=np.shape(y)
         
         
        if(row_x==0):
             print(" 输入数据维度不足 ")
             sys.exit(1)
        if(row_x!=row_y):
             print(" x y 维度不匹配")
             sys.exit(1)
        if(col_y!=1):
             print(" y 维度有问题 ")
        if(np.shape(y[y==0])[0]!=0):
            y[y==0]=-1
        if row_x<self.batch_size:
            self.batch_size=row_x
            
        
        self.weights=np.random.rand(col_x,1)
        print(" init : ",self.weights.T)
        #self.weights=np.zeros((col_x,1))
        #print("self.weight : ",np.shape(self.weights))
        for i in range(self.itr):
            
            batch_data_idx=np.random.randint(0,row_x,self.batch_size)
            batch_data_x=X#[batch_data_idx,:]
            batch_data_y=y#[batch_data_idx,:]
            for j in range(row_x):
                
                tmp_x=np.reshape(batch_data_x[j],np.shape(self.weights))
                y_w_x=np.exp(-batch_data_y[j]*np.dot(self.weights.T,tmp_x))
                grad=y_w_x*(-batch_data_y[j]*tmp_x)/(1+y_w_x)
                
                #grad=self.sgd(batch_data_x[j,:],batch_data_y[j,:])
            
                self.weights=self.weights-self.learning_rate*grad
            
            if(self.verbose):
                if(i%2==0):
                    #print(" grad : ",grad)
                    label_=self.predict(X)
                    label_[label_==0]=-1
                    
                    print("itr : ",i," accuracy : ",score_sup(label_,y))
     """           
     def sgd(self,batch_data_x,batch_data_y):
         
         grad=np.zeros(np.shape(self.weights))
         
         for i in range(self.batch_size):
             
             tmp_x=np.reshape(batch_data_x[i],np.shape(self.weights))
             """
             y_w_x=np.exp(-y * W^T * x)
             
             """
             y_w_x=np.exp(-batch_data_y[i]*np.dot(self.weights.T,tmp_x))
             
             """
              grad=(1+y_w_x)*(-y*x)/(1+y_w_x)
              
             """
             
             grad+=y_w_x*(-batch_data_y[i]*tmp_x)/(1+y_w_x)
             
             
         grad=grad/self.batch_size
         #print("grad : ",grad)
         return grad
     """
     def proba(self,x):
        tmp_x=np.dot(x,self.weights)
        
        """
        proba=np.exp( w^T* x)/(np.exp(w^T*x)+np.exp(-w^T*x))
        
        """
       
        proba_=1.0/(1+np.exp(-tmp_x))
        
        ##proba_=np.exp(tmp_x)/(np.exp(tmp_x)+np.exp(-tmp_x))
        
        return proba_
            
    
     def predict(self,x):
         
         proba_=self.proba(x)
         
         label_=np.zeros(np.shape(proba_))
         label_[proba_>0.5]=1
         
         return label_
     
     def score(self,x,y):
         
         label_=self.predict(x)
         score_=score_sup(label_,y)
         #print(" total sample : ",np.shape(y)[0]," correct : ",correct," accuracy : ",score_)
         #print(y)
         
         return score_

         
data=load_iris() 
X=data.data
y=data.target
y[y>1]=1
y=y[:,np.newaxis] 

flag_choose=np.arange(np.shape(y)[0])
flag_train=(flag_choose%8!=0)
flag_test=(flag_choose%8==0)

for i in range(2):
    model=LogisticRegression1(learning_rate=0.18,itr=10000,batch_size=160,verbose=False)
    model.fit(X[flag_train],y[flag_train])
    #print(y[flag_train])
    model_sklearn=LR(C=100000000000)
    model_sklearn.fit(X[flag_train],y[flag_train])
    
    print("my : ",model.weights.ravel())
    print(model_sklearn.coef_)
print("score : ",model.score(X[flag_test],y[flag_test]))       
print("score sk :",model_sklearn.score(X[flag_test],y[flag_test]))         
     
    