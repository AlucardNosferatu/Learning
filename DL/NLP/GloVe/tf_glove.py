from __future__ import division

import os
import os.path
import pickle
from collections import Counter, defaultdict
from random import shuffle

# noinspection PyUnresolvedReferences
import tensorflow.compat.v1 as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.platform import gfile


class NotTrainedError(Exception):
    pass


class NotFitToCorpusError(Exception):
    pass


class GloVeModel:
    def __init__(self, embedding_size, context_size, max_vocab_size=10000, min_occurrences=75,
                 scaling_factor=3 / 4, cooccurrence_cap=100, batch_size=512, learning_rate=0.05,
                 max_occurrences=200):
        self.embedding_size = embedding_size
        if isinstance(context_size, tuple):
            self.left_context, self.right_context = context_size
        elif isinstance(context_size, int):
            self.left_context = self.right_context = context_size
        else:
            raise ValueError("`context_size` should be an int or a tuple of two ints")
        self.max_vocab_size = max_vocab_size
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences
        self.scaling_factor = scaling_factor
        self.cooccurrence_cap = cooccurrence_cap
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.__words = None
        self.__word_to_id = None
        self.__cooccurrence_matrix = None
        self.__embeddings = None

    def fit_to_corpus(self, corpus):
        self.__fit_to_corpus(corpus, self.max_vocab_size, self.min_occurrences,
                             self.left_context, self.right_context)
        self.__build_graph()

    def __fit_to_corpus(self, corpus, vocab_size, min_occurrences, left_size, right_size):
        word_counts = Counter()
        cooccurrence_counts = defaultdict(float)
        if os.path.isfile('embeddings/words.pkl'):
            self.__words = pickle.load(open('embeddings/words.pkl', "rb"))
            self.__word_to_id = pickle.load(open('embeddings/word_id.pkl', "rb"))
            self.__cooccurrence_matrix = pickle.load(open('embeddings/cooccurrence.pkl', "rb"))
        else:
            print('fitting corpus, please wait')
            for region in corpus:
                word_counts.update(region)
                for l_context, word, r_context in _context_windows(region, left_size, right_size):
                    if len(word) <= 1:
                        continue
                    if len(l_context) <= 1:
                        continue
                    if len(r_context) <= 1:
                        continue
                    # print(l_context, word, r_context )
                    for i, context_word in enumerate(l_context[::-1]):
                        # add (1 / distance from focal word) for this pair
                        cooccurrence_counts[(word, context_word)] += 1 / (i + 1)
                    for i, context_word in enumerate(r_context):
                        cooccurrence_counts[(word, context_word)] += 1 / (i + 1)
            if len(cooccurrence_counts) == 0:
                raise ValueError("No coccurrences in corpus. Did you try to reuse a generator?")
            self.__words = [word for word, count in word_counts.most_common(vocab_size)
                            if count >= min_occurrences]
            self.__word_to_id = {word: i for i, word in enumerate(self.__words)}
            self.__cooccurrence_matrix = {
                (self.__word_to_id[words[0]], self.__word_to_id[words[1]]): count
                for words, count in cooccurrence_counts.items()
                if words[0] in self.__word_to_id and words[1] in self.__word_to_id}

            with gfile.FastGFile('embeddings/words.pkl', 'wb') as f:
                pickle.dump(self.__words, f)
            with gfile.FastGFile('embeddings/word_id.pkl', 'wb') as f:
                pickle.dump(self.__word_to_id, f)
            with gfile.FastGFile('embeddings/cooccurrence.pkl', 'wb') as f:
                pickle.dump(self.__cooccurrence_matrix, f)

    def __build_graph(self):
        self.__graph = tf.Graph()
        with self.__graph.as_default():
            count_max = tf.constant([self.cooccurrence_cap], dtype=tf.float32,
                                    name='max_cooccurrence_count')
            scaling_factor = tf.constant([self.scaling_factor], dtype=tf.float32,
                                         name="scaling_factor")

            self.__focal_input = tf.placeholder(tf.int32, shape=[self.batch_size],
                                                name="focal_words")
            self.__context_input = tf.placeholder(tf.int32, shape=[self.batch_size],
                                                  name="context_words")
            self.__cooccurrence_count = tf.placeholder(tf.float32, shape=[self.batch_size],
                                                       name="cooccurrence_count")

            focal_embeddings = tf.Variable(
                tf.random_uniform([self.vocab_size, self.embedding_size], 1.0, -1.0),
                name="focal_embeddings")
            context_embeddings = tf.Variable(
                tf.random_uniform([self.vocab_size, self.embedding_size], 1.0, -1.0),
                name="context_embeddings")

            focal_biases = tf.Variable(tf.random_uniform([self.vocab_size], 1.0, -1.0),
                                       name='focal_biases')
            context_biases = tf.Variable(tf.random_uniform([self.vocab_size], 1.0, -1.0),
                                         name="context_biases")

            focal_embedding = tf.nn.embedding_lookup([focal_embeddings], self.__focal_input)
            context_embedding = tf.nn.embedding_lookup([context_embeddings], self.__context_input)
            focal_bias = tf.nn.embedding_lookup([focal_biases], self.__focal_input)
            context_bias = tf.nn.embedding_lookup([context_biases], self.__context_input)

            weighting_factor = tf.minimum(
                1.0,
                tf.pow(
                    tf.div(self.__cooccurrence_count, count_max),
                    scaling_factor))

            embedding_product = tf.reduce_sum(tf.multiply(focal_embedding, context_embedding), 1)

            log_cooccurrences = tf.log(tf.to_float(self.__cooccurrence_count))

            distance_expr = tf.square(tf.add_n([
                embedding_product,
                focal_bias,
                context_bias,
                tf.negative(log_cooccurrences)]))

            single_losses = tf.multiply(weighting_factor, distance_expr)
            self.__total_loss = tf.reduce_sum(single_losses)
            self.__optimizer = tf.train.AdagradOptimizer(self.learning_rate).minimize(
                self.__total_loss)
            self.__summary = tf.summary.merge_all()

            self.__combined_embeddings = tf.add(focal_embeddings, context_embeddings,
                                                name="combined_embeddings")

    def train(self, num_epochs, log_dir='logs', summary_batch_interval=10,
              tsne_epoch_interval=None):
        should_write_summaries = log_dir is not None and summary_batch_interval
        should_generate_tsne = log_dir is not None and tsne_epoch_interval
        batches = self.__prepare_batches()
        total_steps = 0
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.device('/gpu:0'):
            with tf.Session(graph=self.__graph, config=config) as session:
                if should_write_summaries:
                    print("Writing TensorBoard summaries to {}".format(log_dir))
                    summary_writer = tf.summary.FileWriter(log_dir, graph=session.graph)
                tf.global_variables_initializer().run()
                for epoch in range(num_epochs):
                    shuffle(batches)
                    print(epoch)
                    for batch_index, batch in enumerate(batches):
                        i_s, j_s, counts = batch
                        if len(counts) != self.batch_size:
                            continue
                        feed_dict = {
                            self.__focal_input: i_s,
                            self.__context_input: j_s,
                            self.__cooccurrence_count: counts}
                        session.run([self.__optimizer], feed_dict=feed_dict)
                        total_steps += 1
                    self.__embeddings = self.__combined_embeddings.eval()
                    if should_generate_tsne and (epoch + 1) % tsne_epoch_interval == 0:
                        output_path = os.path.join(log_dir, "epoch{:03d}.png".format(epoch + 1))
                        self.generate_tsne(output_path, embeddings=self.__embeddings)
                    if should_write_summaries and (epoch + 1) % summary_batch_interval == 0:
                        tf.summary.scalar("GloVe_loss", self.__total_loss)
                        summary = tf.summary.merge_all()
                        summary_str = session.run(summary, feed_dict=feed_dict)
                        summary_writer.add_summary(summary_str, total_steps)
                        print(self.__total_loss)

                if should_write_summaries:
                    summary_writer.close()
                    saver = tf.train.Saver()
                    saver.save(session, os.path.join('logs', "model.ckpt"), epoch)

                    output_graph_def = graph_util.convert_variables_to_constants(
                        session, self.__graph.as_graph_def(), ['combined_embeddings'])
                    with gfile.FastGFile('embeddings/graph.pg', 'wb') as f:
                        f.write(output_graph_def.SerializeToString())

    def embedding_for(self, word_str_or_id):
        if isinstance(word_str_or_id, str):
            return self.embeddings[self.__word_to_id[word_str_or_id]]
        elif isinstance(word_str_or_id, int):
            return self.embeddings[word_str_or_id]

    def __prepare_batches(self):
        if self.__cooccurrence_matrix is None:
            raise NotFitToCorpusError(
                "Need to fit model to corpus before preparing training batches.")
        cooccurrences = [(word_ids[0], word_ids[1], count)
                         for word_ids, count in self.__cooccurrence_matrix.items()]
        i_indices, j_indices, counts = zip(*cooccurrences)
        return list(_batchify(self.batch_size, i_indices, j_indices, counts))

    @property
    def vocab_size(self):
        return len(self.__words)

    @property
    def words(self):
        if self.__words is None:
            raise NotFitToCorpusError("Need to fit model to corpus before accessing words.")
        return self.__words

    @property
    def embeddings(self):
        if self.__embeddings is None:
            raise NotTrainedError("Need to train model before accessing embeddings")
        return self.__embeddings

    def id_for_word(self, word):
        if self.__word_to_id is None:
            raise NotFitToCorpusError("Need to fit model to corpus before looking up word ids.")
        return self.__word_to_id[word]

    def generate_tsne(self, path='tsne.png', size=(200, 200), word_count=10000, embeddings=None):
        if embeddings is None:
            embeddings = self.embeddings
        from sklearn.manifold import TSNE
        tsne = TSNE(perplexity=20, n_components=2, init='pca', n_iter=5000)
        low_dim_embs = tsne.fit_transform(embeddings[:word_count, :])
        labels = self.words[:word_count]
        return _plot_with_labels(low_dim_embs, labels, path, size, embeddings[:word_count, :])

    def write_metadata(self):
        with open("embeddings/metadata.tsv", "w") as myfile:
            # noinspection PyTypeChecker
            myfile.write('Word\tId\n')
            for i, label in enumerate(self.words):
                myfile.write(label + '\t' + str(i) + '\n')


