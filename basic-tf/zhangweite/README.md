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
第二行代码只包括tf的节点操作，Assign操的作用作是改变原节点的值，所以第二行代码唯一的操作是修改了W节点的值，W指向的一直是这个Variable，因此多次sess.run(W.assign_sub(0.1 * g))的值是改变的。
而第一行代码既包括节点操作也包括python的“-，=”操作，首先右边W-0.1*g其实是新建了一个Tensor节点，然后“W=新建节点”其实是改变了W的引用（即从原来的Variable指向了新建的Tensor），所以多次sess.run(W)的结果是不变的。

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
在神经网络中，深层的网络维度一般比浅层的要小，所以TensorFlow采用的是反向自动微分方式计算梯度。  
建立反向图的原因是tensorflow中的tensor都只记录了输入，而无法找到输出，所以需要建立反向图。  


5. tensorboard的直方图怎么查看? 怎么将训练集和测试集的数据显示在同一张图上?  
tensorboard --logdir=log，进入tensorboard选择直方图查看。  
在tensorboard网页scalars页面左下角都钩上即可。
tensorflow直方图是指计算图中的某些tensor随着时间变化的分布情况，比平常的直方图多一个时间切片维度。

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
对于计算图的可视化，变量作用域会给予域内的计算图一个封装，使得可视化后计算图的逻辑更加清晰。  

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


12.dropout  
为了更好的拟合训练数据，神经网络的参数数量一般设置过大，从而会导致过拟合。  
不改变模型结构的基础上，处理过拟合的方式有一般以下几种：  
1.数据增强，2.降低网络复杂度，3.Early stopping，4.正则化，5.对网络的各个部分加噪，6.贝叶斯方法。  
改变模型结构的方式有：Bagging, boosting, dropout  
dropout作用于layer，他的作用是在网络训练的过程中，随机使该layer的部分神经元输出为零，并且在更新参数时忽略这些零输出的神经元。这相当于是在训练过程中随机的简化模型，使得每个batch训练时的模型的结构都是变化的。在预测时，该layer全部神经元正常运行，但需要对其权值乘以dropout的概率p，以达到预测和训练输出值大小上相对一致的效果。  
dropout能够起到防止过拟合效果的原因如下：  
1.对一个layer加dropout，在训练时相当于训练多个具有相关性的layer“子集”，而在预测时这些“子集”同时激活，使得输出值是全部“子集”的加权和，这相当于是模型维度的“bagging”。  
2.dropout在训练时对神经元“随机采样”，降低了原本可能具有固定关系的神经元的相互依赖性，提升了模型的鲁棒性。  


13.batch normalization  
神经网络在训练中，由于网络中参数变化会引起内部结点数据分布发生变化，被称作Internal Covariate Shift。  
这一现象会使得上层网络需要不断调整以适应输入分布的变化，降低网络训练速度。同时，如果输入分布不断变化的情况下，会降低激活函数的效果，比如sigmoid函数会陷入饱和区。  
所以BN的思路就是统一输入的每个特征的分布（0均值1方差），但强硬的归一化输入分布会削弱数据的表达能力，使得整个网络学不到东西。所以BN就在归一化分布的基础上，添加了恢复其分布的线形操作，并将恢复过程的参数加入网络进行训练，相当于让网络自己权衡输入分布的统一和输入数据的表达能力。  
在训练过程中，每个batch的训练按上述操作即可，但需要存储所有特征的均值和方差。  
在预测过程中，输入数据归一化步骤的均值和方差即采用训练时统计的所有数据的均值和方差。  
BN使得输入数据的分布变得相对稳定，使得模型学习过程更加稳定，一定程度上简化了调参过程，加快了模型的学习速率，也具备了一定的正则化效果（弱化了输入数据的表达能力）。  

   
14.网络权值初始化方差  
为了使得信息再网络中更好的传播，每一层layer输出的方差应该尽量相等。  
假设layer权值服从独立同分布，为了使得输出方差等于输入方差，权值方差应该为1/n，其中n为上一层layer神经元数量。而在方向传播中，同理得到权值方差应该为1/m，其中m为下一层layer的神经元数量。为了综合前向与后向，权值方差应为2/（m+n）。  


15.md和ps在实现lr时都差异  
mapreduce实现分布式lr：  
1.Root节点向计算节点发送参数Wt  
2.计算节点根据样本维度和特征维度同时计算梯度Gt，计算完毕后发送给root节点  
3.root节点根据Gt更新参数为Wt+1，检验是否收敛，进行下一次训练  
Parameter sever实现分布式lr：  
1.sever节点分布式存储参数Wt  
2.worker同样以样本维度和特征维度分别负责对应部分，训练时worker向server请求参数数据（pull），计算对应参数的梯度，更新参数后回传给server（push）。所有worker可以完全异步进行训练，也可以按照一定的规则半异步进行训练。  
3.server节点将worker传输的局部更新进行汇总后更新全局参数，进行下一次迭代  


16.tf.GraphKeys   
Tensorflow 内部定义了许多标准 Key，全部定义在了 tf.GraphKeys 这个类中。其中有一些常用的，tf.GraphKeys.TRAINABLE_VARIABLES, tf.GraphKeys.GLOBAL_VARIABLES 等等。tf.trainable_variables() 与 tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES) 是等价的；tf.global_variables() 与 tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES) 是等价的。  
tf.collection 是为了方便用户对图中的操作和变量进行管理，而创建的一个概念。它可以说是一种“集合”，通过一个 key（string类型）来对一组 Python 对象进行命名的集合。这个key既可以是tensorflow在内部定义的一些key，也可以是用户自己定义的名字（string）。  


17.is_chief的作用  
is_chief：如果True，它将负责初始化和恢复底层TensorFlow会话。如果False，它将等待主管初始化或恢复TensorFlow会话。  


18.local_variables_initializer  
local变量在的集合, 用tf.local_variables_initializer()初始化 collections=[tf.GraphKeys.LOCAL_VARIABLES]  
一般建立的变量(就是tf.Variable())在的集合，用tf.global_variables_initializer()初始化collections=[tf.GraphKeys.VARIABLES]  
GraphKeys.LOCAL_VARIABLE中的变量指的是被添加入图中，但是未被储存的变量。  


19.tf.GraphKeys.UPDATE_OPS  
tf.GraphKeys.UPDATE_OPS 保存一些需要在训练操作之前完成的操作，比如batch_normaliazation中更新均值和标准差，dropout网络输出等。  
（并配合tf.control_dependencies函数使用）  
