## Flink 教程
- 阅读flink官方文档,完成getstart的作业和下列思考题
    - 官方文档1.8 <https://ci.apache.org/projects/flink/flink-docs-release-1.8/>
    - 中文翻译1.7 <https://flink.sojb.cn/>
    
## 思考题
- flink 中的 `dataset` 和 `datastream` 的区别是什么?如果你熟悉Spark,请对比与Spark的 `dataset/dataframe/rdd` 以及 Sparkstream 中的 `stream` 的关系和区别
- flink 如何实现容错机制?请以一个具体的例子,用自己的话说明这个过程
- flink 和 strom 相比,在API层面上有哪些区别?你更喜欢那个?为什么?
- 在online learning中,需要将点击曝光流与特征流进行关联,并发给训练机器流式更新模型。请设计一个这样的系统,实现流式训练,要求:
    - 请列出每条流的数据格式和类型,并举几个例子
    - 实现两个流的JOIN操作,并思考几个问题:
        1. 以点击率预估模型为例,正负样本在一个时间窗中很有可能极不均衡(比如全是负样本),如何解决这个问题
        2. id特征中,某些id出现次数很少,通常要做一些措施(比如过滤频率较低的特征,或者某种正则项),请设计一种解决该问题的方案
        3. 写出JOIN操作的关键代码
        4. 写出流失训练的伪代码,可以以逻辑回归为例进行说明
- 如何理解flink的聚合操作?比如sum操作。因为stream的数据是源源不断地过来,那么sum的含义是什么?请至少说出两种sum聚合的意义,并写出对应的SQL代码,说明
- 什么时候需要使用 `processFunction` 来实现自己的逻辑?请用自己的话说明flink API的不同层级以及操作的抽象对象是什么?

## 实现
- [tracholar](tracholar/)
- [getstart](getstart/)