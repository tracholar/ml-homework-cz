# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

def price_list(n = 700, inc=0.001, period=300, period_amp=0.2, rnd=0.05):
    x = np.arange(0, n)
    y = np.exp(inc * x) * (1 + period_amp * np.sin(2*np.pi/period*x)) * (1 + rnd * np.random.randn(n))
    return x, y


x, y = price_list(100)
plt.plot(x, y)
plt.savefig('img/rnd_price.svg')