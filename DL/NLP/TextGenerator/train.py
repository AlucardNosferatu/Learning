import tensorflow as tf

from config import noise_dim, weight_path
from data import spawn_data_seq
from model.CGAN import ConditionalGAN
from model.discriminator import spawn_d
from model.generator import spawn_g

cond_gan = ConditionalGAN(
    discriminator=spawn_d(), generator=spawn_g(), latent_dim=noise_dim
)

d = spawn_data_seq()
increment = True
if increment:
    cond_gan.load_weights(weight_path)
for _ in range(100):
    if cond_gan.train_dis:
        save_by_loss = 'd_loss'
        mini_epoch = 10
    else:
        save_by_loss = 'g_loss'
        mini_epoch = 100
    ckpt = tf.keras.callbacks.ModelCheckpoint(
        weight_path,
        monitor=save_by_loss,
        save_best_only=True,
        save_weights_only=True,
        mode='min',
        save_freq='epoch'
    )
    cond_gan.compile(
        d_optimizer=tf.keras.optimizers.Adam(learning_rate=0.000003),
        g_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
        loss_fn=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    )
    cond_gan.fit(d, epochs=mini_epoch, callbacks=[ckpt])
    cond_gan.train_dis = not cond_gan.train_dis
