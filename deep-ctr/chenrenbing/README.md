## DeepCTR启动代码

1. 实验原理

   ​    DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 

   ​    DCN：Deep & Cross Network for Ad Click Predictions 

   ​    W&D：Wide & Deep Learning for Recommender Systems

2. 实验结果

   |               | LR      | LR with Cross | DNN    | W&D    | deepFM |
   | ------------- | ------- | ------------- | ------ | ------ | ------ |
   | 测试集AUC     | 0.56470 | 0.5808        | 0.7981 | 0.7992 | 0.7675 |
   | 测试集LogLoss | 25.01   | 23.5072       | 16.69  | 16.64  | 17.609 |

   

3. 自己的思考

   DeepCtr 模型的演变在于提高算法对特征间不可观测关系的捕获