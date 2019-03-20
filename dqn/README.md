## Deep Q-learning Network
- 参考论文: Human-level control through deep reinforcement learning
- 实现一个简单的DQN,基于简单的游戏任务
- 使用 CartPole-v1 环境,需要安装gym,参考<https://gym.openai.com/envs/CartPole-v1/>
    - 状态空间 S 是一个4维的浮点数
    - 动作空间 A 只有两个,+1, -1两个动作
    - 回报 R 每一步的回报都是+1,直到挂了
    - 结束条件: 偏离垂直15度,或者车离开中心2.4个单位

