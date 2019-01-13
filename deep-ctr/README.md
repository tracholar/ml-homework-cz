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