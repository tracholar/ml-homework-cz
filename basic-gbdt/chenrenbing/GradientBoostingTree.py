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

    def __init__(self,depth=3):

        self.depth=depth
        self.root=node()


    def fit(self,X,y):

        self.construct_tree(X,y,self.root,self.depth)



    def construct_tree(self,X,y,root,depth):
        depth-=1
        if depth==0:
            root.is_leaf=1
            target_=np.sum(y)/np.sum(np.abs(y)*(2-np.abs(y)))
            root.setTarget(target_)

        else:
            idx,val=cart(X,y)
            root.fea_idx=idx
            root.value=val

            flag=X[:,idx]<=val
            root.left=self.construct_tree_(X[flag],y[flag],depth)

            root.right=self.construct_tree_(X[~flag],y[~flag],depth)

    def construct_tree_(self,X,y,depth):
        depth-=1
        root=node()

        if (depth==0)|(np.var(y)==0):
            root.is_leaf=1

            target_=np.sum(y)/np.sum(np.abs(y)*(1-np.abs(y)))
            print("target_ :",target_)
            root.setTarget(target_)
            return root
        else:
            idx,val=cart(X,y)

            root.fea_idx=idx
            root.value=val

            flag=X[:,idx]<=val
            root.left=self.construct_tree_(X[flag],y[flag],depth)
            root.right=self.construct_tree_(X[~flag],y[~flag],depth)
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
def cart(X,y):

    row_x,col_x=np.shape(X)

    feat_list=[]

    for i in range(col_x):
        feat_list.append(list(set(X[:,i])))
    feat_idx=-1
    feat_val=-1.0
    min_var=10000000.0
    for idx in range(len(feat_list)):
        for feat_value in feat_list[idx]:


            flag=X[:,idx]<=feat_value
            left_y=y[flag]
            right_y=y[~flag]
            if(len(left_y)==0)|(len(right_y)==0):
                continue
            else:
                var_=np.var(left_y)+np.var(right_y)
                if(var_<min_var):
                    min_var=var_
                    feat_idx=idx
                    feat_val=feat_value

    print(" feat_idx : ",feat_idx," ",feat_val)
    return feat_idx,feat_val

class GradientBoostingTree:

    def __init__(self,itr=3,depth=3,learning_rate=0.01):
        self.itr=itr
        self.depth=depth
        self.learning_rate=0.01
        self.tree_list=[]
        self.learning_rate=learning_rate
    def fit(self,X,y):

        pre_y=np.random.rand(np.shape(y)[0],np.shape(y)[1])


        for i in range(self.itr):

            tree=DecisionTree(depth=self.depth)

            hat_y=y/(1+np.exp(y*pre_y))

            tree.fit(X,hat_y)

            pre_y+=self.learning_rate*tree.predict(X)
            self.tree_list.append(tree)



    def predict_proba(self,X):
        pre_y=np.zeros((np.shape(X)[0],1))
        for tree_ in self.tree_list:
            pre_y+=self.learning_rate*tree_.predict(X)

        return sigmoid(pre_y)

    def predict(self,X):
        pre_y=self.proba(X)

        pre_y[pre_y>0.5]=1
        pre_y[pre_y<0.5]=-1
        pre_y=pre_y.astype(int)
        return pre_y



if __name__=="__main__":

    model=GradientBoostingTree(itr=30,learning_rate=0.1)
    X,y=load_data()
    y=y[:,np.newaxis]
    model.fit(X,y)
    pre_y=model.predict(X)
    print(" ........................ ........")

    print(model.predict_proba(X))
    #print(np.insert(pre_y,0,values=y[:,0],axis=1))
    """
    from xgboost import XGBClassifier

    model2 = XGBClassifier(n_estimators=20,max_depth=3,objective='binary:logistic')

    #param = {'max_depth':3, 'eta':1, 'silent':1, 'objective':'binary:logistic' }
    #num_round = 2
    bst = model2.fit(X,y.ravel())

    preds = bst.predict(X)
    #print(preds)
    print(np.sum(np.array(preds)[:,np.newaxis]!=y))
    print(model2.predict_proba(X))
    print(model2.get_params())
    """