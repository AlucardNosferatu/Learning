import tensorflow as tf

from config import latent_dim
from data import spawn_data
from model.CGAN import ConditionalGAN
from model.discriminator import spawn_d
from model.generator import spawn_g

cond_gan = ConditionalGAN(
    discriminator=spawn_d(), generator=spawn_g(), latent_dim=latent_dim
)
cond_gan.compile(
    d_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
    g_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
    loss_fn=tf.keras.losses.BinaryCrossentropy(from_logits=True),
)

cond_gan.fit(spawn_data(), epochs=1)
cond_gan.save('save/cgan.h5')
