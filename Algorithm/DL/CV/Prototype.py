# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:58:18 2017

@author: Scrooge
"""
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

from keras.models import load_model

batch_size = 128 
nb_classes = 10
nb_epoch = 20 

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = load_model('mnist-mlp-trained.h5')

model.compile(loss='categorical_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

history=model.fit(X_train, Y_train,batch_size=batch_size, nb_epoch=nb_epoch,verbose=1,validation_data=(X_test,Y_test))

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

model.save('mnist-mlp-trained.h5')