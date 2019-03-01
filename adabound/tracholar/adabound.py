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