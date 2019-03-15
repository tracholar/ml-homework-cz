#coding:utf-8

import keras
import matplotlib.pyplot as plt
import numpy as np
from keras import Model
from keras.layers import Input,Dense,Conv2D,MaxPooling2D,UpSampling2D
from keras.models import Sequential
from keras.datasets import mnist


def build_model():
    """
    创建你的模型,
    :return: Model
    """
    # TODO 定义好你的模型

    input_img = Input(shape=(784,))
    encoded = Dense(256, activation='relu')(input_img)
    decoded = Dense(256, activation='relu')(encoded)
    decoded = Dense(784, activation='sigmoid')(decoded)
    autoencoder = Model(input_img, decoded)
    return autoencoder

def build_cnn():
    input_img = Input(shape=(28, 28, 1))

    x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(16, (3, 3), activation='relu')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = Model(input_img, decoded)
    return autoencoder

def gen_dae_data(p = 0.3):
    """
    创建去噪自编码机的数据集,输入时加入噪声的图像数据,输出是没有加噪的图像数据
    p 是加噪的概率
    你需要实现训练集和验证集的划分, mnist.load_data 函数可以直接返回划分好的数据
    :return: (X_noise, X, X_val_noise, X_val)
    """

    (x_train, _), (x_test, _) = mnist.load_data()
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
    x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

    noise_factor = 0.5
    x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
    x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)

    x_train_noisy = np.clip(x_train_noisy, 0., 1.)
    x_test_noisy = np.clip(x_test_noisy, 0., 1.)

    return x_train_noisy,x_train,x_test_noisy,x_test

def compare_image(noise, denoise):
    X  = np.zeros((30, 60))
    X[0:28, 0:28] = noise.reshape((28,28))
    X[0:28, 32:60] = denoise.reshape((28,28))
    plt.figure()
    plt.imshow(X, 'gray')
    plt.title('noise vs de-noise')
    plt.show()

def train(flag='MLP'):

    (X_noise, X, X_val_noise, X_val) = gen_dae_data()
    if flag=='MLP':
        model = build_model()
        X_noise=X_noise.reshape((-1, 784))
        X=X.reshape((-1, 784))
        X_val_noise=X_val_noise.reshape((-1, 784))
        X_val=X_val.reshape((-1, 784))
        im_noise = X_val_noise[0, :].reshape(1, 784)
    else:
        model = build_cnn()
        im_noise = X_val_noise[0, :][np.newaxis,:,:,:]

    model.compile(optimizer='adadelta', loss='binary_crossentropy')

    model.fit(X_noise, X,
                    epochs=3,
                    batch_size=256,
                    shuffle=True,
                    validation_data=(X_val_noise, X_val))
    im = model.predict(im_noise)

    compare_image(im_noise, im)

if __name__ == '__main__':
    import sys
    flag=sys.argv[0]
    train(flag)