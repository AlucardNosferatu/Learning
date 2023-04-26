# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:24:00 2017
@author: Scrooge
"""
from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(1337)#将随机数种子设置为1337

from keras.datasets import mnist#从数据集中导入MNIST数据
from keras.models import Sequential#导入序贯模型
from keras.layers.core import Dense, Dropout, Activation#导入层模型：全连接、掉队、激活
from keras.optimizers import SGD, Adam, RMSprop#导入优化方法：随机小批量梯度下降（SGD）、Adam、RMSprop
from keras.utils import np_utils
#from keras.utils.vis_utils import plot_model

batch_size=128#批（一次对比前输入的数据量）大小
nb_classes=10#分类个数10（对应0-9）
nb_epoch=20#20个训练周期

(X_train, y_train),(X_test, y_test)=mnist.load_data()
X_train = X_train.reshape(60000,784)
X_test = X_test.reshape(10000,784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0],'train samples')
print(X_test.shape[0],'test samples')

Y_train=np_utils.to_categorical(y_train,nb_classes)
Y_test=np_utils.to_categorical(y_test,nb_classes)

dims=[256,512,256,128,10]

model=Sequential()

for index in range(0,len(dims)):
    if(index==0):
        model.add(Dense(dims[index],input_shape=(784,)))#第一内隐层，每层512个神经元
    else:
        model.add(Dense(dims[index]))#第二内隐层，每层512个神经元        
    if(index==(len(dims)-1)):
        model.add(Activation('softmax'))
    else:
        model.add(Activation('relu'))
        model.add(Dropout(0.2))#估计就是这里用到了随机数

#plot_model(model, to_file='model.png')

model.compile(loss='categorical_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

#score = model.evaluate(X_test, Y_test, verbose=0)
#print('Test score:', score[0])
#print('Test accuracy:', score[1])

model.save('mnist-mlp-novice.h5')

history=model.fit(X_train,Y_train,batch_size=batch_size,nb_epoch=nb_epoch,verbose=1,validation_data=(X_test,Y_test))
history=history.history
acc=pd.DataFrame(np.array(history['acc']))

loss=pd.DataFrame(np.array(history['loss']))

loss.plot(figsize=(20,5))
acc.plot(figsize=(20,5))
plt.show()

#score = model.evaluate(X_test, Y_test, verbose=0)
#print('Test score:', score[0])
#print('Test accuracy:', score[1])

model.save('mnist-mlp-trained.h5')