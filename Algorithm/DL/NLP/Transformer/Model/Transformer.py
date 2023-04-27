import numpy as np
import tensorflow as tf

from Model.Decoder import decoder
from Model.Encoder import encoder
from Model.Masking import create_padding_mask, create_look_ahead_mask
from config import MAX_SL, N_LAYERS, UNITS, WORD_VEC_DIM, N_HEADS, DROP, TGT_VOC_SIZE


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


def transformer_encoder_only(
        seq_length,
        # vocab_size,
        # num_layers,
        # units,
        # word_vec_dim,
        # num_heads,
        # dropout,
        transformer_encoder,
        name="transformer_encoder_only"
):
    inputs = tf.keras.Input(shape=(seq_length,), name="inputs")
    causal_attention_mask = tf.constant(
        np.triu(
            np.ones(
                (1, 1, seq_length, seq_length),
                dtype="float32"
            ) * -np.inf,
            k=1
        )
    )
    # enc_outputs = encoder(
    #     vocab_size=vocab_size,
    #     num_layers=num_layers,
    #     units=units,
    #     word_vec_dim=word_vec_dim,
    #     num_heads=num_heads,
    #     dropout=dropout,
    # )(inputs=[inputs, causal_attention_mask])
    transformer_encoder.trainable = False
    enc_outputs = transformer_encoder(inputs=[inputs, causal_attention_mask])
    output = tf.keras.layers.LayerNormalization(epsilon=1e-5)(enc_outputs)
    # 因为只用了编码器，自然不需要dec_inputs
    return tf.keras.Model(inputs=inputs, outputs=output, name=name)


if __name__ == '__main__':
    t_full = transformer(
        vocab_size=TGT_VOC_SIZE,
        num_layers=N_LAYERS,
        units=UNITS,
        word_vec_dim=WORD_VEC_DIM,
        num_heads=N_HEADS,
        dropout=DROP,
        name="transformer"
    )
    t_encoder = transformer_encoder_only(
        seq_length=MAX_SL,
        # vocab_size=TGT_VOC_SIZE,
        # num_layers=N_LAYERS,
        # units=UNITS,
        # word_vec_dim=WORD_VEC_DIM,
        # num_heads=N_HEADS,
        # dropout=DROP,
        transformer_encoder=t_full.get_layer(name='encoder')
    )
    print('Done')
