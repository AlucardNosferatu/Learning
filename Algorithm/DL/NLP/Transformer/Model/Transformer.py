import numpy as np
import tensorflow as tf

from Model.Decoder import decoder
from Model.Encoder import encoder
from Model.Masking import create_padding_mask, create_look_ahead_mask


def transformer(
        vocab_size,
        num_layers,
        units,
        d_model,
        num_heads,
        dropout,
        name="transformer"
):
    inputs = tf.keras.Input(shape=(None,), name="inputs")
    dec_inputs = tf.keras.Input(shape=(None,), name="dec_inputs")

    enc_padding_mask = tf.keras.layers.Lambda(
        create_padding_mask, output_shape=(1, 1, None),
        name='enc_padding_mask')(inputs)
    # mask the future tokens for decoder inputs at the 1st attention block
    look_ahead_mask = tf.keras.layers.Lambda(
        create_look_ahead_mask,
        output_shape=(1, None, None),
        name='look_ahead_mask')(dec_inputs)
    # mask the encoder outputs for the 2nd attention block
    dec_padding_mask = tf.keras.layers.Lambda(
        create_padding_mask, output_shape=(1, 1, None),
        name='dec_padding_mask')(inputs)

    enc_outputs = encoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        d_model=d_model,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[inputs, enc_padding_mask])

    dec_outputs = decoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        d_model=d_model,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[dec_inputs, enc_outputs, look_ahead_mask, dec_padding_mask])

    outputs = tf.keras.layers.Dense(units=vocab_size, name="outputs")(dec_outputs)

    return tf.keras.Model(inputs=[inputs, dec_inputs], outputs=outputs, name=name)


def transformer_encoder_only(
        vocab_size,
        num_layers,
        units,
        d_model,
        num_heads,
        dropout,
        name="transformer_encoder_only"
):
    inputs = tf.keras.Input(shape=(None,), name="inputs")
    causal_attention_mask = tf.constant(
        np.triu(
            np.ones(
                (1, 1, 77, 77),
                dtype="float32"
            ) * -np.inf,
            k=1
        )
    )
    enc_outputs = encoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        d_model=d_model,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[inputs, causal_attention_mask])
    output = tf.keras.layers.LayerNormalization(epsilon=1e-5)(enc_outputs)
    # 因为只用了编码器，自然不需要dec_inputs
    return tf.keras.Model(inputs=inputs, outputs=output, name=name)
