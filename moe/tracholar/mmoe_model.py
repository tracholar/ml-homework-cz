#coding:utf-8
import numpy as np
import tensorflow as tf

d = 10
x = tf.placeholder(dtype=tf.float32, shape=(None, d))
y1 = tf.placeholder(dtype=tf.float32, shape=(None, ))
y2 = tf.placeholder(dtype=tf.float32, shape=(None, ))

expr1 = tf.layers.dense(x, 16, tf.nn.relu)
expr2 = tf.layers.dense(x, 16, tf.nn.relu)

weight1 = tf.layers.dense(x, 2, tf.nn.softmax)
weight2 = tf.layers.dense(x, 2, tf.nn.softmax)

print weight1,weight2
z1 = tf.gather(weight1, [None,0]) * expr1 + tf.gather(weight1, [None,0]) * expr2
z2 = tf.gather(weight2, [None,0]) * expr1 + tf.gather(weight2, [None,0]) * expr2

y1_ = tf.layers.dense(z1, 1)
y2_ = tf.layers.dense(z2, 1)

loss = tf.losses.mean_squared_error(y1, y1_) + tf.losses.mean_squared_error(y2, y2_)

optimizer = tf.train.AdamOptimizer()
train = optimizer.minimize(loss)

sess = tf.Session()

from datagen import sample_data

dx, dy1, dy2 = sample_data(d, 10000)
for i in range(100):
    _, l = sess.run([train, loss], feed_dict={
        x: dx,
        y1: dy1,
        y2: dy2
    })
    print l

