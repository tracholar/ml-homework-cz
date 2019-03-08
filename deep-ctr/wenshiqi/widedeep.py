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

        # 特征工程
        embedding_dim = 8
        user_embedding = tf.get_variable(name='user_embedding', shape=[kwargs['user_count'], embedding_dim],
                                         dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())
        item_embedding = tf.get_variable(name='item_embedding', shape=[kwargs['item_count'], embedding_dim],
                                         dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())
        cate_embedding = tf.get_variable(name='cate_embedding', shape=[kwargs['cate_count'], embedding_dim],
                                         dtype=tf.float32,
                                         initializer=tf.random_normal_initializer())

        # 类别列表
        cate_list = tf.convert_to_tensor(kwargs['cate_list'], dtype=tf.int32)

        # 获取embedding向量
        uid_embedding_vec = tf.nn.embedding_lookup(user_embedding, self.uid)
        tid_embedding_vec = tf.nn.embedding_lookup(item_embedding, self.tid)
        tid_cate_embedding_vec = tf.nn.embedding_lookup(cate_embedding, tf.gather(cate_list,self.tid))  # self.tid修改为tf.gather(cate_list, self.tid)
        his_item_embedding_vec = tf.nn.embedding_lookup(item_embedding, self.hist_i)
        his_cate_embedding_vec = tf.nn.embedding_lookup(cate_embedding, tf.gather(cate_list, self.hist_i))

        # 特征列表
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
        feats = tf.concat(feature_list, axis=1)


        # 交叉特征
        cate_cross_dim = kwargs['cate_count'] ** 2
        cate_cross_embedding = tf.get_variable(name='cate_cross_embedding', shape=[cate_cross_dim, 1], dtype=tf.float32,
                                               initializer=tf.random_normal_initializer())
        cate_cross = tf.gather(cate_list, self.hist_i) * tf.expand_dims(tf.gather(cate_list, self.tid), 1)
        cate_cross_vec = tf.nn.embedding_lookup(cate_cross_embedding, cate_cross)

        cross_feat_list = [
            tf.reduce_sum(cate_cross_vec, axis=1),
            tf.reduce_mean(cate_cross_vec, axis=1),
            tf.reduce_max(cate_cross_vec, axis=1),
            tf.reduce_min(cate_cross_vec, axis=1)
        ]
        cross_feats = tf.concat(cross_feat_list,axis=1)



        # wide
        wights = tf.get_variable(name='weights',shape=(np.shape(cross_feats)[1],1),dtype=tf.float32,initializer=tf.random_normal_initializer())
        bias = tf.get_variable(name='bias', shape=[1,],dtype=tf.float32,initializer=tf.random_normal_initializer())
        wide_out = tf.reduce_sum(tf.matmul(cross_feats,wights) + bias,axis=1)

        # deep
        nn_hidden1 = tf.layers.dense(inputs=feats, units=128, activation=tf.nn.relu)
        nn_hidden2 = tf.layers.dense(inputs=nn_hidden1, units=64, activation=tf.nn.relu)
        deep_out = tf.reduce_sum(tf.layers.dense(inputs=nn_hidden2, units=1), axis=1)

        self.logits = wide_out + deep_out
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=self.y, logits= self.logits))
        self.opt = tf.train.AdamOptimizer(0.001)

        self.global_step = tf.Variable(initial_value=0, trainable=False, name='global_step')
        self.train_op = self.opt.minimize(loss=self.loss, global_step=self.global_step)

        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y ,predictions=tf.sigmoid(self.logits))