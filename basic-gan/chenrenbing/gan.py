#coding:utf-8

import tensorflow as tf
import random
import matplotlib.pyplot as plt
import numpy as np
import time
import tensorflow.contrib.layers as tf_cl
import tensorflow.layers as tf_layers
from gan_data import *


x_train = mnist(flag='conv')


"""
randomNum = random.randint(0,55000)
image = x_train[randomNum].reshape([28,28])
plt.imshow(image, cmap=plt.get_cmap('gray_r'))
plt.show()
"""

def conv2d(x, W):
    ## TODO 实现filter数目为W的conv2d
    return   tf.nn.conv2d(input=x,filter=W,strides=[1,1,1,1],padding='SAME')


def avg_pool_2x2(x):
    ## TODO 实现2x2 avg pooling
    return tf.nn.avg_pool(value=x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def discriminator(x_image, reuse=False):
    with tf.variable_scope('discriminator') as scope:
        if (reuse):
            tf.get_variable_scope().reuse_variables()
        # TODO 实现判别器CNN网络
        # 输出是未经过sigmoid的score
        # 有用的API:
        #   - tf.reshape
        #   - tf.matmul
        #
        # x_image [batch_size,28,28,1]
        conv1_w=tf.get_variable("d_conv1_w",shape=[3,3,1,16],initializer=tf.random_normal_initializer(stddev=0.02))
        conv1_b=tf.get_variable("d_conv1_b",shape=[16],initializer=tf.random_normal_initializer(stddev=0.02))
        conv1_out=tf.nn.relu(conv2d(x_image,conv1_w)+conv1_b)
        # conv1_out [batch,28,28,16]

        conv2_w=tf.get_variable("d_conv2_w",shape=[2,2,16,8],initializer=tf.random_normal_initializer(stddev=0.02))
        conv2_b=tf.get_variable("d_conv2_b",shape=[8],initializer=tf.random_normal_initializer(stddev=0.02))
        conv2_out=tf.nn.relu(conv2d(conv1_out,conv2_w)+conv2_b)
        # conv2_out [batch,28,28,8]

        conv3_w=tf.get_variable("d_conv3_w",shape=[3,3,8,4],initializer=tf.random_normal_initializer(stddev=0.02))
        conv3_b=tf.get_variable("d_conv3_b",shape=[4],initializer=tf.random_normal_initializer(stddev=0.02))
        conv3_out=tf.nn.relu(conv2d(conv2_out,conv3_w)+conv3_b)
        # conv3_out [batch,28,28,4]

        flat_out=tf.layers.flatten(conv3_out)#  [batch,28*28*4]

        full_out=tf.layers.dense(flat_out,1,activation='relu')

    return full_out



def generator(z, batch_size, z_dim, reuse=False):
    with tf.variable_scope('generator') as scope:
        if (reuse):
            tf.get_variable_scope().reuse_variables()

        # TODO 完成生成器CNN网络, 利用反卷积增加维度
        # 输出是和MNIST图像相同维度的向量
        # 有用的API
        #   - tf.nn.conv2d_transpose
        z_in=tf.reshape(z,[batch_size,10,10,1])

        conv1_w=tf.get_variable("g_conv1_w",shape=[3,3,1,16],initializer=tf.random_normal_initializer(stddev=0.02))
        conv1_b=tf.get_variable("g_conv1_b",shape=[16],initializer=tf.random_normal_initializer(stddev=0.02))
        conv1_out=tf.nn.relu(conv2d(z_in,conv1_w)+conv1_b)
        # conv1_out [batch,5,5,16]
        #print(tf.shape(conv1_out))
        conv2_w=tf.get_variable("g_conv2_w",shape=[2,2,16,8],initializer=tf.random_normal_initializer(stddev=0.02))
        conv2_b=tf.get_variable("g_conv2_b",shape=[8],initializer=tf.random_normal_initializer(stddev=0.02))
        conv2_out=tf.nn.relu(conv2d(conv1_out,conv2_w)+conv2_b)
        # conv2_out [batch,5,5,8]

        conv3_w=tf.get_variable("g_conv3_w",shape=[3,3,8,4],initializer=tf.random_normal_initializer(stddev=0.02))
        conv3_b=tf.get_variable("g_conv3_b",shape=[4],initializer=tf.random_normal_initializer(stddev=0.02))
        conv3_out=tf.nn.relu(conv2d(conv2_out,conv3_w)+conv3_b)
        # conv3_out [batch,5,5,4]

        flat_out=tf.layers.flatten(conv3_out)#  [batch,5*5*4]

        full_out=tf.layers.dense(flat_out,784,activation='relu')
        full_out=tf.reshape(full_out,[batch_size,28,28,1])
    return full_out

z_dimensions = 100
"""
sess = tf.Session()

z_test_placeholder = tf.placeholder(tf.float32, [None, z_dimensions])

sample_image = generator(z_test_placeholder, 1, z_dimensions)
test_z = np.random.uniform(-1, 1, [1,z_dimensions])

sess.run(tf.global_variables_initializer())
temp = (sess.run(sample_image, feed_dict={z_test_placeholder: test_z}))

my_i = temp.squeeze()
plt.imshow(np.reshape(my_i,[28,28]), cmap='gray_r')
plt.show()


   上面的是test数据
"""

batch_size = 16
tf.reset_default_graph() #Since we changed our batch size (from 1 to 16), we need to reset our Tensorflow graph

sess = tf.Session()
x_placeholder = tf.placeholder("float", shape = [None,28,28,1]) #Placeholder for input images to the discriminator
z_placeholder = tf.placeholder(tf.float32, [None, z_dimensions]) #Placeholder for input noise vectors to the generator

Dx = discriminator(x_placeholder) #Dx will hold discriminator prediction probabilities for the real MNIST images
Gz = generator(z_placeholder, batch_size, z_dimensions) #Gz holds the generated images
Dg = discriminator(Gz, reuse=True) #Dg will hold discriminator prediction probabilities for generated images
"""
# TODO 定义损失函数

D_loss=tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.ones_like(Dx),logits=Dx))
G_loss=tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.zeros_like(Dg),logits=Dg))
D_G_loss=D_loss+G_loss

# TODO 定义梯度下降op

opt_d=tf.train.AdamOptimizer(0.001).minimize(D_loss)
opt_g=tf.train.AdamOptimizer(0.001).minimize(G_loss)
"""
g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Dg, labels = tf.ones_like(Dg))) # ensure forward compatibility: function needs to have logits and labels args explicitly used

