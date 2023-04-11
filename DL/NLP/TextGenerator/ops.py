import tensorflow as tf
from tensorflow import keras


class Sigmoid(tf.keras.layers.Layer):

    def __init__(self):
        super(Sigmoid, self).__init__()

    def call(self, inputs, **kwargs):
        return keras.activations.sigmoid(inputs)


class Tanh(tf.keras.layers.Layer):
    def __init__(self):
        super(Tanh, self).__init__()

    def call(self, inputs, **kwargs):
        return keras.activations.tanh(inputs)


class Conv2D(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size, strides=2):
        super(Conv2D, self).__init__()
        self.conv_op = tf.keras.layers.Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding='same',
            kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.02),
            use_bias=True,
            bias_initializer=keras.initializers.Constant(value=0.0)
        )

    def call(self, inputs, **kwargs):
        return self.conv_op(inputs)


class BatchNorm(tf.keras.layers.Layer):
    def __init__(self, is_training=False):
        super(BatchNorm, self).__init__()
        self.bn = tf.keras.layers.BatchNormalization(
            epsilon=1e-5,
            momentum=0.9,
            scale=True,
            trainable=is_training
        )

    # noinspection PyMethodOverriding
    def call(self, inputs, training):
        x = self.bn(inputs, training=training)
        return x


class DenseLayer(tf.keras.layers.Layer):
    def __init__(self, hidden_n):
        super(DenseLayer, self).__init__()
        self.fc_op = tf.keras.layers.Dense(
            hidden_n,
            kernel_initializer=keras.initializers.RandomNormal(stddev=0.02),
            bias_initializer=keras.initializers.Constant(value=0.0)
        )

    def call(self, inputs, **kwargs):
        x = self.fc_op(inputs)

        return x


class UpConv2D(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size, strides):
        super(UpConv2D, self).__init__()
        self.up_conv_op = tf.keras.layers.Conv2DTranspose(
            filters,
            kernel_size=kernel_size,
            strides=strides,
            padding='same',
            kernel_initializer=keras.initializers.RandomNormal(stddev=0.02),
            use_bias=True,
            bias_initializer=keras.initializers.Constant(value=0.0)
        )

    def call(self, inputs, **kwargs):
        x = self.up_conv_op(inputs)
        return x


def conv_cond_concat(x, y):
    """Concatenate conditioning vector on feature map axis."""
    x_shapes = tf.shape(x)
    y_shapes = tf.shape(y)
    y = tf.reshape(y, [-1, 1, 1, y_shapes[1]])
    y_shapes = tf.shape(y)
    return tf.concat([x, y * tf.ones([x_shapes[0], x_shapes[1], x_shapes[2], y_shapes[3]])], 3)
