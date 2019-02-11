#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
from model import ModelMixin

class LR(ModelMixin):
    def __init__(self, **kwargs):
        self.uid = tf.placeholder(tf.int32, [None, ])
        self.tid = tf.placeholder(tf.int32, [None, ])
        self.y = tf.placeholder(tf.float32, [None,])
        self.hist_i = tf.placeholder(tf.int32, [None, None])
        self.hist_len = tf.placeholder(tf.int32, [None, ])

        ## TODO 创建计算图
        # 可能有用的函数:
        #   - tf.get_variable
        #   - tf.convert_to_tensor
        #   - tf.nn.embedding_lookup
        #   - tf.gather
        #   - tf.concat
        #   - tf.layers.dense
        #   - tf.expand_dims
        #   - tf.nn.sigmoid_cross_entropy_with_logits
        #   - tf.metrics.auc
        #   - tf.nn.sigmoid
        #

        self.logits = None
        self.loss = None

        self.global_step = None
        self.train_op = None

        self.auc, self.auc_update_op = None

        raise NotImplementedError()