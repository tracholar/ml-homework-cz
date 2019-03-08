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
    with tf.variable_scope('discriminator', reuse=tf.AUTO_REUSE):
        hn = 32
        h1 = tf.layers.dense(X,
                             units=hn,
                             kernel_initializer=tf.truncated_normal_initializer(stddev=1.414),
                             activation=tf.nn.relu,
                             kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001))
        h2 = tf.layers.dense(h1,
                             units=hn,
                             kernel_initializer=tf.truncated_normal_initializer(stddev=1/np.sqrt(hn/2)),
                             activation=tf.nn.relu,
                             kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001))
        logits = tf.layers.dense(h2,
                                 units=1,
                                 kernel_initializer=tf.truncated_normal_initializer(stddev=1./np.sqrt(hn/2)),
                                 kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001))
    return logits, h1, h2

def generator(Z):
    with tf.variable_scope('generator', reuse=tf.AUTO_REUSE):
        hn = 32
        h1 = tf.layers.dense(Z,
                             units=hn,
                             kernel_initializer=tf.truncated_normal_initializer(stddev=1.414),
                             activation=tf.nn.relu,
                             kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001))
        h2 = tf.layers.dense(h1,
                             units=hn,
                             kernel_initializer=tf.truncated_normal_initializer(stddev=1/np.sqrt(hn/2)),
                             activation=tf.nn.relu,
                             kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001))
        output = tf.layers.dense(h2,
                                 units=1,
                                 kernel_initializer=tf.truncated_normal_initializer(stddev=1./np.sqrt(hn/2)),
                                 kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001))
    return output
sess = tf.Session()
x_placeholder = tf.placeholder(tf.float32, [None, 1])
z_placeholder = tf.placeholder(tf.float32, [None, 1])

Dx, hx1, hx2 = discriminator(x_placeholder)
Gz = generator(z_placeholder)
Dg, hg1, hg2 = discriminator(Gz)

tf.summary.scalar('dh1_var', tf.reduce_mean(hx1**2))
tf.summary.scalar('gh1_var', tf.reduce_mean(hg1**2))
tf.summary.histogram('dh1_hist', hx1)

fm_loss = tf.reduce_mean((hx1 - hg1)**2) + tf.reduce_mean((hx2 - hg2)**2)
g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dg, labels=tf.ones_like(Dg))) + tf.reduce_sum(tf.losses.get_regularization_losses(scope='generator')) + 0*fm_loss
d_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dx, labels=tf.ones_like(Dx))) + tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dg, labels=tf.zeros_like(Dg))) + tf.reduce_sum(tf.losses.get_regularization_losses(scope='discriminator'))

tvars = tf.trainable_variables()
d_vars = [v for v in tvars if 'discriminator' in v.name]
g_vars = [v for v in tvars if 'generator' in v.name]

print d_vars
print g_vars

opt = tf.train.GradientDescentOptimizer(0.001)
d_train = opt.minimize(d_loss, var_list=d_vars)
g_train = opt.minimize(g_loss, var_list=g_vars)


def eval_gan(iter, show=False):
    x = unlabeled_data_gen(10000)
    z = np.random.rand(10000,1)
    gz, dx = sess.run([Gz, Dx], feed_dict={x_placeholder:x, z_placeholder: z})

    fig, ax1 = plt.subplots()
    ax1.hist(x.squeeze(), bins=50, alpha=0.7)
    ax1.hist(gz.squeeze(), bins=50, alpha=0.7)
    ax1.legend(['real', 'generator'])

    ax2 = ax1.twinx()
    px, py = zip(*sorted(zip(x.squeeze(), sigmoid(dx.squeeze())), key=lambda x:x[0]))
    ax2.plot(px, py, 'r')
    plt.ylim([0,1])
    #ax2.legend(['D(G(z))'])
    plt.title('step %d' % iter)
    plt.xlabel('G(z)/x')
    if show:
        plt.show()
        return
    fig.savefig('%d.png' % iter)
    plt.close(fig)


merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter( 'data/train',
                                     sess.graph)

batch_size = 64
sess.run(tf.global_variables_initializer())
step = 10
dloss, gloss = 0, 0
for i in range(3000):
    z = np.random.rand(batch_size, 1)
    x = unlabeled_data_gen(batch_size)

    _, dloss, summary = sess.run([d_train, d_loss, merged], feed_dict={x_placeholder:x, z_placeholder: z})
    _, gloss, fmloss = sess.run([g_train, g_loss, fm_loss], feed_dict={x_placeholder:x, z_placeholder:z})

    train_writer.add_summary(summary, i)

    if i > 100 and step <= 10:
        step = 100
    if i % step == 0:
        print time.asctime(), 'train', i, 'iters. dLoss =', dloss, 'gLoss =', gloss, 'fmloss=', fmloss
        eval_gan(i)

eval_gan(i, show=True)


