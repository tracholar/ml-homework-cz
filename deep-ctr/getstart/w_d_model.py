#coding:utf-8
import tensorflow as tf



class WideDeep(object):
    def __init__(self):
        # TODO 初始化计算图
        raise NotImplementedError()

    def fit(self, sess, data):
        # TODO 模型训练
        raise NotImplementedError()

    def predict(self,sess,  data):
        # TODO 预测
        raise NotImplementedError()

    def eval(self, sess, data):
        # TODO 模型评估
        raise NotImplementedError()
