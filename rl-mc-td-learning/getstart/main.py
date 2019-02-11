#coding:utf-8

import numpy as np

nS = 10
nA = 2  #不要改这个参数
Done = nS - 1
p0 = 0.1
p1 = 0.1
P = np.zeros((nS, nA, nS)) # 转移概率
R = np.zeros((nS, nA, nS)) - 1.0 # 回报都是-1
gamma = 1

for s in range(nS):
    if s == Done: # 终止态转移概率都为0
        continue
    for a in range(nA):
        inc = a * 2 - 1 # 步长
        P[s, a, s] += p0 # 不动
        P[s, a, max(0, s - inc)] += p1 # 反方向
        P[s, a, max(0, s + inc)] += 1 - p0 - p1 # 正常运动




def go_next(s, a):
    r = np.random.rand()
    i = 0
    p = 0
    while True:
        if r < p + P[s, a, i]:
            return i
        p += P[s, a, i]
        i += 1
    return len(P[s, a])

# 模拟特卡罗方法
def MC():
    Q = np.zeros((nS, nA))
    pi = np.random.randint(0, nA, nS)
    alpha = 0.01
    for it in range(1000):
        if it % 50 == 0:
            print 'iter', it, 'pi=', pi

        # 策略评估：根据目前策略仿真一条状态-动作路径，更新Q函数
        for s in range(nS):
            for a in range(nA):
                # 仿真一条状态-动作路径
                history = []
                ss = s
                while ss != Done:
                    ss_next = go_next(ss, a)
                    history.append((ss, a, R[ss,a,ss_next], ss_next))
                    ss = ss_next
                    a = pi[ss] #更新动作
                    #print ss

                # TODO 你的代码

        # 策略提升：根据更新后的Q函数，更新策略
        # TODO 你的代码

    print 'V=', np.max(Q, axis=1)
    print 'pi=', pi



# 时间差分方法
def QLearning():
    Q = np.zeros((nS, nA))
    pi = np.random.randint(0, nA, nS)

    alpha = 0.01
    epsilon = 0.9 # 探索
    for it in range(100):
        if it % 10 == 0:
            print 'iter', it, 'epsilon=', epsilon, 'V[0]=', max(Q[0])

        # 根据目前策略仿真一条状态-动作路径，并同时更新Q函数
        for s in range(nS):
            if s == Done:
                continue
            for a in range(nA):
                # 仿真一条状态-动作路径
                ss = s
                while ss != Done:
                    ss_next = go_next(ss, a)
                    # TODO 你的代码

        epsilon = max(0.01, epsilon *0.99)

    # 策略提升
    # TODO 你的代码

    print 'V=', np.max(Q, axis=1)
    print 'pi=', pi


if __name__ == '__main__':
    MC()
    QLearning()