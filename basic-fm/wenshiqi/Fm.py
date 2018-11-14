#coding:utf-8


import xlearn as xl

fm_model = xl.create_fm()
fm_model.setTrain("/Users/wenshiqi/Documents/homework/xlearn/demo/classification/mushroom/agaricus_train.txt")
fm_model.setValidate("/Users/wenshiqi/Documents/homework/xlearn/demo/classification/mushroom/agaricus_test.txt")

#模型参数
#  0. binary classification
#  1. learning rate: 0.2
#  2. lambda: 0.002
#  3. evaluation metric: accuarcy
#  4. use sgd optimization method
param = {'task':'binary',
         'lr':0.2,
         'lambda':0.002,
         'metric':'acc',
         'opt':'sgd'}

# 模型训练
# The trained model will be stored in fm_model.out
fm_model.fit(param, './fm_model.out')

# 模型预测
# The output result will be stored in fm_output.txt
fm_model.setTest("/Users/wenshiqi/Documents/homework/xlearn/demo/classification/mushroom/agaricus_test.txt")
fm_model.predict('./fm_model.out',"fm_output.txt")
