# coding:utf-8
"""
代码参考：https://mp.weixin.qq.com/s/jBxtdDQEPSMLXidFNphBCA
"""
import keras
import tensorflow as tf
import argparse
import logging
from keras import Input
from keras.layers import Dense, Concatenate
from keras.models import Model, save_model
from keras.optimizers import Adam
from keras.losses import BinaryCrossentropy
from keras.metrics import AUC, BinaryAccuracy, Recall, Precision
from keras.callbacks import TensorBoard, LearningRateScheduler
from os import path
from datetime import datetime, timedelta
from math import exp, pow


DATE_FMT = '%Y%m%d'

MODEL_CONF = {
    'learning_rate': 1e-3,
    'batch_size': 128
}
def get_cur_date():
    cur_date = datetime.now()
    return cur_date.strftime(DATE_FMT)

def get_date_list(end_date, days=1):
    date_list = []
    cur = datetime.strptime(end_date, DATE_FMT)
    for x in range(days):
        delta = timedelta(days=-x)
        new_date = cur + delta
        date_list.insert(0, new_date.strftime(DATE_FMT))
    return date_list

def get_data_set(base_dir, date_list, feature_columns):
    return None, None


class LearningRateDecay(object):
    def __int__(self, init_lr, decay_epochs, decay_rate):
        self.init_lr = init_lr
        self.decay_epochs = decay_epochs
        self.decay_rate = decay_rate

    def __call__(self, epoch):
        lr = self.init_lr * pow(self.decay_rate, epoch/self.decay_epochs)
        return lr
def init_args():
    parser = argparse.ArgumentParser(description="DSSM")
    parser.add_argument("--mode", default="train", help="train|test")
    parser.add_argument("--train_data_dir", help="训练数据目录")
    parser.add_argument("--model_output_dir", default="./model", help="模型输出目录")
    parser.add_argument("--cur_date", default=get_cur_date(), help="档期日期")
    parser.add_argument("--days", default=1, type=int, help="刷数据的天数")
    parser.add_argument("--log", default="./log/tensorboard")
    parser.add_argument("--use_gpu", default=False, type=bool)
    args = parser.parse_args()
    return args

def get_feature_column_map():
    key_hash_size_map = {
        "adid": 10000,
        "site_id": 10000,
        "site_domain": 10000,
        "site_category": 10000,
        "app_id": 10000,
        "app_domain": 10000,
        "app_category": 1000,
        "device_id": 1000,
        "device_ip": 10000,
        "device_type": 10,
        "device_conn_type": 10,
    }

    feature_column_map = dict()
    for name, hash_size in key_hash_size_map.items():
        feature_column_map[name] = tf.feature_column.categorical_column_with_hash_bucket(
            name, hash_size, dtype=tf.string
        )

    return feature_column_map


def build_embedding():
    feature_map = get_feature_column_map()
    feature_input_list = []

    def get_field_emb(key, emb_size=16, input_shape=(1,)):
        emb_col = tf.feature_column.embedding_column(feature_map[key], emb_size)

        dense_feat_layer = tf.keras.layers.DenseFeatures(emb_col)
        input_layer = Input(shape = input_shape, dtype=tf.string, name=key)
        feature_input_list.append(input_layer)

        return dense_feat_layer({key : input_layer})

    emb_map = {}
    for key in feature_map.keys():
        emb_map[key] = get_field_emb(key, 16)

    return emb_map, feature_input_list

def build_dnn_net(net, dnn_hidden_sizes, name='ctr'):
    for i, hidden_size in enumerate(dnn_hidden_sizes):
        net = Dense(hidden_size, activation='relu', name='{}_fc{}'.format(name, i))(net)
    return net

def build_model(emb_map, input_list):
    assert isinstance(emb_map, dict)

    define_list = []
    adid_emb = emb_map['adid']
    device_id_emb = emb_map['device_id']
    ad_x_device = adid_emb * device_id_emb

    define_list.append(ad_x_device)

    common_list = emb_map.values()

    shared_emb = Concatenate()(define_list + common_list)

    # shared
    shared_output = build_dnn_net(shared_emb, [256, 64], 'shared_bottom')

    # ctr, cvr output
    ctr_head = Dense(1, activation='sigmoid', name='ctr_head')(shared_output)
    cvr_head = Dense(1, activation='sigmoid', name='cvr_head')(shared_output)

    ctcvr_head = ctr_head * cvr_head

    model = Model(inputs=input_list, outputs=[ctr_head, ctcvr_head])

    return model, ctr_head, ctcvr_head

def train():
    output_root_dir = path.join(args.model_output_dir, args.cur_date)
    model_full_output_dir = path.join(output_root_dir, 'model_savedmodel')

    logging.info('model output: %s', model_full_output_dir)

    tf.keras.backend.clear_session()
    logging.info('start train')

    train_date_list = get_date_list(args.cur_date, args.days)
    logging.info('train date list: %s', train_date_list)

    feature_column_map = get_feature_column_map()
    train_set, test_set = get_data_set(args.train_data_dir, train_date_list, feature_column_map.values())

    emb_map, feature_input_list = build_embedding()
    model, ctr_head, ctcvr_head = build_model(emb_map, feature_input_list)

    opt = Adam(learning_rate=MODEL_CONF['learning_rate'])
    model.compile(optimizer=opt,
                  loss=[BinaryCrossentropy(), BinaryCrossentropy()],
                  loss_weights=[1., 1.],
                  metrics=[AUC(),
                           BinaryAccuracy(),
                           Recall(),
                           Precision()])
    model.summary()


    tensorboard_cb = TensorBoard(
        log_dir=args.log,
        histogram_freq=1,
        write_graph=True,
        update_freq=MODEL_CONF['batch_size'] * 200,
        embeddings_freq=1,
        profile_batch=0
    )

    lr_schedule = LearningRateDecay(MODEL_CONF['learning_rate'], 1, 0.99)
    lr_schedule_cb = LearningRateScheduler(lr_schedule, verbose=1)

    model.fit(
        train_set,
        epochs=1,
        callbacks=[tensorboard_cb, lr_schedule_cb]
    )

    save_model(model, model_full_output_dir)
    logging.info('save model success!')




if __name__ == '__main__':
    args = init_args()
    print(args)



