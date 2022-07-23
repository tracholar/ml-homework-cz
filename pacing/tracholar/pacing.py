# coding:utf-8
# 模拟广告预算的pacing算法
import numpy as np
import matplotlib.pyplot as plt


def pacing(t, kp, ki, kd):
    x = 0
    out = [x]
    err = 0
    cum_err = err
    d_err = err
    out_err = [err]
    for ti in t:
        old_err = err
        err = ti - x
        cum_err += err
        d_err = err - old_err
        weight = kp * err + ki * cum_err + kd * d_err
        x = x + weight

        out.append(x)
        out_err.append(err)

    return out, out_err

n = 1000
target = np.sin(np.linspace(0, 10, n))
y, y_err = pacing(target, 0.1, 0.1, 0.1)

plt.plot(target)
plt.plot(y)
plt.plot(y_err)
plt.legend(['target', 'y', 'y_err'])
plt.show()
