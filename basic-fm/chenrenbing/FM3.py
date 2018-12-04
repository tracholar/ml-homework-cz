#encoding:utf-8


import numpy as np
import scipy.sparse as sp
from FmUtil import *

class FMClassifier:
    def __init__(self,num_iter=10,learning_rate=0.01,num_factors=3):
        self.num_factors=num_factors
        self.num_iter=num_iter
        self.learning_rate=learning_rate
        self.t=1.0
        self.t0=0.001
        self.init_stdev=0.1


    def fit(self,X,y):

        if isinstance(X,sp.csr_matrix) is False:
            X=sp.csr_matrix(X)

        indptr=X.indptr
        indices=X.indices
        data=X.data

        row,col=X.shape
        self.num_attribute=col

        self.w0 = 0.0
        self.w = np.zeros(self.num_attribute)
        #np.random.seed(28)
        #self.v = np.random.normal(scale=self.init_stdev,size=( self.num_attribute,self.num_factors))
        self.v = np.random.randn(self.num_attribute,self.num_factors)
        print("init v :",self.v)

        for itr in range(self.num_iter):
            for i in range(0,indptr.shape[0]-1):
                self.learning_rate = 1.0 / (self.t + self.t0)

                x=data[indptr[i]:indptr[i+1]]
                idx=indices[indptr[i]:indptr[i+1]]

                p,sum_=self.predict_instance(x,idx)

                grad_f=p-y[i]
                grad_w=np.zeros(self.w.shape)
                grad_v=np.zeros(self.v.shape)
                for x_,idx_ in zip(x,idx):
                    grad_w[idx_]+=grad_f*self.learning_rate*x_

                for f in xrange(self.num_factors):
                    for x_,idx_ in zip(x,idx):
                        grad_v[idx_,f]=grad_f*self.learning_rate*x_*(sum_[f]-x_*self.v[idx_,f])

                self.t+=1
                self.w-=grad_w
                self.v-=grad_v
                self.w0-=self.learning_rate*grad_f

    def predict_instance(self,x,idx):

        result=0.0
        result+=self.w0

        sum_=np.zeros(self.num_factors)
        sum_sqr_=np.zeros(self.num_factors)

        for x_,idx_ in zip(x,idx):
            result+=self.w[idx_]*x_

        for f in range(self.num_factors):
            sum_[f]=0
            sum_sqr_[f]=0
            for x_,idx_ in zip(x,idx):

                d=self.v[idx_][f]*x_
                sum_[f]+=d
                sum_sqr_[f]+=d*d

            result+= 0.5 * (sum_[f] * sum_[f] - sum_sqr_[f])

        return sigmoid(result),sum_


    def predict(self,X):
        if isinstance(X,sp.csr_matrix) is False:
            X=sp.csr_matrix(X)

        indptr=X.indptr
        indices=X.indices
        data=X.data

        row,col=X.shape

        proba=np.zeros(row)

        self.v=np.random.randn(col,self.num_factors)
        self.w=np.random.randn(col,1)
        self.w0=np.random.randn(1)


        for i in range(0,indptr.shape[0]-1):

            x=data[indptr[i]:indptr[i+1]]
            idx=indices[indptr[i]:indptr[i+1]]

            sum_v_x=np.zeros(self.num_factors)

            sum_vv_xx=0
            wx=0
            for x_,idx_ in zip(x,idx):

                wx+=self.w[idx_]*x_


                sum_v_x+=self.v[idx_,:]*x_

                sum_vv_xx+=np.dot(self.v[idx_,:],self.v[idx_,:])*x_*x_



            fx=self.w0+wx+0.5*(np.dot(sum_v_x,sum_v_x)-sum_vv_xx)

            proba[i]=sigmoid(fx)

        return proba

    def param_print(self):
        print(" w :",self.w)
        print(" v :",self.v)










