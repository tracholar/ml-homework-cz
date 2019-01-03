#coding:utf-8

import pickle
import tensorflow as tf


with open('../dataset.pkl', 'rb') as f:
    train_set = pickle.load(f)
    test_set = pickle.load(f)
    cate_list = pickle.load(f)
    user_count, item_count, cate_count = pickle.load(f)


uid = tf.placeholder(tf.int32, [None, ])
hist = tf.placeholder(tf.int32, [None, None])
tid  = tf.placeholder(tf.int32, [None, ])
y  =  tf.placeholder(tf.float32, [None, ])

## 转成Tensor, cate_list 是一个map,key是商品id,value是cate id
cate_list = tf.convert_to_tensor(cate_list, dtype=tf.int64)

hist_cat = tf.gather(cate_list, hist)


## 模型参数, embedding 矩阵
hidden_units = 16
user_emb_w = tf.get_variable("user_emb_w", [user_count, hidden_units])
item_emb_w = tf.get_variable("item_emb_w", [item_count, hidden_units ])
item_b = tf.get_variable("item_b", [item_count],
                         initializer=tf.constant_initializer(0.0))
cate_emb_w = tf.get_variable("cate_emb_w", [cate_count, hidden_units ])

## 计算 logit
u_emb = tf.nn.embedding_lookup(user_emb_w, uid)
hist_item_emb = tf.nn.embedding_lookup(item_emb_w, hist)
hist_cat_emb = tf.nn.embedding_lookup(cate_emb_w, hist_cat)
item_emb = tf.nn.embedding_lookup(item_emb_w, tid)  ## hist 和 item 使用相同的参数
item_bv = tf.gather(item_b, tid)

s1 = tf.reduce_sum(u_emb * item_emb, axis=-1)
s2 = tf.reduce_sum(hist_item_emb * item_emb, )
print logit

