import tensorflow as tf

from config import batch_size, latent_dim


def get_noise_with_condition(one_hot_labels):
    random_latent_vectors = tf.random.normal(shape=(batch_size, latent_dim))
    random_vector_labels = tf.concat(
        [random_latent_vectors, one_hot_labels], axis=1
    )
    return random_vector_labels

