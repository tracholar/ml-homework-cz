#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
from model import ModelMixin

class WideDeep(ModelMixin):
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

        # cross feature, item cross 单机扛不住, 只能用 cate 做cross
        # item_cross_dim = kwargs['item_count'] ** 2
        cate_cross_dim = kwargs['cate_count'] ** 2
        # print(item_cross_dim, cate_cross_dim)

        # item_cross = self.hist_i * self.tid
        cate_cross = tf.gather(cate_list, self.hist_i) * tf.expand_dims(tf.gather(cate_list, self.tid), 1)
        print(cate_cross)
        # item_cross_emb_w = tf.get_variable("item_cross_emb", shape=[item_cross_dim, 1])
        cate_cross_emb_w = tf.get_variable("cate_cross_emb", shape=[cate_cross_dim, 1])
        cross_out = tf.reduce_sum(tf.nn.embedding_lookup(cate_cross_emb_w, cate_cross), axis=[1, 2]) #  + tf.reduce_sum(tf.nn.embedding_lookup(item_cross_emb_w, item_cross), axis=[1, 2])


        print(mlp_out, cross_out)
        self.logits = mlp_out + cross_out
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels=self.y))
        self.opt = tf.train.AdagradOptimizer(0.1)

        self.global_step = tf.Variable(0, trainable=False, name='grobal_step')
        self.train_op = self.opt.minimize(self.loss, global_step=self.global_step)

        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))