d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Dx, labels = tf.ones_like(Dx)))
d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = Dg, labels = tf.zeros_like(Dg)))
d_loss = d_loss_real + d_loss_fake

tvars = tf.trainable_variables()
d_vars = [var for var in tvars if 'd_' in var.name]
g_vars = [var for var in tvars if 'g_' in var.name]

adam = tf.train.AdamOptimizer()
opt_d = adam.minimize(d_loss, var_list=d_vars)
opt_g = adam.minimize(g_loss, var_list=g_vars)


sess.run(tf.global_variables_initializer())
iterations = 3000
for i in range(iterations):
    # TODO 执行训练逻辑
    z_batch = np.random.uniform(-1, 1, size=[batch_size, z_dimensions])
    x_,y= x_train(batch_size)
    #print(y[0])

    #for j in range(5):
    _,D_loss=sess.run([opt_d,d_loss],feed_dict={x_placeholder:x_,z_placeholder:z_batch})
    _,G_loss=sess.run([opt_g,g_loss],feed_dict={x_placeholder:x_,z_placeholder:z_batch})
    #print(" epoch:",i)
    if i % 100 == 0:
        print(time.asctime(), 'train', i, 'iters. dLoss =', D_loss, 'gLoss =', G_loss)
print ''

sample_image = generator(z_placeholder, 1, z_dimensions, reuse=True)
z_batch = np.random.uniform(-1, 1, size=[1, z_dimensions])
temp = (sess.run(sample_image, feed_dict={z_placeholder: z_batch}))
my_i = temp.squeeze()
plt.imshow(my_i, cmap='gray_r')
plt.show()