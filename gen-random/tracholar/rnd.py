#coding:utf-8
import random
from math import log, pi, cos, sqrt, tan
from scipy.special import beta
import matplotlib.pyplot as plt

def urnd():
    return random.random()

def exp_rnd(lb):
    assert lb > 0
    x = urnd()
    return -1/lb*log(1-x)

def gaussian_rnd():
    r = sqrt(- 2 * log(urnd()))
    theta = 2*pi*urnd()
    return r * cos(theta)

def cauchy_rnd():
    z = (urnd()-0.5) * pi
    return tan(z)

def cauchy_rnd2():
    x = gaussian_rnd()
    y = gaussian_rnd()
    if y == 0.0:
        return cauchy_rnd()
    return x/y

def reject_samping_beta(a, b):
    assert a>1 and b>1
    reject = True
    z = 0
    while reject:
        z = urnd()
        p = z**(a-1) * (1-z) ** (b-1) / beta(a, b)
        u = urnd()
        reject = u > p
    return z

def rand_i(w):
    w = w/w.sum()
    j = 0
    s = w[j]
    r = random.random()
    while s < r:
        j += 1
        s += w[j]
    return j
import numpy as np
def MetropolisHastings():
    p_target = [0.1, 0.2, 0.2, 0.5]
    q = np.ones((4,4)) * 0.25
    #q = q/q.sum(axis=0)
    print q
    print q[0]

    x = np.random.randint(4)
    x0 = x
    rx = []
    for i in range(100000):
        x = rand_i(q[x0])
        aij = p_target[x] * q[x, x0] / (p_target[x0] * q[x0, x])  # 接受率
        aij = min(1, aij)
        if urnd() > aij:
            continue
        if i> 10000:
            rx.append(x)
        x0 = x # update
    return rx

def gibbs_sampling():
    pass


if __name__ == '__main__':
    plt.hist(MetropolisHastings())
    plt.show()
    #plt.hist([cauchy_rnd2() for _ in range(10000)], bins=50, range=[-5,5])
    #plt.show()