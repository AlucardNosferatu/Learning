import tensorflow as tf

from Model.Transformer import transformer
from config import NUM_LAYERS, D_MODEL, NUM_HEADS, UNITS, DROPOUT, BATCH_SIZE, EPOCHS, SAVE_PERIOD, TARGET_VOCAB_SIZE
from data import load_conversations_from_json, load_conversations_from_csv
from metric import loss_function, accuracy, perplexity
from tokenizer import do_tokenize, conv_task

tf.keras.backend.clear_session()


class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):

    def get_config(self):
        pass

    def __init__(self, d_model, warmup_steps=200):
        super(CustomSchedule, self).__init__()

        self.d_model = d_model
        self.d_model = tf.cast(self.d_model, tf.float32)

        self.warmup_steps = warmup_steps

    def __call__(self, step):
        arg1 = tf.math.rsqrt(step)
        arg2 = step * (self.warmup_steps ** -1.5)

        return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)


def prepare_model():
    model = transformer(
        vocab_size=TARGET_VOCAB_SIZE + 2,
        num_layers=NUM_LAYERS,
        units=UNITS,
        d_model=D_MODEL,
        num_heads=NUM_HEADS,
        dropout=DROPOUT)
    print('模型初始化完成')
    learning_rate = CustomSchedule(D_MODEL)
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


if __name__ == '__main__':
    questions, answers = load_conversations_from_json('Data/dataset.json')
    questions2, answers2 = load_conversations_from_csv('Data/20200325_counsel_chat.csv')
    questions += questions2
    answers += answers2
    dataset = do_tokenize(questions, answers, conv_task, False)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
    mdl = prepare_model()
    increment = True
    if increment:
        mdl.load_weights('Save/bot_4')
    for i in range(0, EPOCHS):
        print('当前周期：', i + 1)
        with tf.device('/gpu:0'):
            mdl.fit(dataset, epochs=1)
        if (i + 1) % SAVE_PERIOD == 0:
            mdl.save_weights('Save/bot_4')
            print('训练进度已保存')
