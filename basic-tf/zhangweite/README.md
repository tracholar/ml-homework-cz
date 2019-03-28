## 实验报告
## 实验原理
1.利用TensorFlow搭建MLP（LR）、CNN和RNN网络，实现MNIST数据集的分类。  
2.利用summary与tensorboard记录权值与结果，根据结果调整网络超参数。
## 主要步骤
1.获取MNIST数据集，并利用placeholder或dataset方式输入网络（分别是dnn.py和dnn_dataset.py）。  
2.MLP相当于在LR的基础上添加了hidden layer。  
3.基本的CNN网络由多个卷积层、pooling层和flatten层组成，利用stride=2的卷积层代替max_pooling层会有更好的效果。  
4.RNN的结构采用lstm，同理可扩展为双向RNN和多层RNN。  
5.网络层参数维度较大的情况添加dropout层。  
6.batch_normalization在该例子中效果并不是很好（batch=100）。  
7.网络权值随机初始化能够加速网络收敛，甚至能和激活函数搭配使用（selu）。  
8.test准确率不能直接调用tf.metrics.accuracy，它指的是整个session内，所有feed_dict数据的正确率。  
## 实验结果
batch_size=100的情况下，  
-MLP训练10000个batch，test acc=0.9398  
-CNN训练1000个batch，test acc=0.9832  
-RNN训练10000个batch，test acc=0.9804  
上述三个网络均采用了简单的网络结构（电脑跑不动），并且在训练中没有收敛。  
总结来说，CNN网络能够较好的对图片做分类，但RNN能够在参数量较少的情况下达到较高的准确率令人惊讶。  

## 思考题
1. 请使用自己的语言举例说明TensorFlow的声明式编程和我们日常的编程方式上的区别? 如何理解TensorFlow中一切都是计算图上的节点? TensorFlow中写日志操作也是计算图中的节点吗?  
-TF的声明式编程相当于提前建立好计算框架，包括计算节点以及数据维度，在搭建框架时并不进行计算。在执行的时候给予输入以及执行命令，整个计算框架才开始计算。而日常的编程则是顺序执行的，一旦执行完语句之后就会得到结果。TF这种运行模式适合于机器学习训练以及预测的模式。  
-TF中的计算图包括节点与连接线，节点表示数据输入/输出、权值以及计算模块，连接线则表示了数据的传递方向，所以TensorFlow计算图上的节点基本反应了整个计算框架。  
-写日志操作只是记录节点输出，应该不算计算图中的节点。  

2. 下面的代码有区别吗?请详细说明。 其中预定义 `W = tf.Variable(tf.zeros(10))`, `g = np.random.rand(10)`
    - `W = W - 0.1 * g`
    - `W.assign_sub(0.1 * g)`  
原先W是Variable，第一行代码返回的是Tensor，第二行代码返回的是Variable。  

3. 请说明张量、操作、变量之间的区别和联系  
Variable和Tensor的属性如下：  
tf.Variable(initial_value, trainable, collections, validate_shape, name)  
tf.Tensor(device, dtype, graph, name, op, shape, value_index)   
Api里对variable和tensor的重点解释如下：  
A variable maintains state in the graph across calls to run()  
A Tensor is a symbolic handle to one of the outputs of an Operation  
我的理解是，  
variable具有存储空间，在训练过程中属性保持不变，并且可以更新其数值。  
tensor保存的是数据从输入到输出的一系列计算过程，并提供op可以run出当前状态的输出结果。  
在计算类型中，能够用tensor类型计算的都可以利用variable类型替代。  
在计算逻辑中，variable是最简单的tensor，没有任何计算过程。  
操作（Session.run）是指执行某一部分计算图的过程。  

