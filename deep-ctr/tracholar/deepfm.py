#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np


class DeepFM(object):
    def __init__(self, **kwargs):
        self.uid = tf.placeholder(tf.int32, [None, ])
        self.tid = tf.placeholder(tf.int32, [None, ])
        self.y = tf.placeholder(tf.float32, [None,])
        self.hist_i = tf.placeholder(tf.int32, [None, None])
        self.hist_len = tf.placeholder(tf.int32, [None, ])

        emb_dim = 16
        uid_emb_w = tf.get_variable("uid_emb", shape=[kwargs['user_count'], emb_dim])
        tid_emb_w = tf.get_variable("tid_emb", shape=[kwargs['item_count'], emb_dim])
        cate_emb_w = tf.get_variable("cate_emb", shape=[kwargs['cate_count'], emb_dim])

        cate_list = tf.convert_to_tensor(kwargs['cate_list'], dtype=tf.int64)


        all_emb = [
            tf.nn.embedding_lookup(uid_emb_w, self.uid),
            tf.nn.embedding_lookup(tid_emb_w, self.tid),
            tf.reduce_sum(tf.nn.embedding_lookup(tid_emb_w, self.hist_i), axis=1),
            tf.nn.embedding_lookup(cate_emb_w, tf.gather(cate_list, self.tid)),
            tf.reduce_sum(tf.nn.embedding_lookup(cate_emb_w, tf.gather(cate_list, self.hist_i)), axis=1),
        ]
        mlp_input = tf.concat(all_emb, axis=1)
        mlp_hidden = tf.layers.dense(inputs=mlp_input, units=64, activation=tf.nn.relu)
        mlp_out = tf.reduce_sum(tf.layers.dense(inputs=mlp_hidden, units=1, activation=None), axis=1)

        fm_out = tf.reduce_sum( all_emb[0]* all_emb[1] + all_emb[0] *  all_emb[3] + all_emb[1] * all_emb[2] + all_emb[
            3] * all_emb[4], axis=1)

        self.logits = mlp_out + fm_out
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels=self.y))
        self.opt = tf.train.AdagradOptimizer(0.1)

        self.global_step = tf.Variable(0, trainable=False, name='grobal_step')
        self.train_op = self.opt.minimize(self.loss, global_step=self.global_step)

        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))





    def fit(self, sess, train_set):

        loss_sum = 0
        for epoch in range(5):
            for _, row in DataInput(train_set, 128):
                reviewerId, asin, y, hist, hist_len = row
                loss, _ , _= sess.run([self.loss,  self.train_op, self.auc_update_op], feed_dict = {
                    self.uid : reviewerId,
                    self.tid : asin,
                    self.y : y,
                    self.hist_i : hist,
                    self.hist_len: hist_len
                })
                loss_sum += loss
                if self.global_step.eval(session=sess) % 1000 == 0:
                    log_data = {'loss' : loss_sum,
                                'global_step': self.global_step.eval(session=sess),
                                'auc' : self.auc.eval(session=sess),
                                'epoch' : epoch}
                    print('Epoch {epoch}, Global step = {global_step}, Loss = {loss}, AUC = {auc}s'.format(**log_data))

                    loss_sum = 0

    def eval(self, sess, data_set, name='eval'):

        loss_sum = 0
        logits_arr = np.array([])
        y_arr = np.array([])

        for _, row in DataInput(data_set, 128000):
            reviewerId, asin, y, hist, hist_len = row
            loss,  logits = sess.run([self.loss, self.logits], feed_dict = {
                self.uid : reviewerId,
                self.tid : asin,
                self.y : y,
                self.hist_i : hist,
                self.hist_len: hist_len
            })
            loss_sum += loss

            logits_arr = np.append(logits_arr, logits)
            y_arr = np.append(y_arr, y)

        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(y_arr, logits_arr)

        log_data = {'name': name,
                    'loss' : loss_sum,
                    'auc' : auc,
                    }
        print('Eval {name} : loss = {loss} auc = {auc}'.format(**log_data))

    def predict(self, **kwargs):
        pass
