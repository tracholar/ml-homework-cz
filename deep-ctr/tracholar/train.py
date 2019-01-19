#coding:utf-8
import pickle
import numpy as np
import pandas as pd
from lr import LR
import tensorflow as tf
import sys


with open('../dataset.pkl', 'rb') as f:
    train_set = pickle.load(f)
    test_set = pickle.load(f)
    cate_list = pickle.load(f)
    user_count, item_count, cate_count = pickle.load(f)

from widedeep import WideDeep
model = WideDeep(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)

with tf.Session() as sess:
    ## 初始化
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    model.fit(sess, train_set)
    model.eval(sess, train_set, name='train')
    model.eval(sess, test_set, name='test')