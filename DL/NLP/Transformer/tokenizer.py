import json
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds
from tqdm import tqdm
from data import load_conversations, load_conversations_from_csv
from config import MAX_SENTENCE_LENGTH, BATCH_SIZE, TARGET_VOCAB_SIZE, DATA_BUFFER_SIZE

file = open('Data/dataset.json')
data_json = json.load(file)
questions, answers = load_conversations(data_json)
data_csv = pd.read_csv('Data/20200325_counsel_chat.csv')
questions2, answers2 = load_conversations_from_csv(data_csv)
questions += questions2
answers += answers2
print('对话数据读取完成')
print('条数：', len(questions), len(answers))
print('')
print_sample = True
if print_sample:
    print('打印前10条样本：')
    for i in range(0, 10):
        print(questions[i])
        print(answers[i])
        print('====================')
new_tokenizer = False
if new_tokenizer:
    print('开始初始化词向量生成器')
    tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
        questions + answers,
        target_vocab_size=TARGET_VOCAB_SIZE
    )
    print('词向量生成器初始化完成')
    tokenizer.save_to_file('Save/tokenizer')
    print('词向量生成器已保存')
else:
    tokenizer = tfds.deprecated.text.SubwordTextEncoder.load_from_file('Save/tokenizer')
    print('词向量生成器已读取')
START_TOKEN, END_TOKEN = [tokenizer.vocab_size], [tokenizer.vocab_size + 1]

VOCAB_SIZE_WITH_START_AND_END = tokenizer.vocab_size + 2


def tokenize_and_filter(inputs, outputs):
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

    return tokenized_inputs, tokenized_outputs


def do_tokenize(que, ans):
    que, ans = tokenize_and_filter(que, ans)
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
    return ds


if __name__ == '__main__':
    dataset = do_tokenize(questions, answers)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
