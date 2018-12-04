import numpy as np
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression as LR
import warnings
from FmUtil import *

warnings.filterwarnings('error')

def score_sup(p,y):
    correct=np.sum(p==y)
    score_=correct*1.0/np.shape(y)[0]
    return score_
def load_data():


    data, target = load_iris(return_X_y=True)
    print(set(target))
    #target=target.astype(int)

    target[target>1]=1

    return data, target

class FMClassifier:
    def __init__(self,num_factors=3,learning_rate=0.01,itr=30):

        self.num_factors=num_factors
        self.learning_rate=0.01
        self.itr=itr
        self.t0=0.001
        self.t=1

    def fit(self,X,y):
         row_x,col_x=np.shape(X)

         self.v=np.random.rand(col_x,self.num_factors)
         self.factor_num=col_x
         self.w=np.random.rand(col_x)

         loss=0.0

         for i in range(self.itr):

             grad_factor_vector=np.zeros(np.shape(self.v))
             grad_w=np.zeros(np.shape(self.w))


             for j in range(row_x):
                 tmp_x=X[j,:]

                 vx=self.compute_vx(tmp_x)

                 fx=np.dot(self.w,tmp_x)+np.sum(0.5*self.v*vx)


                 grad_f=(sigmoid(fx)-y[j])






                 grad_factor_vector=vx*grad_f
                 grad_w=grad_f*tmp_x

                 self.v-=self.learning_rate*grad_factor_vector
                 self.w-=self.learning_rate*grad_w

                 self.learning_rate = 1.0 / (self.t + self.t0)
                 self.t+=1

    def proba_(self,X):
        return sigmoid(self.compute_vx(X))

    def compute_vx(self,X):
        result=np.zeros(np.shape(self.v))

        for i in range(self.factor_num):
            for j in range(self.factor_num):
                result[i]+=self.v[j]*X[i]*X[j]
            result[i]-=self.v[i]*X[i]*X[i]
        return result

    def predict_instance(self,x):

        vx=self.compute_vx(x)

        fx=np.dot(self.w,x)+np.sum(0.5*self.v*vx)
        y=sigmoid(fx)
        return y

    def predict(self,X):
        row_x=X.shape[0]

        y=np.zeros((row_x,1))

        for i in range(row_x):
            tmp_x=X[i]
            vx=self.compute_vx(tmp_x)

            fx=np.dot(self.w,tmp_x)+np.sum(0.5*self.v*vx)
            y[i]=sigmoid(fx)
        return y

    def param_print(self):
        print(" w :",self.w)
        print(" v :",self.v)

