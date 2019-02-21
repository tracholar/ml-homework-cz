#coding:utf-8
from __future__ import print_function
import tensorflow as tf
from input import DataInput
import numpy as np
from model import ModelMixin
import pickle

class LR(ModelMixin):
    def __init__(self,user_count,item_count,cate_count,cate_list):

        self.user=tf.placeholder(tf.int32,[None,])
        self.item=tf.placeholder(tf.int32,[None,])# 目标点击的item

        self.y=tf.placeholder(tf.float32,[None,])# 目标

        self.click_hist=tf.placeholder(tf.int32,[None,None])

        self.click_len=tf.placeholder(tf.int32,[None,])

        hidden_units=1
        user_embedding=tf.get_variable("user_embedding",[user_count,hidden_units],initializer=tf.random_normal_initializer())
        item_embedding=tf.get_variable("item_embedding",[item_count,hidden_units],initializer=tf.random_normal_initializer())
        cate_embedding=tf.get_variable("cate_embedding",[cate_count,hidden_units],initializer=tf.random_normal_initializer())

        """
          用户 的 embedding 向量。
        """
        user_emb=tf.nn.embedding_lookup(user_embedding,self.user)

        """
           target embedding
        """

        cate_list=tf.convert_to_tensor(cate_list,dtype=tf.int32)

        item2cate=tf.gather(cate_list,self.item)

        item_emb=tf.nn.embedding_lookup(item_embedding,self.item)
        cate_emb=tf.nn.embedding_lookup(cate_embedding,item2cate)

        """
         点击的list 做embedding 并求和压缩统一维度
        """
        click_hist_cate=tf.gather(cate_list,self.click_hist)
        click_list_cate_emb=tf.nn.embedding_lookup(cate_embedding,click_hist_cate)
        click_list_item_emb=tf.nn.embedding_lookup(item_embedding,self.click_hist)


        click_list_cate_=tf.reduce_sum(click_list_cate_emb,1)
        click_list_item_=tf.reduce_sum(click_list_item_emb,1)



        mlp_input=tf.concat([user_emb,item_emb,cate_emb,click_list_item_,click_list_cate_],axis=1)


        self.lr_out=tf.reduce_sum(mlp_input,axis=1)

        self.cross_w1=tf.get_variable("cross_w1",shape=[1,hidden_units],initializer=tf.random_normal_initializer())
        self.cross_w2=tf.get_variable("cross_w2",shape=[1,hidden_units],initializer=tf.random_normal_initializer())

        self.cross_out=tf.reduce_sum(user_emb*item_emb*self.cross_w1+user_emb*cate_emb*self.cross_w2,axis=1)

        self.logits=self.lr_out+self.cross_out

        self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels=self.y))

        self.optimizer=tf.train.AdamOptimizer(0.001).minimize(self.loss)

        #self.auc=tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))
        self.auc, self.auc_update_op = tf.metrics.auc(labels=self.y, predictions=tf.nn.sigmoid(self.logits))


    def fit(self,sess,train_data):

        for i in range(5):

            for j,data in DataInput(train_data,batch_size=128):

                loss_output,_,_=sess.run([self.loss,self.optimizer,self.auc_update_op],feed_dict={
                    self.user:data[0],
                    self.item:data[1],
                    self.y:data[2],
                    self.click_hist:data[3],
                    self.click_len:data[4]
                })

                if j%1000==0:

                    log={'itr':i,'step':j,'loss':loss_output,'auc':self.auc.eval(session=sess)}
                    print("itr : {itr} , step: {step}, loss : {loss},auc : {auc}".format(**log))
    def eval(self,sess,data_set,name='eval'):
        loss_sum = 0
        logits_arr = np.array([])
        y_arr = np.array([])

        for j,data in DataInput(data_set,batch_size=12800):

            loss_output,logits=sess.run([self.loss,self.logits],feed_dict={
                self.user:data[0],
                self.item:data[1],
                self.y:data[2],
                self.click_hist:data[3],
                self.click_len:data[4]
            })
            loss_sum += loss_output

            logits_arr = np.append(logits_arr, logits)
            y_arr = np.append(y_arr, data[2])

        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(y_arr, logits_arr)

        log_data = {'name': name,
                    'loss' : loss_sum,
                    'auc' : auc,
                    }
        print('Eval {name} : loss = {loss} auc = {auc}'.format(**log_data))

if __name__=='__main__':
    with open('../dataset.pkl', 'rb') as f:
        train_set=pickle.load(f)
        test_set=pickle.load(f)
        cate_list=pickle.load(f)
        user_count, item_count, cate_count=pickle.load(f)

    model=LR(user_count=user_count, item_count=item_count, cate_count=cate_count, cate_list=cate_list)
    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())

        model.fit(sess,train_set)
        model.eval(sess,train_set,'train')
        model.eval(sess,test_set,'test')
