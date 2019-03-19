#coding:utf-8

"""Reproduce MNIST experiment
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/")


tf.Variable