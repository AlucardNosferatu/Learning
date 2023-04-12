# Create the generator.
import tensorflow as tf

from config import generator_in_channels


def spawn_g():
    generator = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer((generator_in_channels,)),
            # We want to generate 128 + num_classes coefficients to reshape into a
            # 7x7x(128 + num_classes) map.
            tf.keras.layers.Dense(7 * 7 * generator_in_channels),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Reshape((7, 7, generator_in_channels)),
            tf.keras.layers.Conv2DTranspose(128, (4, 4), strides=(2, 2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2DTranspose(128, (4, 4), strides=(2, 2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(1, (7, 7), padding="same", activation="sigmoid"),
        ],
        name="generator",
    )
    return generator
