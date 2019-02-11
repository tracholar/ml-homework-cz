#coding:utf-8
import pickle
import tensorflow as tf
import sys
import os



if not os.path.exists('../dataset.pkl'):
    print('please generate dataset first!')
    sys.exit(1)

if len(sys.argv) < 2 or sys.argv[1] not in ['lr', 'lrcross', 'deepfm', 'dnn', 'widedeep']:
    print('usage train.py lr|lrcross|dnn|widedeep|deepfm')
    sys.exit(1)

with open('../dataset.pkl', 'rb') as f:
    train_set = pickle.load(f)
    test_set = pickle.load(f)
    cate_list = pickle.load(f)
    user_count, item_count, cate_count = pickle.load(f)


if sys.argv[1] == 'deepfm':
    from deepfm import DeepFM
    model = DeepFM(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
elif sys.argv[1] == 'lr':
    from lr import LR
    model = LR(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
elif sys.argv[1] == 'lrcross':
    from lrcross import LR
    model = LR(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
elif sys.argv[1] == 'dnn':
    from dnn import DNN
    model = DNN(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
elif sys.argv[1] == 'widedeep':
    from widedeep import WideDeep
    model = WideDeep(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
else:
    print('usage train.py lr|dnn|widedeep|deepfm')
    sys.exit(1)



with tf.Session() as sess:
    ## 初始化
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    model.fit(sess, train_set, test_set)