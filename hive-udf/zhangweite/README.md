
## 思考题
- 写一个UDF的单元测试?
- UDAF中的 `init`, `iterate`, `terminatePartial`, `merge`, `terminate` 方法分别在MapReduce的哪些过程中执行, 请实现一个测试用例,模拟MapReduce执行过程,并构造伪造的数据,本地测试UDAF

init初始化，iterate 逐条处理数据，terminalPartial返回处理好的数据节点，他们处在map过程中。
merge 汇总terminalPartial的数据， terminate生成最终的结果，他们处在reduce过程中。

- UDTF中的 `initialize`, `process`, `close` 分别在MapReduce的哪些阶段执行, 请实现一个测试用例,模拟MapReduce执行过程,并构造伪造的数据,本地测试UDTF

initialize, process 在map过程执行， close 在reduce过程执行

- `ObjectInspector`是什么, Hadoop使用`ObjectInspector`有什么好处?
- 阅读 [hivemall 的源码](https://github.com/apache/incubator-hivemall/blob/master/core/src/main/java/hivemall/classifier/GeneralClassifierUDTF.java),用自己的话描述hivemall是如何实现如下功能的?
    1. UDF是如何将训练参数传入的? 参数又是如何解析的? 如何保证参数只解析一次?
    2. UDF只会遍历一次数据, hivemall是如何实现多次遍历数据训练的?
    3. 每一个执行UDF的机器上,UDF之间是无法实现通信的, hivemall有两种方式实现不同机器之间的通信, 请简要说明每一种方式的原理,并指出跟PS-Server有哪些异同和优劣?
    
    这个思考题仍需时间研究。

## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)
- [zhangweite](zhangweite/)