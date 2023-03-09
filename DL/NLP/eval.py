import language_tool_python
import tensorflow as tf

from Model.Transformer import transformer
from config import NUM_LAYERS, D_MODEL, NUM_HEADS, UNITS, DROPOUT, MAX_SENTENCE_LENGTH
from data import preprocess_sentence
from tokenizer import START_TOKEN, tokenizer, END_TOKEN, VOCAB_SIZE

tool = language_tool_python.LanguageTool('en-US')


def evaluate(sentence, trained_model):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(START_TOKEN + tokenizer.encode(sentence) + END_TOKEN, axis=0)

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

    predicted_sentence = tokenizer.decode(
        [i for i in prediction if i < tokenizer.vocab_size])

    matches = tool.check(predicted_sentence)
    predicted_sentence = language_tool_python.LanguageTool.correct(predicted_sentence, matches)

    print('Input: {}'.format(sentence))
    print('Output: {}'.format(predicted_sentence))

    return predicted_sentence


model = transformer(
    vocab_size=VOCAB_SIZE,
    num_layers=NUM_LAYERS,
    units=UNITS,
    d_model=D_MODEL,
    num_heads=NUM_HEADS,
    dropout=DROPOUT)
print('模型初始化完成')
model.load_weights('Save/bot_4')
# learning_rate = CustomSchedule(D_MODEL)
# print('学习率规划完成')
# optimizer = tf.keras.optimizers.Adam(
#     learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)
# print('优化器初始化完成')
# model.compile(
#     optimizer=optimizer,
#     loss=loss_function,
#     metrics=[accuracy, perplexity],
#     run_eagerly=True
# )
# print('模型编译完成')


input_str = "I feel incredibly stressed out."
print(input_str)
output_str = predict(input_str, model)
print(output_str)
