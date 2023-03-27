import pickle
import re

import nltk
import numpy as np

import tf_glove


def extract_reddit_comments(path):
    # A regex for extracting the comment body from one line of JSON (faster than parsing)
    body_snatcher = re.compile(r"\{.*?(?<!\\)\"body(?<!\\)\":(?<!\\)\"(.*?)(?<!\\)\".*}")
    with open(path) as file_:
        for line in file_:
            match = body_snatcher.match(line)
            if match:
                body = match.group(1)
                # Ignore deleted comments
                if not body == '[deleted]':
                    # Return the comment as a string (not yet tokenized)
                    yield body


def tokenize_comment(comment_str):
    # Use the excellent NLTK to tokenize the comment body
    #
    # Note that we're lower-casing the comments here. tf_glove is case-sensitive,
    # so if you want 'You' and 'you' to be considered the same word, be sure to lower-case everything.
    return nltk.wordpunct_tokenize(comment_str.lower())


def reddit_comment_corpus(path):
    # A generator that returns lists of tokens representing individual words in the comment
    return (tokenize_comment(comment) for comment in extract_reddit_comments(path))


def get_trained_model(emb_size=64, ctx_size=4, train_epoch=10, corpus_path="data/xaa"):
    model = tf_glove.GloVeModel(embedding_size=emb_size, context_size=ctx_size)
    corpus = reddit_comment_corpus(corpus_path)
    model.fit_to_corpus(corpus)
    model.train(num_epochs=train_epoch)
    model.write_metadata()
    return model


def save_embeddings(model):
    emb = np.copy(model.embeddings)

    np.save('embeddings/emb', model.embeddings)


def embed_word(word_str, words_list=None, embeddings_array=None):
    if words_list is None:
        words_list = pickle.load(open('embeddings/words.pkl', "rb"))
    if embeddings_array is None:
        embeddings_array = np.load('embeddings/emb')
    if word_str not in words_list:
        raise ValueError('word:', word_str, 'not in vocab')
    else:
        word_index = words_list.index(word_str)
        return embeddings_array[word_index], words_list, embeddings_array


def embed_sentences(sentence_without_pad_as_words_list, words_list=None, embeddings_array=None):
    if words_list is None:
        words_list = pickle.load(open('embeddings/words.pkl', "rb"))
    if embeddings_array is None:
        embeddings_array = np.load('embeddings/emb')
    merged_embedd = {}
    for word, index in enumerate(words_list):
        merged_embedd.__setitem__(word, embeddings_array[index])
    sentence_vec_without_pad = [merged_embedd[word_str] for word_str in sentence_without_pad_as_words_list]
    return sentence_vec_without_pad


if __name__ == '__main__':
    mdl = get_trained_model()
    save_embeddings(mdl)
    # word_vec, _, _ = embed_word('reddit')
    # print(word_vec)
