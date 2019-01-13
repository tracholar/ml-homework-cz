#coding:utf-8

import tensorflow as tf



class LR(object):
    def __init__(self, **kwargs):
        self.uid = tf.placeholder(tf.int32, [None, ])
        self.tid = tf.placeholder(tf.int32, [None, ])
        self.y = tf.placeholder(tf.float32, [None,])
        self.hist_i = tf.placeholder(tf.int32, [None, None])
        self.hist_len = tf.placeholder(tf.int32, [None, ])

        uid_emb_w = tf.get_variable("uid_emb", shape=[kwargs['user_count'], 1])
        tid_emb_w = tf.get_variable("tid_emb", shape=[kwargs['item_count'], 1])
        cate_emb_w = tf.get_variable("cate_emb", shape=[kwargs['cate_count'], 1])

        cate_list = tf.convert_to_tensor(kwargs['cate_list'], dtype=tf.int64)

        all_emb = [
            tf.nn.embedding_lookup(uid_emb_w, self.uid),
            tf.nn.embedding_lookup(tid_emb_w, self.tid),
            tf.reduce_sum(tf.nn.embedding_lookup(tid_emb_w, self.hist_i), axis=1),
            tf.nn.embedding_lookup(cate_emb_w, tf.gather(cate_list, self.tid)),
            tf.reduce_sum(tf.nn.embedding_lookup(cate_emb_w, tf.gather(cate_list, self.hist_i)), axis=1),
        ]
        logits = tf.reduce_sum(tf.concat(all_emb), axis=1)
        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=self.y))
        self.opt = tf.train.GradientDescentOptimizer(0.1)

        self.global_step = tf.Variable(0, trainable=False, name='grobal_step')
        self.train_op = self.opt.minimize(self.loss, global_step=self.global_step)




    def fit(self, train_set, test_set, cate_list, **kwargs):
        pass

    def eval(self, **kwargs):
        pass

    def predict(self, **kwargs):
        pass
