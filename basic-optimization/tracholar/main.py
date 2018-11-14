#coding:utf-8

def bgd_optimizer(w, g, lr=0.1, l1=0, l2=0.1):
    """
    实现批量梯度下降
    :param w:
    :param g:
    :param lr:
    :return:
    """
    if l1 == 0:
        raise NotImplementedError()
    else: # l1范数软阈值算法
        raise NotImplementedError()
    return w

def sgd_optimizer(w, g, lr=0.1, l1=0, l2=0.1):
    """
    实现随机梯度下降
    :param w:
    :param g:
    :param lr:
    :return:
    """
    if l1 == 0:
        raise NotImplementedError()
    else: # l1 范数 FTRL 算法
        raise NotImplementedError()
    return w


if __name__ =='__main__':
    # 测试批量梯度下降
    from problem import *

    w_dim = 1024
    # 光滑函数
    w = np.random.randn(w_dim)
    _, X, y = gen_batch(bath_size=100000, dim=w_dim)
    for i in range(100):
        loss, gradient = loss_function(w, X, y)
        w = bgd_optimizer(w, gradient, l1=0, l2=0.1)
    print w

    # 非光滑函数
    w = np.random.randn(w_dim)
    _, X, y = gen_batch(bath_size=100000, dim=w_dim)
    for i in range(100):
        loss, gradient = loss_function(w, X, y)
        w = bgd_optimizer(w, gradient, l1=0.1, l2=0.1)

    print w

    # 随机梯度下降

    # 光滑函数
    w = np.random.randn(w_dim)
    for i in range(100):
        _, X, y = gen_batch(bath_size=128, dim=w_dim)
        loss, gradient = loss_function(w, X, y)
        w = sgd_optimizer(w, gradient, l1=0, l2=0.1)

    print w

    # 非光滑函数
    w = np.random.randn(w_dim)
    for i in range(100):
        _, X, y = gen_batch(bath_size=128, dim=w_dim)
        loss, gradient = loss_function(w, X, y)
        w = sgd_optimizer(w, gradient, l1=0.1, l2=0.1)

    print w
