#coding:utf-8
import tensorflow as tf
import numpy as np

class Dataset(object):
    def __init__(self):
        pass

class Word2Vec(object):
    def __init__(self, word_size, word_len=128, reg = 1e-3, window_size = 5):
        """
        创建计算图, 注意我这个模型跟标准的w2v有些差异,
        我只使用了一个词向量矩阵, 左向量和右向量是相同的
        """
        self.word_size = word_size
        self.word_len = word_len
        self.reg = reg
        self.window_size = window_size
        self.W = tf.Variable(np.random.rand(word_size, word_len), name='W')
        self.c = tf.placeholder(tf.int64, shape=(None, ))
        self.pos = tf.placeholder(tf.int64, shape=(None, None))
        self.neg = tf.placeholder(tf.int64, shape=(None, None))

        wc = tf.expand_dims(tf.nn.embedding_lookup(self.W, self.c), 1)
        wpos = tf.nn.embedding_lookup(self.W, self.pos)
        wneg = tf.nn.embedding_lookup(self.W, self.neg)
        ypos = tf.nn.sigmoid(tf.reduce_sum(wc * wpos, axis=2))
        yneg = tf.nn.sigmoid(- tf.reduce_sum(wc * wneg, axis=2))

        self.main_loss = tf.reduce_mean(tf.log(ypos)) + tf.reduce_mean(tf.log(yneg))
        self.reg_loss = tf.reduce_sum(wc**2) + tf.reduce_sum(wpos**2) + tf.reduce_sum(wneg**2)
        self.loss = self.main_loss + self.reg * self.reg_loss
        opt = tf.train.AdamOptimizer(1e-3)
        self.train_op = opt.minimize(self.loss)



    def fit(self, dataset):
        """
        拟合数据
        :param data: 数据集
        :return:
        """
        trainSet = dataset.getTrainSentences()
        sess = tf.Session()
        for s in trainSet:
            s = s[0]
            for i in range(self.window_size, len(s) - self.window_size):
                wc = s[i]
                pos = [s[j] for j in range(max(0, i - self.window_size), min(len(s), i+self.window_size))]
                neg = []
                while len(neg) < 10:
                    idx = dataset.sampleTokenIdx()
                    if idx not in pos and idx != wc:
                        neg.append(idx)
                loss, _ = sess.run([self.loss, self.train_op], feed_dict={self.c: wc,
                                                      self.pos: pos,
                                                      self.neg: neg})
                print('{} loss: {}'.format(i, loss))

    def predict(self, words):
        """
        将word转化为向量
        :param words: 单词
        :return:
        """
        raise NotImplementedError()



if __name__ == '__main__':
    from dataset.data_utils import *
    dataset = StanfordSentiment()
    tokens = dataset.tokens()
    w2v = Word2Vec(len(tokens))
    w2v.fit(dataset)

