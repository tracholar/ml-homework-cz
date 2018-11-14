
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 20:31:28 2018

@author: bing
"""
from numpy import math
import sys
import __future__
import numpy as np

from sklearn.datasets import load_iris
def score_sup(p,y):
    correct=np.sum(p==y)
    score_=correct*1.0/np.shape(y)[0]
    return score_

def getPoissonData():
    n_samples = 10000
    n_features = 4

    np.random.seed(2018)
    w = np.random.rand(n_features) * 0.3
    b = np.random.rand() * 0.1

    X = np.random.rand(n_samples, n_features)
    lamb = np.exp(np.dot(X, w) + b)
    return X,np.random.poisson(lamb),w,b
    """
    for i in range(n_samples):
        n = np.random.poisson(lamb[i])
        print(n)
        fstr = ' '.join('{0}:{1:.3g}'.format(k, v) for k,v in zip(range(n_features), X[i]))
        print('{0} {1}'.format(n, fstr))
    """
class PoissonRegression:
     
     def __init__(self,learning_rate=0.01,itr=1000,batch_size=16,verbose=False):
         self.learning_rate=learning_rate
         self.itr=itr
         self.batch_size=batch_size
         self.verbose=verbose
     def fit(self,X,y):
         
        row_x,col_x=np.shape(X)
        row_y,col_y=np.shape(y)
        
        np.random.seed(2018)   
        self.weights=np.random.rand(col_x+1,1)
        #print(" init : ",self.weights.ravel())
        X_=np.insert(X,np.shape(X)[1],values=np.ones(np.shape(X)[0]),axis=1)
        
        for i in range(self.itr):
            

            for j in range(row_x):
                tmp_x=np.reshape(X_[j],np.shape(self.weights))
                """               
                grad=-y*x+np.exp(w^Tx)*x
                """              
                grad=-tmp_x*y[j]+np.exp(np.dot(self.weights.T,tmp_x))*tmp_x 
                """
                w=w-alpha * grad(w)
                """
                self.weights-=self.learning_rate*grad
            
            if(self.verbose):
                if(i%10==0):
                    print("itr : ",i," logloss : ",self.logloss(X,y))    
     def logloss(self,X,y):
         lambda_=np.exp(np.dot(X,self.weights[:-1])+self.weights[-1])
         
         tmp_y=np.zeros(np.shape(y))
         for i in range(np.shape(y)[0]):
               tmp_y[i]=log_factorial(y[i])
         """
         loos=-y*x+lambda+log(y!)
         """
         logloss_=-np.dot(y.T,np.log(lambda_))+np.sum(lambda_)\
                 +np.sum(tmp_y)
         return logloss_
     def proba(self,x):
         pass
            
    
     def predict(self,x):
         
         pass
     
     def score(self,x,y):
         
         pass
     
def log_factorial(x):
    return np.log(np.math.factorial(x))   
      
data=load_iris() 
X,y,W,b=getPoissonData()
y=y[:,np.newaxis] 
flag_choose=np.arange(np.shape(y)[0])
flag_train=(flag_choose%8!=0)
flag_test=(flag_choose%8==0)

print("actual weights : ",W," \nactual bias : ",b)
print("train ............. ")
for i in range(5):
    model=PoissonRegression(learning_rate=0.01,itr=100,batch_size=2,verbose=False)
    model.fit(X,y)
    print("my model's weights: ",model.weights.ravel())       
    ##print(" *********** ")   
    
    