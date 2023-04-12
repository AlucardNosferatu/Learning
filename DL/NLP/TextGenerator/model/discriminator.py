# Create the discriminator.
import tensorflow as tf

from config import discriminator_in_channels, image_size


def spawn_d():
    discriminator = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer((image_size, image_size, discriminator_in_channels)),
            tf.keras.layers.Conv2D(64, (3, 3), strides=(2, 2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(128, (3, 3), strides=(2, 2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.GlobalMaxPooling2D(),
            tf.keras.layers.Dense(1),
        ],
        name="discriminator",
    )
    return discriminator
