#coding:utf-8
from grid import *

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/500etf.txt', sep='\t', header=None)
prices = list(reversed(list(df[1])))



print '中证500'
s1 = BasicGridStrategy()
s2 = DingtouStrategy(amount=100)
print '网格策略', s1.simulate(prices)
print '定投策略', s2.simulate(prices)

plt.subplot(2, 2, 1)
plt.plot(prices)
plt.title(u'基金净值')

plt.subplot(2,2,2)
plt.plot(s1.inc_ammount, 'r')
plt.plot(s2.inc_ammount, 'g')
plt.legend([u'网格', u'定投'])
plt.title(u'收益')

plt.subplot(2,2,3)
plt.plot(s1.cost, 'r')
plt.plot(s2.cost, 'g')
plt.legend([u'网格', u'定投'])
plt.title(u'投入')

plt.subplot(2,2,4)
plt.plot(np.array(s1.inc_ammount)/np.array(s1.cost), 'r')
plt.plot(np.array(s2.inc_ammount)/np.array(s2.cost), 'g')
plt.legend([u'网格', u'定投'])
plt.title(u'收益率')

fig = plt.gcf()
fig.savefig('fig.svg')

plt.show()