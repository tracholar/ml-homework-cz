## Flink 教程
- 阅读flink官方文档,完成getstart的作业和下列思考题
    - 官方文档1.8 <https://ci.apache.org/projects/flink/flink-docs-release-1.8/>
    - 中文翻译1.7 <https://flink.sojb.cn/>
    
## 思考题
- flink 中的 `dataset` 和 `datastream` 的区别是什么?如果你熟悉Spark,请对比与Spark的 `dataset/dataframe/rdd` 以及 Sparkstream 中的 `stream` 的关系和区别
dataset是批式处理，datastream是流式处理  

- flink 如何实现容错机制?请以一个具体的例子,用自己的话说明这个过程

容错机制是指当有任务失败时，可以恢复失败前的数据流程。  
批处理系统比较容易实现容错机制，由于文件可以重复访问，当某个任务失败后重启即可。  
但是在流处理系统中，由于数据源是无限的数据流，无法将所有数据缓存或是持久化达到重复访问的目的。  
Flink基于分布式快照与可部分重发的数据源实现了容错，用户可自定义对整个Job进行快照的时间间隔，当出现任务失败时，Flink将整个Job恢复到最近一次快照的状态，并从数据源重发快照之后的数据。容错机制会持续的给data flow 拍摄快照，这个快照动作是轻量级的并不影响流处理，流的状态会保存在配置的地方。  

- flink 和 strom 相比,在API层面上有哪些区别?你更喜欢那个?为什么?

flink可以进行流处理和批处理，但storm只能进行流处理。  
flink在流处理时还提供了Map、GroupBy、Window和Join等api来代替storm的bolt在一个或多个readers和collectors的功能。  
flink用起来肯定更加便捷实用。  

- 在online learning中,需要将点击曝光流与特征流进行关联,并发给训练机器流式更新模型。请设计一个这样的系统,实现流式训练,要求:
    - 请列出每条流的数据格式和类型,并举几个例子
    - 实现两个流的JOIN操作,并思考几个问题:
        1. 以点击率预估模型为例,正负样本在一个时间窗中很有可能极不均衡(比如全是负样本),如何解决这个问题
        2. id特征中,某些id出现次数很少,通常要做一些措施(比如过滤频率较低的特征,或者某种正则项),请设计一种解决该问题的方案
        3. 写出JOIN操作的关键代码
        4. 写出流失训练的伪代码,可以以逻辑回归为例进行说明

这个后续再补充。  

- 如何理解flink的聚合操作?比如sum操作。因为stream的数据是源源不断地过来,那么sum的含义是什么?请至少说出两种sum聚合的意义,并写出对应的SQL代码,说明

聚合操作的使用场景应该包括：  
1.一条数据中的聚合统计，比如统计一条数据中的单词数。  
2.数据流在一段时间内数据的聚合，比如作业中的分窗统计：  
```scala
val counts = stream.map((_, 1)).keyBy(0).timeWindow(Time.seconds(3)).sum(1)
```

- 什么时候需要使用 `processFunction` 来实现自己的逻辑?请用自己的话说明flink API的不同层级以及操作的抽象对象是什么?

processFunction是一个用来维护状态和计时的api。在数据流的处理中，对处理状态和处理时间比较敏感的情况下，需要processFunction来实现。  
flink api的层级：  
1.底层是最基础的数据流，对应的就是ProcessFunctions，他被主要用来处理包含单独事件的一个或两个输入流或者是分组到一个窗口类的事件，所以提供了对时间和状态的细粒度控制。ProcessFunctions可强制修改state、重注册未来某时触发回调函数的timer，所以可以实现复杂事件处理逻辑。  
2.第二层是datastream和dataset层，分别对应了流操作和批操作，提供了很多实用的api。  
3.第三层是SQL和Table，提供了更高级的api。  

## 实现
- [tracholar](tracholar/)
- [getstart](getstart/)