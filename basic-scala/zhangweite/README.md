## Scala基础教程
- 阅读scala教程,选择其中一个即可,如果有更好的教程材料欢迎提交PR
    - <https://www.runoob.com/scala/scala-tutorial.html>
    - <https://docs.scala-lang.org/tour/tour-of-scala.html>
    - <https://twitter.github.io/scala_school/>
- 完成编程作业和思考题


## 思考题
- 函数式编程中的「函数」与一般编程语言(如C/Java等)中所说的「函数」有什么联系和区别?

两者都有输入、计算逻辑和输出，但前者更注重数据的映射关系，后者更关心程序运行的顺序。  

- 有人说函数式编程语言非常适合写并行和分布式程序,请根据自己的思考分析这个观点是否正确,并举例说明理由。

函数式编程的思想确实很适合分布式，比如map,filter等函数很容易做分布式，但函数式编程语言整体上并不一定适合写分布式程序，还是要看需要实现的算法逻辑是否适合。  

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

```scala
val arr=Array(1,2,3,4,5,6)
arr.filter(_%2==1).size
```

- 什么是偏函数 partial function, 它和普通的函数有什么区别?

偏函数是具有类型PartialFunction[T1,T2]的一种函数，其中T1和T2分别是其接受的函数类型，和返回的结果类型。  
偏函数最大的特点就是它只接受和处理其参数定义域的一个子集，而对于这个子集之外的参数则抛出运行时异常，和Case语句的逻辑基本一致。 
定义偏函数的好处是在一些参数的返回值需要根据具体环境确定时，可以到时候再补充，同时偏函数之间的逻辑也可以相关联。  


- 什么是函数的科里化?举一个例子说明, 并指出它有什么价值?

函数的Curry是指将函数的参数分为多个参数列表，他的好处有：  
1.把多个参数转化为单参数函数的级联，达到了动态确定参数的目的。  
2.当某些参数不确定时，可以先保留一个存根，等剩余的参数确定以后，就可以通过存根调用剩下的参数。  
3.把复杂的函数切分为多个小模块的组合，逻辑更清晰。  

- 高阶函数与普通函数的区别是什么? 请列出scala中的至少3个高阶函数,并给出每个函数至少一种使用例子,并加以说明。

高阶函数的特点是可以接受函数参数或者返回一个函数。

```scala
val arr=Array(1,2,3,4,5,6)
arr.map(_-1)
arr.filter(_>3)
arr.apply(function, value) // function为某个函数，value为他的参数
```


- 了解scala的隐式转换`implicit`, 并实现一个简单的隐式转换, 将一个类转换为JSON字符串。

implicit是当参数类型不对时，编译器自动借助隐式类型转换。  

```scala
class Person(val name:String, val age:Int){}
implicit def class2str(p:Person)=gson.toJson(p, classOf[Person])
```

- 写出`zip`函数的一个使用场景

特征和值分别是a,b[Array]，然后可以用 dict(zip(a,b)) 获得特征和值的map。  

- 样本类有什么用处?
(case class)
1.样本类会添加与类名一致的构造方法，可以用Person("x")来构造Person对象。  
2.样本类参数列表中的所有参数隐式获得val前缀。  
3.编译器为样本类添加了方法toString、hashCode和equals的实现。  


- scala的类型推断有什么价值? scala中每个变量都有确定的类型么?

scala中的变量定义时可以省略类型，类型推断可以在一个复杂的流处理后自动得到输出流的数据类型，而且类型推断得到的类型往往更加宽泛、实用。  
scala中某些变量类型应该是在实际运行时才能确定下来，这和变量的上游数据流类型有关。  



- 请先实现一个libsvm格式解析函数,函数原型`def parseLibSVMRecord(line: String): (Double, Array[Int], Array[Double])`, 输入是一行,输出一个label和sparsevector。

同作业：  
```scala
def asPair(x:String) = (x.split(":")(0).toInt,x.split(":")(1).toDouble)
def parse(line: String) : (Double, Array[Int], Array[Double]) = {
	//TODO 实现parse过程
	val temp=line.split(" ")
	val (feat,value)=temp.slice(1,temp.length).map(asPair(_)).unzip
	(temp(0).toDouble, feat , value)
}
```

- 完成之后,阅读Spark中解析libsvm数据格式的一个函数源代码,请写出至少3个你们实现上的差异,进行对比. <https://github.com/apache/spark/blob/022667cea666190bea651a3873234700a472326c/mllib/src/main/scala/org/apache/spark/mllib/util/MLUtils.scala#L126>

整体逻辑差不多，都是map处理后unzip，区别在于源码中1.index调成从0开始，2.确认了index是否有重复以及是否排好序，3.最后转成Array（不转也行）  

- scala的异常处理`catch`部分实际上是一个函数! 请指出这个观点的正确性?

scala里的catch其实是用了模式匹配的方式来做的异常匹配，所以catch中使用了一堆case和finally语句来判断异常类型，所以从某种角度可以把catch部分理解成match。  

## 实现列表
- [getstart](getstart/)
- [tracholar](tracholar/)