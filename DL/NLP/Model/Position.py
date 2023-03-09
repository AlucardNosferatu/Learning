import numpy as np
import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer


def get_angle(pos, dim, d_model):
    return pos / np.power(10000, 2 * (dim // 2) / d_model)


def get_positional_angle(pos, d_model):
    return [get_angle(pos, dim, d_model) for dim in range(d_model)]


class SinusoidalPositionalEncoding(Layer):
    # Inspired from https://github.com/graykode/nlp-tutorial/blob/master/5-1.Transformer/Transformer_Torch.ipynb
    def __init__(self, d_model, max_token_length):
        super(SinusoidalPositionalEncoding, self).__init__()
        self.sinusoidal_encoding = np.array([get_positional_angle(pos, d_model) for pos in range(max_token_length)],
                                            dtype=np.float32)
        self.sinusoidal_encoding[:, 0::2] = np.sin(self.sinusoidal_encoding[:, 0::2])
        self.sinusoidal_encoding[:, 1::2] = np.cos(self.sinusoidal_encoding[:, 1::2])
        self.sinusoidal_encoding = tf.cast(self.sinusoidal_encoding,
                                           dtype=tf.float32)  # Casting the array to Tensor for slicing

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x):
        return x + self.sinusoidal_encoding[:tf.shape(x)[1]]
        # return x + tf.slice(self.sinusoidal_encoding, [0, 0], [tf.shape(x)[1], d_model])

    def compute_output_shape(self, input_shape):
        return input_shape
