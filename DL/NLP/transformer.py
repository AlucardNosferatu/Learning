import numpy as np
import re
import tensorflow as tf
import unicodedata
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Lambda, Layer, Embedding, LayerNormalization

# We should avoid keras.backend at all cases unless using ONNX support
# import tensorflow.keras.backend as backend

sentences = [
    ("Do you want a cup of coffee?", "I've had coffee already."),
    ("I've had coffee already.", "Would you like to have another one?"),
    ("Can I get you a coffee?", "No, please no."),
    ("Please give me some coffee.", "How about make it by yourself?"),
    ("Would you like me to make coffee?", "Sure, but not for me."),
    ("Two coffees, please.", "You've drunk too much!"),
    ("How about a cup of coffee?", "Thanks, that's all I need!"),
    ("I drank two cups of coffee.", "I drank two more cups than you."),
    ("Would you like to have a cup of coffee?", "I've had two cups of coffee already."),
    ("There'll be coffee and cake at five.", "The cake is a lie!"),
    ("Another coffee, please.", "Ask your mother for it!"),
    ("I made coffee.", "Tasted like shit."),
    ("I would like to have a cup of coffee.", "Why ask me?"),
    ("Do you want me to make coffee?", "All I need is your love"),
    ("It is hard to wake up without a strong cup of coffee.", "And it is hard to fall asleep without your kiss."),
    ("All I drank was coffee.", "Won't you throw up?"),
    ("I've drunk way too much coffee today.", "You smell like coffee."),
    ("Which do you prefer, tea or coffee?", "Only kids make choices!"),
    ("There are many kinds of coffee.", "But only few of them are tasty."),
    ("I will make some coffee.", "You make, you drink.")
]


# noinspection RegExpDuplicateCharacterInClass
def preprocess(s):
    # for details, see https://www.tensorflow.org/alpha/tutorials/sequences/nmt_with_attention
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r"([?.!¡,¿])", r" \1 ", s)  # Add spaces around punctuations
    s = re.sub(r"[\" \"]+", " ", s)  # Remove extra space
    s = re.sub(r"[^a-zA-Z?.!¡,¿áéíóú¡üñ]+", " ", s)  # Remove other characters
    s = s.strip()
    s = '<start> ' + s + ' <end>'
    return s


print("Original:", sentences[0])
sentences = [(preprocess(en), preprocess(es)) for (en, es) in sentences]
print("Preprocessed:", sentences[0])

# print("Original:", "测试一下中文输入语句")
# print("Preprocessed:", preprocess("测试一下中文输入语句"))

source_sentences, target_sentences = list(zip(*sentences))

# In this illustration, I choose not to specify num_words and oov_token due to the size of data.
# for details, please visit https://keras.io/preprocessing/text/
source_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
source_tokenizer.fit_on_texts(source_sentences)
source_data = source_tokenizer.texts_to_sequences(source_sentences)
print("Sequence:", source_data[0])
source_data = tf.keras.preprocessing.sequence.pad_sequences(source_data, padding='post')
print("Padded:", source_data[0])

target_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
target_tokenizer.fit_on_texts(target_sentences)
target_data = target_tokenizer.texts_to_sequences(target_sentences)
target_data = tf.keras.preprocessing.sequence.pad_sequences(target_data, padding='post')

# Machine translation models take the entire source sentence and an incomplete sentence in
# target language as inputs at once, and predict the next word for the incomplete sentence.
# We create labels for the decoder by shifting the target sequence one to the right.
target_labels = np.zeros(target_data.shape)
target_labels[:, 0:target_data.shape[1] - 1] = target_data[:, 1:]

print("Target sequence", target_data[0])
print("Target label", target_labels[0])

source_vocab_len = len(source_tokenizer.word_index) + 1
target_vocab_len = len(target_tokenizer.word_index) + 1

print("Size of source vocabulary: ", source_vocab_len)
print("Size of target vocabulary: ", target_vocab_len)

dataset = tf.data.Dataset.from_tensor_slices((source_data, target_data, target_labels)).batch(5)
# Transformer parameters
d_model = 64  # 512 in the original paper
d_k = 16  # 64 in the original paper
d_v = 16  # 64 in the original paper
n_heads = 4  # 8 in the original paper
n_encoder_layers = 2  # 6 in the original paper
n_decoder_layers = 2  # 6 in the original paper

max_token_length = 20  # 512 in the original paper


