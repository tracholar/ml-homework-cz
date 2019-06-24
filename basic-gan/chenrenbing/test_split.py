#coding:utf-8

import  tensorflow as tf
import numpy as np

x=tf.random.normal(shape=[10,20,5])

t=tf.split(x,5*[1],2)
t1=tf.transpose(t)
t2=tf.matmul(t,t,transpose_b=True)
t3=tf.reduce_sum(x,2,keep_dims=False)
#t3=tf.matmul(t1,t2)

with tf.Session() as sess:
     x,t,t1,t3=sess.run([x,t,t1,t3])
     print(np.shape(x))
     print(np.shape(t))
     print(np.shape(t1))
     print(np.shape(t2))

     print(np.shape(t3))
