#coding:utf-8

import tensorflow as tf

class Adabound(tf.train.Optimizer):
    """ Optimizer that implements Adabound algorithm.
    See parer "Adaptive Gradient Methods with Dynamic Bound of Learning Rate" for details.
    Implement refer https://github.com/luochuwei/Custom-Optimizer-in-TensorFlow/blob/master/AMSGrad.py
    """
    def __init__(self, **kwargs):
        pass

    def _create_slots(self, var_list):
        raise NotImplementedError()

    def _prepare(self):
        raise NotImplementedError()

    def _apply_dense(self, grad, var):
        raise NotImplementedError()

    def _apply_sparse(self, grad, var):
        raise NotImplementedError("Sparse gradient updates are not supported yet.")

from keras.optimizers import Optimizer
from keras.legacy import interfaces

class KAdabound(Optimizer):
    """Optimizer that implements Adabound algorithm for Keras.
    """
    def __init__(self, **kwargs):
        pass

    @interfaces.legacy_get_updates_support
    def get_updates(self, loss, params):
        raise NotImplementedError()

    def get_config(self):
        raise NotImplementedError()