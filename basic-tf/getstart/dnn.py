#coding:utf-8
import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('./MNIST_data')


## 创建计算图中的关键节点
with tf.name_scope('input'):
    ## TODO 输入节点
    x = None

def logistic_regression(x_):
    with tf.name_scope('logistic_regression'):
        # TODO 定义逻辑回归
        pass

    # TODO 增加直方图summary
    return y

def conv_net(x_):
    with tf.name_scope('conv'):
        ## TODO 定义卷积网络
        pass
    ## TODO 增加隐层节点的直方图summary
    return y


y = conv_net(x)

## 定义损失函数
with tf.name_scope('loss'):
    ## TODO 定义交叉熵
    cross_entropy = None

    ## TODO 定义预测准确率
    acc = None

## TODO 定义一个step全局变量和优化器,并指定 global_step
step = None
optimizer = tf.train.AdamOptimizer(1e-3)
train_op = None
update_op = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

## TODO 添加summary: loss, acc



merged = tf.summary.merge_all()





with tf.Session() as sess:
    ## TODO 定义训练集和测试集日志writer
    logdir = './tmp/log'
    train_writer = None
    test_writer = None

    ## TODO 初始化全局变量

    ## 定义模型checkpoint保存对象, 检查路径是否存在, 如果存在就从checkpoint文件中恢复
    saver = None
    ckpt_path = './tmp/mnist/model.ckpt'
    if os.path.exists(os.path.dirname(ckpt_path)):
        saver.restore(sess, ckpt_path)
    else:
        os.mkdir(os.path.dirname(ckpt_path))

    ## 训练模型
    for _ in range(10000):
        xs, ys = mnist.train.next_batch(100)
        ##TODO 训练模型

        if i % 100 == 0:
            ## TODO 评估模型在训练集和测试集上的效果,并将日志保存到日志文件中


            print i, 'loss', loss, \
                'train acc', acc_train, \
                'test acc', acc_test

            ## TODO 保存模型
            saver.save(sess, ckpt_path)
