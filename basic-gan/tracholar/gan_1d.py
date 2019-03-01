#coding:utf-8
"""1D Generative Adversarial Network demo.
z -> x , z ~ rand, x ~ normal distribution
"""
import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt

def unlabeled_data_gen(batch_size=128):
    return np.random.randn(batch_size, 1)
def sigmoid(x):
    return 1/(1+np.exp(-x))

def discriminator(X):
    with tf.variable_scope('discriminator', reuse=tf.AUTO_REUSE) as scope:
        hn = 128
        w1 = tf.get_variable('w1', shape=(1, hn), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1.414))
        b1 = tf.get_variable('b1', shape=(1), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1.414))
        h1 = tf.nn.relu(tf.matmul(X, w1) + b1)

        w2 = tf.get_variable('w2', shape=(hn, 1), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1/np.sqrt(hn)))
        b2 = tf.get_variable('b2', shape=(1), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1/np.sqrt(hn)))
        logits = tf.matmul(h1, w2) + b2
    return logits

def generator(Z):
    with tf.variable_scope('generator', reuse=tf.AUTO_REUSE) as scope:
        hn = 64
        w1 = tf.get_variable('w1', shape=(1, hn), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1.414))
        b1 = tf.get_variable('b1', shape=(1), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1.414))
        h1 = tf.nn.relu(tf.matmul(Z, w1) + b1)

        w2 = tf.get_variable('w2', shape=(hn, 1), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1/np.sqrt(hn)))
        b2 = tf.get_variable('b2', shape=(1), dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=1/np.sqrt(hn)))
        output = tf.matmul(h1, w2) + b2

    return output


sess = tf.Session()
x_placeholder = tf.placeholder(tf.float32, [None, 1])
z_placeholder = tf.placeholder(tf.float32, [None, 1])

Dx = discriminator(x_placeholder)
Gz = generator(z_placeholder)
Dg = discriminator(Gz)

g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dg, labels=tf.ones_like(Dg)))
d_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dx, labels=tf.ones_like(Dx))) + tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dg, labels=tf.zeros_like(Dg)))

tvars = tf.trainable_variables()
d_vars = [v for v in tvars if 'discriminator' in v.name]
g_vars = [v for v in tvars if 'generator' in v.name]

print d_vars
print g_vars

opt = tf.train.GradientDescentOptimizer(0.0001)
d_train = opt.minimize(d_loss, var_list=d_vars)
g_train = opt.minimize(g_loss, var_list=g_vars)

batch_size = 64
sess.run(tf.global_variables_initializer())
for i in range(13000):
    z = np.random.randn(batch_size, 1)
    x = unlabeled_data_gen(batch_size)

    _, dloss = sess.run([d_train, d_loss], feed_dict={x_placeholder:x, z_placeholder: z})
    _, gloss = sess.run([g_train, g_loss], feed_dict={z_placeholder:z})

    if i % 100 == 0:
        print time.asctime(), 'train', i, 'iters. dLoss =', dloss, 'gLoss =', gloss

print

x = unlabeled_data_gen(10000)
z = np.sort(np.random.randn(10000,1), axis=0)
gz, dg = sess.run([Gz, Dg], feed_dict={z_placeholder: z})

fig, ax1 = plt.subplots()
ax1.hist(x.squeeze(), bins=50, alpha=0.7)
ax1.hist(gz.squeeze(), bins=50, alpha=0.7)
ax1.legend(['real', 'generator'])

ax2 = ax1.twinx()
ax2.plot(z.squeeze(), sigmoid(dg.squeeze()), 'r')
plt.ylim([0,1])
#ax2.legend(['D(G(z))'])
plt.show()
