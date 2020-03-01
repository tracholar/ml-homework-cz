#coding:utf-8
"""合成数据"""
import numpy as np

def sample_data(d = 10, n = 1000):
    # step1: generate normlized u1, u2, u1^T u2 = 0
    u1 = np.random.randn(d)
    u2 = np.random.randn(d)
    u1 = u1 / np.linalg.norm(u1)
    u2 = u2 - np.dot(u1, u2) * u1
    u2 = u2 / np.linalg.norm(u2)

    # step2: generate w1, w2
    c = 1.0
    p = 0.7
    w1 = c * u1
    w2 = c * (p * u1 + np.sqrt(1 - p*p) * u2)

    # step3: sample gaussian vector
    x = np.random.randn(n, d)

    # step4: generate label
    m = 5
    alpha = np.random.rand(m)
    belta = np.random.rand(m)
    y1 = np.dot(x, w1) + sum(np.sin(alpha[i]*np.dot(x, w1) + belta[i]) for i in range(m)) + np.random.randn(n) * 0.01
    y2 = np.dot(x, w2) + sum(np.sin(alpha[i]*np.dot(x, w2) + belta[i]) for i in range(m)) + np.random.randn(n) * 0.01


    return x, y1, y2

if __name__ == '__main__':
    x, u1, u2 = sample_data()
    print u1, u2
    print np.linalg.norm(u1),np.linalg.norm(u2), np.dot(u1, u2)


    print np.dot(u1, u2)/np.linalg.norm(u1)/np.linalg.norm(u2)


