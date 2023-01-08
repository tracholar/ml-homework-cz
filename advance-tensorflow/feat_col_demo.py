# coding:utf-8
import tensorflow as tf

# 连续特征
price = tf.feature_column.numeric_column('price')
price_bucket = tf.feature_column.bucketized_column(price, [0., 1.5, 3.5, 10])

features = {'price':[[1.], [5.]],
            'name' : [['Tensorflow', 'Keras', 'RNN', 'LSTM', 'CNN'], ['LSTM', 'CNN', 'Tensorflow', 'Keras', 'RNN']]
            }

f_names = tf.feature_column.categorical_column_with_hash_bucket('name', 1000)
f_names_emb = tf.feature_column.embedding_column(f_names, 16)

f_seq = tf.feature_column.sequence_categorical_column_with_hash_bucket('name', 1000)
f_seq_emb = tf.feature_column.embedding_column(f_seq, 16)

feature_layer = tf.keras.layers.DenseFeatures([f_names_emb])
print('dense', feature_layer(features))

seq_feature_layer = tf.keras.experimental.SequenceFeatures([f_seq_emb])
print('seq', seq_feature_layer(features))