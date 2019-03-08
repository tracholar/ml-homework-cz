#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
from model import ModelMixin

class DeepFM(ModelMixin):
    def __init__(self, **kwargs):
        self.uid = tf.placeholder(tf.int32, [None, ])
        self.tid = tf.placeholder(tf.int32, [None, ])
        self.y = tf.placeholder(tf.float32, [None,])
        self.hist_i = tf.placeholder(tf.int32, [None, None])
        self.hist_len = tf.placeholder(tf.int32, [None, ])

        # 类别列表
        cate_list = tf.convert_to_tensor(kwargs['cate_list'], dtype=tf.int32)

        # FM部分
        ## 一次项权重
        fm_user_1dim_weights = tf.get_variable(name='fm_user_1dim_weights', shape=[kwargs['user_count'], 1],
                                               dtype=tf.float32, initializer=tf.random_normal_initializer())
        fm_item_1dim_weights = tf.get_variable(name='fm_item_1dim_weights', shape=[kwargs['item_count'], 1],
                                               dtype=tf.float32, initializer=tf.random_normal_initializer())
        fm_cate_1dim_weights = tf.get_variable(name='fm_cate_1dim_weights', shape=[kwargs['cate_count'], 1],
                                               dtype=tf.float32, initializer=tf.random_normal_initializer())
        cate_cross_dim = kwargs['cate_count'] ** 2
        fm_cate_cross_1dim_weights = tf.get_variable(name='fm_cate_cross_1dim_weights', shape=[cate_cross_dim, 1],
                                               dtype=tf.float32, initializer=tf.random_normal_initializer())
        cate_cross = tf.gather(cate_list, self.hist_i) * tf.expand_dims(tf.gather(cate_list, self.tid), 1)

        fm_user_1dim_vec = tf.nn.embedding_lookup(fm_user_1dim_weights, self.uid)
        fm_item_1dim_vec = tf.nn.embedding_lookup(fm_item_1dim_weights, self.tid)
        fm_item_cate_1dim_vec = tf.nn.embedding_lookup(fm_cate_1dim_weights, tf.gather(cate_list, self.tid))
        fm_his_item_1dim_vec = tf.nn.embedding_lookup(fm_item_1dim_weights, self.hist_i)
        fm_his_cate_1dim_vec = tf.nn.embedding_lookup(fm_cate_1dim_weights, tf.gather(cate_list, self.hist_i))
        fm_cate_cross_idim_vec = tf.nn.embedding_lookup(fm_cate_cross_1dim_weights, cate_cross)

        fm_1dim_vecs = [
            fm_user_1dim_vec,
            fm_item_1dim_vec,
            fm_item_cate_1dim_vec,
            tf.reduce_sum(fm_his_item_1dim_vec, axis=1),
            tf.reduce_sum(fm_his_cate_1dim_vec, axis=1),
            tf.reduce_sum(fm_cate_cross_idim_vec, axis=1)
        ]
        fm_1dim_vec = tf.concat(fm_1dim_vecs,axis=1)
        fm_1dim_out = tf.reduce_sum(fm_1dim_vec, axis=1) # fm1次项部分输出

        ## 交叉项权重 -- nn和fm交叉项共享embedding
        embedding_dim = 16
        user_embedding = tf.get_variable(name='user_embedding', shape=[kwargs['user_count'], embedding_dim], dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())
        item_embedding = tf.get_variable(name='item_embedding', shape=[kwargs['item_count'], embedding_dim], dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())
        cate_embedding = tf.get_variable(name='cate_embedding', shape=[kwargs['cate_count'], embedding_dim], dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())

        uid_embedding_vec = tf.nn.embedding_lookup(user_embedding, self.uid)
        tid_embedding_vec = tf.nn.embedding_lookup(item_embedding, self.tid)
        tid_cate_embedding_vec = tf.nn.embedding_lookup(cate_embedding, tf.gather(cate_list, self.tid))
        his_item_embedding_vec = tf.nn.embedding_lookup(item_embedding, self.hist_i)
        his_cate_embedding_vec = tf.nn.embedding_lookup(cate_embedding, tf.gather(cate_list, self.hist_i))

        feature_list = [
            uid_embedding_vec,
            tid_embedding_vec,
            tid_cate_embedding_vec,
            tf.reduce_mean(his_item_embedding_vec, axis=1),
            tf.reduce_max(his_item_embedding_vec, axis=1),
            tf.reduce_min(his_item_embedding_vec, axis=1),
            tf.reduce_sum(his_item_embedding_vec, axis=1),
            tf.reduce_mean(his_cate_embedding_vec, axis=1),
            tf.reduce_max(his_cate_embedding_vec, axis=1),
            tf.reduce_min(his_cate_embedding_vec, axis=1),
            tf.reduce_sum(his_cate_embedding_vec, axis=1)
        ]

        fm_2dim_vec =0
        for i in range(np.shape(feature_list)[0]):
            for j in range(i+1,np.shape(feature_list)[0]):
                fm_2dim_vec += feature_list[i] * feature_list[j]
        fm_2dim_out = tf.reduce_sum(fm_2dim_vec, axis=1)

        fm_out = fm_1dim_out +fm_2dim_out

        # NN部分
        feats = tf.concat(feature_list, axis=1)
        # 3层的nn,神经元个数分别为：[128,64,1]
        nn_hidden1 = tf.layers.dense(inputs=feats, units=128, activation=tf.nn.relu)
        nn_hidden2 = tf.layers.dense(inputs=nn_hidden1, units=64, activation=tf.nn.relu)
        nn_output = tf.reduce_sum(tf.layers.dense(inputs=nn_hidden2, units=1), axis=1)

        self.logits = fm_out + nn_output
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=self.y, logits=self.logits))
        self.opt = tf.train.AdamOptimizer(0.001)

        self.global_step = tf.Variable(initial_value=0, trainable=False, name='global_step')
        self.train_op = self.opt.minimize(self.loss, global_step=self.global_step)

        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))






