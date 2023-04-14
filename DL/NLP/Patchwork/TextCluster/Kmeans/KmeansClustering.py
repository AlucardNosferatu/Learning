# -*- coding: utf-8 -*-
import os
import pickle

import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans


class KmeansClustering:
    def __init__(self, stopwords_path=None):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()

    @staticmethod
    def load_stopwords(stopwords=None):
        """
        加载停用词
        :param stopwords:
        :return:
        """
        if stopwords:
            with open(stopwords, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f]
        else:
            return []

    def preprocess_data(self, corpus_path):
        """
        文本预处理，每行一个文本
        :param corpus_path:
        :return:
        """
        corpus = []
        if type(corpus_path) is str:
            corpus_path = [corpus_path]
        for corpus_file in corpus_path:
            with open(corpus_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('q\t') or line.startswith('a\t'):
                        line = line.split('\t')[1]
                    corpus.append(
                        ' '.join(
                            [
                                word for word in jieba.lcut(line.strip()) if word not in self.stopwords
                            ]
                        )
                    )
        return corpus

    def get_text_tfidf_matrix(self, corpus):
        """
        获取tfidf矩阵
        :param corpus:
        :return:
        """
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))

        # 获取词袋中所有词语，很重要，用于标记增量文本（保证文本向量化一致性，计算聚类中心距离才不会错乱）
        words = self.vectorizer.vocabulary_

        # 获取tfidf矩阵中权重
        weights = tfidf.toarray()
        return weights, words

    def kmeans(self, corpus_path, n_clusters=5):
        """
        KMeans文本聚类
        :param corpus_path: 语料路径（每行一篇）,文章id从0开始
        :param n_clusters: ：聚类类别数目
        :return: {cluster_id1:[text_id1, text_id2]}
        """
        corpus = self.preprocess_data(corpus_path)
        weights, words = self.get_text_tfidf_matrix(corpus)

        clf = KMeans(n_clusters=n_clusters)

        # clf.fit(weights)

        index2label = clf.fit_predict(weights)

        # 中心点，用于给增量文本进行标记（最小余弦距离匹配），很重要，需要保存起来
        centers = clf.cluster_centers_

        # 用来评估簇的个数是否合适,距离约小说明簇分得越好,选取临界点的簇的个数
        # score = clf.inertia_

        # 每个样本所属的簇
        label2index = {}
        for text_idx, label_idx in enumerate(index2label):
            if label_idx not in label2index:
                label2index[label_idx] = [text_idx]
            else:
                label2index[label_idx].append(text_idx)
        return label2index, index2label, centers, words


if __name__ == '__main__':
    # Kmeans = KmeansClustering(stopwords_path='../data/stop_words.txt')
    Kmeans = KmeansClustering()
    # res = Kmeans.kmeans('../data/test_data.txt', n_clusters=5)
    c_dir = '../../../Transformer/Data_xiaoice/texts'
    c_path = os.listdir(c_dir)
    c_path = [os.path.join(c_dir, f_path) for f_path in c_path if f_path.endswith('_mat.txt')]
    l2i, i2l, c, w = Kmeans.kmeans(c_path, n_clusters=10)
    # n_cluster must be equal in different modules
    with open('../output/file_order.txt', 'w', encoding='utf-8') as f_order:
        f_order.writelines([f_path + '\n' for f_path in c_path])
    with open('../output/label2index.pkl', 'wb') as f_l2i:
        pickle.dump(l2i, f_l2i)
    with open('../output/word2vector.pkl', 'wb') as f_w2v:
        # 用于文本增量标记（总不可能每次从头生成n个分类）
        pickle.dump(w, f_w2v)
    np.save('../output/index2label.npy', i2l)
    # 用于文本增量标记（总不可能每次从头生成n个分类）
    np.save('../output/centers.npy', c)
