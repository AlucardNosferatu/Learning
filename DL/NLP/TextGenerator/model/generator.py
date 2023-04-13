# Create the generator.
import tensorflow as tf

from config import generator_in_channels, image_size

first_fm_size = 8
stride1 = 2


def spawn_g():
    assert image_size % (first_fm_size * stride1) == 0
    stride2 = int(image_size / (first_fm_size * stride1))
    generator = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer((generator_in_channels,)),
            # We want to generate 128 + num_classes coefficients to reshape into a
            # 7x7x(128 + num_classes) map.
            tf.keras.layers.Dense(first_fm_size * first_fm_size * generator_in_channels),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Reshape((first_fm_size, first_fm_size, generator_in_channels)),
            tf.keras.layers.Conv2DTranspose(256, (4, 4), strides=(stride1, stride1), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2DTranspose(256, (4, 4), strides=(stride2, stride2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(64, (4, 4), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(1, (4, 4), padding="same", activation="sigmoid")
        ],
        name="generator",
    )
    return generator
