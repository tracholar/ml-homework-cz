#coding:utf-8

import numpy as np


class Optimizer():
    def __init__(self, **kwargs):
        pass
    def update(self, theta, g):
        pass

class SGD(Optimizer):
    def __init__(self, lr):
        raise NotImplementedError()

    def update(self, theta, g):
        """ 计算更新量
        :param theta:
        :param g:
        :return: 注意: 返回更新量, 而不是更新后的权重
        """
        raise NotImplementedError()


class SGDMomentum(Optimizer):
    def __init__(self, lr, gamma = 0.9):
        raise NotImplementedError()

    def update(self, theta, g):
        raise NotImplementedError()

class Adagrad(Optimizer):
    def __init__(self, lr, epsilon = 0.1):
        raise NotImplementedError()

    def update(self, theta, g):
        raise NotImplementedError()

class RMSprop(Optimizer):
    def __init__(self, lr, epsilon = 0.1, gamma=0.9):
        raise NotImplementedError()

    def update(self, theta, g):
        raise NotImplementedError()

class Adam(Optimizer):
    def __init__(self, lr, epsilon = 0.1, gamma=0.9, beta=0.9, AMSGrad = True):
        raise NotImplementedError()

    def update(self, theta, g):
        raise NotImplementedError()

class Adabound(Optimizer):
    def __init__(self, lr, epsilon = 0.1, gamma=0.9, beta=0.9, **kwargs):
        raise NotImplementedError()
    def update(self, theta, g):
        raise NotImplementedError()

from problem import *
def main():
    w0, X, y = gen_batch(bath_size=128)
    w = np.random.rand(w0.shape[0])/np.sqrt(w0.shape[0])

    optimizer = Adam(lr=0.001, AMSGrad=False)
    for i in range(3000):
        _, X, y = gen_batch(bath_size=128)
        """ 1. 实现基本的梯度更新
            2. 实现Nesterov加速式的更新
        """
        print '\rstep', i,', loss =', loss,
    print w0
    print w

if __name__ == '__main__':
    main()