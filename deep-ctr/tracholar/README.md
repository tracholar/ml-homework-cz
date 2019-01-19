## 试验报告


### 实验原理
- LR 线性模型
- DNN 就是先将离散特征 embedding, 然后输入到MLP中
- wide & deep, 就是 DNN 与 LR Boosting 融合
- deepFM , 就是 DNN 与 FM (可能还包括LR) 融合

### 主要步骤
- 特征预处理
    - 依次执行一下步骤, 即可在 'deep-ctr/' 目录下生成 `dataset.pkl` 数据集文件
        1. 1_convert_pd.py 
        2. 2_remap_id.py
        3. build_dataset.py
    - 预处理后的数据大概是这样
    ```
    reviewID, hist_list, asin, label
    23423434, [23,123,123], 232, 0
    ```
    - 数据集中包含了这几个数据
        - `train_set` 训练集
        - `test_set` 测试集
        - `cate_list` 类别列表,实际上index代表产品id(即asin),利用这个列表可以生成类别特征
        - `user_count, item_count, cate_count` 统计信息: 用户数目, item数目, cate数目
    - 加载代码如下
    ```python
    with open('../dataset.pkl', 'rb') as f:
        train_set = pickle.load(f)
        test_set = pickle.load(f)
        cate_list = pickle.load(f)
        user_count, item_count, cate_count = pickle.load(f)
    ```
- embedding的实现使用 `tf.nn.embedding_lookup`
- LR 的实现也用的是embedding,只是embedding的维度为1, 然后利用 `tf.reduce_sum` 得到和
- DNN 的全连接层使用了 `tf.layers.dense` 这个高级API,而不是用原始的矩阵乘法
- WideDeep 的cross特征是通过类别id相乘(即交叉)得到, 也试过用用户历史asin与候选asin交叉,发现维度太高,有几十亿维,单机扛不住,就没搞了,在工业环境其实可以用这个交叉特征进一步增强模型的记忆能力
    - 遇到一个问题,在tf中,不同dim的张量相乘会出问题, 会报`Incompatible shapes: [128,155] vs. [128]`这种不兼容shape的错误, 可以通过 `tf.expand_dims`将其中一个张量的dim扩大的方法解决, 不会自动做broadcast?
- FM实现是通过对 embedding 向量 先做元素乘法, 然后利用 `tf.reduce_sum` 在特征维度求和, 实现向量内积
- DeepFM相当于在WideDeep上加了FM
- 运行方法 `python train.py` 可以把里面的模型改为其他模型测试效果
- `tf.metrics.auc` 可以流式计算AUC,但是根据训练完了之后,根据预测结果重新计算的AUC相差很大,因此,在评估效果时,需要重新计算AUC,不能按照这个的输出计算AUC。


### 实验结果

|          | LR | LR with Cross feature| DNN | wide & deep | deep FM |
| -------- | -- | -------------------- | --- | ----------- | ------- |
| test auc |0.590165193261 | 0.673147679661 | 0.750348928931|0.783477438994| 0.728536323932 |
| test loss| 2.71778810024| 2.77127897739   | 2.33468127251 | 2.27425599098 | 3.2091177702 |

- 目前还是一个初步试验结果, 目前没有加正则
- 试验发现 Adagrad 的优化效果比SGD要快,可能参数选得不对,没有详细调整
- 目前尚未实现在训练的时候打出验证集的效果
- LR没有交叉特征,所以效果明显很差,需要优化


### 思考与总结
- 目前只初步实现了大体框架
- 数据用的是 feed_dict 灌入,后面考虑改为 Dataset
