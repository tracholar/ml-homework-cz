## Scala基础教程
- 阅读scala教程,选择其中一个即可,如果有更好的教程材料欢迎提交PR
    - <https://www.runoob.com/scala/scala-tutorial.html>
    - <https://docs.scala-lang.org/tour/tour-of-scala.html>
    - <https://twitter.github.io/scala_school/>
- 完成编程作业和思考题


## 思考题
- 函数式编程中的「函数」与一般编程语言(如C/Java等)中所说的「函数」有什么联系和区别?
- 有人说函数式编程语言非常适合写并行和分布式程序,请根据自己的思考分析这个观点是否正确,并举例说明理由。
- 请使用scala修改下列java代码,并要求具有scala style

```java
int[] arr = new int[] {1,2,3,4,5,6,7,8,9,10};
int sum = 0;
for(int i : arr){
    if(i % 2 == 0) continue;
    sum += i;
}
System.out.println(sum);
```

- 什么是偏函数 partial function, 它和普通的函数有什么区别?
- 什么是函数的科里化?举一个例子说明, 并指出它有什么价值?
- 高阶函数与普通函数的却别是什么? 请列出scala中的至少3个高阶函数,并给出每个函数至少一种使用例子,并加以说明。
- 了解scala的隐式转换`implicit`, 并实现一个简单的隐式转换, 将一个类转换为JSON字符串

```scala
class Person(val name:String, val age:Int){}
```

- 写出`zip`函数的一个使用场景
- 样本类有什么用处?
- scala的类型推断有什么价值? scala中每个变量都有确定的类型么?
- 请先实现一个libsvm格式解析函数,函数原型`def parseLibSVMRecord(line: String): (Double, Array[Int], Array[Double])`, 输入是一行,输出一个label和sparsevector。
- 完成之后,阅读Spark中解析libsvm数据格式的一个函数源代码,请写出至少3个你们实现上的差异,进行对比. <https://github.com/apache/spark/blob/022667cea666190bea651a3873234700a472326c/mllib/src/main/scala/org/apache/spark/mllib/util/MLUtils.scala#L126>
- scala的异常处理`catch`部分实际上是一个函数! 请指出这个观点的正确性?
- 