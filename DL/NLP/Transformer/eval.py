import jieba
import tensorflow as tf

from Model.Transformer import transformer
from config import N_LAYERS, D_MODEL, N_HEADS, UNITS, DROP, MAX_SENTENCE_LENGTH, WGT_PATH
from data import preprocess_sentence
# noinspection PyUnresolvedReferences
from tokenizer import task_conv_eng, padding, task_conv_chn


def evaluate(sent, trained_model, start_token, end_token, tok):
    if type(tok) is list:
        # todo: add preprocess for CN question
        start_token = [start_token]
        end_token = [end_token]
        sent = jieba.lcut(sent)
        sent = [tok[1][word] for word in sent if word in list(tok[1].keys())]
        while len(sent) > MAX_SENTENCE_LENGTH - 2:
            sent.pop(-1)
        sent = [start_token + sent + end_token]
        while len(sent[0]) < MAX_SENTENCE_LENGTH:
            sent[0].append(tok[1]['<PAD>'])
        sent = padding(tok, sent)
    else:
        sent = preprocess_sentence(sent)
        sent = padding(tok, [start_token + tok.encode(sent) + end_token])
    output = tf.expand_dims(start_token, 0)
    for i in range(MAX_SENTENCE_LENGTH):
        predictions = trained_model(inputs=[sent, output], training=False)
        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
        if tf.equal(predicted_id, end_token[0]):
            break
        output = tf.concat([output, predicted_id], axis=-1)
    return tf.squeeze(output, axis=0)


def predict(sentence, trained_model, start_token, end_token, tokenizer):
    prediction = evaluate(sentence, trained_model, start_token, end_token, tokenizer)
    if type(tokenizer) is list:
        predicted_sentence = ''.join(
            [
                tokenizer[0][index] for index in prediction if tokenizer[0][index] not in ['<STA>', '<END>', '<PAD>']
            ]
        )
    else:
        predicted_sentence = tokenizer.decode(
            [i for i in prediction if i < tokenizer.vocab_size]
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
