#coding:utf-8


from __future__ import division
import numpy as np

def load_data():
    """
    请利用 sklearn.datasets.load_iris 函数构造数据集, 要求返回一个二元组 (X, y),
    X (n_samples, n_feature) 二维数组,类型 np.array
    y (n_samples,)           一维数组,取值为 +1  和  -1
    """

    # TODO: 你的代码
    from sklearn.datasets import load_iris
    data, target = load_iris(return_X_y=True)
    target = (target == 0).astype(int) * 2 - 1
    return data, target


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
            #print(y)
            root.setTarget(np.mean(y))

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
            #print("tree_:",y,X)
            root.setTarget(np.mean(y))
            return root
        else:
            idx,val=cart(X,y)

            root.fea_idx=idx
            root.value=val
            #print(idx)
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
            #print(feat_value)

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

if __name__=="__main__":

    model=DecisionTree(depth=3)
    X,y=load_data()
    y=y[:,np.newaxis]
    model.fit(X,y)
    pre_y=model.predict(X)
    for i in range(np.shape(pre_y)[0]):
        if pre_y[i]!=y[i]:
            print(" i : ",i)
    print(np.shape(y),np.shape(pre_y))
    print(np.shape(X))
    print(np.insert(X,0,values=y[:,0],axis=1))



