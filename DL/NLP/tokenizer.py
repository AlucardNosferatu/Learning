import json
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds

from data import load_conversations, load_conversations_from_csv
from config import MAX_SENTENCE_LENGTH

BUFFER_SIZE = 20000

file = open('Data/dataset.json')
data_json = json.load(file)
questions, answers = load_conversations(data_json)
data_csv = pd.read_csv('Data/20200325_counsel_chat.csv')
questions2, answers2 = load_conversations_from_csv(data_csv)
questions += questions2
answers += answers2
print('对话数据读取完成')
print(len(questions), len(answers))
tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
    questions + answers,
    target_vocab_size=2 ** 13
)
print('词向量生成器初始化完成')

START_TOKEN, END_TOKEN = [tokenizer.vocab_size], [tokenizer.vocab_size + 1]

VOCAB_SIZE = tokenizer.vocab_size + 2


def tokenize_and_filter(inputs, outputs):
    tokenized_inputs, tokenized_outputs = [], []
    for (sentence1, sentence2) in zip(inputs, outputs):
        # tokenize sentence
        sentence1 = START_TOKEN + tokenizer.encode(sentence1) + END_TOKEN
        sentence2 = START_TOKEN + tokenizer.encode(sentence2) + END_TOKEN
        # check tokenized sentence max length
        if len(sentence1) <= MAX_SENTENCE_LENGTH and len(sentence2) <= MAX_SENTENCE_LENGTH:
            tokenized_inputs.append(sentence1)
            tokenized_outputs.append(sentence2)

    # pad tokenized sentences
    tokenized_inputs = tf.keras.preprocessing.sequence.pad_sequences(
        tokenized_inputs, maxlen=MAX_SENTENCE_LENGTH, padding='post')
    tokenized_outputs = tf.keras.preprocessing.sequence.pad_sequences(
        tokenized_outputs, maxlen=MAX_SENTENCE_LENGTH, padding='post')

    return tokenized_inputs, tokenized_outputs


def do_tokenize(que, ans):
    que, ans = tokenize_and_filter(que, ans)
    print('对话数据向量化完成')
    dataset = tf.data.Dataset.from_tensor_slices((
        {
            'inputs': que,
            'dec_inputs': ans[:, :-1]
        },
        {
            'outputs': ans[:, 1:]
        },
    ))

    dataset = dataset.cache()
    dataset = dataset.shuffle(BUFFER_SIZE)
    print('对话数据缓冲完成')
    return dataset
