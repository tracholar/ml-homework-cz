## 思考题
Q1. 函数式编程中的「函数」与一般编程语言(如C/Java等)中所说的「函数」有什么联系和区别?

A. 函数式编程中的函数不是程序中的函数，而是数学中的函数（映射关系）。函数式编程是一种编程模型，将计算机运算看做是数学中函数的计算，并且避免了状态以及变量的概念 。
C/Java中的函数是一组一起执行一个任务的语句。

Q2. 有人说函数式编程语言非常适合写并行和分布式程序,请根据自己的思考分析这个观点是否正确,并举例说明理由。

A. 1）函数式编程中不会有任何数据被同一线程修改两次。2）使用函数式编程对数据进行操作，并不会对原集合对象带来影响，比如map，flatMap。3）函数式编程之间没有共享的变量，通过参数和返回值来传递数据。

Q3. 请使用scala修改下列java代码,并要求具有scala style

```java
int[] arr = new int[] {1,2,3,4,5,6,7,8,9,10};
int sum = 0;
for(int i : arr){
    if(i % 2 == 0) continue;
    sum += i;
}
System.out.println(sum);
```

- scala
```scala
val arr = 1 to 10
val res = arr.filter(_%2 == 0).sum
res: Int = 30
```

Q4. 什么是偏函数 partial function, 它和普通的函数有什么区别?

A. 偏函数是对部分数据的映射，是一种不为每个可能的输入值都提供答案的函数。而普通函数是对数据的全映射。
```scala
scala> List(1, 3, 5, "seven") collect { case i: Int => i + 1 }
res3: List[Int] = List(2, 4, 6)
```

Q5. 什么是函数的科里化?举一个例子说明, 并指出它有什么价值?

A. 函数柯里化是把接受多个参数的函数变换成接受一个单一参数（最初函数的第一个参数）的函数，并且返回接受余下的参数而且返回结果.
```scala
scala> def addCurry(x: Int)(y: Int) = x + y
addCurry: (x: Int)(y: Int)Int

scala> addCurry(1)(2) 
res6: Int = 3
```
好处：1）接受多个参数的函数变换成接受一个单一参数。2）简化嵌套函数的开发。

Q6. 高阶函数与普通函数的却别是什么? 请列出scala中的至少3个高阶函数,并给出每个函数至少一种使用例子,并加以说明。

A. 高阶函数：接受一个或多个函数作为输入或者返回为另外一个函数。
example: map
```scala
scala> val arr = 1 to 4      
arr: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3, 4)
scala> val res = arr.map(_ + 1)
res: scala.collection.immutable.IndexedSeq[Int] = Vector(2, 3, 4, 5)
```
reduce
```scala
scala> val arr = 1 to 4      
arr: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3, 4)
scala> val res2 = arr.reduce((v1, v2) => v1 + v2)
res2: Int = 10
```
filter
```scala
scala> val arr = 1 to 4
arr: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3, 4)
scala> val res3 = arr.filter(_%2 == 0)
res3: scala.collection.immutable.IndexedSeq[Int] = Vector(2, 4)
```

Q7. 了解scala的隐式转换`implicit`, 并实现一个简单的隐式转换, 将一个类转换为JSON字符串

A. 隐式转换：当Scala编译器进行类型匹配时，如果找不到合适的候选，那么隐式转化提供了另外一种途径来告诉编译器如何将当前的类型转换成预期类型。
```scala
class Person(val name:String, val age:Int){}
implicit def classToJson(person: Person) = new JSONObject(person)
```

Q8. 写出`zip`函数的一个使用场景

A. zip函数将传进来的两个参数中相应位置上的元素组成一个pair数组(k, v)。比如在计算AUC时，label和score构成
```scala
scala> val label = Array(1,0,3,5)
label: Array[Int] = Array(1, 0, 3, 5)

scala> val score = Array(0.5, 0.1, 0.9, 1)
score: Array[Double] = Array(0.5, 0.1, 0.9, 1.0)

scala> label zip score
res7: Array[(Int, Double)] = Array((1,0.5), (0,0.1), (3,0.9), (5,1.0))
```

Q9. 样本类(case class)有什么用处?

A. 支持模式匹配

Q10. scala的类型推断有什么价值? scala中每个变量都有确定的类型么?

A. 避免类型不匹配的异常。还存在着same的类型（不确定？），比如join的操作会带来same的情况。
 
Q11. 
- 请先实现一个libsvm格式解析函数,函数原型`def parseLibSVMRecord(line: String): (Double, Array[Int], Array[Double])`, 输入是一行,输出一个label和sparsevector。

```scala
def parseLibSVMRecord(line: String): (Double, Array[Int], Array[Double])
```
- 完成之后,阅读Spark中解析libsvm数据格式的一个函数源代码,请写出至少3个你们实现上的差异,进行对比. <https://github.com/apache/spark/blob/022667cea666190bea651a3873234700a472326c/mllib/src/main/scala/org/apache/spark/mllib/util/MLUtils.scala#L126>

A. 1) 没有考虑到 indices should be one-based and in ascending order
```scala
val index = indexAndValue(0).toInt - 1 // Convert 1-based indices to 0-based.
```
2）head 和 tail 的使用

3）items.tail.filter(_.nonEmpty) 判断为空的考虑

Q12. scala的异常处理`catch`部分实际上是一个函数! 请指出这个观点的正确性?

在 Scala 里，借用了模式匹配的思想来做异常的匹配，因此，在 catch 的代码里，是一系列 case 字句。