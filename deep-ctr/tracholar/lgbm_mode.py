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

LR(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
#print train_set[:10], test_set[:10], cate_list

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


from input import DataInput, DataInputTest



for _, row in DataInput(train_set, 2):
    reviewId, asin, y, hist, hist_len = row
    print reviewId, asin, y, hist, hist_len
    break