## TensorFlow入门教程
- 通过MNIST数据集训练一个多分类神经网络
- 熟悉TensorFlow的基本使用
    1. 定义计算图
    2. placeholder和dataset两种方式的数据输入
    3. 优化器的使用
    4. summary的使用
    5. tensorboard的使用
- 参考 
    - 《深入理解TensorFlow》
    - TensorFlow白皮书
    - <http://dlsys.cs.washington.edu/schedule>

## 思考题
1. 请使用自己的语言举例说明TensorFlow的声明式编程和我们日常的编程方式上的区别? 如何理解TensorFlow中一切都是计算图上的节点? TensorFlow中写日志操作也是计算图中的节点吗?
2. 下面的代码有区别吗?请详细说明。 其中预定义 `W = tf.Variable(tf.zeros(10))`, `g = np.random.rand(10)`
    - `W = W - 0.1 * g`
    - `W.assign_sub(0.1 * g)`
3. 请说明张量、操作、变量之间的区别和联系
4. 请使用tensorboard查看计算图可视化的结果, 思考: 为什么TensorFlow要建立一张反向计算图, 而不是直接在原图中实现BP算法?
5. tensorboard的直方图怎么查看? 怎么将训练集和测试集的数据显示在同一张图上?
6. 从checkpoint中恢复模型的原理是什么?是如何将保存的值和张量关联上的?
7. 使用变量作用域的好处是啥?
8. 分布式训练的时候, 程序是如何组织server端代码和worker端代码, 使得两部分代码可以放到一个脚本文件中的?
9. 用自己的话简述分布式训练时Server和Worker分别做了哪些事情? 参数服务器与MapReduce的区别有哪些?
10. 分布式训练的时候,同步更新和异步更新的区别和优缺点,TensorFlow在异步更新的时候如何保证server端数据的一致性?
11. `placeholder`方式输入数据和`dataset`方式的区别和利弊有哪些?为什么实际使用中更倾向于使用`dataset`API?

## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)
