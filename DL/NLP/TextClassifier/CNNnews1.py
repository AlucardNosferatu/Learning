import jieba
import numpy as np
import pandas as pd
import tensorflow as tf
from gensim.models import word2vec
from keras.layers import *
from keras.models import Model
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder

train_data = pd.read_csv('data_train.csv', lineterminator='\n')
test_data = pd.read_csv('data_test.csv', lineterminator='\n')
n_classes = 2


# 利用LabelEncoder对数据标签进行规格化处理
def encode_label(data):
    listLable = []
    for lable in data['lable']:
        listLable.append(lable)
    # 到这里都是把lable整合到一起，下面是规格化处理
    le = LabelEncoder()
    resultLable = le.fit_transform(listLable)
    return resultLable


trainLable = encode_label(train_data)
testLable = encode_label(test_data)


# 这里出来是所有review的集合：
def get_review(data):
    listReview = []
    # le = LabelEncoder()
    for review in data['review']:
        listReview.append(review)
    return listReview


trainReview = get_review(train_data)
testReview = get_review(test_data)

stoplist = [None, '.', ':', '-', '+', '/', ',', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


# 分词：
def word_cut(Review):
    Mat = []
    for rec in Review:
        seten = []
        sent = list(
            map(lambda x: x.strip().lower() if len(x.strip().lower()) > 0 else None, jieba.cut(rec)))  # 每句话里的单词拿出来
        for word_ in sent:
            if not (word_ in stoplist):
                seten.append(word_)
        Mat.append(seten)
    return Mat


trainCut = word_cut(trainReview)
testCut = word_cut(testReview)
wordCut = trainCut + testCut
# 求句子最大长度
maxLen = 0
for sentence in wordCut:
    length = 0
    for wd in sentence:
        if not (wd in stoplist):
            length = length + 1
    if length > maxLen:
        maxLen = length

# fit_on_texts函数可以将输入的文本中的每个词编号，编号是根据词频的，词频越大，编号越小
tokenizer = Tokenizer()
tokenizer.fit_on_texts(wordCut)
vocab = tokenizer.word_index  # 得到每个词的编号，这里的vocab已经剔除掉stoplist了

# word2vec的训练:
# 设置词语向量维度
num_featrues = 300
# 保证被考虑词语的最低频度
min_word_count = 5
# 设置并行化训练使用CPU计算核心数量
num_workers = 4
# 设置词语上下文窗口大小
context = 5
new_w2v = False
if new_w2v:
    w2v_model = word2vec.Word2Vec(wordCut, workers=num_workers, min_count=min_word_count, window=context)
    w2v_model.init_sims(replace=True)
    # 输入一个路径，保存训练好的模型，其中./data/model目录事先要存在
    w2v_model.save("CNNw2vModel2")
else:
    w2v_model = word2vec.Word2Vec.load("CNNw2vModel2")

# 特征数字编号
trainID = tokenizer.texts_to_sequences(trainCut)
testID = tokenizer.texts_to_sequences(testCut)
trainSeq = tf.keras.preprocessing.sequence.pad_sequences(trainID, maxlen=maxLen)
testSeq = tf.keras.preprocessing.sequence.pad_sequences(testID, maxlen=maxLen)

# 标签的独热编码
trainCate = to_categorical(trainLable, num_classes=n_classes)  # 将标签转换为one-hot编码
testCate = to_categorical(testLable, num_classes=n_classes)  # 将标签转换为one-hot编码

# 利用训练后的word2vec自定义Embedding的训练矩阵，每行代表一个词（结合独热码和矩阵乘法理解）
embedding_matrix = np.zeros((len(vocab) + 1, w2v_model.vector_size))
for word, i in vocab.items():
    try:
        index = w2v_model.wv.key_to_index[str(word)]
        embedding_vector = w2v_model.wv.get_normed_vectors()[index, :]
        embedding_matrix[i] = embedding_vector
    except KeyError:
        continue


# 训练模型
def text_cnn_model_1(x_train_padded_seqs, train_cate, inc=True):
    if not inc:
        main_input = Input(shape=(maxLen,), dtype='float64')
        # 词嵌入（使用预训练的词向量）
        embedder = Embedding(
            len(vocab) + 1,
            w2v_model.vector_size,
            input_length=maxLen,
            weights=[embedding_matrix],
            trainable=False
        )
        embed = embedder(main_input)
        # 卷积核个数为6，词窗大小分别为3,4,5
        cnn1 = Conv1D(128, 2, padding='same', strides=1, activation='relu')(embed)
        cnn1 = MaxPooling1D(pool_size=maxLen - 1)(cnn1)
        cnn2 = Conv1D(128, 3, padding='same', strides=1, activation='relu')(embed)
        cnn2 = MaxPooling1D(pool_size=maxLen - 2)(cnn2)
        cnn3 = Conv1D(128, 4, padding='same', strides=1, activation='relu')(embed)
        cnn3 = MaxPooling1D(pool_size=maxLen - 3)(cnn3)
        cnn4 = Conv1D(128, 6, padding='same', strides=1, activation='relu')(embed)
        cnn4 = MaxPooling1D(pool_size=maxLen - 5)(cnn4)
        # 合并三个模型的输出向量
        cnn = concatenate([cnn1, cnn2, cnn3, cnn4], axis=-1)
        flat = Flatten()(cnn)
        drop = Dropout(0.2)(flat)
        main_output = Dense(n_classes, activation='softmax')(drop)
        mdl = Model(inputs=main_input, outputs=main_output)
        mdl.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    else:
        mdl = load_model('TextCNN6')
    mdl.fit(x_train_padded_seqs, train_cate, batch_size=1024, epochs=1000)
    mdl.save("TextCNN6")


# 主程序调用训练模型：
text_cnn_model_1(trainSeq, trainCate)

# 预测与评估
mainModel = load_model('TextCNN6')
result = mainModel.predict(testSeq)  # 预测样本属于每个类别的概率
score = mainModel.evaluate(testSeq, testCate, batch_size=32)
print(score)