class SingleHeadAttention(Layer):
    # noinspection PyShadowingNames,PyUnusedLocal
    def __init__(self, input_shape=(3, -1, d_model), dropout=.0, masked=None):
        super(SingleHeadAttention, self).__init__()
        self.q = Dense(d_k, input_shape=(-1, d_model), kernel_initializer='glorot_uniform',
                       bias_initializer='glorot_uniform')
        self.normalize_q = Lambda(lambda x: x / np.sqrt(d_k))
        self.k = Dense(d_k, input_shape=(-1, d_model), kernel_initializer='glorot_uniform',
                       bias_initializer='glorot_uniform')
        self.v = Dense(d_v, input_shape=(-1, d_model), kernel_initializer='glorot_uniform',
                       bias_initializer='glorot_uniform')
        self.dropout = dropout
        self.masked = masked

    # Inputs: [query, key, value]
    # noinspection PyMethodOverriding
    def call(self, inputs, training=None):
        assert len(inputs) == 3
        # We use a lambda layer to divide vector q by sqrt(d_k) according to the equation
        q = self.normalize_q(self.q(inputs[0]))
        k = self.k(inputs[1])
        # The dimensionality of q is (batch_size, query_length, d_k) and that of k is (batch_size, key_length, d_k)
        # So we will do a matrix multiplication by batch after transposing last 2 dimensions of k
        # tf.shape(attn_weights) = (batch_size, query_length, key_length)
        attn_weights = tf.matmul(q, tf.transpose(k, perm=[0, 2, 1]))
        if self.masked:  # Prevent future attentions in decoding self-attention
            # Create a matrix where the strict upper triangle (not including main diagonal) is filled with -inf and 0
            # elsewhere
            length = tf.shape(attn_weights)[-1]
            # attn_mask = np.triu(tf.fill((length, length), -np.inf), k=1)
            # We need to use tensorflow functions instead of numpy
            attn_mask = tf.fill((length, length), -np.inf)
            attn_mask = tf.linalg.band_part(attn_mask, 0, -1)  # Get upper triangle
            attn_mask = tf.linalg.set_diag(attn_mask,
                                           tf.zeros(length))  # Set diagonal to zeros to avoid operations with infinity
            # This matrix is added to the attention weights so all future attention will have -inf logits (0 after
            # softmax)
            attn_weights += attn_mask
        # Softmax along the last dimension
        attn_weights = tf.nn.softmax(attn_weights, axis=-1)
        if training:
            # Attention dropout included in the original paper. This is possibly to encourage multi-head diversity.
            attn_weights = tf.nn.dropout(attn_weights, rate=self.dropout)
        v = self.v(inputs[2])
        return tf.matmul(attn_weights, v)


class MultiHeadAttention(Layer):
    def __init__(self, dropout=.0, masked=None):
        super(MultiHeadAttention, self).__init__()
        self.attn_heads = list()
        for i in range(n_heads):
            self.attn_heads.append(SingleHeadAttention(dropout=dropout, masked=masked))
        self.linear = Dense(d_model, input_shape=(-1, n_heads * d_v), kernel_initializer='glorot_uniform',
                            bias_initializer='glorot_uniform')

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x, training=None):
        attentions = [self.attn_heads[i](x, training=training) for i in range(n_heads)]
        concatenated_attentions = tf.concat(attentions, axis=-1)
        return self.linear(concatenated_attentions)


# noinspection PyAttributeOutsideInit
class TransformerEncoder(Layer):
    def __init__(self, dropout=.1, attention_dropout=.0, **kwargs):
        super(TransformerEncoder, self).__init__(**kwargs)
        self.dropout_rate = dropout
        self.attention_dropout_rate = attention_dropout

    def build(self, input_shape):
        self.multi_head_attention = MultiHeadAttention(dropout=self.attention_dropout_rate)
        self.dropout1 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization1 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)

        self.linear1 = Dense(input_shape[-1] * 4, input_shape=input_shape, activation='relu',
                             kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform')
        self.linear2 = Dense(input_shape[-1], input_shape=self.linear1.compute_output_shape(input_shape),
                             kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform')
        self.dropout2 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization2 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)
        super(TransformerEncoder, self).build(input_shape)

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x, training=None):
        sublayer1 = self.multi_head_attention((x, x, x), training=training)
        sublayer1 = self.dropout1(sublayer1, training=training)
        layer_norm1 = self.layer_normalization1(x + sublayer1)

        sublayer2 = self.linear2(self.linear1(layer_norm1))
        layer_norm2 = self.layer_normalization2(layer_norm1 + sublayer2)
        return layer_norm2

    def compute_output_shape(self, input_shape):
        return input_shape


