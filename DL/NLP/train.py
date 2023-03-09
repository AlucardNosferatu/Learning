import tensorflow as tf
from tensorflow.python.keras.callbacks import ModelCheckpoint

from Model.Transformer import transformer
from config import NUM_LAYERS, D_MODEL, NUM_HEADS, UNITS, DROPOUT, BATCH_SIZE, EPOCHS
from metric import loss_function, accuracy, perplexity
from tokenizer import VOCAB_SIZE, do_tokenize, questions, answers

tf.keras.backend.clear_session()


class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):

    def __init__(self, d_model, warmup_steps=2000):
        super(CustomSchedule, self).__init__()

        self.d_model = d_model
        self.d_model = tf.cast(self.d_model, tf.float32)

        self.warmup_steps = warmup_steps

    def __call__(self, step):
        arg1 = tf.math.rsqrt(step)
        arg2 = step * (self.warmup_steps ** -1.5)

        return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)


model = transformer(
    vocab_size=VOCAB_SIZE,
    num_layers=NUM_LAYERS,
    units=UNITS,
    d_model=D_MODEL,
    num_heads=NUM_HEADS,
    dropout=DROPOUT)
print('模型初始化完成')
learning_rate = CustomSchedule(D_MODEL)
print('学习率规划完成')
optimizer = tf.keras.optimizers.Adam(
    learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)
print('优化器初始化完成')
model.compile(
    optimizer=optimizer,
    loss=loss_function,
    metrics=[accuracy, perplexity],
    run_eagerly=True
)
print('模型编译完成')

if __name__ == '__main__':
    dataset = do_tokenize(questions, answers)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    print('数据集分批+配置预取完成')
    history = model.fit(dataset, epochs=EPOCHS)
    model.save_weights('Save/bot_4')