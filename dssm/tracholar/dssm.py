#coding:utf-8
from __future__ import print_function
from keras.layers import Embedding, Dense, Conv1D, Input, GlobalAveragePooling1D, dot, Activation
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.preprocessing import sequence
import numpy as np
import random
sentence_maxlen = 64
word_cnt = 128
class DSSM(object):
    def __init__(self, ):
        x1 = Input(shape=(sentence_maxlen,))
        x2 = Input(shape=(sentence_maxlen,))
        model = Sequential([
            Embedding(word_cnt, 64, input_shape=(sentence_maxlen, )),
            Conv1D(filters=64, kernel_size=3 ),
            GlobalAveragePooling1D(),
            Dense(32)
        ])
        s1 = model(x1)
        s2 = model(x2)
        s = dot([s1, s2], axes=1)
        y_ = Activation(activation='sigmoid')(s)
        self.model = Model(inputs=[x1, x2], outputs=[y_,])
        self.model.compile(Adam(), loss=binary_crossentropy, metrics=['accuracy'])

    def fit(self, train_set, eval_set = None, **kwargs):
        self.model.fit_generator(train_set, validation_data=eval_set, **kwargs)

    def predict(self, sess, test_set):
        pass


def test_training():
    def train_set():
        while True:
            x1 = [[1,3,4,7,9], [5,9,10]]
            x2 = [[4,6], [5,11]]
            x1 = sequence.pad_sequences(x1, maxlen=sentence_maxlen)
            x2 = sequence.pad_sequences(x2, maxlen=sentence_maxlen)
            y = np.array([[1], [0]])
            yield ([x1, x2], y)
    dssm = DSSM()
    g = train_set()
    print(g.__next__())
    print(g.__next__())
    dssm.fit(g, steps_per_epoch=10)

def training():
    global sentence_maxlen
    global word_cnt
    import pickle
    data = pickle.load(open("data.pkl"))
    word_cnt = 1 + data['wordcnt']
    sentence_maxlen = 1 + max(len(d['title']) for d in data['train'])
    print(sentence_maxlen)

    def data_set(train_or_test = 'train'):
        if train_or_test == 'test':
            dataset = data['test']
        else:
            dataset = data['train']
        while True:
            x1 = []
            x2 = []
            y = []
            n_samples = len(dataset)
            for i in range(n_samples):
                d = dataset[i]
                x1.append(d['title'])
                x2.append(d['tags'])
                y.append([1])

                j = i
                while j == i:
                    j = random.randint(0, n_samples-1)

                d = dataset[j]
                x1.append(d['title'])
                x2.append(d['tags'])
                y.append([0])

                if (i+1) % 16 == 0:
                    x1 = sequence.pad_sequences(x1, maxlen=sentence_maxlen)
                    x2 = sequence.pad_sequences(x2, maxlen=sentence_maxlen)
                    y = np.array(y)
                    yield ([x1, x2], y)

                    x1 = []
                    x2 = []
                    y = []

    dssm = DSSM()
    g_train = data_set('train')
    g_test = data_set('test')
    print(g_train.next())
    dssm.fit(g_train, eval_set=g_test, steps_per_epoch=1024,
             validation_steps=1024, epochs=10)





if __name__ == '__main__':
    test_training()