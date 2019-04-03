#coding:utf-8

import tensorflow as tf
import random
import matplotlib.pyplot as plt
import numpy as np
import time

from gan_data import *


x_train = mnist(flag='conv')


def discriminator(x_image, reuse=False):
    with tf.variable_scope('discriminator') as scope:
        if (reuse):
            tf.get_variable_scope().reuse_variables()

        layer1=tf.layers.conv2d(x_image,kernel_size=(5,5),filters=16,strides=(1,1),padding='same',activation='relu',kernel_initializer=tf.truncated_normal_initializer(stddev=0.1))
        layer2=tf.layers.conv2d(layer1,kernel_size=(3,3),filters=8,strides=(1,1),padding='same',activation='relu',kernel_initializer=tf.truncated_normal_initializer(stddev=0.1))
        layer3=tf.layers.conv2d(layer2,kernel_size=(2,2),filters=4,strides=(1,1),padding='same',activation='relu',kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))

        flat=tf.layers.flatten(layer3)

        full_out=tf.layers.dense(flat,1)

    return full_out



def generator(z, batch_size, z_dim, reuse=False):
    with tf.variable_scope('generator') as scope:
        if (reuse):
            tf.get_variable_scope().reuse_variables()
    z_in=tf.reshape(z,[batch_size,5,5,1])
    layer1=tf.layers.conv2d(z_in,kernel_size=(2,2),filters=16,strides=(1,1),padding='same',activation='relu',kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
    layer2=tf.layers.conv2d(layer1,kernel_size=(2,2),filters=8,strides=(1,1),padding='same',activation='relu',kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
    layer3=tf.layers.conv2d(layer2,kernel_size=(2,2),filters=4,strides=(1,1),padding='same',activation='relu',kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))

    flat=tf.layers.flatten(layer3)

    full_out=tf.layers.dense(flat,784)

    full_out=tf.reshape(full_out,[batch_size,28,28,1])

    return full_out

z_dimensions = 25


batch_size = 32
tf.reset_default_graph() #Since we changed our batch size (from 1 to 16), we need to reset our Tensorflow graph

sess = tf.Session()
x_placeholder = tf.placeholder("float", shape = [None,28,28,1]) #Placeholder for input images to the discriminator
z_placeholder = tf.placeholder(tf.float32, [None, z_dimensions]) #Placeholder for input noise vectors to the generator

Dx = discriminator(x_placeholder) #Dx will hold discriminator prediction probabilities for the real MNIST images
Gz = generator(z_placeholder, batch_size, z_dimensions) #Gz holds the generated images
Dg = discriminator(Gz, reuse=True) #Dg will hold discriminator prediction probabilities for generated images

# 怎么确保更新 discriminator 的时候，不更新 generator.反之，亦然。
g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Dg, labels = tf.ones_like(Dg))) # ensure forward compatibility: function needs to have logits and labels args explicitly used

d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Dx, labels = tf.ones_like(Dx)))
d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Dg, labels = tf.zeros_like(Dg)))
d_loss = d_loss_real + d_loss_fake


opt_d=tf.train.AdamOptimizer(0.001).minimize(d_loss)
opt_g=tf.train.AdamOptimizer(0.001).minimize(g_loss)
sample_image = generator(z_placeholder, 1, z_dimensions, reuse=True)

sess.run(tf.global_variables_initializer())
iterations = 1000
for i in range(iterations):
    # TODO 执行训练逻辑
    z_batch = np.random.uniform(-1, 1, size=[batch_size, z_dimensions])
    x_,y= x_train(batch_size)
    #print(y[0])

    for j in range(3):
        _,D_loss=sess.run([opt_d,d_loss],feed_dict={x_placeholder:x_,z_placeholder:z_batch})
    _,G_loss=sess.run([opt_g,g_loss],feed_dict={x_placeholder:x_,z_placeholder:z_batch})
    #print(" epoch:",i)
    if i % 100 == 0:
        print(time.asctime(), 'train', i, 'iters. dLoss =', D_loss, 'gLoss =', G_loss)
print ''


z_batch = np.random.uniform(-1, 1, size=[1, z_dimensions])
temp = (sess.run(sample_image, feed_dict={z_placeholder: z_batch}))
my_i = temp.squeeze()
plt.imshow(my_i, cmap='gray_r')
plt.show()