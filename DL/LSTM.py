# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 23:35:45 2017

@author: Scrooge
"""

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.datasets import mnist
from keras.utils import np_utils
from keras import initializers
from keras.utils.vis_utils import plot_model
def init_weights(shape, name=None):
    #return initializers.normal(shape, scale=0.01, name=name)
    return initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
    
# Hyper parameters
batch_size = 128
nb_epoch = 10
# Parameters for MNIST dataset
img_rows, img_cols = 28, 28
nb_classes = 10
# Parameters for LSTM network
nb_lstm_outputs = 30
nb_time_steps = img_rows
dim_input_vector = img_cols

(X_train, y_train), (X_test, y_test) = mnist.load_data()
print('X_train original shape:', X_train.shape)
input_shape = (nb_time_steps, dim_input_vector)
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

model = Sequential()
model.add(LSTM(nb_lstm_outputs, input_shape=input_shape))
#model.add(Dense(nb_classes, activation='softmax', init=init_weights))
model.add(Dense(nb_classes, activation='softmax', kernel_initializer='random_uniform',bias_initializer='zeros'))
plot_model(model, to_file='lstm_model.png')

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

score = model.evaluate(X_test, Y_test, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model.save('mnist-lstm-novice.h5')

history = model.fit(X_train, Y_train, nb_epoch=nb_epoch, batch_size=batch_size, shuffle=True, verbose=1)

score = model.evaluate(X_test, Y_test, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model.save('mnist-lstm-trained.h5')