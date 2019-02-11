#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
from model import ModelMixin

class DNN(ModelMixin):
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

        self.logits = tf.reduce_sum(tf.layers.dense(inputs=mlp_hidden, units=1, activation=None), axis=1)
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels=self.y))
        self.opt = tf.train.AdagradOptimizer(0.1)

        self.global_step = tf.Variable(0, trainable=False, name='grobal_step')
        self.train_op = self.opt.minimize(self.loss, global_step=self.global_step)

        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))




