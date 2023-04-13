# Create the generator.
import tensorflow as tf

from config import generator_in_channels, image_size

k_size = 8
stride1 = 2


def spawn_g():
    assert image_size % (k_size * stride1) == 0
    stride2 = int(image_size / (k_size * stride1))
    generator = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer((generator_in_channels,)),
            # We want to generate 128 + num_classes coefficients to reshape into a
            # 7x7x(128 + num_classes) map.
            tf.keras.layers.Dense(k_size * k_size * generator_in_channels),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Reshape((k_size, k_size, generator_in_channels)),
            tf.keras.layers.Conv2DTranspose(128, (4, 4), strides=(stride1, stride1), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2DTranspose(128, (4, 4), strides=(stride2, stride2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(1, (8, 8), padding="same", activation="sigmoid")
        ],
        name="generator",
    )
    return generator
