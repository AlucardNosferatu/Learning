import os

import tensorflow as tf
from tqdm import tqdm

from Model.Transformer import transformer
from config import N_LAYERS, D_MODEL, N_HEADS, UNITS, DROP, SET_BS, EPOCHS, WGT_PATH, SET_TCOUNT
# noinspection PyUnresolvedReferences
from data import load_translation_from_lf, load_translation_from_code, load_conversation_list_cn
from metric import loss_function, accuracy, perplexity, LossHistory
# noinspection PyUnresolvedReferences
from tokenizer import do_tokenize, task_conv_eng, task_conv_chn

tf.keras.backend.clear_session()
new_tokenizer = False
increment = True
increment = increment and not new_tokenizer


def prepare_model(v_size):
    model = transformer(
        vocab_size=v_size,
        num_layers=N_LAYERS,
        units=UNITS,
        d_model=D_MODEL,
        num_heads=N_HEADS,
        dropout=DROP)
    print('模型初始化完成')
    learning_rate = 0.001
    print('学习率规划完成')
    optimizer = tf.keras.optimizers.Adam(
        learning_rate,
        beta_1=0.9,
        beta_2=0.98,
        epsilon=1e-9
    )
    print('优化器初始化完成')
    model.compile(
        optimizer=optimizer,
        loss=loss_function,
        metrics=[accuracy, perplexity],
        run_eagerly=True
    )
    print('模型编译完成')
    return model


def fill_to_specified_size(seqs, spec_size):
    while len(seqs) > spec_size:
        seqs.pop(-1)
    prev_size = len(seqs)
    while len(seqs) < spec_size:
        dist = len(seqs) - prev_size
        seqs.append(seqs[dist])
    return seqs


if __name__ == '__main__':
    # questions, answers = load_conversations_from_json('Data/dataset.json')
    # questions2, answers2 = load_conversations_from_csv('Data/20200325_counsel_chat.csv')
    # questions += questions2
    # answers += answers2
    # questions, answers = load_translation_from_lf('Data/europarl-v7.es-en.en', 'Data/europarl-v7.es-en.es')
    # questions2, answers2 = load_translation_from_code()
    # print('原始数据已导入')
    questions, answers = [], []
    text_dir = 'Data_xiaoice/texts'
    files = os.listdir(text_dir)
    for file in tqdm(files):
        if file.endswith('_mat.txt'):
            q, a = load_conversation_list_cn(os.path.join(text_dir, file))
            questions += q
            answers += a

    # q_test = questions
    # a_test = answers
    q_test = fill_to_specified_size(questions, SET_TCOUNT)
    a_test = fill_to_specified_size(answers, SET_TCOUNT)

    dataset, vocab_size = do_tokenize(q_test, a_test, task_conv_chn, new_tokenizer)
    dataset = dataset.batch(SET_BS)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
    mdl = prepare_model(vocab_size)
    ckpt = tf.keras.callbacks.ModelCheckpoint(
        WGT_PATH,
        monitor='loss',
        verbose=1,
        save_best_only=True,
        save_weights_only=True,
        mode='min',
        save_freq='epoch'
    )
    log_metric = LossHistory()
    cb_list = [ckpt, log_metric]
    if increment:
        mdl.load_weights(WGT_PATH)
    with tf.device('/gpu:0'):
        mdl.fit(dataset, epochs=EPOCHS, callbacks=cb_list)
