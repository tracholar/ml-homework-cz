import numpy as np

nS = 10
nA = 2  #不要改这个参数
Done = nS - 1
p0 = 0.1
p1 = 0.1
P = np.zeros((nS, nA, nS)) # 转移概率
R = np.zeros((nS, nA, nS)) - 1.0 # 回报都是-1
gamma = 1

# 环境构建
for s in range(nS):
    if s == Done: # 终止态转移概率都为0
        continue
    for a in range(nA):
        inc = a * 2 - 1 # 步长
        P[s, a, s] += p0 # 不动
        P[s, a, max(0, s - inc)] += p1 # 反方向
        P[s, a, max(0, s + inc)] += 1 - p0 - p1 # 正常运动



V = np.zeros(nS)
# 值迭代
for it in range(1000):

    ## YOUR CODE HERE

    ## END
    pass

print 'iteral steps:', it
print V





# 策略迭代

pi = np.zeros(nS, dtype=int) #初始策略全部往左

for it in range(100):
    V = np.zeros(nS)
    # 策略评估，解线性方程

    ## YOUR CODE HERE

    ## END

    # 策略提升

    ## YOUR CODE HERE

    ## END

print 'pi =', pi
print 'V =', V
