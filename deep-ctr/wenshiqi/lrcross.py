# coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
from model import ModelMixin


class LR(ModelMixin):
    def __init__(self, **kwargs):
        self.uid = tf.placeholder(tf.int32, [None, ])
        self.tid = tf.placeholder(tf.int32, [None, ])
        self.y = tf.placeholder(tf.float32, [None, ])
        self.hist_i = tf.placeholder(tf.int32, [None, None])
        self.hist_len = tf.placeholder(tf.int32, [None, ])

        ### 特征工程
        user_embedding = tf.get_variable(name='user_embedding', shape=[kwargs['user_count'], 1], dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())
        item_embedding = tf.get_variable(name='item_embedding', shape=[kwargs['item_count'], 1], dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())
        cate_embedding = tf.get_variable(name='cate_embedding', shape=[kwargs['cate_count'], 1], dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())

        cate_list = tf.convert_to_tensor(kwargs['cate_list'], dtype=tf.int32)

        uid_embedding_vec = tf.nn.embedding_lookup(user_embedding, self.uid)
        tid_embedding_vec = tf.nn.embedding_lookup(item_embedding, self.tid)
        tid_cate_embedding_vec = tf.nn.embedding_lookup(cate_embedding, tf.gather(cate_list, self.tid))
        his_item_embedding_vec = tf.nn.embedding_lookup(item_embedding, self.hist_i)
        his_cate_embedding_vec = tf.nn.embedding_lookup(cate_embedding, tf.gather(cate_list, self.hist_i))

        ## 交叉特征
        # item_cross_dim = kwargs['item_count'] ** 2
        cate_cross_dim = kwargs['cate_count'] ** 2
        # user_item_cross_dim = kwargs['user_count'] * kwargs['item_count']
        user_cate_cross_dim = kwargs['user_count'] * kwargs['cate_count']

        # item_cross_embedding = tf.get_variable(name='item_cross_embedding', shape=[item_cross_dim, 1], dtype=tf.float32,
        #                                       initializer=tf.random_normal_initializer())
        cate_cross_embedding = tf.get_variable(name='cate_cross_embedding', shape=[cate_cross_dim, 1], dtype=tf.float32,
                                               initializer=tf.random_normal_initializer())
        # user_item_cross_embedding = tf.get_variable(name='user_item_cross_embedding', shape=[user_item_cross_dim, 1],
        #                                            dtype=tf.float32, initializer=tf.random_normal_initializer())
        user_cate_cross_embedding = tf.get_variable(name='user_cate_cross_embedding', shape=[user_cate_cross_dim, 1],
                                                    dtype=tf.float32, initializer=tf.random_normal_initializer())

        # item_cross = self.hist_i * self.tid
        # cate_cross = tf.squeeze(tf.gather(cate_list, self.hist_i)) * tf.gather(cate_list, self.tid) 不能使用squeeze，因为如果hist_i只有1个也会被消除
        cate_cross = tf.gather(cate_list, self.hist_i) * tf.expand_dims(tf.gather(cate_list, self.tid), 1)
        # print(cate_cross.get_shape()[0])
        # user_item_cross = self.uid * self.tid
        user_cate_cross = self.uid * tf.gather(cate_list, self.tid)
        # item_cross_vec = tf.nn.embedding_lookup(item_cross_embedding, item_cross)
        cate_cross_vec = tf.nn.embedding_lookup(cate_cross_embedding, cate_cross)
        # user_item_cross_vec = tf.nn.embedding_lookup(user_item_cross_embedding, user_item_cross)
        user_cate_cross_vec = tf.nn.embedding_lookup(user_cate_cross_embedding, user_cate_cross)

        # 特征列表
        feature_list = [
            uid_embedding_vec,
            tid_embedding_vec,
            tid_cate_embedding_vec,
            # item_cross_vec,
            # user_item_cross_vec,
            # user_cate_cross_vec,

            tf.reduce_sum(cate_cross_vec, axis=1),
            tf.reduce_mean(cate_cross_vec, axis=1),
            tf.reduce_min(cate_cross_vec, axis=1),
            tf.reduce_max(cate_cross_vec, axis=1),

            tf.reduce_mean(his_item_embedding_vec, axis=1),
            tf.reduce_max(his_item_embedding_vec, axis=1),
            tf.reduce_min(his_item_embedding_vec, axis=1),
            tf.reduce_sum(his_item_embedding_vec, axis=1),

            tf.reduce_mean(his_cate_embedding_vec, axis=1),
            tf.reduce_max(his_cate_embedding_vec, axis=1),
            tf.reduce_min(his_cate_embedding_vec, axis=1),
            tf.reduce_sum(his_cate_embedding_vec, axis=1)
        ]

        feats = tf.concat(feature_list, axis=1)

        weights = tf.get_variable(name='weights', shape=(feats.get_shape()[1], 1), dtype=tf.float32,
                                  initializer=tf.random_normal_initializer())
        bias = tf.get_variable(name='bias', shape=[1, ], dtype=tf.float32, initializer=tf.zeros_initializer())
        self.logits = tf.squeeze(tf.matmul(feats, weights) + bias)
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels=self.y))
        self.opt = tf.train.AdamOptimizer(0.001)

        self.global_step = tf.Variable(initial_value=0, trainable=False, name='global_step')
        self.train_op = self.opt.minimize(self.loss, global_step=self.global_step)

        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))
