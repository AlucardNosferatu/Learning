import tensorflow as tf

from Model.Transformer import transformer
from config import N_LAYERS, D_MODEL, N_HEADS, UNITS, DROP, MAX_SENTENCE_LENGTH, WGT_PATH
from data import preprocess_sentence
from tokenizer import task_conv_eng, padding


def evaluate(sentence, trained_model, start_token, end_token, tokenizer):
    sentence = preprocess_sentence(sentence)
    sentence = padding(tokenizer, [start_token + tokenizer.encode(sentence) + end_token])
    output = tf.expand_dims(start_token, 0)
    for i in range(MAX_SENTENCE_LENGTH):
        predictions = trained_model(inputs=[sentence, output], training=False)

        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

        if tf.equal(predicted_id, end_token[0]):
            break

        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)


def predict(sentence, trained_model, start_token, end_token, tokenizer):
    prediction = evaluate(sentence, trained_model, start_token, end_token, tokenizer)

    predicted_sentence = tokenizer.decode(
        [i for i in prediction if i < tokenizer.vocab_size]
    )

    # print('Input: {}'.format(sentence))
    # print('Output: {}'.format(predicted_sentence))

    return predicted_sentence


if __name__ == '__main__':
    tok, START_TOK, END_TOK, VOCAB_SIZE = task_conv_eng(None, None, False, False)
    model = transformer(
        vocab_size=VOCAB_SIZE,
        num_layers=N_LAYERS,
        units=UNITS,
        d_model=D_MODEL,
        num_heads=N_HEADS,
        dropout=DROP)
    print('模型初始化完成')
    model.load_weights(WGT_PATH)

    input_str = "Why are no-smoking areas not enforced?"
    while input_str != '':
        print('输入：', input_str)
        output_str = predict(input_str, model, START_TOK, END_TOK, tok)
        print('输出：', output_str)
        input_str = input()
