#coding:utf-8

from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
import logging

logging.basicConfig()

class ModelMixin(object):
    def fit(self, sess, train_set, eval_set = None):
        """
        模型已定义好的张量有:
            - self.uid  用户ID
            - self.tid  产品ID
            - self.y  target
            - self.hist_i   用户历史asin序列
            - self.hist_len  历史序列长度
            - self.loss      loss
            - self.train_op   训练op
            - self.auc        auc
            - self.auc_update_op  auc更新的op
            - self.global_step     步数
            - self.logits          模型输出的对数几率
        :param sess:
        :param train_set:  训练集
        :param eval_set:   验证集
        :return: None
        """
        loss_sum = 0
        for epoch in range(5):
            for _, row in DataInput(train_set, 128):
                reviewerId, asin, y, hist, hist_len = row

                ## TODO 实现模型训练逻辑, 并且每隔1000次迭代打印出部分调试信息
                raise NotImplementedError()

            ## TODO 每一个epoch完成之后,调用 eval() 方法实现模型评估
            raise NotImplementedError()

    def eval(self, sess, data_set, name='eval'):

        loss_sum = 0
        logits_arr = np.array([])
        y_arr = np.array([])

        for _, row in DataInput(data_set, 128000):
            reviewerId, asin, y, hist, hist_len = row

            ## TODO 实现预测逻辑并累加loss
            raise NotImplementedError()

        ## TODO 实现模型评估, 计算AUC, 并打印出效果日志
        raise NotImplementedError()

    def predict(self, sess, data_set, **kwargs):
        ## TODO 输出预测概率值
        raise NotImplementedError()