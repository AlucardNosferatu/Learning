import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Embedding

from Model.Decoder import TransformerDecoder
from Model.Encoder import TransformerEncoder
from Model.Position import SinusoidalPositionalEncoding
from tokenizer import source_vocab_len, target_vocab_len


class TransformerModel(Model):
    def get_config(self):
        pass

    def __init__(self, n_heads, d_v, d_k, d_model, max_token_length, n_encoder_layers, n_decoder_layers, dropout=.1,
                 attention_dropout=.0, **kwargs):
        super(TransformerModel, self).__init__(**kwargs)
        self.encoding_embedding = Embedding(source_vocab_len, d_model)
        self.decoding_embedding = Embedding(target_vocab_len, d_model)
        self.pos_encoding = SinusoidalPositionalEncoding(d_model, max_token_length)
        self.encoder = [
            TransformerEncoder(n_heads, d_v, d_k, d_model, dropout=dropout, attention_dropout=attention_dropout) for _
            in
            range(n_encoder_layers)
        ]
        self.decoder = [
            TransformerDecoder(n_heads, d_v, d_k, d_model, dropout=dropout, attention_dropout=attention_dropout) for _
            in
            range(n_decoder_layers)
        ]
        self.decoder_final = Dense(target_vocab_len, input_shape=(None, d_model))

    # noinspection PyMethodOverriding
    def call(self, inputs, training=None):  # Source_sentence and decoder_input
        source_sentence, decoder_input = inputs
        embedded_source = self.encoding_embedding(source_sentence)
        encoder_output = self.pos_encoding(embedded_source)
        for encoder_unit in self.encoder:
            encoder_output = encoder_unit(encoder_output, training=training)

        embedded_target = self.decoding_embedding(decoder_input)
        decoder_output = self.pos_encoding(embedded_target)
        for decoder_unit in self.decoder:
            decoder_output = decoder_unit(decoder_output, encoder_output, training=training)
        if training:
            decoder_output = self.decoder_final(decoder_output)
            decoder_output = tf.nn.softmax(decoder_output, axis=-1)
        else:
            decoder_output = self.decoder_final(decoder_output[:, -1:, :])
            decoder_output = tf.nn.softmax(decoder_output, axis=-1)
        return decoder_output
