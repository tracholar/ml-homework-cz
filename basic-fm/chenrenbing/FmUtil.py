from sklearn.feature_extraction import DictVectorizer
from sklearn.datasets import make_classification
from sklearn.cross_validation import train_test_split
import numpy as np

def loadData(filename,path="../data/ml-100k"):
    data=[]
    y=[]
    users=set()
    items=set()
    with open(path+filename) as f:
        for line in f:
            (user,movieid,rating,ts)=line.split('\t')
            data.append({"user_id":str(user),"movie_id":str(movieid)})

def classification_data():
    X,y=make_classification(n_samples=8000,n_features=4,n_clusters_per_class=1)
    data=[{v:k for k,v in dict(zip(i,range(len(i)))).items()} for i in X]
    X_train,X_test,y_train,y_test=train_test_split(data,y,test_size=0.1,random_state=42)


    v=DictVectorizer()
    X_train=v.fit_transform(X_train)
    X_test=v.transform(X_test)

    return X_train,y_train,X_test,y_test

def gradient_check(f, x0, epsilon=1e-4):
    x1 = np.zeros(x0.shape)
    x2 = np.zeros(x0.shape)


    g = np.zeros(x0.shape)
    #print(x0.shape)

    x1 = x0
    x2 = x0

    x1 += epsilon
    x2 -= epsilon
    y1 = f(x1)
    y2 = f(x2)

    #print(np.shape(y1))
    print(x1,x2)
    print(y1,y2)
    g = (y1 - y2)/2/epsilon
    return g

def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))
def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

def logloss(y,p):

    return -y*np.log(p)-(1-y)*np.log(1-p)
def logloss_check(y,fx):
    return -y*np.log(sigmoid(fx))-(1-y)*np.log(1-sigmoid(fx))
