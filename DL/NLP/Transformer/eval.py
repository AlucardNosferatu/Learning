import jieba
import tensorflow as tf

from Model.Transformer import transformer
from config import N_LAYERS, D_MODEL, N_HEADS, UNITS, DROP, MAX_SL, WGT_PATH
from data import preprocess_sentence
# noinspection PyUnresolvedReferences
from tokenizer import task_conv_eng, padding, task_conv_chn


def evaluate(sent, trained_model, start_token, end_token, tok):
    if type(tok) is list:
        # todo: add preprocess for CN question
        sent = jieba.lcut(sent)
        sent = [tok[1][word] for word in sent if word in list(tok[1].keys())]
        while len(sent) > MAX_SL - 2:
            sent.pop(-1)
        sent = [start_token + sent + end_token]

    else:
        sent = preprocess_sentence(sent)
        sent = [start_token + tok.encode(sent) + end_token]
    sent = padding(tok, sent)
    output = tf.expand_dims(start_token, 0)
    for i in range(MAX_SL):
        predictions = trained_model(inputs=[sent, output], training=False)
        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
        if tf.equal(predicted_id, end_token[0]):
            break
        output = tf.concat([output, predicted_id], axis=-1)
    return tf.squeeze(output, axis=0)


def predict(sentence, trained_model, start_token, end_token, tok):
    prediction = evaluate(sentence, trained_model, start_token, end_token, tok)
    if type(tok) is list:
        vocab_size = len(tok[0])
        predicted_sentence = ''.join(
            [
                tok[0][i] for i in prediction if i < vocab_size
            ]
        )
    else:
        vocab_size = tok.vocab_size
        predicted_sentence = tok.decode(
            [
                i for i in prediction if i < vocab_size
            ]
        )

    # print('Input: {}'.format(sentence))
    # print('Output: {}'.format(predicted_sentence))

    return predicted_sentence


def main():
    tok, start_tok, end_tok, vocab_size = task_conv_chn(None, None, False, False)
    model = transformer(
        vocab_size=vocab_size,
        num_layers=N_LAYERS,
        units=UNITS,
        d_model=D_MODEL,
        num_heads=N_HEADS,
        dropout=DROP)
    print('模型初始化完成')
    model.load_weights(WGT_PATH)
    input_str = "老婆，我去上班了。"
    while input_str != '':
        print('输入：', input_str)
        output_str = predict(input_str, model, start_tok, end_tok, tok)
        print('输出：', output_str)
        input_str = input()


if __name__ == '__main__':
    main()
