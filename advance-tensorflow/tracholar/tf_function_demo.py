# coding:utf-8
# analysis `tf.function`
import tensorflow as tf
import tensorflow.python.framework.ops as ops
from math import exp
import numpy as np


@tf.function
def f(x):
    g = ops.get_default_graph()
    print('graph in f:',g)
    return x ** 2 + tf.exp(x)

g0 = ops.get_default_graph()
print(g0.as_graph_def())
print(f(4.))
print(type(f))
print(type(f.get_concrete_function(1.)))
print(f.get_concrete_function(1.).graph)

g1 = ops.get_default_graph()
g = f.get_concrete_function(1.).graph
assert g0 == g.outer_graph
print('default graph:', g0)
print('function graph:', g)
# assert g1 == g
print(g0.as_graph_def())
print('g1:', g1.as_graph_def())
print('outputs', g.outputs)
print('inputs', g.inputs)
print(g.name)
print(g.as_graph_def())
print(g.get_operations())
print(g.get_all_collection_keys())

for op in g.get_operations():
    print(op.name, type(op))
    print()


logdir = './log/tf_function_demo'
writer = tf.summary.create_file_writer(logdir)
tf.summary.trace_on(graph=True)

for epoch, x in enumerate(np.linspace(0, 10, 100)):
    r = f(x)

    with writer.as_default():
        tf.summary.scalar('x', x, step=epoch)
        tf.summary.scalar('y', r.numpy(), step=epoch)

with writer.as_default():
    tf.summary.trace_export('my_def_function', step=0)
