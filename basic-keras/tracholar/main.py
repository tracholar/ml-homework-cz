#coding:utf-8

import keras
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.datasets import mnist


def build_model():
    """
    创建你的模型,
    :return: Model
    """
    # TODO 定义好你的模型
    return Sequential([

    ])

def gen_dae_data(p = 0.3):
    """
    创建去噪自编码机的数据集,输入时加入噪声的图像数据,输出是没有加噪的图像数据
    p 是加噪的概率
    你需要实现训练集和验证集的划分, mnist.load_data 函数可以直接返回划分好的数据
    :return: (X_noise, X, X_val_noise, X_val)
    """
    raise NotImplementedError()

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
    model.fit(X_noise, X, batch_size=32, epochs=5, verbose=1)

    im_noise = X_val_noise[0, :]
    im = model.predict(im_noise)

    compare_image(im_noise, im)

if __name__ == '__main__':
   train()