import math

import tensorflow as tf

from config import MAX_SENTENCE_LENGTH


def loss_function(y_true, y_pred):
    y_true = tf.reshape(y_true, shape=(-1, MAX_SENTENCE_LENGTH - 1))

    loss = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction='none')(y_true, y_pred)

    mask = tf.cast(tf.not_equal(y_true, 0), tf.float32)
    loss = tf.multiply(loss, mask)

    return tf.reduce_mean(loss)


def perplexity(real, pred):
    """
    This function returns the perplexity for model's predictions on a batch
    of data in comparison with the real outputs at a timestep.
    Arguments:
        real: real output, a Tensorflow tensor with a shape
              of: (batch_size, max_seq_length)
        pred: model's predictions at a certain timestep, a Tensorflow tensor
              with a shape of: (batch_size, max_seq_length)
    Returns:
        A Tensorflow tensor with the perplexity.
    """
    real = tf.reshape(real, shape=(-1, MAX_SENTENCE_LENGTH - 1))
    loss = loss_function(real, pred)

    return tf.cast(tf.pow(math.e, loss), dtype=tf.keras.backend.floatx())


def accuracy(y_true, y_pred):
    # ensure labels have shape (batch_size, MAX_SENTENCE_LENGTH - 1)
    y_true = tf.reshape(y_true, shape=(-1, MAX_SENTENCE_LENGTH - 1))
    return tf.keras.metrics.sparse_categorical_accuracy(y_true, y_pred)
