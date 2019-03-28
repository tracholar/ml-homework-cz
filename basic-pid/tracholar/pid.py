#coding:utf-8
"""PID控制器仿真"""

import numpy as np
import matplotlib.pyplot as plt


n_step = 10000
ts = np.linspace(0, 10, n_step)
rt = np.cos(ts*np.clip(1*ts, 0, 2)*2*np.pi)
yout = np.zeros(n_step)
err = np.zeros(n_step)
ut = np.zeros(n_step)

kp = 1
ki = 2.3
kd = 0.1
P, I, D = (0, 0, 0)
model = np.array([0.5, 0.1, -0.1, -0.1])
for i in range(2, n_step):
    err[i-1] = rt[i-1] - yout[i-1]
    P = err[i-1] #P
    I += err[i-1] #I
    D = err[i-1] - err[i-2] #D

    ut[i] = np.clip(kp * P + ki * I + kd * D, -5, 5)
    yout[i] = np.sum(model * np.array([ut[i], ut[i-1], yout[i-1], yout[i-2]])) + np.random.rand()*0.1
    yout[i] = np.clip(yout[i], -2,2)


plt.plot(ts, rt, 'r')
plt.plot(ts, yout, 'g--', alpha=0.6)
plt.legend(['real', 'pid'], loc='best')
plt.show()
