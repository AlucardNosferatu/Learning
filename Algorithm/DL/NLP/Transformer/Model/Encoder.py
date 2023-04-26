import tensorflow as tf

from Model.Attention import MultiHeadAttention
from Model.Position import PositionalEncoding


def encoder_layer(units, word_vec_dim, num_heads, dropout, name="encoder_layer"):
    inputs = tf.keras.Input(shape=(None, word_vec_dim), name="inputs")
    padding_mask = tf.keras.Input(shape=(1, None, None), name="padding_mask")

    attention = MultiHeadAttention(
        word_vec_dim,
        num_heads,
        name="attention"
    ).call(
        {
            'query': inputs,
            'key': inputs,
            'value': inputs,
            'mask': padding_mask
        }
    )
    attention = tf.keras.layers.Dropout(rate=dropout)(attention)
    attention = tf.keras.layers.LayerNormalization(
        epsilon=1e-6)(inputs + attention)

    outputs = tf.keras.layers.Dense(units=units, activation='relu')(attention)
    outputs = tf.keras.layers.Dense(units=word_vec_dim)(outputs)
    outputs = tf.keras.layers.Dropout(rate=dropout)(outputs)
    outputs = tf.keras.layers.LayerNormalization(
        epsilon=1e-6)(attention + outputs)

    return tf.keras.Model(
        inputs=[inputs, padding_mask], outputs=outputs, name=name
    )


def encoder(vocab_size,
            num_layers,
            units,
            word_vec_dim,
            num_heads,
            dropout,
            name="encoder"):
    inputs = tf.keras.Input(shape=(None,), name="inputs")
    padding_mask = tf.keras.Input(shape=(1, None, None), name="padding_mask")

    embeddings = tf.keras.layers.Embedding(vocab_size, word_vec_dim)(inputs)
    embeddings *= tf.math.sqrt(tf.cast(word_vec_dim, tf.float32))
    # CLIP模型这里没有使用正弦编码，而是用了另一个嵌入层（可训练）来编码位置信息
    # 我偷懒先不改这个，编码功能上没变化就行（不改还能少写一个从0到max_len的pos_id输入）
    embeddings = PositionalEncoding(vocab_size, word_vec_dim).call(embeddings)
    outputs = tf.keras.layers.Dropout(rate=dropout)(embeddings)

    for i in range(num_layers):
        outputs = encoder_layer(
            units=units,
            word_vec_dim=word_vec_dim,
            num_heads=num_heads,
            dropout=dropout,
            name="encoder_layer_{}".format(i),
        )([outputs, padding_mask])

    return tf.keras.Model(
        inputs=[inputs, padding_mask], outputs=outputs, name=name)