# noinspection PyAttributeOutsideInit
class TransformerDecoder(Layer):
    def __init__(self, dropout=.0, attention_dropout=.0, **kwargs):
        super(TransformerDecoder, self).__init__(**kwargs)
        self.dropout_rate = dropout
        self.attention_dropout_rate = attention_dropout

    def build(self, input_shape):
        self.multi_head_self_attention = MultiHeadAttention(dropout=self.attention_dropout_rate, masked=True)
        self.dropout1 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization1 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)

        self.multi_head_encoder_attention = MultiHeadAttention(dropout=self.attention_dropout_rate)
        self.dropout2 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization2 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)

        self.linear1 = Dense(input_shape[-1] * 4, input_shape=input_shape, activation='relu',
                             kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform')
        self.linear2 = Dense(input_shape[-1], input_shape=self.linear1.compute_output_shape(input_shape),
                             kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform')
        self.dropout3 = tf.keras.layers.Dropout(self.dropout_rate)
        self.layer_normalization3 = LayerNormalization(input_shape=input_shape, epsilon=1e-6)
        super(TransformerDecoder, self).build(input_shape)

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x, hidden, training=None):
        sublayer1 = self.multi_head_self_attention((x, x, x))
        sublayer1 = self.dropout1(sublayer1, training=training)
        layernorm1 = self.layer_normalization1(x + sublayer1)

        sublayer2 = self.multi_head_encoder_attention((x, hidden, hidden))
        sublayer2 = self.dropout2(sublayer2, training=training)
        layernorm2 = self.layer_normalization2(layernorm1 + sublayer2)

        sublayer3 = self.linear2(self.linear1(layernorm1))
        sublayer3 = self.dropout3(sublayer3, training=training)
        layernorm3 = self.layer_normalization2(layernorm2 + sublayer3)
        return layernorm3

    def compute_output_shape(self, input_shape):
        return input_shape


# Testing if the dimension matches!
x = tf.ones((3, 26, d_model))
x1 = tf.ones((3, 18, d_model))
single_att = SingleHeadAttention(masked=None)
multi_att = MultiHeadAttention()
encoder = TransformerEncoder()
decoder = TransformerDecoder()
y = single_att((x, x, x))  # Self attention
y1 = multi_att((x1, x, x))  # Encoder-decoder attention
print(tf.shape(y))
print(tf.shape(y1))
y2 = encoder(x)
y3 = decoder(x, y2)

print(tf.shape(y2))
print(tf.shape(y3))


# print(layer.trainable_weights)

def get_angle(pos, dim):
    return pos / np.power(10000, 2 * (dim // 2) / d_model)


def get_positional_angle(pos):
    return [get_angle(pos, dim) for dim in range(d_model)]


class SinusoidalPositionalEncoding(Layer):
    # Inspired from https://github.com/graykode/nlp-tutorial/blob/master/5-1.Transformer/Transformer_Torch.ipynb
    def __init__(self):
        super(SinusoidalPositionalEncoding, self).__init__()
        self.sinusoidal_encoding = np.array([get_positional_angle(pos) for pos in range(max_token_length)],
                                            dtype=np.float32)
        self.sinusoidal_encoding[:, 0::2] = np.sin(self.sinusoidal_encoding[:, 0::2])
        self.sinusoidal_encoding[:, 1::2] = np.cos(self.sinusoidal_encoding[:, 1::2])
        self.sinusoidal_encoding = tf.cast(self.sinusoidal_encoding,
                                           dtype=tf.float32)  # Casting the array to Tensor for slicing

    # noinspection PyMethodOverriding,PyShadowingNames
    def call(self, x):
        return x + self.sinusoidal_encoding[:tf.shape(x)[1]]
        # return x + tf.slice(self.sinusoidal_encoding, [0, 0], [tf.shape(x)[1], d_model])

    def compute_output_shape(self, input_shape):
        return input_shape


class Transformer(Model):
    def get_config(self):
        pass

    def __init__(self, dropout=.1, attention_dropout=.0, **kwargs):
        super(Transformer, self).__init__(**kwargs)
        self.encoding_embedding = Embedding(source_vocab_len, d_model)
        self.decoding_embedding = Embedding(target_vocab_len, d_model)
        self.pos_encoding = SinusoidalPositionalEncoding()
        self.encoder = [TransformerEncoder(dropout=dropout, attention_dropout=attention_dropout) for _ in
                        range(n_encoder_layers)]
        self.decoder = [TransformerDecoder(dropout=dropout, attention_dropout=attention_dropout) for _ in
                        range(n_decoder_layers)]
        self.decoder_final = Dense(target_vocab_len, input_shape=(None, d_model))

    # noinspection PyMethodOverriding
    def call(self, inputs, training=None):  # Source_sentence and decoder_input
        source_sentence, decoder_input = inputs
        embedded_source = self.encoding_embedding(source_sentence)
        encoder_output = self.pos_encoding(embedded_source)
        for encoder_unit in self.encoder:
            encoder_output = encoder_unit(encoder_output, training=training)

        embedded_target = self.decoding_embedding(decoder_input)
        decoder_output = self.pos_encoding(embedded_target)
        for decoder_unit in self.decoder:
            decoder_output = decoder_unit(decoder_output, encoder_output, training=training)
        if training:
            decoder_output = self.decoder_final(decoder_output)
            decoder_output = tf.nn.softmax(decoder_output, axis=-1)
        else:
            decoder_output = self.decoder_final(decoder_output[:, -1:, :])
            decoder_output = tf.nn.softmax(decoder_output, axis=-1)
        return decoder_output


# Demonstration on calling transformer model
transformer = Transformer(dropout=.1)
print(tf.shape(transformer([np.ones((5, 15)), np.ones((5, 12))], training=False)))

# Specify loss, optimizer and training function
crossentropy = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)


def calc_loss(targets, logits):
    mask = tf.math.logical_not(tf.math.equal(targets, 0))
    mask = tf.cast(mask, dtype=tf.int64)
    return crossentropy(targets, logits, sample_weight=mask)


optimizer = tf.keras.optimizers.Adam()


# noinspection PyShadowingNames
@tf.function  # remove this annotation when debugging
def train_step(source_seq, target_seq, target_labels):
    with tf.GradientTape() as tape:
        logits = transformer([source_seq, target_seq], training=True)  # Set training=True to use dropout in training
        loss = calc_loss(target_labels, logits)

    variables = transformer.trainable_variables
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))

    return loss


