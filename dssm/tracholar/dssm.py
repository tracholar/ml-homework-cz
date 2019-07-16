#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from keras.layers import Embedding, Dense, Conv1D, Input, GlobalAveragePooling1D, dot
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.preprocessing import sequence
from keras import backend as K

sentence_maxlen = 64
class DSSM(object):
    def __init__(self):
        x1 = Input(shape=(sentence_maxlen,))
        x2 = Input(shape=(sentence_maxlen,))
        model = Sequential([
            Embedding(10, 64, input_shape=(sentence_maxlen, )),
            Conv1D(filters=64, kernel_size=3 ),
            GlobalAveragePooling1D(),
            Dense(32)
        ])
        s1 = model(x1)
        s2 = model(x2)
        y_ = Dense(1,activation='sigmoid')(dot([s1, s2], axes=1))
        self.model = Model(inputs=[x1, x2], outputs=[y_,])
        self.model.compile(Adam(), loss=binary_crossentropy, metrics=['accuracy'])

    def fit(self, train_set, eval_set = None, **kwargs):
        self.model.fit_generator(train_set, **kwargs)

    def predict(self, sess, test_set):
        pass


def test_training():
    def train_set():
        while True:
            x1 = [[1,3,4,7,9], [5,9,10]]
            x2 = [[4,6], [5,11]]
            x1 = sequence.pad_sequences(x1, maxlen=sentence_maxlen)
            x2 = sequence.pad_sequences(x2, maxlen=sentence_maxlen)
            y = [1, 0]

            yield ([x1, x2], y)
    dssm = DSSM()
    dssm.fit(train_set(), steps_per_epoch=1024)


if __name__ == '__main__':
    test_training()