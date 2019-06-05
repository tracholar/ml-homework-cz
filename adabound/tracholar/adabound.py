#coding:utf-8

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import math_ops, state_ops, control_flow_ops

class Adabound(tf.train.Optimizer):
    """ Optimizer that implements Adabound algorithm.
    See parer "Adaptive Gradient Methods with Dynamic Bound of Learning Rate" for details.
    Implement refer https://github.com/luochuwei/Custom-Optimizer-in-TensorFlow/blob/master/AMSGrad.py
    """
    def __init__(self, learning_rate=0.001, final_lr=0.1, beta1 = 0.9, beta2 = 0.99,
                 gamma=1e-3, epsilon=1e-8,
                 use_locking=False, name="Adabound", **kwargs):
        super(Adabound, self).__init__(use_locking=use_locking, name=name)

        self._lr = learning_rate
        self._final_lr = final_lr
        self._beta1 = beta1
        self._beta2 = beta2
        self._gamma = gamma
        self._epsilon = epsilon

    def _create_slots(self, var_list):
        # 一阶矩和二阶矩
        for v in var_list:
            self._zeros_slot(v, "m", self._name)
            self._zeros_slot(v, "v", self._name)

    def _prepare(self):
        self._lr_t = ops.convert_to_tensor(self._lr)
        self._final_lr_t = ops.convert_to_tensor(self._final_lr)
        self._beta1_t = ops.convert_to_tensor(self._beta1)
        self._beta2_t = ops.convert_to_tensor(self._beta2)
        self._epsilon_t = ops.convert_to_tensor(self._epsilon)
        self._gamma_t = ops.convert_to_tensor(self._gamma)

    def _apply_dense(self, grad, var):
        beta1 = math_ops.cast(self._beta1_t, var.dtype.base_dtype)
        beta2 = math_ops.cast(self._beta2_t, var.dtype.base_dtype)
        lr = math_ops.cast(self._lr_t, var.dtype.base_dtype)
        epsilon = math_ops.cast(self._epsilon_t, var.dtype.base_dtype)

        m = self.get_slot(var, "m")
        m_g = grad * (1 - beta1)
        m_t = state_ops.assign(m, beta1 * m + m_g, use_locking=self._use_locking)

        v = self.get_slot(var, "v")
        v_g = grad * grad * (1 - beta2)
        v_t = state_ops.assign(v, beta2 * v + v_g, use_locking=self._use_locking)
        v_sqrt = math_ops.sqrt(v_t)

        var_update = state_ops.assign(var, lr / (v_sqrt + epsilon) * m_t, use_locking=self._use_locking)

        return control_flow_ops.group(*[var_update, m_t, v_t])



    def _apply_sparse(self, grad, var):
        raise NotImplementedError("Sparse gradient updates are not supported yet.")

from keras.optimizers import Optimizer
from keras.legacy import interfaces
from keras.backend import backend as K

class KAdabound(Optimizer):
    """Optimizer that implements Adabound algorithm for Keras.
    """
    def __init__(self, lr=1e-3, betas=(0.9, 0.999), final_lr=0.1, gamma=1e-3,
                 eps=1e-8, weight_decay=0, **kwargs):
        super(KAdabound, self).__init__(**kwargs)

        self.lr = lr
        self.beta1 = betas[0]
        self.beta2 = betas[1]
        self.final_lr = final_lr
        self.gamma = gamma
        self.eps = eps
        self.weight_decay = weight_decay

    @interfaces.legacy_get_updates_support
    def get_updates(self, loss, params):
        grads = self.get_gradients(loss, params)
        self.updates = [K.update_add(self.iterations, 1)]
        lr = self.lr

        for p, g in zip(params, grads):
            new_p = p - lr * g

            self.updates.append(K.update(p, new_p))
        return self.updates

    def get_config(self):
        conf = { 'lr' : self.lr,
                 'betas' : (self.beta1, self.beta2)
        }
        base_config = super(KAdabound, self).get_config()
        return dict(list(base_config.items()) + list(conf.items()))