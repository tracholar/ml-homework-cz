#coding:utf-8
import pickle
import numpy as np
import pandas as pd
from lr import LR
import tensorflow as tf
import sys


with open('./dataset.sample.pkl', 'rb') as f:
    train_set = pickle.load(f)
    test_set = pickle.load(f)
    cate_list = pickle.load(f)
    user_count, item_count, cate_count = pickle.load(f)


print train_set[:10], test_set[:10], cate_list

def train_input_dataset():
    def _map_fn(data):
        reviewId = data[0]
        hist = data[1]
        asin = data[2]
        label = data[3]
        feat = {
            'reviewId' : reviewId,
            'hist' : hist,
            'asin' : asin
        }
        return feat, label
    def _flat_map_fn(*args):
        return map(_map_fn, train_set)

    return tf.data.Dataset.from_tensor_slices([1]).flat_map(_flat_map_fn).shuffle(1000).batch(128).repeat()

def test_input_dataset():
    def _map_fn(data):
        reviewId = data[0]
        hist = data[1]
        pos, neg = data[2]

        pos_sample = ({
            'reviewId' : reviewId,
            'hist' : hist,
            'asin' : pos
        }, 1)
        neg_sample = ({
                'reviewId' : reviewId,
                'hist' : hist,
                'asin' : neg
            }, 0)
        return [pos_sample, neg_sample]

    return tf.data.Dataset.from_tensor_slices(test_set).flat_map(_map_fn).shuffle(1000).batch(128).repeat()


np.array([(1,np.array([32423,23423]), 324324)])

train_dataset = train_input_dataset()
iter = train_dataset.make_initializable_iterator()
next_element = iter.get_next()

with tf.Session() as sess:
    sess.run(iter.initializer)
    for i in range(10):
        print i, sess.run(next_element)