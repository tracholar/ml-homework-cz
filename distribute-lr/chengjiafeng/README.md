## 思考与总结
Q1. 什么情况下,模型参数数量会特别大,以致于单机存不下? 试着说明这种情况下,参数主要来自于模型的哪个部分?

A1. 1) 在特征维度很大的时候，导致模型参数量过大。2) 在模型的网络层数变多的时候，模型保存的网络参数变多，模型的参数量会特别大。

Q2. 如果参数数量太大,要分布在多台机器上, Server 端和 Worker 端在执行pull和push的时候要做哪些修改?
   
A2. 所有的worker读取batch的不同部分，计算损失函数的gradient，最后server将每个worker的gradient整合之后更新模型。
所以Server端pull work对应的weight，Worker端push server对应的梯度更新。

Q3. 了解一下 AllReduce, 试着说明利用PS如何实现 AllReduce 操作?

A3. AllReduce是一类算法，目标是高效得将不同机器中的数据整合（reduce）之后再把结果分发给各个机器。其中，一种算法：Ring AllReduce算法分为两个阶段。
第一阶段，将N个worker分布在一个环上，并且把每个worker的数据分成N份。其中，对于第k个worker，这个worker会把第k份数据发给下一个worker，同时从前一个worker收到第k-1份数据。
之后worker会把收到的第k-1份数据和自己的第k-1份数据整合，再将整合的数据发送给下一个worker。以此循环N次之后，每一个worker都会包含最终整合结果的一份。
第二阶段，每个worker将整合好的部分发送给下一个worker。worker在收到数据之后更新自身数据对应的部分。

