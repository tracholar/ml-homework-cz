## 基于TensorFlow实现基本的CTR预估DNN模型
- 实现 LR
- 实现 DNN(Embedding + MLP)
- 实现 DNN + LR (wide & deep)
- 实现 DeepFM (DNN + FM + LR)
- 数据集请使用脚本 0_download_raw.sh 下载,便于对比,请在README文件中报告你的测试集上的效果!便于横向对比
  数据预处理请依次执行:
   1. 1_convert_pd.py 
   2. 2_remap_id.py
   3. build_dataset.py
- 启动代码参考 `getstart/` 目录
- 完成基本的实验报告
    1. 实验原理
    2. 主要步骤
    3. 实验结果
    4. 自己的思考
- 思考下列问题
    1. LR为什么要做特征交叉,其物理意义或者业务意义是什么?请举一个例子,用自己的语言说明这种交叉的意义
    2. FM 和 DNN 中的embedding有什么相同之处,有什么不同之处?请论证这里的FM实现和基本FM中的实现等价
    3. 思考怎么实现如下正则? 如果某个id出现的次数过少或者虽然出现很多次但是这个id加或者不加对模型没有影响, 怎么将它的embedding向量全部置0? 试着在你的DNN模型中增加这种正则
    
## 实现列表
提交PR的时候,请在下方列出你的项目

- [getstart](getstart/)
- [tracholar](tracholar/)