4. 请使用tensorboard查看计算图可视化的结果, 思考: 为什么TensorFlow要建立一张反向计算图, 而不是直接在原图中实现BP算法?  
TensorFlow的求导方式为自动微分方式（介于符号计算和数值计算之间），即每个最小计算单元（op）都定义好了forward和backward（grad）函数，整个计算图里的求导则按照链式法则计算。  
自动微分具有前向和后向两种方式，当求dy/dx时（x的维度为m，y的维度为n），所求的结果是一个m*n的雅可比矩阵。借由微分的加法原则，求一次d/dx和一次d/dy都是一次矩阵乘法，所以前向计算方式需要计算m次自动微分，后向方式需要计算n次自动微分。  
在神经网络中，深层的网络维度一般比浅层的要小，所以TensorFlow采用的是反向自动微分方式计算梯度，所以需要建立反向图。  

5. tensorboard的直方图怎么查看? 怎么将训练集和测试集的数据显示在同一张图上?  
tensorboard --logdir=log，进入tensorboard选择直方图查看。  
在tensorboard网页scalars页面左下角都钩上即可。

6. 从checkpoint中恢复模型的原理是什么?是如何将保存的值和张量关联上的?  
checkpoint文件是结构与权重分离的四个文件，  
checkpoint：保存模型文件的路径信息列表，可以查询到最新保存的文件信息  
model.ckpt.meta：保存网络结构  
model.ckpt.data：保存网络权值  
model.ckpt.index：保存索引信息，作用是将Tensor name对应到Tensor的类型、形状、偏移和校验等信息，即关联meta文件和data文件。   

7. 使用变量作用域的好处是啥?  
tf中的作用域包括名称作用域和变量作用域，名称作用域中的variable和tensor都会加上作用域前缀。  
为了共享变量，定义了tf.get_variable(‘name’,)，它无视名称作用域，若定义变量名称已经存在则会报错。  
为了进一步管理tf.get_variable，定义了变量作用域，tf.get_variable在变量作用域中会加前缀。同时变量作用域还可以通过设定reuse=True来定义共享变量，并且定义了一个变量作用域后，相当于间接定义了一个名称作用域。此外，变量作用域还可以为tf.get_variable(‘name',)设置默认的初始化分布。  
综上，变量作用域相当于加强版的名称作用域，可以更好的管理变量命名以及变量共享。  

8. 分布式训练的时候, 程序是如何组织server端代码和worker端代码, 使得两部分代码可以放到一个脚本文件中的?  
利用如下代码来组织两端的程序，  
if FLAGS.job_name == "ps":  
	server.join()  
elif FLAGS.job_name == "worker":  
如果是ps端，则等待worker端的请求；如果是worker端，则依次进行初始化、模型训练等操作。   

9. 用自己的话简述分布式训练时Server和Worker分别做了哪些事情? 参数服务器与MapReduce的区别有哪些?  
-Server负责更新参数，Worker负责计算梯度。  
-参数服务器相较于MapReduce的优点：参数全局共享，支持异步通信，新增节点不需要重启。  
1.server初始化参数；worker从server获取参数，同时读取训练数据迭代更新参数。  
2.任一worker一次训练完成后，将参数梯度传回至server；server根据一定的策略更新参数。  
3.worker重新获取server更新后的参数，并读取下一batch的训练数据，回到2。  

10. 分布式训练的时候,同步更新和异步更新的区别和优缺点,TensorFlow在异步更新的时候如何保证server端数据的一致性?  
-同步更新是指全部worker完成后再统一更新参数，优点是参数更新稳定，缺点是有木桶效应。  
异步更新是指任一worker完成后直接更新server的参数（更新方式：1.利用其他worder的历史数据来平均，2.单独利用该worker的结果更新，3.取一个权衡），优点是效率高，缺点是参数更新不稳定。  
-TensorFlow在异步更新的时候利用一致性hash算法来保证server端数据一致性，算法主要原理是将数据和server利用hash算法映射到圆环上，并将数据存储到顺时针最近的server上。一致性hash算法也使得server增删时，失效的缓存数量最少。  
 

11. `placeholder`方式输入数据和`dataset`方式的区别和利弊有哪些?为什么实际使用中更倾向于使用`dataset`API?  
-Placeholder方式只能读内存数据，并需要提前确定数据维度。  
-Dataset同时支持从内存和硬盘里读取数据，并根据第一个维度利用iterator迭代读取，具有repeat、map、shuffle、batch等变换功能。  
