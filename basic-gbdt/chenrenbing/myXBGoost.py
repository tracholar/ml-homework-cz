#coding:utf-8

import numpy as np
from util import *

class node:
    def __init__(self,is_leaf=0,idx=None,val=None):
        self.left=None
        self.right=None
        self.is_leaf=is_leaf
        self.target=None

        self.value=val
        self.fea_idx=idx

    def setTarget(self,val):
        self.target=val

class DecisionTree:

    def __init__(self,depth=3,alpha=1):

        self.depth=depth
        self.root=node()
        self.alpha=alpha

    def fit(self,X,y,pred):

        self.construct_tree(X,y,pred,self.root,self.depth)



    def construct_tree(self,X,y,pred,root,depth):
        depth-=1
        if depth==0:
            root.is_leaf=1
            target_=-getG(pred,y)/(getH(pred)+self.alpha)
            root.setTarget(target_)

        else:
            idx,val=cart(X,y,pred,self.alpha)

            root.fea_idx=idx
            root.value=val

            flag=X[:,idx]<=val

            root.left=self.construct_tree_(X[flag],y[flag],pred[flag],depth)
            root.right=self.construct_tree_(X[~flag],y[~flag],pred[~flag],depth)

    def construct_tree_(self,X,y,pred,depth):
        depth-=1
        root=node()

        if (depth==0):
            root.is_leaf=1

            target_=-getG(pred,y)/(getH(pred)+self.alpha)

            print("target_ :",target_)
            root.setTarget(target_)
            return root
        else:
            idx,val=cart(X,y,pred,self.alpha)

            root.fea_idx=idx
            root.value=val

            flag=X[:,idx]<=val
            root.left=self.construct_tree_(X[flag],y[flag],pred[flag],depth)
            root.right=self.construct_tree_(X[~flag],y[~flag],pred[~flag],depth)

        return root

    def predict(self,X):
        y=np.zeros((np.shape(X)[0],1))
        for i in range(np.shape(X)[0]):
            y[i]=self.search_tree(X[i,:],self.root)
        return y

    def search_tree(self,x,root):
        if root.is_leaf==1:
            return root.target
        else:
            if x[root.fea_idx]<=root.value:
                return self.search_tree(x,root.left)
            else:
                return self.search_tree(x,root.right)
def getH(pred):
    return np.sum(pred*(1-pred))
def getG(pred,label):

    return np.sum(pred-label)

def cart(X,y,pred,alpha):

    row_x,col_x=np.shape(X)
    feat_list=[]
    for i in range(col_x):
        feat_list.append(list(set(X[:,i])))
    feat_idx=-1
    feat_val=-1.0
    min_var=-10000000.0
    for idx in range(len(feat_list)):
        for feat_value in feat_list[idx]:
            flag=X[:,idx]<=feat_value
            left_y=y[flag];left_pred=pred[flag]
            right_y=y[~flag];right_pred=pred[~flag]
            if(len(left_y)==0)|(len(right_y)==0):
                continue
            else:

                var_=np.power(getG(left_pred,left_y),2)/(getH(left_pred)+alpha)\
                     +np.power(getG(right_pred,right_y),2)/(getH(right_pred)+alpha)\
                     -np.power(getG(pred,y),2)/(getH(pred)+alpha)-alpha

                if(var_>min_var):
                    min_var=var_
                    feat_idx=idx
                    feat_val=feat_value


    print(" feat_idx : ",feat_idx," ",feat_val)
    return feat_idx,feat_val


class xgboost_:

    def __init__(self,itr=3,depth=3,learning_rate=0.1,alpha=1):
        self.itr=itr
        self.depth=depth
        self.learning_rate=0.01
        self.tree_list=[]
        self.alpha=alpha

    def fit(self,X,y):

        #f_y=np.random.rand(np.shape(y)[0],np.shape(y)[1])
        f_y=np.ones(np.shape(y))*1.0/(1+np.exp((1+np.mean(y))/(1-np.mean(y))))

        for i in range(self.itr):
            print(" itr : ",i)
            tree=DecisionTree(depth=self.depth,alpha=self.alpha)
            #hat_y=- y/(1+np.exp(y*pre_y))
            #print(" hat_y : ",hat_y)
            pre_y=sigmoid(f_y)
            tree.fit(X,y,pre_y)

            f_y+=self.learning_rate*tree.predict(X)
            self.tree_list.append(tree)


    def proba(self,X):
        pre_y=np.zeros((np.shape(X)[0],1))
        for tree_ in self.tree_list:
            pre_y+=self.learning_rate*tree_.predict(X)

        return sigmoid(pre_y)

    def predict(self,X):
        pre_y=self.proba(X)
        print(pre_y)
        pre_y[pre_y>0.5]=1
        pre_y[pre_y<0.5]=0
        pre_y=pre_y.astype(int)
        return pre_y



if __name__=="__main__":

    model=xgboost_(itr=10,depth=3,learning_rate=1,alpha=1)


    X,y=load_data()
    y[y==-1]=0
    y=y[:,np.newaxis]
    model.fit(X,y)
    pre_y=model.predict(X)
    print(" ........................ ........")
    print(" error count : ",np.sum(pre_y!=y))
    import xgboost


