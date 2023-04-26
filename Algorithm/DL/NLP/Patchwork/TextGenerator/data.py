import os

import jieba
import numpy as np
import tensorflow as tf
from gensim.models import word2vec

from config import batch_size, image_size, w2v_path, npy_path, forder_path, i2l_path, num_classes

# 设置词语上下文窗口大小
w2v_context_size = 5
w2v_min_word_count = 1
set_max_length = 32


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
    all_labels = tf.keras.utils.to_categorical(all_labels, num_classes)
    # Create tf.data.Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((all_digits, all_labels))
    dataset = dataset.shuffle(buffer_size=1024).batch(batch_size)
    return dataset


def spawn_data_seq():
    all_digits = np.load(npy_path)
    all_labels = np.load(i2l_path)
    # 这里输入的句矩阵已经是归一化的，不需要再归一化了
    # all_digits = all_digits.astype("float32") / np.max(all_digits)
    dim = all_digits.shape[1]
    all_digits = np.reshape(all_digits, (-1, dim, dim, 1))
    all_labels = tf.keras.utils.to_categorical(all_labels, num_classes)
    dataset = tf.data.Dataset.from_tensor_slices((all_digits, all_labels))
    dataset = dataset.shuffle(buffer_size=1024).batch(batch_size)
    return dataset


def seq2array(new_w2v=False):
    def getv(w2v, w):
        return w2v.wv.get_vector(w, True)

    # dir_path = '../Transformer/Data_xiaoice/texts'
    # files = os.listdir(dir_path)
    with open(forder_path, 'r', encoding='utf-8') as f_order:
        files = f_order.readlines()
    files = [file.strip('\n').replace('../', '') for file in files]
    dir_path = '../..'
    all_lines = []
    for file in files:
        # if file.endswith('_mat.txt'):
        if True:
            with open(os.path.join(dir_path, file), 'r', encoding='utf-8') as f:
                all_lines += f.readlines()
    all_lines = [line.split('\t')[1].strip('\n') for line in all_lines]
    all_lines = [jieba.lcut(line) for line in all_lines]
    max_length = 0
    for line in all_lines:
        if len(line) > max_length:
            max_length = len(line)
    max_length = max(max_length, set_max_length)
    for i in range(len(all_lines)):
        last = True
        while len(all_lines[i]) < max_length:
            if last:
                all_lines[i].append('<PAD>')
                last = False
            else:
                all_lines[i].insert(0, '<PAD>')
                last = True
    if new_w2v:
        w2v_mdl = word2vec.Word2Vec(
            all_lines,
            workers=4,
            min_count=w2v_min_word_count,
            window=w2v_context_size,
            vector_size=max_length
            # this is for generate square array
        )
        w2v_mdl.init_sims(replace=True)
        # 输入一个路径，保存训练好的模型，其中./data/model目录事先要存在
        w2v_mdl.save(w2v_path)
    else:
        w2v_mdl = word2vec.Word2Vec.load(w2v_path)

    all_lines = np.array(
        [
            [
                getv(w2v_mdl, word) if w2v_mdl.wv.has_index_for(word) else getv(w2v_mdl, '<PAD>') for word in line
            ] for line in all_lines
        ]
    )
    np.save(npy_path, all_lines)


if __name__ == '__main__':
    seq2array(False)
    spawn_data_seq()
