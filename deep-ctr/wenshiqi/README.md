## 试验报告


### 实验原理
- LR 线性模型
    - 将embedding的步骤看成是特征工程的部分，当做是将稀疏的cate和id特征映射到稠密向量，然后再接一个wx+b来构建模型
- LR-CROSS
    - 在lr的基础上增加 <user,item>, <user,cate>, <item, his_i>, <cate, hist_i_cate>的交叉特征，但是由于机器性能原因，最终只加入交叉特征<cate, hist_i_cate>,加入交叉特征后，性能较lr有所提升
- DNN 
    - 先将稀疏特征 embedding 成稠密向量（embedding维度为8），再输入一个3层的全连接网络
- Wide & deep
    - 先将类别特征进行embedding映射，然后分别输入lr 和dnn, 将两者的输出结果值相加，得到最终输出
- deepFM 
    - 一维部分：相当于lr
    - 特征交叉：相当于fm
    - deep部分：相当于dnn
    - 最终将3个值相加，得到最终输出


### 主要步骤
- 特征预处理：直接用了左老师代码：）
- LR: 
    - 用tf.nn.embedding_lookup将离散特征转稠密特征
    - wx+b在获取特征维度的时候用了 `np.shape(feats)[1]`，也可以用`feats.get_shape()[1]` (但是这里要求feats必须是tensor，返回为tuple),还有一种方法是`tf.shape(feats)`,但是这样返回的是tensor会报错
- DNN:
    - 将embedding向量维度设置为8维，在获取his_item的item和cate的embeding时，用了reduce_sum/mean/min/max的操作，相当于多构建了一些特征
- Wide&deep:
    - 做特征交叉的时候本来想任何两个特征都来个交叉，但是后来跑不动，就改成只做cate特征的交叉了
    - 在算交叉特征的id时（cateid相乘）,本来写法是`cate_cross = tf.squeeze(tf.gather(cate_list, self.hist_i)) * tf.gather(cate_list, self.tid)`，目的是消除hist_i进行gather操作之后多出来的1维，但是squeeze会消除所有为1的维度，当只有一个his_i的时候，hist_id的维度也会被消除，所以运行出错。后面改成了`tf.expand_dims(tf.gather(cate_list, self.tid), 1)` 
- Deepfm:
    - 分成了lr,fm,dnn3个部分
    - lr是直接查embedding，然后reduce_sum得到结果
    - fm对所有特征之间都做了交叉
    - dnn还是用的3层的全连接
    


### 实验结果

|          | LR | LR with Cross feature| DNN | wide & deep | deep FM |
| -------- | -- | -------------------- | --- | ----------- | ------- |
| test auc | 0.766424415463 | 0.803966237561 | 0.80109151774| 0.813970135661| 0.705766318559|
| test loss| 5.93037188134e-06| 5.58606841707e-06   | 5.64389145599e-06 | 5.49726073986e-06 | 0.0022221827835|

- 目前看来deepfm的效果最差，我感觉是我没调好的问题ORZ..

### 思考与总结
- 目前只是按照自己的理解实现了这几个算法，还没有将内容整理到相关的博客，后面会进行整理
- lr的实现我在embeding后面又接了一个wx+b,我觉得可以理解为特征映射之后再做lr
- wide&deep 我也是直接用的embedding映射后的结果后面又接了一个wx+b
- deepfm我给了1维的特征单独的权重，并且fm特征交叉的时候所有特征都做了两两交叉,但是得到的结果还是很差，这是因为fm适用于数据量大且非常稀疏的数据，我们这样的样本不能充分训练所有的权重么
- 在实现算法的过程中经常出现维度对不上的问题，而TensorFlow的图中间也不能打出具体的值，看不到具体的特征维度，后面还是要多了解一下相关的只是

