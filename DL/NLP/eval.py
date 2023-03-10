import tensorflow as tf
import tensorflow_datasets as tfds
from Model.Transformer import transformer
from config import NUM_LAYERS, D_MODEL, NUM_HEADS, UNITS, DROPOUT, MAX_SENTENCE_LENGTH
from data import preprocess_sentence
from tokenizer import VOCAB_SIZE_WITH_START_AND_END, START_TOKEN, END_TOKEN

old_tokenizer = tfds.deprecated.text.SubwordTextEncoder.load_from_file('Save/tokenizer')


def evaluate(sentence, trained_model):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(START_TOKEN + old_tokenizer.encode(sentence) + END_TOKEN, axis=0)

    output = tf.expand_dims(START_TOKEN, 0)

    for i in range(MAX_SENTENCE_LENGTH):
        predictions = trained_model(inputs=[sentence, output], training=False)

        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

        if tf.equal(predicted_id, END_TOKEN[0]):
            break

        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)


def predict(sentence, trained_model):
    prediction = evaluate(sentence, trained_model)

    predicted_sentence = old_tokenizer.decode(
        [i for i in prediction if i < old_tokenizer.vocab_size])

    # print('Input: {}'.format(sentence))
    # print('Output: {}'.format(predicted_sentence))

    return predicted_sentence


model = transformer(
    vocab_size=VOCAB_SIZE_WITH_START_AND_END,
    num_layers=NUM_LAYERS,
    units=UNITS,
    d_model=D_MODEL,
    num_heads=NUM_HEADS,
    dropout=DROPOUT)
print('模型初始化完成')
model.load_weights('Save/bot_4')

input_str = "I feel incredibly stressed out."
while input_str != '':
    print('输入：', input_str)
    output_str = predict(input_str, model)
    print('输出：', output_str)
    input_str = input()
