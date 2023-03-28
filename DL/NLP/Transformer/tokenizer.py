import itertools
import pickle

import nltk
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tqdm import tqdm

from config import MAX_SENTENCE_LENGTH, SET_BS, TGT_VOC_SIZE, DATA_BUFFER_SIZE, TOK_PATH
from data import load_translation_from_code, load_conversation_list_cn


def task_conv_eng(inputs, outputs, new_tokenizer=False, print_sample=True):
    if new_tokenizer:
        print('对话数据读取完成')
        print('条数：', len(inputs), len(outputs))
        print('')
        if print_sample:
            print('打印前10条样本：')
            for i in range(0, 10):
                print(inputs[i])
                print(outputs[i])
                print('====================')
        print('开始初始化词向量生成器')
        tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            inputs + outputs,
            target_vocab_size=TGT_VOC_SIZE
        )
        print('词向量生成器初始化完成')
        tokenizer.save_to_file(TOK_PATH)
        print('词向量生成器已保存')
    else:
        tokenizer = tfds.deprecated.text.SubwordTextEncoder.load_from_file(TOK_PATH)
        print('词向量生成器已读取')
    START_TOKEN, END_TOKEN = [tokenizer.vocab_size], [tokenizer.vocab_size + 1]

    VOCAB_SIZE_WITH_START_AND_END = tokenizer.vocab_size + 2
    return tokenizer, START_TOKEN, END_TOKEN, VOCAB_SIZE_WITH_START_AND_END


def task_conv_chn(inputs, outputs, new_tokenizer=False, print_sample=True):
    if new_tokenizer:
        print('对话数据读取完成')
        print('条数：', len(inputs), len(outputs))
        print('')
        if print_sample:
            print('打印前5条样本：')
            for i in range(0, 5):
                print(inputs[i])
                print(outputs[i])
                print('====================')
        print('开始初始化词向量生成器')
        freq_dist = nltk.FreqDist(itertools.chain(*(inputs + outputs)))
        vocab = freq_dist.most_common(TGT_VOC_SIZE)
        index2word = [x[0] for x in vocab]
        word2index = dict([(w, i) for i, w in enumerate(index2word)])
        print('词向量生成器初始化完成')
        with open(TOK_PATH + '_idx2p.pkl', 'wb') as f:
            pickle.dump(index2word, f)
        with open(TOK_PATH + '_p2idx.pkl', 'wb') as f:
            pickle.dump(word2index, f)
        with open(TOK_PATH + '_fdist.pkl', 'wb') as f:
            pickle.dump(freq_dist, f)
        print('词向量生成器已保存')
    else:
        with open(TOK_PATH + '_idx2p.pkl', 'rb') as f:
            index2word = pickle.load(f)
        with open(TOK_PATH + '_p2idx.pkl', 'rb') as f:
            word2index = pickle.load(f)
        with open(TOK_PATH + '_fdist.pkl', 'rb') as f:
            freq_dist = pickle.load(f)
        print('词向量生成器已读取')
    START_TOKEN, END_TOKEN = word2index['<STA>'], word2index['<END>']

    VOCAB_SIZE_WITH_START_AND_END = len(index2word)
    return [index2word, word2index, freq_dist], START_TOKEN, END_TOKEN, VOCAB_SIZE_WITH_START_AND_END


def tokenize_and_filter(inputs, outputs, task_func, new_tokenizer):
    tokenizer, START_TOKEN, END_TOKEN, VOCAB_SIZE_WITH_START_AND_END = task_func(inputs, outputs, new_tokenizer)
    tokenized_inputs, tokenized_outputs = [], []
    for (sentence1, sentence2) in tqdm(zip(inputs, outputs)):
        # tokenize sentence
        if type(tokenizer) is list:
            word2index = tokenizer[1]
            sentence1 = [word2index[word] for word in sentence1]
            sentence2 = [word2index[word] for word in sentence2]
        else:
            sentence1 = START_TOKEN + tokenizer.encode(sentence1) + END_TOKEN
            sentence2 = START_TOKEN + tokenizer.encode(sentence2) + END_TOKEN
        # check tokenized sentence max length
        if len(sentence1) <= MAX_SENTENCE_LENGTH and len(sentence2) <= MAX_SENTENCE_LENGTH:
            tokenized_inputs.append(sentence1)
            tokenized_outputs.append(sentence2)
    if type(tokenizer) is not list:
        # pad tokenized sentences
        tokenized_inputs = tf.keras.preprocessing.sequence.pad_sequences(
            tokenized_inputs, maxlen=MAX_SENTENCE_LENGTH, padding='post')
        tokenized_outputs = tf.keras.preprocessing.sequence.pad_sequences(
            tokenized_outputs, maxlen=MAX_SENTENCE_LENGTH, padding='post')
    else:
        tokenized_inputs = np.array(tokenized_inputs)
        tokenized_outputs = np.array(tokenized_outputs)

    return tokenized_inputs, tokenized_outputs, VOCAB_SIZE_WITH_START_AND_END


def do_tokenize(que, ans, task_func, new_tokenizer):
    que, ans, v_size = tokenize_and_filter(que, ans, task_func, new_tokenizer)
    print('对话数据向量化完成')
    ds = tf.data.Dataset.from_tensor_slices((
        {
            'inputs': que,
            'dec_inputs': ans[:, :-1]
        },
        {
            'outputs': ans[:, 1:]
        },
    ))

    ds = ds.cache()
    ds = ds.shuffle(DATA_BUFFER_SIZE)
    print('对话数据缓冲完成')
    return ds, v_size


if __name__ == '__main__':
    # questions, answers = load_conversations_from_json('Data/dataset.json')
    # questions2, answers2 = load_conversations_from_csv('Data/20200325_counsel_chat.csv')
    # questions += questions2
    # answers += answers2
    # questions, answers = load_translation_from_lf('Data/europarl-v7.es-en.en', 'Data/europarl-v7.es-en.es')
    # questions, answers = load_translation_from_code()
    questions, answers = load_conversation_list_cn('Data/conv_zh.txt')
    dataset, vocab_size = do_tokenize(questions, answers, task_conv_chn, False)
    dataset = dataset.batch(SET_BS)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
