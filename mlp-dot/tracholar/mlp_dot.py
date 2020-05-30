# coding:utf-8
from __future__ import print_function
import tensorflow as tf
import numpy as np
import logging
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam, SGD
from keras.losses import mean_squared_error


def gen_data(n_sample=10000, emb_len=10, noise=0.1):
    p = np.random.randn(n_sample, emb_len)
    q = np.random.randn(n_sample, emb_len)
    y = np.sum(p * q, axis=-1) \
        + np.random.randn(n_sample) * noise
    return np.concatenate((p, q), axis=1), y


def main():
    emb_len = 10
    model = Sequential([
        Dense(128, input_dim=emb_len * 2, activation='relu'),
        Dense(128, activation='relu'),
        Dense(1)
    ])
    optimizer = Adam(lr=0.001)
    model.compile(optimizer=optimizer, loss=mean_squared_error, metrics=[])

    X, y = gen_data(n_sample=100000)
    X_, y_ = gen_data()
    model.fit(X, y, epochs=25, batch_size=32, validation_data=(X_, y_))

    X, y = gen_data()
    loss_and_metrics = model.evaluate(X, y, batch_size=128)
    print(loss_and_metrics)


if __name__ == '__main__':
    main()