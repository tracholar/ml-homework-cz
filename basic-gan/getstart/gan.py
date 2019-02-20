#coding:utf-8

import tensorflow as tf
import random
import matplotlib.pyplot as plt
import numpy as np
import time

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/")

x_train = mnist.train.images[:55000,:]
print x_train.shape

randomNum = random.randint(0,55000)
image = x_train[randomNum].reshape([28,28])
plt.imshow(image, cmap=plt.get_cmap('gray_r'))
plt.show()


def conv2d(x, W):
    ## TODO 实现filter数目为W的conv2d
    raise NotImplementedError()

def avg_pool_2x2(x):
    ## TODO 实现2x2 avg pooling
    raise NotImplementedError()

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
        pass



def generator(z, batch_size, z_dim, reuse=False):
    with tf.variable_scope('generator') as scope:
        if (reuse):
            tf.get_variable_scope().reuse_variables()

        # TODO 完成生成器CNN网络, 利用反卷积增加维度
        # 输出是和MNIST图像相同维度的向量
        # 有用的API
        #   - tf.nn.conv2d_transpose



sess = tf.Session()
z_dimensions = 100
z_test_placeholder = tf.placeholder(tf.float32, [None, z_dimensions])

sample_image = generator(z_test_placeholder, 1, z_dimensions)
test_z = np.random.uniform(-1, 1, [1,z_dimensions])

sess.run(tf.global_variables_initializer())
temp = (sess.run(sample_image, feed_dict={z_test_placeholder: test_z}))

my_i = temp.squeeze()
plt.imshow(my_i, cmap='gray_r')
plt.show()


batch_size = 16
tf.reset_default_graph() #Since we changed our batch size (from 1 to 16), we need to reset our Tensorflow graph

sess = tf.Session()
x_placeholder = tf.placeholder("float", shape = [None,28,28,1]) #Placeholder for input images to the discriminator
z_placeholder = tf.placeholder(tf.float32, [None, z_dimensions]) #Placeholder for input noise vectors to the generator

Dx = discriminator(x_placeholder) #Dx will hold discriminator prediction probabilities for the real MNIST images
Gz = generator(z_placeholder, batch_size, z_dimensions) #Gz holds the generated images
Dg = discriminator(Gz, reuse=True) #Dg will hold discriminator prediction probabilities for generated images

# TODO 定义损失函数
# 有用的API
#   - tf.nn.sigmoid_cross_entropy_with_logits
raise NotImplementedError()


# TODO 定义梯度下降op
# 有用的API
#   - optimizer.minimize(loss, var_list=vars)
raise NotImplementedError()

sess.run(tf.global_variables_initializer())
iterations = 13000
for i in range(iterations):
    z_batch = np.random.uniform(-1, 1, size=[batch_size, z_dimensions])
    real_image_batch = mnist.train.next_batch(batch_size)
    real_image_batch = np.reshape(real_image_batch[0],[batch_size,28,28,1])

    # TODO 执行训练逻辑
    # 有用的API
    #   - sess.run

    if i % 100 == 0:
        print '\r', time.asctime(), 'train', i, 'iters. ',
print ''

sample_image = generator(z_placeholder, 1, z_dimensions, reuse=True)
z_batch = np.random.uniform(-1, 1, size=[1, z_dimensions])
temp = (sess.run(sample_image, feed_dict={z_placeholder: z_batch}))
my_i = temp.squeeze()
plt.imshow(my_i, cmap='gray_r')
plt.show()