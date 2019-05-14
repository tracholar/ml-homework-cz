# HIVE-UDF
做数据挖掘写HVIE SQL是司空见惯的事情了,HIVE中的一个利器就是UDF, 利用UDF还可以做模型训练,
可以参考[hivemall](https://github.com/apache/incubator-hivemall/)和Google的
[BigQuery ML](https://cloud.google.com/bigquery/docs/bigqueryml-intro)。

- 本地安装 HIVE
- 利用模板实现三个 UDF,UDAF,UDTF
- 打包并在本地测试, 安装Hive测试


## 思考题
- 写一个UDF的单元测试?
- UDAF中的 `init`, `iterate`, `terminatePartial`, `merge`, `terminate` 方法分别在MapReduce的哪些过程中执行, 请实现一个测试用例,模拟MapReduce执行过程,并构造伪造的数据,本地测试UDAF
- UDTF中的 `initialize`, `process`, `close` 分别在MapReduce的哪些阶段执行, 请实现一个测试用例,模拟MapReduce执行过程,并构造伪造的数据,本地测试UDTF
- `ObjectInspector`是什么, Hadoop使用`ObjectInspector`有什么好处?
- 阅读 [hivemall 的源码](https://github.com/apache/incubator-hivemall/blob/master/core/src/main/java/hivemall/classifier/GeneralClassifierUDTF.java),用自己的话描述hivemall是如何实现如下功能的?
    1. UDF是如何将训练参数传入的? 参数又是如何解析的? 如何保证参数只解析一次?
    2. UDF只会遍历一次数据, hivemall是如何实现多次遍历数据训练的?
    3. 每一个执行UDF的机器上,UDF之间是无法实现通信的, hivemall有两种方式实现不同机器之间的通信, 请简要说明每一种方式的原理,并指出跟PS-Server有哪些异同和优劣?

## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)
- [zhangweite](zhangweite/)