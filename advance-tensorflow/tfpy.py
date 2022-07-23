import tensorflow as tf
import numpy as np
def test_fun(x):
    return x * np.sign(x)

x = tf.constant(1.0)
print(tf.py_function(test_fun, inp=[x], Tout=tf.float32))
print(tf.numpy_function(test_fun, inp=[tf.constant([1.0, -4.0])], Tout=tf.float32))