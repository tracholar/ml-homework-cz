## 思考题

Q1: 为什么要使用thrift来定义接口，有什么好处?

A: 满足当前大数据量、分布式、跨语言、跨平台数据通讯的需求。
通过简单定义Thrift描述语言文件，使用Thrift -gen命令可以生成多种语言的代码，这些代码包含了网络通信，数据编解码的功能。
这就免去了前后台编写这部分繁琐的代码，同时也统一了前后台的实现逻辑。

Q2: thrift的序列化与JSON和XML序列化之间的差异和优劣是什么?

A: 1）差异：Thrift的序列化被嵌入到Thrift框架里面，Thrift框架本身并没有透出序列化和反序列化接口。
2）优点：Thrift在空间开销和解析性能上有较大优势，对于对性能要求比较高的分布式系统，一般采用Thrift。
3）缺点：由于Thrift没有透出序列化和反序列化接口，这导致其很难和其他传输层协议共同使用（例如HTTP）。

Q3: 用自己的话描述一下RPC和本地函数调用的关系与区别，请举一个例子进行描述。

A: RPC和本地函数调用都是调用函数，如调用function。RPC是service端和client端建立连接，通过client.py / client.java 等来调用service端的function。
而本地函数调用，则在本地进行。

Q4: spring bean是什么? 请举例说明。

A: bean 是由 Spring IoC 容器管理的对象。一般对于大型项目，常用XML来配置，因为其结构清晰。XML 配置文件的根元素是 <beans>，该元素包含了多个子元素 <bean>。
使用 id 属性定义了 bean，并使用 class 属性指定了 bean 对应的类。
比如：

    <bean id="helloWorld" class="com.chengjiafeng.HelloWorld">
        <property name="print" value="Hello World!" />
    </bean>

Q5: junit 的@Before 和 @After有什么用途? 请在你的单元测试中使用一次

A: Before一般用来创建实例，After销毁实例。

Q6: 阅读以下fb303.thrift的源代码,请描述一下它做了哪些事情?

A: 定义了一个FileStruct，包含service中的4个函数，enum枚举了CatMode两个属性TXT & BIN。