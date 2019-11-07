# 行列式点过程
- 行列式点过程可以用来增加多样性，本次作业模拟一个行列式点过程增加推荐多样性的任务
- 阅读论文 Practical Diversified Recommendations on YouTube with Determinantal Point Processes 完成仿真数据下的DPP算法


# 思考题
- DPP 跟行列式有啥关系？
- DPP为什么可以建模多样性？请举例说明
- DPP的L和核矩阵K的关系是什么？
- L矩阵为什么一定要半正定对称阵(PSD)？算法中如何保证(PSD)的？google论文中的Deep DPP是如何保证PSD的？
- 给定矩阵L下，寻找最大似然子序列为什么是NP-hard问题？请解释贪心算法求解过程，举例说明
- alpha参数越大越有可能出现PSD还是越不可能出现PSD？为什么
- 解释一下Deep DPP的极大似然估计公式（12），式中的Yj的意义是什么？ log det(L(w) + I) 是什么意思？


# 实现
- [tracholar](tracholar/)