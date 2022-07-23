# coding:utf-8
import tensorflow as tf

x = tf.constant([[2.0, 3.0], [1.0, 4.0]])
targets = tf.constant([[1.], [-1.]])

dense = tf.keras.layers.Dense(1)
dense.build([None, 2])

with tf.autodiff.ForwardAccumulator(
        primals=dense.kernel,
        tangents=tf.constant([[1.], [0.]])
    ) as acc:
    loss = tf.reduce_sum((dense(x) - targets) ** 2)

print(acc.jvp(loss))