import tensorflow as tf

from config import noise_dim, increment, weight_path
from data import spawn_data
from model.CGAN import ConditionalGAN
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
ckpt = tf.keras.callbacks.ModelCheckpoint(
    weight_path,
    monitor='g_loss',
    verbose=1,
    save_best_only=True,
    save_weights_only=True,
    mode='min',
    save_freq='epoch'
)
if increment:
    cond_gan.load_weights(weight_path)
cond_gan.fit(spawn_data(), epochs=100, callbacks=[ckpt])
