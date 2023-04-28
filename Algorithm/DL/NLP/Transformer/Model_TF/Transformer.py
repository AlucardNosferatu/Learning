import tensorflow as tf

from Model_TF.Decoder import decoder
from Model_TF.Encoder import encoder
from Model_TF.Masking import create_padding_mask, create_look_ahead_mask


def transformer(
        vocab_size,
        num_layers,
        units,
        word_vec_dim,
        num_heads,
        dropout,
        name="transformer"
):
    inputs = tf.keras.Input(shape=(None,), name="inputs")
    enc_padding_mask = tf.keras.layers.Lambda(
        create_padding_mask, output_shape=(1, 1, None),
        name='enc_padding_mask')(inputs)
    dec_padding_mask = tf.keras.layers.Lambda(
        create_padding_mask, output_shape=(1, 1, None),
        name='dec_padding_mask')(inputs)

    dec_inputs = tf.keras.Input(shape=(None,), name="dec_inputs")
    look_ahead_mask = tf.keras.layers.Lambda(
        create_look_ahead_mask,
        output_shape=(1, None, None),
        name='look_ahead_mask')(dec_inputs)
    # mask the encoder outputs for the 2nd attention block

    enc_outputs = encoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        word_vec_dim=word_vec_dim,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[inputs, enc_padding_mask])

    dec_outputs = decoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        d_model=word_vec_dim,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[dec_inputs, enc_outputs, look_ahead_mask, dec_padding_mask])

    outputs = tf.keras.layers.Dense(units=vocab_size, name="outputs")(dec_outputs)

    return tf.keras.Model(inputs=[inputs, dec_inputs], outputs=outputs, name=name)


if __name__ == '__main__':
    print('Done')
