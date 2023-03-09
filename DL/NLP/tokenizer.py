import numpy as np
import tensorflow as tf

from data import source_sentences, target_sentences

# In this illustration, I choose not to specify num_words and oov_token due to the size of data.
# for details, please visit https://keras.io/preprocessing/text/
source_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
source_tokenizer.fit_on_texts(source_sentences)
source_data = source_tokenizer.texts_to_sequences(source_sentences)
source_data = tf.keras.preprocessing.sequence.pad_sequences(source_data, padding='post')

target_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
target_tokenizer.fit_on_texts(target_sentences)
target_data = target_tokenizer.texts_to_sequences(target_sentences)
target_data = tf.keras.preprocessing.sequence.pad_sequences(target_data, padding='post')

target_labels = np.zeros(target_data.shape)
target_labels[:, 0:target_data.shape[1] - 1] = target_data[:, 1:]

source_vocab_len = len(source_tokenizer.word_index) + 1
target_vocab_len = len(target_tokenizer.word_index) + 1
