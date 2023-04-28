import tensorflow as tf


def get_angles(position, i, word_vec_dim):
    angles = 1 / tf.pow(10000, (2 * (i // 2)) / tf.cast(word_vec_dim, tf.float32))
    return position * angles


def positional_encoding(vocab_size, word_vec_dim):
    angle_rads = get_angles(
        position=tf.range(vocab_size, dtype=tf.float32)[:, tf.newaxis],
        i=tf.range(word_vec_dim, dtype=tf.float32)[tf.newaxis, :],
        word_vec_dim=word_vec_dim
    )
    # apply sin to even index in the array
    sines = tf.math.sin(angle_rads[:, 0::2])
    # apply cos to odd index in the array
    cosines = tf.math.cos(angle_rads[:, 1::2])

    pos_encoding = tf.concat([sines, cosines], axis=-1)
    pos_encoding = pos_encoding[tf.newaxis, ...]
    return tf.cast(pos_encoding, tf.float32)


class PositionalEncoding(tf.keras.layers.Layer):

    def __init__(self, vocab_size, word_vec_dim):
        super(PositionalEncoding, self).__init__()
        self.pos_encoding = positional_encoding(vocab_size, word_vec_dim)

    def call(self, inputs, **kwargs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]
