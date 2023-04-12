import numpy as np
import tensorflow as tf

from config import batch_size, image_size


def spawn_data():
    # We'll use all the available examples from both the training and test
    # sets.
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    all_digits = np.concatenate([x_train, x_test])
    all_labels = np.concatenate([y_train, y_test])
    # Scale the pixel values to [0, 1] range, add a channel dimension to
    # the images, and one-hot encode the labels.
    all_digits = all_digits.astype("float32") / 255.0
    all_digits = np.reshape(all_digits, (-1, image_size, image_size, 1))
    all_labels = tf.keras.utils.to_categorical(all_labels, 10)
    # Create tf.data.Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((all_digits, all_labels))
    dataset = dataset.shuffle(buffer_size=1024).batch(batch_size)
    return dataset


if __name__ == '__main__':
    d = spawn_data()
