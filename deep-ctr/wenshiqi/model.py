#coding:utf-8

from __future__ import print_function
import tensorflow as tf
from input import DataInput
from sklearn.metrics import  roc_auc_score
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
                loss, _, _,= sess.run([self.loss, self.train_op, self.auc_update_op], feed_dict={
                    self.uid: reviewerId,
                    self.tid: asin,
                    self.y: y,
                    self.hist_i: hist,
                    self.hist_len: hist_len
                })
                loss_sum += loss

                if self.global_step.eval(session=sess) % 1000 == 0:
                    log_data = {'loss' : loss_sum,
                                'global_step': self.global_step.eval(session=sess),
                                'auc' : self.auc.eval(session=sess),
                                'epoch' : epoch}
                    print('Epoch {epoch}, Global step = {global_step}, Loss = {loss}, AUC = {auc}'.format(
                        **log_data))

                    loss_sum = 0
            ## TODO 每一个epoch完成之后,调用 eval() 方法实现模型评估
            print('Epoch {epoch}, '.format(epoch=epoch), end='')
            self.eval(sess, train_set, name='train')
            if eval_set is not None:
                print('Epoch {epoch}, '.format(epoch=epoch), end='')
                self.eval(sess, eval_set, name='eval')

    def eval(self, sess, data_set, name='eval'):

        loss_sum = 0
        logits_arr = np.array([])
        y_arr = np.array([])

        for _, row in DataInput(data_set, 128000):
            reviewerId, asin, y, hist, hist_len = row
            loss ,logits = sess.run([self.loss, self.logits], feed_dict={
                self.uid : reviewerId,
                self.tid : asin,
                self.y : y,
                self.hist_i : hist,
                self.hist_len : hist_len

            })

            loss_sum += loss
            logits_arr = np.append(logits_arr, logits)
            y_arr = np.append(y_arr, y)


        ## TODO 实现模型评估, 计算AUC, 并打印出效果日志
        auc = roc_auc_score(y_arr, logits_arr)
        log_data = {'name': name,
                    'loss': loss_sum / len(data_set),
                    'auc': auc,
                    }
        print('Eval {name} : avg loss = {loss} auc = {auc}'.format(**log_data))


    def predict(self, sess, data_set, **kwargs):
        ## TODO 输出预测概率值
        logits_arr = np.array([])

        for _, row in DataInput(data_set, 128000):
            reviewerId, asin, y, hist, hist_len = row
            logits = sess.run([self.logits], feed_dict={
                self.uid: reviewerId,
                self.tid: asin,
                self.y: y,
                self.hist_i: hist,
                self.hist_len: hist_len
            })

            logits_arr = np.append(logits_arr, logits)
        return 1 / (1 + np.exp(- logits_arr))  # 输出概率