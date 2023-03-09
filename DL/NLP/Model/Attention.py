import numpy as np
import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.layers import Dense, Lambda


class SingleHeadAttention(Layer):
    # noinspection PyShadowingNames,PyUnusedLocal
    def __init__(self, d_k, d_v, d_model, dropout=.0, masked=None):
        # input_shape = (3, -1, d_model)
        super(SingleHeadAttention, self).__init__()
        self.q = Dense(d_k, input_shape=(-1, d_model), kernel_initializer='glorot_uniform',
                       bias_initializer='glorot_uniform')
        self.normalize_q = Lambda(lambda x: x / np.sqrt(d_k))
        self.k = Dense(d_k, input_shape=(-1, d_model), kernel_initializer='glorot_uniform',
                       bias_initializer='glorot_uniform')
        self.v = Dense(d_v, input_shape=(-1, d_model), kernel_initializer='glorot_uniform',
                       bias_initializer='glorot_uniform')
        self.dropout = dropout
        self.masked = masked

    # Inputs: [query, key, value]
    # noinspection PyMethodOverriding
    def call(self, inputs, training=None):
        assert len(inputs) == 3
        # We use a lambda layer to divide vector q by sqrt(d_k) according to the equation
        q = self.normalize_q(self.q(inputs[0]))
        k = self.k(inputs[1])
        # The dimensionality of q is (batch_size, query_length, d_k) and that of k is (batch_size, key_length, d_k)
        # So we will do a matrix multiplication by batch after transposing last 2 dimensions of k
        # tf.shape(attn_weights) = (batch_size, query_length, key_length)
        attn_weights = tf.matmul(q, tf.transpose(k, perm=[0, 2, 1]))
        if self.masked:  # Prevent future attentions in decoding self-attention
            # Create a matrix where the strict upper triangle (not including main diagonal) is filled with -inf and 0
            # elsewhere
            length = tf.shape(attn_weights)[-1]
            # attn_mask = np.triu(tf.fill((length, length), -np.inf), k=1)
            # We need to use tensorflow functions instead of numpy
            attn_mask = tf.fill((length, length), -np.inf)
            attn_mask = tf.linalg.band_part(attn_mask, 0, -1)  # Get upper triangle
            attn_mask = tf.linalg.set_diag(attn_mask,
                                           tf.zeros(length))  # Set diagonal to zeros to avoid operations with infinity
            # This matrix is added to the attention weights so all future attention will have -inf logits (0 after
            # softmax)
            attn_weights += attn_mask
        # Softmax along the last dimension
        attn_weights = tf.nn.softmax(attn_weights, axis=-1)
        if training:
            # Attention dropout included in the original paper. This is possibly to encourage multi-head diversity.
            attn_weights = tf.nn.dropout(attn_weights, rate=self.dropout)
        v = self.v(inputs[2])
        return tf.matmul(attn_weights, v)


class MultiHeadAttention(Layer):
    def __init__(self, n_heads, d_k, d_v, d_model, dropout=.0, masked=None):
        self.n_heads = n_heads
        super(MultiHeadAttention, self).__init__()
        self.attn_heads = list()
        for i in range(self.n_heads):
            self.attn_heads.append(
                SingleHeadAttention(d_k=d_k, d_v=d_v, d_model=d_model, dropout=dropout, masked=masked))
        self.linear = Dense(d_model, input_shape=(-1, self.n_heads * d_v), kernel_initializer='glorot_uniform',
                            bias_initializer='glorot_uniform')

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x, training=None):
        attentions = [self.attn_heads[i](x, training=training) for i in range(self.n_heads)]
        concatenated_attentions = tf.concat(attentions, axis=-1)
        return self.linear(concatenated_attentions)
