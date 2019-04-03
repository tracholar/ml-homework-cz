#coding:utf-8

import numpy as np
import  argparse
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
        # 类似轮盘赌输法来返回数值。r是概率累积
            return i
        p += P[s, a, i]# 转移概率
        i += 1
    return len(P[s, a])

# 模拟特卡罗方法
def MC():
    print("*********************************")
    print("**********      MC      *********")
    print("*********************************")
    Q = np.zeros((nS, nA),dtype=float)
    pi = np.random.randint(0,nA, nS)
    alpha = 0.1
    gamma = 0.1
    for it in range(100):
        if it % 50 == 0:
            print 'iter', it, 'pi=', pi

        # 策略评估：根据目前策略仿真一条状态-动作路径，更新Q函数
        # 采用 Monte Carlo explore  start 算法
        for s in range(nS):
            for a in range(nA):
                # 仿真一条状态-动作路径
                history = []
                ss = s
                mid_action=a
                while ss != Done:
                    ss_next = go_next(ss, mid_action)
                    history.append((ss, mid_action, R[ss,mid_action,ss_next], ss_next))
                    ss = ss_next
                    mid_action = pi[ss] #更新动作

                r_q_a=0.0
                for i in range(len(history)):
                    r_q_a+=history[i][2]*np.power(0.9,i)# 累积奖赏

                Q[s,a]=Q[s,a]+(-Q[s,a]+r_q_a)/(it+1)
                #print(" s:{%d},a:{%d},Q:{%f}"%(s,a,Q[s,a]))

        #print(" it : ",it,"  ",Q)
        # 策略提升：根据更新后的Q函数，更新策略
        # TODO 你的代码

        pi=np.argmax(Q,axis=1)
        #print("pi :",pi)
    print(Q)
    print 'V=', np.max(Q, axis=1)
    print 'pi=', pi



# 时间差分方法
def QLearning():
    print("*********************************")
    print("**********  QLearning   *********")
    print("*********************************")

    Q = np.zeros((nS, nA))
    pi = np.random.randint(0, nA, nS)

    alpha = 0.01
    epsilon = 0.9 # 探索
    for it in range(5000):
        #if it % 1000 == 0:
        #   print 'iter', it, 'epsilon=', epsilon, 'V[0]=', max(Q[0])

        # 根据目前策略仿真一条状态-动作路径，并同时更新Q函数
        begin_s=np.random.randint(0,nS)
        ss=begin_s
        while ss != Done:
            eps=np.random.rand()
            best_action=np.argmax(Q[ss,:])# 最优action
            action=best_action
            # e-greedy 策略
            if eps<epsilon:
               while action==best_action:
                   action=np.random.randint(0,len(Q[ss,:]))

            ss_next=go_next(ss,action)
            r=R[ss,action,ss_next]
            Q[ss,action]=Q[ss,action]+alpha*(r+0.8*np.max(Q[ss_next,:])-Q[ss,action])
            ss=ss_next


        epsilon = max(0.01, epsilon *0.99)

    # 策略提升
    # TODO 你的代码
        pi=np.argmax(Q,axis=1)
    print("epsilon:",epsilon)
    print("Q= ",Q)
    print 'V=', np.max(Q, axis=1)
    print 'pi=', pi
def epsilon_greedy(Q,ss,epsilon):
    eps=np.random.rand()
    best_action=np.argmax(Q[ss,:])# 最优action
    action=best_action
    # e-greedy 策略
    if eps<epsilon:
        while action==best_action:
            action=np.random.randint(0,len(Q[ss,:]))
    return action
def Saras():
    print("*********************************")
    print("************   Saras   **********")
    print("*********************************")

    Q = np.zeros((nS, nA))
    pi = np.random.randint(0, nA, nS)

    alpha = 0.01
    epsilon = 0.9 # 探索
    for it in range(5000):
        #if it % 1000 == 0:
        #    print 'iter', it, 'epsilon=', epsilon, 'V[0]=', max(Q[0])

        # 根据目前策略仿真一条状态-动作路径，并同时更新Q函数
        begin_s=np.random.randint(0,nS)
        ss=begin_s
        action=epsilon_greedy(Q,ss,epsilon)
        while ss != Done:

            ss_next=go_next(ss,action)
            r=R[ss,action,ss_next]
            new_action=epsilon_greedy(Q,ss_next,epsilon)

            Q[ss,action]=Q[ss,action]+alpha*(r+0.5*(Q[ss_next,new_action])-Q[ss,action])
            ss=ss_next
            action=new_action


        epsilon = max(0.01, epsilon *0.99)

        # 策略提升
        # TODO 你的代码
        pi=np.argmax(Q,axis=1)
    print("epsilon:",epsilon)
    print("Q= ",Q)
    print 'V=', np.max(Q, axis=1)
    print 'pi=', pi

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='You choose RL algorithm MC or QLearning or Saras')
    parser.add_argument("al")
    args=parser.parse_args()

    if args.al=='MC':
            MC()
    if args.al=='QLearning':
            QLearning()
    if args.al=='Saras':
            Saras()