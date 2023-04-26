# -*- coding: utf-8 -*-
"""
@author: Scrooge
"""
#一个用来比较典型深度神经网络、卷积神经网络、循环神经网络对MNIST手写数字是别的性能的程序

from __future__ import print_function
import numpy as np
np.random.seed(1337)

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D
from keras.datasets import mnist
from keras.utils import np_utils
from keras import initializers
#from keras.utils.vis_utils import plot_model
from keras import backend as K#这里应该是指tensorflow卷积核
from keras.callbacks import Callback
from matplotlib import pyplot as plt

def init_weights(shape, name=None):
    #return initializers.normal(shape, scale=0.01, name=name)
    return initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
    
class LossHistory(Callback):#让拟合的回调函数作为精度和误差记录类初始化的参数
    def on_train_begin(self,logs={}):
        self.losses={'batch':[],'epoch':[]}#训练误差初始化
        self.accuracy={'batch':[],'epoch':[]}#训练精度初始化
        self.val_loss={'batch':[],'epoch':[]}#检验误差初始化
        self.val_acc={'batch':[],'epoch':[]}#检验精度初始化
    def on_batch_end(self,batch,logs={}):
        self.losses['batch'].append(logs.get('loss'))#训练误差按训练批次加上新的值
        self.accuracy['batch'].append(logs.get('acc'))#训练精度按训练批次加上新的值
        self.val_loss['batch'].append(logs.get('val_loss'))#检验误差按训练批次加上新的值
        self.val_acc['batch'].append(logs.get('val_acc'))#检验精度按训练批次加上新的值
    def on_epoch_end(self,batch,logs={}):
        self.losses['epoch'].append(logs.get('loss'))#训练误差按训练周期加上新的值
        self.accuracy['epoch'].append(logs.get('acc'))#训练精度按训练周期加上新的值
        self.val_loss['epoch'].append(logs.get('val_loss'))#检验误差按训练周期加上新的值
        self.val_acc['epoch'].append(logs.get('val_acc'))#检验精度按训练周期加上新的值
    def loss_plot(self,loss_type):
        iters=range(len(self.losses[loss_type]))#从训练误差的长度来得到迭代次数
        plt.figure()#开始画图
        plt.plot(iters.self.accuracy[loss_type],'r',label='train acc')
        plt.plot(iters.self.losses[loss_type],'g',label='train loss')
        if loss_type=='epoch':
            plt.plot(iters.self.val_acc[loss_type],'b',label='val acc')
            plt.plot(iters.self.val_loss[loss_type],'k',label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()

batch_size = 128#批次大小
nb_epoch_CRNN = 10#CNN和RNN的训练周期
nb_epoch_DNN = 20#DNN的训练周期
img_rows, img_cols = 28, 28#MNIST的手写字均为28*28像素的图像
nb_classes = 10#0-9这10个数字作为分类

nb_lstm_outputs = 30#LSTM循环神经网络蹭的输出参数

nb_filters = 32#CNN所需滤波器个数
pool_size = (2, 2)#池化面积
kernel_size = (3, 3)#卷积核大小

input_shape = (img_rows, img_cols, 1)
(X_train, y_train), (X_test, y_test) = mnist.load_data()
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

DNN = Sequential()
DNN.add(Dense(512,input_shape=(784,),activation='relu'))#输入层，每层512个神经元
DNN.add(Dropout(0.2))#估计就是这里用到了随机数，该层神经元有20%随机掉线
DNN.add(Dense(512,activation='relu'))#第一内隐层，每层512个神经元
DNN.add(Dropout(0.2))
DNN.add(Dense(512,activation='relu'))#第二内隐层，每层512个神经元
DNN.add(Dropout(0.2))
DNN.add(Dense(10,activation='softmax'))#输出层，每层10个神经元（对应0-9这10个数字的概率）
#plot_model(DNN, to_file='DNN.png')

CNN = Sequential()
CNN.add(Convolution2D(nb_filters,kernel_size[0],kernel_size[1],border_mode='valid',input_shape=input_shape))#卷积输入层，用于特征提取
CNN.add(Activation('relu'))
CNN.add(Convolution2D(nb_filters,kernel_size[0],kernel_size[1]))#第二卷积层，用于特征提取
CNN.add(Activation('relu'))
CNN.add(MaxPooling2D(pool_size=pool_size))#池化层，用于特征归纳
CNN.add(Dropout(0.25))
CNN.add(Flatten())
CNN.add(Dense(128,activation='relu'))
CNN.add(Dropout(0.5))
CNN.add(Dense(nb_classes, activation='softmax', kernel_initializer='random_uniform',bias_initializer='zeros'))
#plot_model(CNN, to_file='CNN.png')

RNN = Sequential()
RNN.add(LSTM(nb_lstm_outputs, input_shape=input_shape))
RNN.add(Dense(nb_classes, activation='softmax', kernel_initializer='random_uniform',bias_initializer='zeros'))
#plot_model(RNN, to_file='RNN.png')

DNN.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
CNN.compile(loss='categorical_crossentropy',optimizer='adadelta',metrics=['accuracy'])
RNN.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

X_train_D = X_train.reshape(60000,784)
X_test_D = X_test.reshape(10000,784)
X_train_D = X_train_D.astype('float32')
X_test_D = X_test_D.astype('float32')
X_train_D /= 255
X_test_D /= 255

history_DNN = LossHistory()
DNN.fit(X_train_D,Y_train,batch_size=batch_size,nb_epoch=nb_epoch_DNN,verbose=1,validation_data=(X_test_D,Y_test),callbacks=[history_DNN])

X_train_C = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
X_test_C = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
X_train_C = X_train_C.astype('float32')
X_test_C = X_test_C.astype('float32')
X_train_C /= 255
X_test_C /= 255

history_CNN = LossHistory()
CNN.fit(X_train_C, Y_train, batch_size=batch_size, nb_epoch=nb_epoch_CRNN,verbose=1, validation_data=(X_test_C, Y_test),callbacks=[history_CNN])

X_train_R = X_train.astype('float32') / 255.
X_test_R = X_test.astype('float32') / 255.

history_RNN = LossHistory()
RNN.fit(X_train_R, Y_train, nb_epoch=nb_epoch_CRNN, batch_size=batch_size, shuffle=True, verbose=1,callbacks=[history_RNN])

score_DNN = DNN.evaluate(X_test_D, Y_test, verbose=1)
print('Test score:', score_DNN[0])
print('Test accuracy:', score_DNN[1])
DNN.save('DNN.h5')
score_CNN = CNN.evaluate(X_test_C, Y_test, verbose=1)
print('Test score:', score_CNN[0])
print('Test accuracy:', score_CNN[1])
CNN.save('CNN.h5')
score_RNN = RNN.evaluate(X_test_R, Y_test, verbose=1)
print('Test score:', score_RNN[0])
print('Test accuracy:', score_RNN[1])
RNN.save('RNN.h5')

history_DNN.loss_plot('epoch')
history_CNN.loss_plot('epoch')
history_RNN.loss_plot('epoch')
