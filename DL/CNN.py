# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:17:26 2017

@author: Scrooge
"""
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D#重点
from keras.utils import np_utils
from keras import backend as K#这里应该是指tensorflow卷积核
from keras.utils.vis_utils import plot_model

batch_size = 128 
nb_classes = 10
nb_epoch = 12

img_rows, img_cols = 28, 28
# 使用的卷积滤波器的数量
nb_filters = 32
# 用于 max pooling 的池化面积
pool_size = (2, 2)
# 卷积核的尺寸
kernel_size = (3, 3)

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()
model.add(Convolution2D(nb_filters,kernel_size[0],kernel_size[1],border_mode='valid',input_shape=input_shape))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters,kernel_size[0],kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(0.25))
model.add(Flatten())#
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

plot_model(model, to_file='model-cnn.png')

model.compile(loss='categorical_crossentropy',optimizer='adadelta',metrics=['accuracy'])

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model.save('mnist-cnn-novice.h5')

model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,verbose=1, validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model.save('mnist-cnn-trained.h5')