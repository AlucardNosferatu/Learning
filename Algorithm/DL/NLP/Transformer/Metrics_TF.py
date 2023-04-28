import math
import time

import tensorflow as tf
from matplotlib import pyplot as plt

from Config_TF import MAX_SL


def loss_function(y_true, y_pred):
    y_true = tf.reshape(y_true, shape=(-1, MAX_SL - 1))

    loss = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction='none')(y_true, y_pred)

    mask = tf.cast(tf.not_equal(y_true, 0), tf.float32)
    loss = tf.multiply(loss, mask)

    return tf.reduce_mean(loss)


def perplexity(real, pred):
    """
    This function returns the perplexity for model's predictions on a batch
    of Data_FCN in comparison with the real outputs at a timestep.
    Arguments:
        real: real output, a Tensorflow tensor with a shape
              of: (batch_size, max_seq_length)
        pred: model's predictions at a certain timestep, a Tensorflow tensor
              with a shape of: (batch_size, max_seq_length)
    Returns:
        A Tensorflow tensor with the perplexity.
    """
    real = tf.reshape(real, shape=(-1, MAX_SL - 1))
    loss = loss_function(real, pred)

    return tf.cast(tf.pow(math.e, loss), dtype=tf.keras.backend.floatx())


def accuracy(y_true, y_pred):
    # ensure labels have shape (batch_size, MAX_SENTENCE_LENGTH - 1)
    y_true = tf.reshape(y_true, shape=(-1, MAX_SL - 1))
    return tf.keras.metrics.sparse_categorical_accuracy(y_true, y_pred)


class LossHistory(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.perplexity = None
        self.accuracy = None
        self.loss = None

    def on_train_begin(self, logs=None):
        if logs is None:
            pass
        self.loss = {'batch': [], 'epoch': []}
        self.accuracy = {'batch': [], 'epoch': []}
        self.perplexity = {'batch': [], 'epoch': []}

    def on_batch_end(self, batch, logs=None):
        if logs is None:
            logs = {}
        self.loss['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('accuracy'))
        self.perplexity['batch'].append(logs.get('perplexity'))
        if int(time.time()) % 5 == 0:
            draw_p(self.loss['batch'], 'loss', 'train_batch')
            draw_p(self.accuracy['batch'], 'accuracy', 'train_batch')
            draw_p(self.perplexity['batch'], 'perplexity', 'train_batch')

    def on_epoch_end(self, epoch, logs=None):
        if logs is None:
            logs = {}
        self.loss['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('accuracy'))
        self.perplexity['epoch'].append(logs.get('perplexity'))
        if int(time.time()) % 5 == 0:
            draw_p(self.loss['epoch'], 'loss', 'train_epoch')
            draw_p(self.accuracy['epoch'], 'accuracy', 'train_epoch')
            draw_p(self.perplexity['epoch'], 'perplexity', 'train_epoch')

    def end_draw(self):
        draw_p(self.loss['batch'], 'loss', 'train_batch')
        draw_p(self.accuracy['batch'], 'accuracy', 'train_batch')
        draw_p(self.perplexity['batch'], 'perplexity', 'train_batch')
        draw_p(self.loss['epoch'], 'loss', 'train_epoch')
        draw_p(self.accuracy['epoch'], 'accuracy', 'train_epoch')
        draw_p(self.perplexity['epoch'], 'perplexity', 'train_epoch')


def draw_p(lists, label, type_str):
    plt.figure()
    plt.plot(range(len(lists)), lists, 'r', label=label)
    plt.ylabel(label)
    plt.xlabel(type_str)
    plt.legend(loc='upper right')
    plt.savefig(type_str + '_' + label + '.jpg')
