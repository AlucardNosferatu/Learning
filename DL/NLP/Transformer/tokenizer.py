import tensorflow as tf
import tensorflow_datasets as tfds
from tqdm import tqdm

import config
from config import MAX_SENTENCE_LENGTH, BSIZE, TGT_VOC_SIZE, DATA_BUFFER_SIZE, TOK_PATH
from data import load_conversations_from_json, load_conversations_from_csv, load_translation


def set_max_sentence_length(msl):
    config.MAX_SENTENCE_LENGTH = msl


def conv_task(inputs, outputs, new_tokenizer=False, print_sample=True):
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


def tran_task(inputs, outputs, new_tokenizer=False):
    if new_tokenizer:
        tokenizer_en = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            inputs,
            target_vocab_size=TGT_VOC_SIZE
        )
        tokenizer_es = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            outputs,
            target_vocab_size=TGT_VOC_SIZE
        )
        tokenizer_en.save_to_file(TOK_PATH + '_en')
        tokenizer_es.save_to_file(TOK_PATH + '_es')
    else:
        tokenizer_en = tfds.deprecated.text.SubwordTextEncoder.load_from_file(TOK_PATH + '_en')
        tokenizer_es = tfds.deprecated.text.SubwordTextEncoder.load_from_file(TOK_PATH + '_es')
    v_size_en = tokenizer_en.vocab_size + 2
    v_size_es = tokenizer_es.vocab_size + 2
    MAX_LENGTH = 0
    for i in tqdm(inputs + outputs):
        longitud = len(tokenizer_es.encode(i))
        if MAX_LENGTH < longitud:
            MAX_LENGTH = longitud
    set_max_sentence_length(MAX_LENGTH)
    START_TOKEN, END_TOKEN = None, None
    return [tokenizer_en, tokenizer_es], START_TOKEN, END_TOKEN, [v_size_en, v_size_es]


def tokenize_and_filter(inputs, outputs, task_func, new_tokenizer):
    tokenizer, START_TOKEN, END_TOKEN, VOCAB_SIZE_WITH_START_AND_END = task_func(inputs, outputs, new_tokenizer)
    tokenized_inputs, tokenized_outputs = [], []
    for (sentence1, sentence2) in tqdm(zip(inputs, outputs)):
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
    questions, answers = load_translation('Data/europarl-v7.es-en.en', 'Data/europarl-v7.es-en.es')
    dataset, vocab_size = do_tokenize(questions, answers, tran_task, True)
    dataset = dataset.batch(BSIZE)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
