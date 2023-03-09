import json
import re

from config import MAX_SENTENCE_LENGTH

file = open('dataset.json')
data = json.load(file)


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


def preprocess_sentence(sentence):
    sentence = clean_text(sentence)
    sentence = sentence.replace('_comma_', ',')
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)
    sentence = re.sub(r"  ", "", sentence)
    sentence = sentence.strip()
    return sentence


def load_conversations():
    count = 0
    inputs, outputs = [], []
    for convo in data:
        for i in range(len(convo) - 1):
            count = count + 1
            if len(convo[i]) <= MAX_SENTENCE_LENGTH and len(convo[i + 1]) <= MAX_SENTENCE_LENGTH:
                inputs.append(preprocess_sentence(convo[i]))
                outputs.append(preprocess_sentence(convo[i + 1]))
    print(count)
    return inputs, outputs


if __name__ == '__main__':
    questions, answers = load_conversations()
    print('对话数据读取完成')