def _device_for_node(n):
    if n.type == "MatMul":
        return "/gpu:0"
    else:
        return "/cpu:0"


def _context_windows(region, left_size, right_size):
    for i, word in enumerate(region):
        start_index = i - left_size
        end_index = i + right_size
        left_context = _window(region, start_index, i - 1)
        right_context = _window(region, i + 1, end_index)
        yield left_context, word, right_context


def _window(region, start_index, end_index):
    """
    Returns the list of words starting from `start_index`, going to `end_index`
    taken from region. If `start_index` is a negative number, or if `end_index`
    is greater than the index of the last word in region, this function will pad
    its return value with `NULL_WORD`.
    """
    last_index = len(region) + 1
    selected_tokens = region[max(start_index, 0):min(end_index, last_index) + 1]
    return selected_tokens


def _batchify(batch_size, *sequences):
    for i in range(0, len(sequences[0]), batch_size):
        yield tuple(sequence[i:i + batch_size] for sequence in sequences)


def _plot_with_labels(low_dim_embs, labels, path, size, final):
    import matplotlib.pyplot as plt
    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    figure = plt.figure(figsize=size)  # in inches
    for i, label in enumerate(labels):
        x_, y_ = low_dim_embs[i, :]
        plt.scatter(x_, y_)
        plt.annotate(label, xy=(x_, y_), xytext=(5, 2), textcoords='offset points', ha='right',
                     va='bottom')
        with open("logs/vectors.tsv", "a") as myfile:
            myfile.write('\t'.join(map(lambda x: "%.5f" % x, final[i])) + '\n')
        with open("embeddings/metadata.tsv", "a") as myfile:
            myfile.write(label + '\n')
    if path is not None:
        figure.savefig(path)
        plt.close(figure)
