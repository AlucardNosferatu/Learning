import json
import re

import jieba
import pandas as pd
import unicodedata
from tqdm import tqdm

from config import MAX_SENTENCE_LENGTH


def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "that is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"n't", " not", text)
    return text


# noinspection RegExpRepeatedSpace,RegExpDuplicateCharacterInClass
def preprocess_sentence(sentence):
    sentence = clean_text(sentence)
    sentence = sentence.replace('_comma_', ',')
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)
    sentence = re.sub(r"  ", "", sentence)
    sentence = sentence.strip()
    return sentence


def load_conversations_from_json(data_file_path):
    file = open(data_file_path)
    data_json = json.load(file)
    count = 0
    inputs, outputs = [], []
    for convo in tqdm(data_json):
        for i in range(len(convo) - 1):
            count = count + 1
            inputs.append(preprocess_sentence(convo[i]))
            outputs.append(preprocess_sentence(convo[i + 1]))
    # print(count)
    return inputs, outputs


def load_conversations_from_csv(data_file_path):
    data_csv = pd.read_csv(data_file_path)
    inputs, outputs = [], []
    for index, row in tqdm(data_csv.iterrows()):
        ip = preprocess_sentence(row['questionTitle'])
        op = preprocess_sentence(row['answerText'].replace('\n', ' '))
        outputs.append(op.split('.')[0].strip())
        inputs.append(ip)

    return inputs, outputs


def load_conversation_list_cn(dialog_txt_filepath):
    def add_sta_and_end(region, mss=20):
        region.insert(0, '<STA>')
        region.append('<END>')
        if len(region) > mss:
            return None
        else:
            while len(region) < mss:
                region.append('<PAD>')
            return region
    lines = open(dialog_txt_filepath, encoding='UTF-8').read().split('\n')
    filtered_q, filtered_a = [], []
    raw_data_len = len(lines) // 2
    # 需要注意，两行话为一对话，第一句为问，第二句为答，总行数必须为偶数
    for i in range(0, len(lines), 2):
        # 使用jieba库进行中文分词
        qlist, alist = jieba.lcut(lines[i]), jieba.lcut(lines[i + 1])
        qlist = add_sta_and_end(qlist, MAX_SENTENCE_LENGTH)
        alist = add_sta_and_end(alist, MAX_SENTENCE_LENGTH)
        if qlist is not None and alist is not None:
            filtered_q.append(qlist)
            filtered_a.append(alist)
    filt_data_len = len(filtered_q)
    filtered = int((raw_data_len - filt_data_len) * 100 / raw_data_len)
    print(str(filtered) + '% filtered from original data')
    return filtered_q, filtered_a


def read_translation(corpus_path):
    with open(corpus_path, mode='r', encoding='utf-8') as f:
        europarl_en = f.read()
    return europarl_en


def clean_translation(corpus):
    corpus = re.sub(r"\.(?=[0-9]|[a-z]|[A-Z])", '.###', corpus)
    corpus = re.sub(r"\.###", '', corpus)
    corpus = re.sub(r"  +", ' ', corpus)
    corpus = corpus.split('\n')
    return corpus


def load_translation_from_lf(eng_path, des_path):
    eng_corpus = read_translation(eng_path)
    des_corpus = read_translation(des_path)
    eng_corpus = clean_translation(eng_corpus)
    des_corpus = clean_translation(des_corpus)
    return eng_corpus, des_corpus


def load_translation_from_code():
    def preprocess(s):
        # for details, see https://www.tensorflow.org/alpha/tutorials/sequences/nmt_with_attention
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        s = re.sub(r"([?.!,¿])", r" \1 ", s)
        s = re.sub(r'[" "]+', " ", s)
        s = re.sub(r"[^a-zA-Z?.!,¿]+", " ", s)
        s = s.strip()
        s = '<start> ' + s + ' <end>'
        return s

    sentences = [
        ("Do you want a cup of coffee?", "¿Quieres una taza de café?"),
        ("I've had coffee already.", "Ya tomé café."),
        ("Can I get you a coffee?", "¿Quieres que te traiga un café?"),
        ("Please give me some coffee.", "Dame algo de café por favor."),
        ("Would you like me to make coffee?", "¿Quieres que prepare café?"),
        ("Two coffees, please.", "Dos cafés, por favor."),
        ("How about a cup of coffee?", "¿Qué tal una taza de café?"),
        ("I drank two cups of coffee.", "Me tomé dos tazas de café."),
        ("Would you like to have a cup of coffee?", "¿Te gustaría tomar una taza de café?"),
        ("There'll be coffee and cake at five.", "A las cinco habrá café y un pastel."),
        ("Another coffee, please.", "Otro café, por favor."),
        ("I made coffee.", "Hice café."),
        ("I would like to have a cup of coffee.", "Quiero beber una taza de café."),
        ("Do you want me to make coffee?", "¿Quieres que haga café?"),
        (
            "It is hard to wake up without a strong cup of coffee.",
            "Es difícil despertarse sin una taza de café fuerte."
        ),
        ("All I drank was coffee.", "Todo lo que bebí fue café."),
        ("I've drunk way too much coffee today.", "He bebido demasiado café hoy."),
        ("Which do you prefer, tea or coffee?", "¿Qué prefieres, té o café?"),
        ("There are many kinds of coffee.", "Hay muchas variedades de café."),
        ("I will make some coffee.", "Prepararé algo de café.")
    ]
    tagged_sentences = [(preprocess(source), preprocess(target)) for (source, target) in sentences]
    source_sentences, target_sentences = list(zip(*tagged_sentences))
    return source_sentences, target_sentences


if __name__ == '__main__':
    questions, answers = load_conversations_from_json('Data/dataset.json')
    questions2, answers2 = load_conversations_from_csv('Data/20200325_counsel_chat.csv')
    print('对话数据读取完成')
