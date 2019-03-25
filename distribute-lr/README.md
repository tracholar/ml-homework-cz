## 实现分布式机器学习算法
- 了解参数服务器 Parameter Server, 并实现一个简单的训练逻辑回归的 PS
- 实现L2正则和L1正则版分布式逻辑回归
- 尝试单机测试通过后,在多台机器上运行
- 参考文献: 
    1. Parameter Server for Distributed Machine Learning
    2. Scaling Distributed Machine Learning with the Parameter Server
    3. Project Adam: Building an Efficient and Scalable Deep Learning Training System
    4. Tensorflow: Large-scale machine learning on heterogeneous distributed systems
- 参考 getstart/ 启动代码
- [可选] RPC通信采用protobuf二进制格式
- [可选] 实现同步更新和异步更新模型参数


## 思考与总结
1. 什么情况下,模型参数数量会特别大,以致于单机存不下? 试着说明这种情况下,参数主要来自于模型的哪个部分?
2. 如果参数数量太大,要分布在多台机器上, Server 端和 Worker 端在执行pull和push的时候要做哪些修改?
3. 了解一下 AllReduce, 试着说明利用PS如何实现 AllReduce 操作?

## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)
