#coding:utf-8
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


with open('../dataset.pkl', 'rb') as f:
    train_set = pickle.load(f)
    test_set = pickle.load(f)
    cate_list = pickle.load(f)
    user_count, item_count, cate_count = pickle.load(f)

print train_set[0], test_set[0], cate_list