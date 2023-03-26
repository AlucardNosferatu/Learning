import tensorflow as tf
import tensorflow_datasets as tfds
from tqdm import tqdm

from config import MAX_SENTENCE_LENGTH, BATCH_SIZE, TARGET_VOCAB_SIZE, DATA_BUFFER_SIZE, TOK_PATH
from data import load_conversations_from_json, load_conversations_from_csv


def conv_task(inputs, outputs, new_tokenizer=False, print_sample=True):
    print('对话数据读取完成')
    print('条数：', len(inputs), len(outputs))
    print('')
    if print_sample:
        print('打印前10条样本：')
        for i in range(0, 10):
            print(inputs[i])
            print(outputs[i])
            print('====================')

    if new_tokenizer:
        print('开始初始化词向量生成器')
        tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            inputs + outputs,
            target_vocab_size=TARGET_VOCAB_SIZE
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


def tokenize_and_filter(inputs, outputs, task_func, new_tokenizer):
    tokenizer, START_TOKEN, END_TOKEN, VOCAB_SIZE_WITH_START_AND_END = task_func(inputs, outputs, new_tokenizer, False)
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


def do_tokenize(que, ans, task_func, new_tokenizer):
    que, ans = tokenize_and_filter(que, ans, task_func, new_tokenizer)
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
    questions, answers = load_conversations_from_json('Data/dataset.json')
    questions2, answers2 = load_conversations_from_csv('Data/20200325_counsel_chat.csv')
    questions += questions2
    answers += answers2
    dataset = do_tokenize(questions, answers, conv_task, True)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
