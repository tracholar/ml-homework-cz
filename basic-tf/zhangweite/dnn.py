#coding:utf-8
import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


## 创建计算图中的关键节点
with tf.name_scope('input'):
    tf_x = tf.placeholder(tf.float32, [None, 784])
    tf_y = tf.placeholder(tf.float32, [None, 10])
    tf_is_train = tf.placeholder(tf.bool, None)

def mlp_net(x_):
    with tf.name_scope('MLP'):
        l1 = tf.layers.dense(inputs = x_, units = 512, activation = tf.nn.relu, name ='l1',
            kernel_initializer = tf.initializers.random_normal(mean=0, stddev=1))
        # l12 = tf.layers.batch_normalization(l1, training=tf_is_train)
        l1d = tf.layers.dropout(inputs = l1, rate=0.1, training=tf_is_train)
        l2 = tf.layers.dense(inputs = l1d, units = 256, activation = tf.nn.relu, name ='l2',
            kernel_initializer = tf.initializers.random_normal(mean=0, stddev=1))
        # l22 = tf.layers.batch_normalization(l2, training=tf_is_train)
        l2d = tf.layers.dropout(inputs = l2, rate=0.1, training=tf_is_train)
        output = tf.layers.dense(l2d, 10)
        tf.summary.histogram('l1', l1)
        tf.summary.histogram('l2', l2)
    return output

def conv_net(x_):
    with tf.name_scope('conv'):
        in_x = tf.reshape(x_, [-1, 28, 28, 1]) 
        conv_11 = tf.layers.conv2d( 
            inputs=in_x, filters=8, kernel_size=3,strides=1, padding='same', activation=tf.nn.relu, name = 'c11'
        )   #  (28, 28, 1) -> (28, 28, 8)
        conv_12 = tf.layers.conv2d( 
            inputs=conv_11, filters=16, kernel_size=3, strides=1, padding='same', activation=tf.nn.relu, name = 'c12'
        )   #  (28, 28, 8) -> (28, 28, 16)
        conv_13 = tf.layers.conv2d( 
            inputs=conv_12, filters=32, kernel_size=5, strides=2, padding='same', activation=tf.nn.relu, name = 'c13'
        )   #  (28, 28, 16) -> (14, 14, 32)
        ld_14 = tf.layers.dropout(inputs = conv_13, rate=0.4, training=tf_is_train)

        flat = tf.reshape(ld_14, [-1, 14*14*32])  
        l31 = tf.layers.dense(flat, 128) 
        ld_32 = tf.layers.dropout(inputs = l31, rate=0.4, training=tf_is_train)
        output = tf.layers.dense(ld_32, 10) 

    return output


def rnn_net(x_):
    with tf.name_scope('conv'):
        in_x = tf.reshape(x_, [-1, 28, 28]) 
        rnn_cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=28)
        outputs, (h_c, h_n) = tf.nn.dynamic_rnn(
            cell=rnn_cell, inputs=in_x, initial_state=None, 
            dtype=tf.float32, time_major=False
        )                         # [bacth,28,64]
        state = outputs[:,-1,:]
    return state

# mlp
# output = mlp_net(tf_x)

# cnn
# output = conv_net(tf_x)

# rnn
state = rnn_net(tf_x)
output = tf.layers.dense(state, 10)  # [bacth,10]   


## 定义损失函数
with tf.name_scope('loss'):
    ## TODO 定义交叉熵
    Loss = tf.losses.softmax_cross_entropy(onehot_labels=tf_y, logits=output) 
    corr = tf.equal(tf.argmax(output, 1), tf.argmax(tf_y,1))
    acc = tf.reduce_mean(tf.cast(corr, tf.float32))

## TODO 定义一个step全局变量和优化器,并指定 global_step
step = tf.Variable(0, trainable=False)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-3).minimize(Loss, global_step=step)
update_op = tf.get_collection(tf.GraphKeys.UPDATE_OPS)


## TODO 添加summary: loss, acc

tf.summary.scalar('loss', Loss)
tf.summary.scalar('acc', acc)
merged = tf.summary.merge_all()


with tf.Session() as sess:
    ## TODO 定义训练集和测试集日志writer
    logdir = './tmp/log_rnn'
    train_writer = tf.summary.FileWriter(logdir + '/train', sess.graph)
    test_writer = tf.summary.FileWriter(logdir + '/test')

    ## TODO 初始化全局变量
    sess.run(tf.group(tf.global_variables_initializer(), tf.local_variables_initializer()))
   
    ## 定义模型checkpoint保存对象, 检查路径是否存在, 如果存在就从checkpoint文件中恢复
    saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES))
    ckpt_path = './tmp/mnist_rnn/model.ckpt'
    if os.path.exists(os.path.dirname(ckpt_path)):
        saver.restore(sess, ckpt_path)
    else:
        os.mkdir(os.path.dirname(ckpt_path))

    ## 训练模型
    for _ in range(10000):
        xs, ys = mnist.train.next_batch(100)
        ##TODO 训练模型
        loss, i, _, _ = sess.run([Loss, step, optimizer, update_op], 
            feed_dict = {tf_x: xs,tf_y: ys, tf_is_train: True})
        if i % 1000 == 0:
            ## TODO 评估模型在训练集和测试集上的效果,并将日志保存到日志文件中
            acc_train, summary = sess.run([acc, merged], feed_dict={tf_x: mnist.train.images, tf_y: mnist.train.labels, tf_is_train: False})
            train_writer.add_summary(summary, global_step=i)

            acc_test, summary = sess.run([acc, merged], feed_dict={tf_x: mnist.test.images, tf_y: mnist.test.labels, tf_is_train: False})
            test_writer.add_summary(summary, global_step=i)

            print(i, 'loss', loss, \
                'train acc', acc_train, \
                'test acc', acc_test)

            ## TODO 保存模型
            saver.save(sess, ckpt_path)
