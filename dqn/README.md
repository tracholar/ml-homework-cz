## Deep Q-learning Network
- 参考论文: Human-level control through deep reinforcement learning
- 实现一个简单的DQN,基于简单的游戏任务
- 使用 CartPole-v1 环境,需要安装gym,参考<https://gym.openai.com/envs/CartPole-v1/>
    - 状态空间 S 是一个4维的浮点数
    - 动作空间 A 只有两个,+1, -1两个动作
    - 回报 R 每一步的回报都是+1,直到挂了
    - 结束条件: 偏离垂直15度,或者车离开中心2.4个单位
- 记录你的模型收敛后多次重复试验的平均回报

## 思考与总结
1. 试用值函数拟合的方法说明值表法的Q-learning和用状态的onehot编码做特征用线性模型拟合Q函数是等价的
2. 为什么要做经验回放? 有什么办法可以避免经验回放并且不会有你说的哪些问题么? 
3. 为什么要有一个更新比较慢的模型? 
4. 了解Double Q-learning, 阅读论文 Deep Reinforcement Learning with Double Q-learning, 并改进你的模型, 比较DQN和DDQN效果上的差异,并解释DDQN为什么可以不用一个更新比较慢的模型?为什么可以解决过度估计的问题?

## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)