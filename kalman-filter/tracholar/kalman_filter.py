#coding:utf-8
"""
卡尔曼滤波原理仿真
"""
import numpy as np

# X[k] = F X[k-1] + G a[k]
t = 10000
dt = 0.01
x = np.zeros((2, t))
F = np.array([[1, dt], [0, 1]])
G = np.array([dt*dt*0.5, dt])

