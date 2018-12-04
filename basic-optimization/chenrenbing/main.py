#coding:utf-8

def bgd_optimizer(w, g, lr=0.1, l1=0, l2=0.1):
    """
    实现批量梯度下降
    :param w:
    :param g:
    :param lr:
    :return:
    """

    grad_=g+l2*w
    w=w-lr*grad_

    if l1 != 0:
       lamb=l1
       w=w-lr*grad_
       for j in range(np.shape(w)[0]):
           if w[j] > lamb:
              w[j]-=lamb
           elif w[j]< - lamb:
               w[j]+=lamb
           else:
               w[j]=0.0
    return w



def sgd_optimizer(w, z_t,n_t,lr=0.1, l1=0, l2=0.1,alpha=1,beta=1):
    """
    实现随机梯度下降
    :param w:
    :param g:
    :param lr:
    :return:
    """

    if l1 == 0:

        w = -z_t/((beta+np.sqrt(n_t))/alpha+l2)
    else: # l1 范数 FTRL 算法
        for i in range(np.shape(w)[0]):
            if z_t[i] >= l1:
                w[i] = -(z_t[i]-l1)/((beta+np.sqrt(n_t[i]))/alpha+l2)
            elif z_t[i] <= -l1:
                w[i]=-(z_t[i]+l1)/((beta+np.sqrt(n_t[i]))/alpha+l2)
            else:
                w[i]=0
    return w*lr


if __name__ =='__main__':
    # 测试批量梯度下降
    from problem import *
    verbose = True

    w_dim = 128
    # 光滑函数
    w = np.random.randn(w_dim)
    _, X, y = gen_batch(bath_size=1000, dim=w_dim)

    D_k=np.eye(w_dim)
    newton="newton"
    for i in range(250):

        if newton=="newton":
            loss, gradient = loss_function(w, X, y,grad_flag=newton)

        elif newton=="dfp":
            loss,gradient,D_k=dfp(w,X,y,D_k)
        else:
            loss,gradient,D_k=bfgs(w,X,y,D_k)

        w = bgd_optimizer(w, gradient,lr=0.5, l1=0, l2=0.1)

        if verbose &(i%10==0): print(newton+" loss : ",loss)
    print w

    
    # 非光滑函数
    w = np.random.randn(w_dim)
    _, X, y = gen_batch(bath_size=100000, dim=w_dim)
    for i in range(100):
        loss, gradient = loss_function(w, X, y,grad_flag="gd")
        w = bgd_optimizer(w, gradient,lr=1.0/(100000*5), l1=0.01, l2=0.1)
        if verbose &(i%10==0):print(" gradient descent loss : ",loss)
    print w

    
    # 随机梯度下降

    # 光滑函数
    w = np.random.randn(w_dim)

    beta=1
    alpha=1

    z_t=np.zeros(w_dim)
    n_t=np.zeros(w_dim)

    w=sgd_optimizer(w,z_t,n_t,alpha=alpha,beta=beta)
    _, X, y = gen_batch(bath_size=100000, dim=w_dim)
    for i in range(2000):
        loss, z_t,n_t = ftrl(w,z_t,n_t,X, y,alpha=alpha)
        w = sgd_optimizer(w, z_t,n_t,lr=0.5, l1=0, l2=0.1)
        if verbose & (i%200== 0): print(" ftr loss : ",loss)
    print w

    # 非光滑函数
    w = np.random.randn(w_dim)

    z_t=np.zeros(w_dim)
    n_t=np.zeros(w_dim)
    w=sgd_optimizer(w,z_t,n_t,alpha=alpha,beta=beta)

    _, X, y = gen_batch(bath_size=100000, dim=w_dim)

    for i in range(2000):
        loss, z_t,n_t = ftrl(w,z_t,n_t,X, y,alpha=alpha)
        w = sgd_optimizer(w, z_t,n_t,lr=0.5, l1=0.01, l2=0.1)
        if verbose & (i%200 == 0): print(" ftrl l1 loss : ",loss)
    print w


