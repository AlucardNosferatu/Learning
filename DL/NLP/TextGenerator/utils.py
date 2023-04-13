import numpy as np
from gensim.models import word2vec

from config import noise_dim, num_classes, w2v_path


def load_w2v():
    w2v_mdl = word2vec.Word2Vec.load(w2v_path)
    return w2v_mdl


def convert_array(array, w2v=None):
    if w2v is None:
        w2v = load_w2v()
    # array.shape == (batch_size, word_vec_order, seq_order, 1)
    batch_size_this = array.shape[0]
    sentence_length = array.shape[2]
    res = []
    for i in range(batch_size_this):
        sent = []
        for j in range(sentence_length):
            sent.append(
                w2v.wv.most_similar(
                    positive=[array[i, :, j, 0]],
                    topn=1
                )
            )
        res.append(sent)
    return res, w2v


def get_noise_with_condition(label_list):
    batch_size_this = len(label_list)
    one_hot_labels = np.zeros(shape=(batch_size_this, num_classes))
    for i in range(batch_size_this):
        one_hot_labels[i, label_list[i]] = 1
    random_latent_vectors = np.random.normal(size=(batch_size_this, noise_dim))
    random_vector_labels = np.concatenate(
        [random_latent_vectors, one_hot_labels], axis=1
    )
    return random_vector_labels


if __name__ == '__main__':
    get_noise_with_condition([0, 1, 2, 3, 4])
