## 利用thrift和spring搭建服务
 未完成问题：使用springboot 来作为服务端。需要在client和server类上加SpringApplication标注即可。
 配置文件使用的Application.properties,没使用xml。

## 思考题
1. 为什么要使用thrift来定义接口,有什么好处?
      屏蔽底层细节。
2. thrift的序列化与JSON和XML序列化之间的差异和优劣是什么?
      说到底，不是很明白。XML 和JSON数据解析更更容易，但是是基于字符的，耗传输资源。
3. 用自己的话描述一下RPC和本地函数调用的关系与区别,请举一个例子进行描述
      关系：本质上是一回事。区别：多了远程传输的作用，方法作用在另外的主机上。
      例如：美团的 hope -dfs  ls 命令和 linux 的ls 命令。东西都是同一种东西，但是作用在不同机子上。
4. spring bean是什么? 请举例说明
      Spring Bean是事物处理组件类和实体类（POJO）对象的总称
5. junit 的@Before 和 @After有什么用途? 请在你的单元测试中使用一次
       Before 执行其他测试方法之前，会执行的代码；
       After  执行完其他测试方法，会执行的代码。
6. 阅读以下`fb303.thrift`的源代码,请描述一下它做了哪些事情?
       定义了服务器状态及相关查询、设置方法。


## 实现
- [tracholar](tracholar/)
- [getstart](getstart/)