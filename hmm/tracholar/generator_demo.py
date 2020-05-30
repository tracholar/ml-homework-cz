#coding:utf-8
import random

## 隐状态
hide_state = ['健康', '感冒']
## 观测状态
state = ['正常', '畏寒', '头晕']
## 初始概率
pi0 = {'健康':0.6, '感冒':0.4}
## 转移概率
A = {'健康':{'健康':0.7, '感冒':0.3},
     '感冒':{'健康':0.4, '感冒':0.6}}
## 发射概率
B = {
    '健康':{'正常':0.5, '畏寒':0.4, '头晕':0.1},
    '感冒':{'正常':0.1, '畏寒':0.3, '头晕':0.6}
}
def draw_from(p):
    """
    从概率分布采样
    :param p: 分布字典
    :return: key
    """
    s = sum(p.values())
    r = random.random()
    ps = 0
    key = p.keys()
    for k in key:
        ps += p[k]
        if r < ps/s:
            return k

observ = []
for i in range(1000):
    s0 = draw_from(pi0)
    sample = []
    for _ in range(10):
        o = draw_from(B[s0])
        sample.append(o)
        s0 = draw_from(A[s0]) # 转移到下一个状态

    print i,'->'.join(sample)
    observ.append(sample)
