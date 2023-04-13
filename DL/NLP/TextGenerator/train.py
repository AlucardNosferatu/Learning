import tensorflow as tf

from config import noise_dim, weight_path
from data import spawn_data_seq
from model.CGAN import ConditionalGAN, train_dis
from model.discriminator import spawn_d
from model.generator import spawn_g

cond_gan = ConditionalGAN(
    discriminator=spawn_d(), generator=spawn_g(), latent_dim=noise_dim
)
cond_gan.compile(
    d_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
    g_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
    loss_fn=tf.keras.losses.BinaryCrossentropy(from_logits=True),
)
if train_dis:
    save_by_loss = 'd_loss'
else:
    save_by_loss = 'g_loss'
ckpt = tf.keras.callbacks.ModelCheckpoint(
    weight_path,
    monitor=save_by_loss,
    save_best_only=True,
    save_weights_only=True,
    mode='min',
    save_freq='epoch'
)
increment = True
if increment:
    cond_gan.load_weights(weight_path)
cond_gan.fit(spawn_data_seq(), epochs=10 ** 7, callbacks=[ckpt])
