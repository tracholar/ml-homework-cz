## 试验报告


### 实验原理
- LR 线性模型
- DNN 就是先将离散特征 embedding, 然后输入到MLP中
- wide & deep, 就是 DNN 与 LR Boosting 融合
- deepFM , 就是 DNN 与 FM (可能还包括LR) 融合

### 主要步骤
- embedding的实现使用 `tf.nn.embedding_lookup`
- LR 的实现也用的是embedding,只是embedding的维度为1, 然后利用 `tf.reduce_sum` 得到和
- DNN 的全连接层使用了 `tf.layers.dense` 这个高级API,而不是用原始的矩阵乘法
- FM实现是通过对 embedding 向量 先做元素乘法, 然后利用 `tf.reduce_sum` 在特征维度求和, 实现向量内积
- DeepFM没有使用线性项


### 实验结果

|          | LR | DNN | wide & deep | deep FM |
| -------- | -- | --- | ----------- | ------- |
| test auc |0.590165193261 | 0.750348928931|     | 0.728536323932 |
| test loss| 2.71778810024| 2.33468127251 |             | 3.2091177702 |

- 目前还是一个初步试验结果, 目前没有加正则
- 试验发现 Adagrad 的优化效果比SGD要快,可能参数选得不对,没有详细调整
- 目前尚未实现在训练的时候打出验证集的效果
- LR没有交叉特征,所以效果明显很差,需要优化


### 思考与总结
- 目前只初步实现了大体框架
- 数据用的是 feed_dict 灌入,后面考虑改为 Dataset
