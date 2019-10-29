## Spark教程
- 阅读官方文档并动手实践,完成思考题
- 文档: 
    1. <https://spark.apache.org/docs/latest/quick-start.html>
    2. <https://spark.apache.org/docs/latest/rdd-programming-guide.html>
    3. <https://spark.apache.org/docs/latest/sql-getting-started.html>


## 思考题
- `rdd.map(somefunction1).reduceByKey(somefunction2)` 中哪个函数会触发实际执行?
- `map` 和 `mapPartition` 的区别是什么? 设想你需要将`rdd`中每个样本传给一个函数 `obj.predict` 进行处理(例如模型预测), 其中`obj`需要先执行初始化操作 `obj.init()` 并且初始化操作无法序列化,这意味着你无法先初始化`obj`,然后将`obj`传给`map`或者`mapParitition`中的函数,那么此时最佳的代码写法是下列哪种?原因是什么?

```scala
## 第1种
rdd.map{s=>
    val obj = OBJ()
    obj.init()
    obj.predict(s)
}

## 第2种
rdd.mapPartition{iter =>
    val obj = OBJ()
    obj.init()
    iter.map(obj.predict)
}
```

- Spark中的`transformer`和`action`的区别和联系是什么?举例说明。
- 使用一下sparkshell, 记录使用体会
- Spark中的分布式机器学习算法和基于PS的分布式机器学习算法的区别和联系是什么?指出数据并行和模型并行分别在哪些地方有实现?
- `broadcast` 变量和普通的变量传递有什么区别?
- 如何利用Spark实现MAPJOIN?
