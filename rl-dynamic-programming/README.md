# 强化学习：动态规划

- 构建一个简单的环境，有nS个状态，0，1，...，nS-1；其中nS-1是终止状态。 该环境下一共两个动作：0向左运动，1向右运动，每个动作都有概率p0不动，p1的概率会往反方向运动, 1-p0-p1概率正常运动。

|0 | 1 | 2 | ... | 9 |
|--|--|----|-----|---|
|←·→|←·→|←·→|←·→|终点|


- 实现上述问题的值迭代和策略迭代算法
- 环境构建可以参考 getstart 的模板中的代码，如果你不知道如何开始实现，也可以参考 getstart 的模块，补充完成核心代码




## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)
