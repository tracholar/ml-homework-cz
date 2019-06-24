#codin:utf-8

from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

prefix="./data"
class mnist():
    def __init__(self, flag='conv', is_tanh = False):
        datapath = prefix + 'mnist'
        self.X_dim = 784 # for mlp
        self.z_dim = 100
        self.y_dim = 10
        self.size = 28 # for conv
        self.channel = 1 # for conv
        self.data = input_data.read_data_sets(datapath, one_hot=True)
        self.flag = flag
        self.is_tanh = is_tanh

    def __call__(self,batch_size):
        batch_imgs,y = self.data.train.next_batch(batch_size)
        if self.flag == 'conv':
            batch_imgs = np.reshape(batch_imgs, (batch_size, self.size, self.size, self.channel))

        if self.is_tanh:
            batch_imgs = batch_imgs*2 - 1
        return batch_imgs, y
