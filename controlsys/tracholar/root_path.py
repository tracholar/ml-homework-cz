#coding:utf-8
"""根轨迹"""
from control import *
import matplotlib.pyplot as plt

numL = [1,1]
denL = [1,4,0,0]
sysL = tf(numL, denL)
rlocus(sysL)

plt.show()