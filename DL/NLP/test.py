import pickle

import numpy as np
import tensorflow as tf

from Model.Transformer import TransformerModel
from data import preprocess
from tokenizer import source_tokenizer, target_tokenizer

config_file = open('Save/config.pkl', 'rb')
model_spec = pickle.load(config_file)
instance = TransformerModel(
    n_heads=model_spec['n_heads'],
    d_v=model_spec['d_v'],
    d_k=model_spec['d_k'],
    d_model=model_spec['d_model'],
    max_token_length=model_spec['max_token_length'],
    n_encoder_layers=model_spec['n_encoder_layers'],
    n_decoder_layers=model_spec['n_decoder_layers'],
    dropout=model_spec['dropout']
)

instance.load_weights('Save/instance.h5')


def translate(model, source_sentence, target_sentence_start=None):
    if target_sentence_start is None:
        target_sentence_start = [['<start>']]
    if np.ndim(source_sentence) == 1:  # Create a batch of 1 the input is a sentence
        source_sentence = [source_sentence]
    if np.ndim(target_sentence_start) == 1:
        target_sentence_start = [target_sentence_start]
    # Tokenizing and padding
    source_seq = source_tokenizer.texts_to_sequences(source_sentence)
    source_seq = tf.keras.preprocessing.sequence.pad_sequences(source_seq, padding='post', maxlen=15)
    predict_seq = target_tokenizer.texts_to_sequences(target_sentence_start)

    predict_sentence = list(target_sentence_start[0])  # Deep copy here to prevent updates on target_sentence_start
    while predict_sentence[-1] != '<end>' and len(predict_seq) < model_spec['max_token_length']:
        predict_output = model([np.array(source_seq), np.array(predict_seq)], training=None)
        predict_label = tf.argmax(predict_output, axis=-1)  # Pick the label with highest softmax score
        predict_seq = tf.concat([predict_seq, predict_label], axis=-1)  # Updating the prediction sequence
        predict_sentence.append(target_tokenizer.index_word[predict_label[0][0].numpy()])

    return predict_sentence


print("Predicted sentence: ", ' '.join(translate(instance, preprocess("Do you want me to make coffee?").split(' '))))
