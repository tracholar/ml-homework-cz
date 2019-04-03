#coding:utf-8
import numpy as np
import sys
nS = 10 #状态数量
nA = 2  #不要改这个参数
Done = nS - 1
p0 = 0.1 # 保持不变的概率
p1 = 0.1 # 向右运动的概率
P = np.zeros((nS, nA, nS)) # 转移概率
R = np.zeros((nS, nA, nS)) - 1.0 # 回报都是-1
gamma = 0.9

# 环境构建
for s in range(nS):
    if s == Done: # 终止态转移概率都为0
        continue
    for a in range(nA):
        """
           策略1:a=0,
           策略2:a=1,
        """
        inc = a * 2 - 1 # 步长 # nA 限制转移的状态
        P[s, a, s] += p0 # 不动
        P[s, a, max(0, s - inc)] += p1 # 反方向
        P[s, a, max(0, s + inc)] += 1 - p0 - p1 # 正常运动
#print(P[:,0,:])
#print("***********************************************")
#print(P[:,1,:])
def matrix_solve(P,R):
    r= 0.5*np.sum(P*R,axis=(1,2))
    p=0.5*np.sum(P,axis=1)
    i=np.eye(np.shape(p)[0])
    v=np.matmul(np.linalg.inv(i-0.9*p),r)
    print(v)
def MRP(P,R):
    print(" MRP value  iteration ......")
    pi = np.zeros(nS, dtype=int) #初始策略全部往左
    V = np.random.rand(nS)
    R= np.sum(0.5*P*R,axis=(1,2))
    #print(R)
    P=0.5*np.sum(P,axis=1)

    alpha_v=1000
    for it in range(alpha_v):
        tmp_v=np.zeros(nS)
        for v_i in range(nS):
            tmp_v[v_i]+=R[v_i]
            for t_i in range(nS):
                tmp_v[v_i]+=0.9*P[v_i,t_i]*V[t_i]

        for v_i in range(nS):
            V[v_i]=tmp_v[v_i]
    print V

matrix_solve(P,R)
MRP(P,R)
print("*********************************")

value_iteration=True
if value_iteration:
    print(" value  iteration ......")
    pi = np.zeros(nS, dtype=int) #初始策略全部往左
    V = np.zeros(nS)
    # 值迭代
    alpha_v=1000
    for it in range(alpha_v):

        for v_i in range(nS):
            tmp_a=np.zeros(nA)
            for action in range(nA):
                for t_i in range(nS):
                    tmp_a[action]+=P[v_i,action,t_i]*(R[v_i,action,t_i]+gamma*V[t_i])
            pi[v_i]=np.argmax(tmp_a)

        tmp_v=np.zeros(nS)
        for v_i in range(nS):
            for t_i in range(nS):
                tmp_v[v_i]+=P[v_i,pi[v_i],t_i]*(R[v_i,pi[v_i],t_i]+gamma*V[t_i])

        for v_i in range(nS):
            V[v_i]=tmp_v[v_i]


    print V
    print pi

if True:# 策略迭代
    print("policy iteration .....")
    pi = np.zeros(nS, dtype=int) #初始策略全部往左
    #cum_reward=np.zeros((nS, nA, nS))

    alpha=1000# 很重要确保能够收敛
    V = np.zeros(nS)
    for it in range(2):
        # 策略评估，解线性方程
        ##TODO YOUR CODE HERE
        for t in range(alpha):
            tmp_v=np.zeros(nS)
            for v_i in range(nS):
                for t_i in range(nS):
                    #for action in range(nA):
                    tmp_v[v_i]+=P[v_i,pi[v_i],t_i]*(R[v_i,pi[v_i],t_i]+gamma*V[t_i])

            for v_i in range(nS):
                V[v_i]=tmp_v[v_i]

        # 策略提升

        for v_i in range(nS):
            tmp_v=np.zeros(nA)
            for action in range(nA):
                for t_i in range(nS):
                    tmp_v[action]+=P[v_i,action,t_i]*(R[v_i,action,t_i]+gamma*V[t_i])
            V[v_i]=np.max(tmp_v)
            pi[v_i]=np.argmax(tmp_v)
    print 'pi =', pi
    print 'V =', V