EPOCHS = 200

for epoch in range(EPOCHS):
    loss = 999.9
    for batch, (source_seq, target_seq, target_labels) in enumerate(dataset):
        loss = train_step(source_seq, target_seq, target_labels)

    if epoch % 10 == 0:
        print("Epoch #%d, Loss %.4f" % (epoch, loss))
        # input_sent, target_sent, translation = translate()
        # print("Input: %s\nTarget: %s\nTranslation: %s\n" % (input_sent, target_sent, translation))


# noinspection PyShadowingNames
def translate(model, source_sentence, target_sentence_start=None):
    if target_sentence_start is None:
        target_sentence_start = [['<start>']]
    if np.ndim(source_sentence) == 1:  # Create a batch of 1 the input is a sentence
        source_sentence = [source_sentence]
    if np.ndim(target_sentence_start) == 1:
        target_sentence_start = [target_sentence_start]
    # Tokenizing and padding
    source_seq = source_tokenizer.texts_to_sequences(source_sentence)
    source_seq = tf.keras.preprocessing.sequence.pad_sequences(source_seq, padding='post', maxlen=15)
    predict_seq = target_tokenizer.texts_to_sequences(target_sentence_start)

    predict_sentence = list(target_sentence_start[0])  # Deep copy here to prevent updates on target_sentence_start
    while predict_sentence[-1] != '<end>' and len(predict_seq) < max_token_length:
        predict_output = model([np.array(source_seq), np.array(predict_seq)], training=None)
        predict_label = tf.argmax(predict_output, axis=-1)  # Pick the label with highest softmax score
        predict_seq = tf.concat([predict_seq, predict_label], axis=-1)  # Updating the prediction sequence
        predict_sentence.append(target_tokenizer.index_word[predict_label[0][0].numpy()])

    return predict_sentence


print("Source sentence: ", source_sentences[10])
print("Target sentence: ", target_sentences[10])
print("Predicted sentence: ", ' '.join(translate(transformer, source_sentences[10].split(' '))))
