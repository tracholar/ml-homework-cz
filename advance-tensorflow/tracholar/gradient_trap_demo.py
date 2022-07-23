# coding:utf-8
import tensorflow as tf

@tf.function(input_signature=[tf.TensorSpec(shape=None, dtype=tf.float32)])
def f(x):
    with tf.GradientTape() as tape:
        tape.watch(x)
        y = x**2 + tf.exp(-x)

    print(tape.watched_variables())
    dx = tape.gradient(y, x)
    return y, dx

x1 = tf.constant(1.0)
x2 = tf.constant([1.0, 2.0])
print(f(x1))
print(f(x2))

print(f.get_concrete_function(x1) is f.get_concrete_function(x2))
print(f.get_concrete_function(x2))


