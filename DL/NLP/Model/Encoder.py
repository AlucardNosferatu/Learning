import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.layers import LayerNormalization, Dense

from Model.Attention import MultiHeadAttention


class TransformerEncoder(Layer):
    def __init__(self, n_heads, d_v, d_k, d_model, dropout=.1, attention_dropout=.0, **kwargs):
        self.n_heads = n_heads
        self.d_v = d_v
        self.d_k = d_k
        self.d_model = d_model
        super(TransformerEncoder, self).__init__(**kwargs)
        self.dropout_rate = dropout
        self.attention_dropout_rate = attention_dropout

    def build(self, input_shape):
        self.multi_head_attention = MultiHeadAttention(
            n_heads=self.n_heads,
            d_v=self.d_v,
            d_k=self.d_k,
            d_model=self.d_model,
            dropout=self.attention_dropout_rate
        )
        self.dropout1 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization1 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)

        self.linear1 = Dense(input_shape[-1] * 4, input_shape=input_shape, activation='relu',
                             kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform')
        self.linear2 = Dense(input_shape[-1], input_shape=self.linear1.compute_output_shape(input_shape),
                             kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform')
        self.dropout2 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization2 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)
        super(TransformerEncoder, self).build(input_shape)

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x, training=None):
        sublayer1 = self.multi_head_attention((x, x, x), training=training)
        sublayer1 = self.dropout1(sublayer1, training=training)
        layer_norm1 = self.layer_normalization1(x + sublayer1)

        sublayer2 = self.linear2(self.linear1(layer_norm1))
        layer_norm2 = self.layer_normalization2(layer_norm1 + sublayer2)
        return layer_norm2

    def compute_output_shape(self, input_shape):
        return input_shape
