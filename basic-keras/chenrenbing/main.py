#coding:utf-8

import keras
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.datasets import mnist

from util import *
from DAE import *

def build_model():
    """
    创建你的模型,
    :return: Model
    """
    # TODO 定义好你的模型
    dae=DAE_CNN(layer_shape=[16,8],filter=[3,2])
    #dae=DAE_NN(layer_shape=[128,64,32])
    return dae

def gen_dae_data(p = 0.3):
    """
    创建去噪自编码机的数据集,输入时加入噪声的图像数据,输出是没有加噪的图像数据
    p 是加噪的概率
    你需要实现训练集和验证集的划分, mnist.load_data 函数可以直接返回划分好的数据
    :return: (X_noise, X, X_val_noise, X_val)
    """
    x_train,x_train_noisy,x_test,x_test_noisy=cnn_input()
    return x_train_noisy,x_train,x_test_noisy,x_test

def compare_image(noise, denoise):
    X  = np.zeros((30, 60))
    X[0:28, 0:28] = noise.reshape((28,28))
    X[0:28, 32:60] = denoise.reshape((28,28))
    plt.figure()
    plt.imshow(X, 'gray')
    plt.title('noise vs de-noise')
    plt.show()

def train():
    (X_noise, X, X_val_noise, X_val) = gen_dae_data()
    model = build_model()
    model.fit(X_noise, X, batch_size=32, epochs=1, verbose=1)

    im_noise = X_val_noise#[0, :]
    im = model.predict(im_noise)
    print(np.shape(im_noise))
    show_image(X_val[0],im_noise[0], im[0])

if __name__ == '__main__':
   train()