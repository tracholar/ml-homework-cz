## 思考题
Q1 写一个UDF的单元测试?

Q2 UDAF中的 `init`，`iterate`，`terminatePartial`，`merge`，`terminate` 方法分别在MapReduce的哪些过程中执行，请实现一个测试用例，模拟MapReduce执行过程，并构造伪造的数据，本地测试UDAF

A2 init、iterate、terminalPartial在map过程中执行；merge、terminate在reduce过程中执行。

Q3 UDTF中的 `initialize`，`process`，`close` 分别在MapReduce的哪些阶段执行，请实现一个测试用例，模拟MapReduce执行过程，并构造伪造的数据，本地测试UDTF

A3 UDTF还没有做

Q4 `ObjectInspector`是什么，Hadoop使用`ObjectInspector`有什么好处?

A4 UDTF还没有做

Q5 阅读 [hivemall 的源码](https://github.com/apache/incubator-hivemall/blob/master/core/src/main/java/hivemall/classifier/GeneralClassifierUDTF.java)，用自己的话描述hivemall是如何实现如下功能的?
    
1. UDF是如何将训练参数传入的? 参数又是如何解析的? 如何保证参数只解析一次?

2. UDF只会遍历一次数据，hivemall是如何实现多次遍历数据训练的?

3. 每一个执行UDF的机器上，UDF之间是无法实现通信的，hivemall有两种方式实现不同机器之间的通信，请简要说明每一种方式的原理，并指出跟PS-Server有哪些异同和优劣?

A5 
1) 传入：@Nonnull final FeatureValue[] features, final float label，利用final保证解析一次。
2) 对数据大小进行比较？
3) 这个不会。。。
## 实现列表
提交PR的时候，请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)
- [zhangweite](zhangweite/)
- [chengjiafeng](chengjiafeng/)