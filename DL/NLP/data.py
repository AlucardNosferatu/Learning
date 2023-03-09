import json
import re
import pandas as pd
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


def load_conversations(data):
    count = 0
    inputs, outputs = [], []
    for convo in data:
        for i in range(len(convo) - 1):
            count = count + 1
            if len(convo[i]) <= MAX_SENTENCE_LENGTH and len(convo[i + 1]) <= MAX_SENTENCE_LENGTH:
                inputs.append(preprocess_sentence(convo[i]))
                outputs.append(preprocess_sentence(convo[i + 1]))
    # print(count)
    return inputs, outputs


def load_conversations_from_csv(data):
    inputs, outputs = [], []

    for index, row in data.iterrows():
        ip = preprocess_sentence(row['questionTitle'])
        op = preprocess_sentence(row['answerText'].replace('\n', ' '))

        if len(ip.split()) > MAX_SENTENCE_LENGTH:
            continue

        outputs.append(op.split('.')[0].strip())
        inputs.append(ip)

    return inputs, outputs


if __name__ == '__main__':
    file = open('Data/dataset.json')
    data_json = json.load(file)
    questions, answers = load_conversations(data_json)
    data_csv = pd.read_csv('Data/20200325_counsel_chat.csv')
    questions2, answers2 = load_conversations_from_csv(data_csv)
    print('对话数据读取完成')
