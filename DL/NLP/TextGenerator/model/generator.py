# Create the generator.
import tensorflow as tf

from config import generator_in_channels, image_size

first_fm_size = 4
stride1 = 4


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
            tf.keras.layers.Conv2DTranspose(256, (2, 2), strides=(stride1, stride1), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2DTranspose(256, (2, 2), strides=(stride2, stride2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(64, (2, 2), padding="same"),
            tf.keras.layers.LeakyReLU(alpha=0.2),
            tf.keras.layers.Conv2D(1, (4, 4), padding="same", activation="sigmoid")
        ],
        name="generator",
    )
    return generator


def spawn_g_conv1d():
    assert image_size % (first_fm_size * stride1) == 0
    stride2 = int(image_size / (first_fm_size * stride1))
    generator = tf.keras.Sequential()
    generator.add(
        tf.keras.layers.InputLayer((generator_in_channels,))
    )
    generator.add(
        tf.keras.layers.Dense(first_fm_size * generator_in_channels)
    )
    generator.add(
        tf.keras.layers.LeakyReLU(alpha=0.2)
    )
    generator.add(
        tf.keras.layers.Reshape((first_fm_size, generator_in_channels)),
    )
    generator.add(
        tf.keras.layers.Conv1DTranspose(256, 2, stride1, padding="same")
    )
    generator.add(
        tf.keras.layers.LeakyReLU(alpha=0.2)
    )
    generator.add(
        tf.keras.layers.Conv1DTranspose(256, 2, stride2, padding="same")
    )
    generator.add(
        tf.keras.layers.LeakyReLU(alpha=0.2)
    )
    generator.add(
        tf.keras.layers.Reshape((1, image_size, 256)),
    )
    generator.add(
        tf.keras.layers.Conv2DTranspose(1, (1, 2), (image_size, 1), padding="same", activation="sigmoid")
    )
    return generator


if __name__ == '__main__':
    spawn_g_conv1d()
