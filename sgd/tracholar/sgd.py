#coding:utf-8

import numpy as np


class Optimizer():
    def __init__(self, **kwargs):
        pass
    def update(self, theta, g):
        pass

class SGD(Optimizer):
    def __init__(self, lr):
        self.step = 0
        self.lr = lr

    def update(self, theta, g):
        self.step += 1
        return -self.lr / np.sqrt(self.step) * g


class SGDMomentum(Optimizer):
    def __init__(self, lr, gamma = 0.9):
        self.step = 0
        self.lr = lr
        self.gamma = gamma
        self.m = 0

    def update(self, theta, g):
        self.step += 1
        if self.step == 1:
            self.m = g
        else:
            self.m = self.gamma * self.m + (1-self.gamma) * g

        return -self.lr / np.sqrt(self.step) * self.m

class Adagrad(Optimizer):
    def __init__(self, lr, epsilon = 0.1):
        self.step = 0
        self.lr = lr
        self.v = epsilon

    def update(self, theta, g):
        self.step += 1
        self.v += g ** 2

        return -self.lr / np.sqrt(self.v) * g

class RMSprop(Optimizer):
    def __init__(self, lr, epsilon = 0.1, gamma=0.9):
        self.step = 0
        self.lr = lr
        self.v = epsilon
        self.gamma = gamma

    def update(self, theta, g):
        self.v = self.v * self.gamma + (1-self.gamma) * (g**2)
        return -self.lr / np.sqrt(self.v) * g

class Adam(Optimizer):
    def __init__(self, lr, epsilon = 0.1, gamma=0.9, beta=0.9, AMSGrad = True):
        self.step = 0
        self.lr = lr
        self.v = epsilon
        self.gamma = gamma
        self.beta = beta
        self.m = 0
        self.AMSGrad = AMSGrad

    def update(self, theta, g):
        self.step += 1
        if self.step == 1:
            self.m = g
        else:
            self.m = self.gamma * self.m + (1-self.gamma) * g
        v = self.v * self.beta + (1-self.beta) * (g**2)
        if self.AMSGrad:
            self.v = np.maximum(v, self.v)
        else:
            self.v = v
        return -self.lr / np.sqrt(self.v) * self.m

class Adabound(Optimizer):
    def __init__(self, lr=0.001, final_lr=0.001, epsilon = 0.1, gamma=0.9, beta=0.9, alpha=1e-3,AMSGrad=False, **kwargs):
        self.step = 0
        self.lr = lr
        self.final_lr = final_lr
        self.v = epsilon
        self.gamma = gamma
        self.beta = beta
        self.m = 0
        self.AMSGrad = AMSGrad
        self.alpha = alpha
        self.alphai = 0
    def update(self, theta, g):
        self.step += 1
        if self.step == 1:
            self.m = g
        else:
            self.m = self.gamma * self.m + (1-self.gamma) * g

        v = self.v * self.beta + (1-self.beta) * (g**2)
        if self.AMSGrad:
            self.v = np.maximum(self.v, v)
        else:
            self.v = v
        delta = self.lr/ np.sqrt(self.v)
        self.alphai += self.alpha
        eta_l = self.final_lr - self.final_lr/(1 + self.alphai)
        eta_u = self.final_lr + self.final_lr/(self.alphai)
        lr = np.minimum(np.maximum(delta, eta_l), eta_u)
        if self.step % 100 == 0:
            print lr
        return - lr  * self.m

from problem import *
def main():
    w0, X, y = gen_batch(bath_size=128)
    w = np.random.rand(w0.shape[0])/np.sqrt(w0.shape[0])

    optimizer = Adabound(lr=0.001, AMSGrad=True)
    update = 0
    nesterov = True
    for i in range(3000):
        _, X, y = gen_batch(bath_size=128)

        if nesterov:
            loss, g = loss_function(w + update, X, y)
        else:
            loss, g = loss_function(w, X, y)
        update = optimizer.update(w, g)
        w += update
        print '\rstep', i,', loss =', loss,
    print w0
    print w

if __name__ == '__main__':
    main()