#coding:utf-8
import numpy as np


def gen_batch(bath_size = 128, dim = 1024, dense_ratio = 0.1):
    """
    如果用批量梯度下降, batch_size 请设置为100000, 且只获取一次
    :param bath_size:
    :param dim:
    :param dense_ratio:
    :return: (w, X, y)
    """
    np.random.seed(2018) # 保证每次都是相同的w
    w = np.random.randn(dim)

    mask = (np.random.rand(dim) < (1 - dense_ratio)).astype(int)
    w = w * mask

    np.random.seed(None) # 保证每次的数据都是不同的
    X = np.random.randn(bath_size, dim)
    y = np.dot(X, w)
    return w, X, y

def line_search():

    return 0.0
def loss_function(w, X, y,grad_flag="gd"):
    # TODO 返回损失、梯度、海森矩阵

    delta=np.matmul(X,w)-y
    loss=0.5*np.sum(delta**2)
    """
    gd : gradient descent
    newton:
    n newton
    """
    grad=np.matmul(X.T,(np.matmul(X,w)-y))

    if grad_flag=='gd':
        return loss,grad
    if grad_flag=="newton":
        h_f=np.linalg.inv(np.matmul(X.T,X))
        grad=np.matmul(h_f,grad)

    return loss,grad

def dfp(w_k,X,y,D_k):
    """

    :param w_k: (m,)
    :param X: (N,m)
    :param y: (N,)
    :param D_k: (m,m)
    :return:
    """
    debug =False
    if debug : print("w_k :",w_k.shape,"X :",X.shape)
    if debug : print(np.shape(np.matmul(X,w_k)))

    loss=0.5*np.sum((np.matmul(X,w_k)-y)**2)

    g_k=np.matmul(X.T,(np.matmul(X,w_k)-y))

    if debug : print("g_k : ",g_k.shape,)

    d_k= - np.matmul(D_k,g_k)

    if debug : print("d_k : ",d_k.shape)

    X_d_k=np.matmul(X,d_k)# Xd_k

    line_lambda = (np.matmul(X_d_k.T,y)-np.matmul(X_d_k.T,np.matmul(X,w_k)))/np.matmul(X_d_k.T,X_d_k)
    s_k=line_lambda*d_k

    if debug : print("s_k : ",s_k.shape)

    w_k_1=w_k+s_k

    g_k_1=np.matmul(X.T,(np.matmul(X,w_k_1)-y))

    y_k=g_k_1-g_k

    if debug :print('y_k : ',y_k.shape)

    s_k_b=np.reshape(s_k,(np.shape(s_k)[0],1))
    y_k_b=np.reshape(y_k,(np.shape(y_k)[0],1))

    D_k_y_k=np.matmul(D_k,y_k_b)

    y_k_D_k=np.matmul(y_k_b.T,D_k)
    D_1=np.matmul(s_k_b,s_k_b.T)/np.matmul(s_k_b.T,y_k_b)
    D_2=np.matmul(D_k_y_k,y_k_D_k)/np.matmul(y_k_b.T,D_k_y_k)

    D_k_1=D_k+D_1-D_2

    if debug : print(s_k.shape,D_k_1.shape)


    return loss,-s_k,D_k_1

def bfgs(w_k,X,y,D_k):
    """

    :param w_k: (m,)
    :param X: (N,m)
    :param y: (N,)
    :param D_k: (m,m)
    :return:
    """
    debug =False
    if debug : print("w_k :",w_k.shape,"X :",X.shape)
    if debug : print(np.shape(np.matmul(X,w_k)))

    loss=0.5*np.sum((np.matmul(X,w_k)-y)**2)

    g_k=np.matmul(X.T,(np.matmul(X,w_k)-y))

    if debug : print("g_k : ",g_k.shape,)

    d_k= - np.matmul(D_k,g_k)

    if debug : print("d_k : ",d_k.shape)

    X_d_k=np.matmul(X,d_k)# Xd_k

    line_lambda = (np.matmul(X_d_k.T,y)-np.matmul(X_d_k.T,np.matmul(X,w_k)))/np.matmul(X_d_k.T,X_d_k)
    s_k=line_lambda*d_k

    if debug : print("s_k : ",s_k.shape)

    w_k_1=w_k+s_k

    g_k_1=np.matmul(X.T,(np.matmul(X,w_k_1)-y))


    y_k=g_k_1-g_k

    w_dim=np.shape(s_k)[0]

    s_k_b=np.reshape(s_k,(w_dim,1))
    y_k_b=np.reshape(y_k,(w_dim,1))

    ys=np.matmul(y_k_b.T,s_k_b)

    array_one=np.eye(w_dim)

    D_1=np.matmul(array_one-np.matmul(s_k_b,y_k_b.T)/ys,D_k)

    D_2=np.matmul(D_1,(array_one-np.matmul(y_k_b,s_k_b.T))/ys)

    D_k_1=D_k+D_2+np.matmul(s_k_b,s_k_b.T)/ys

    return loss,-s_k,D_k_1

def ftrl(w,z_t,n_t,X,y,alpha=1,):

    loss=0.5*np.sum((np.matmul(X,w)-y)**2)

    i=np.random.randint(np.shape(y)[0])

    x_i=X[i,:]
    y_i=y[i]

    g=x_i*(np.matmul(x_i,w)-y_i)

    delta_t=(np.sqrt(n_t+g*g)-np.sqrt(n_t))/alpha

    z_t=z_t+g-delta_t*w

    n_t=n_t+g*g

    return loss,z_t,n_t





def numeric_gradient(f, w, epsilon=1e-4):
    assert len(w.shape) == 1, "w必须是向量"

    g = np.zeros(w.shape)
    for i in range(w.shape[0]):
        dw = np.zeros(w.shape)
        dw[i] = epsilon
        df = f(w + dw) - f(w - dw)
        g[i] = df / epsilon / 2
    return g
