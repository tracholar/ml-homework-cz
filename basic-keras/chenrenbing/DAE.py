
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Conv2D,Conv2DTranspose
from util import *


class DAE_NN:
    def __init__(self,n_itr=30,layer_shape=None,input_shape=(784,),
                 batch_size=64,optimizer='adam',loss='mse'):
        self.layer_shape=layer_shape
        self.input_shape=input_shape
        self.model=Sequential()
        #self.batch_size=batch_size
        #self.n_itr=n_itr
        self.optimizer=optimizer
        self.loss=loss
    def fit(self,X_noisy,X,epochs=5,batch_size=32,verbose=1):
        self.encoder(X_noisy)
        self.decoder(X_noisy)
        self.model.compile(optimizer=self.optimizer,loss=self.loss)
        self.model.fit(X_noisy,X,epochs=epochs,batch_size=batch_size,verbose=1)



    def encoder(self,X):
        self.model.add(Dense(self.layer_shape[0],input_shape=self.input_shape))
        self.model.add(Activation('sigmoid'))

        for i in range(1,len(self.layer_shape)):
            self.model.add(Dense(self.layer_shape[i]))
            self.model.add(Activation('sigmoid'))


    def decoder(self,X):
        for i in range(len(self.layer_shape)):

            self.model.add(Dense(self.layer_shape[-(i+1)]))
            self.model.add(Activation('sigmoid'))
        self.model.add(Dense(self.input_shape[0]))

    def predict(self,X):
        return self.model.predict(X)


class DAE_CNN:
    def __init__(self,n_itr=30,layer_shape=None,filter=None,input_shape=(28,28,1),
                 batch_size=64,optimizer='adam',loss='mse'):
        self.layer_shape=layer_shape
        self.filter=filter
        self.input_shape=input_shape
        self.model=Sequential()
        #self.batch_size=batch_size
        #self.n_itr=n_itr
        self.optimizer=optimizer
        self.loss=loss
    def fit(self,X_noisy,X,epochs=5,batch_size=32,verbose=1):
        self.encoder(X_noisy)
        self.decoder(X_noisy)
        self.model.compile(optimizer=self.optimizer,loss=self.loss)
        self.model.fit(X_noisy,X,epochs=epochs,batch_size=batch_size,verbose=1)


    def encoder(self,X):

        self.model.add(Conv2D(self.layer_shape[0],kernel_size=self.filter[0],activation='relu',padding='same',input_shape=self.input_shape))

        for i in range(1,len(self.layer_shape)):

            self.model.add(Conv2D(self.layer_shape[i],kernel_size=self.filter[i],activation='relu',padding='same'))


    def decoder(self,X):
        for i in range(len(self.layer_shape)):

            self.model.add(Conv2D(self.layer_shape[-(i+1)],kernel_size=self.filter[-(i+1)],activation='relu',padding='same'))

        self.model.add(Conv2D(1,(3,3),padding='same'))
    def predict(self,X):
        return self.model.predict(X)











