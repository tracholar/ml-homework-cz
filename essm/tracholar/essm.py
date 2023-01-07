# coding:utf-8
"""
代码参考：https://mp.weixin.qq.com/s/jBxtdDQEPSMLXidFNphBCA
"""
import keras
import tensorflow as tf
import argparse
import datetime
from keras import Input
from keras.layers import Dense



def get_cur_date():
    cur_date = datetime.datetime.now()
    return cur_date.strftime("%Y%m%d")


def init_args():
    parser = argparse.ArgumentParser(description="DSSM")
    parser.add_argument("--mode", default="train", help="train|test")
    parser.add_argument("--train_data_dir", help="训练数据目录")
    parser.add_argument("--model_output_dir", default="./model", help="模型输出目录")
    parser.add_argument("--cur_date", default=get_cur_date(), help="档期日期")
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

def build_dnn_net(net, params_conf, name='ctr'):
    for i, hidden_size in enumerate(params_conf.DNN_HIDDEN_SIZES):
        net = Dense(hidden_size, activation='relu', name='{}_fc{}'.format(name, i))(net)
    return net

def build_model(emb_map, input_list):
    pass



if __name__ == '__main__':
    args = init_args()
    print(args)



