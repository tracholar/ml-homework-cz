#coding:utf-8
"""孪生网络
"""
from __future__ import print_function
import tensorflow as tf
import numpy as np
from omniglot_loader import OmniglotLoader
import sys

dataset_path = sys.argv[1]

omniglot_loader = OmniglotLoader(
    dataset_path=dataset_path, use_augmentation=True, batch_size=32)
omniglot_loader.split_train_datasets()

images, labels = omniglot_loader.get_train_batch()

print([i.shape for i in images], labels.shape)

images, labels = omniglot_loader.get_one_shot_batch(32, False)

print([i.shape for i in images], labels.shape)

from keras.models import Sequential, Model
from keras.layers import Conv2D, Dense, MaxPool2D, GlobalAveragePooling2D, BatchNormalization, Activation, Input, Lambda
from keras.regularizers import l2
from keras.optimizers import Adam
import keras.backend as K


input_shape = (105, 105, 1)
model = Sequential([
    Conv2D(16, (5,5), input_shape=input_shape, kernel_regularizer=l2(1e-2), name='conv1'),
    BatchNormalization(),
    Activation('relu'),
    MaxPool2D((2, 2)),
    Conv2D(32, (5,5), kernel_regularizer=l2(1e-2), name='conv2'),
    BatchNormalization(),
    Activation('relu'),
    MaxPool2D((2, 2)),
    Conv2D(64, (5,5), kernel_regularizer=l2(1e-2), name='conv3'),
    GlobalAveragePooling2D(),
    Dense(units=128, activation='tanh', kernel_regularizer=l2(1e-2), name='dense1')
])

input1 = Input(input_shape)
input2 = Input(input_shape)
emb1 = model(input1)
emb2 = model(input2)

l1_distance_layer = Lambda(lambda ts : K.abs(ts[0] - ts[1]))
l1_distance = l1_distance_layer([emb1, emb2])

pred = Dense(1, activation='sigmoid')(l1_distance)

m = Model([input1, input2], pred)
optimizer = Adam(lr=1e-3)

m.compile(loss='binary_crossentropy', metrics=['binary_accuracy'], optimizer=optimizer)

for it in range(1000):
    images, labels = omniglot_loader.get_train_batch()
    train_loss, acc = m.train_on_batch(images, labels)

    print('\r[{}]train loss: {}, acc: {}'.format(it, train_loss, acc), end='')
    if (it + 1) % 100 == 0:
        val_acc = omniglot_loader.one_shot_test(m, 2, 64, False)
        print('train loss: {0}, acc: {1}, val acc: {2}'.format(train_loss, acc, val_acc))

