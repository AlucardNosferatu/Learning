import tensorflow as tf

from config import noise_dim, weight_path
from data import spawn_data_seq
from model.CGAN import ConditionalGAN
from model.discriminator import spawn_d
from model.generator import spawn_g, spawn_g_conv1d

if __name__ == '__main__':
    cond_gan = ConditionalGAN(
        discriminator=spawn_d(),
        generator=spawn_g_conv1d(),
        latent_dim=noise_dim
    )
    dataset = spawn_data_seq()
    increment = False
    if increment:
        cond_gan.load_weights(weight_path)
    cram_school = False
    if cram_school:
        outer_iter = 100
        epoch_modifier = 1
    else:
        outer_iter = 1
        epoch_modifier = 1000
    for _ in range(outer_iter):
        if cond_gan.train_dis:
            save_by_loss = 'd_loss'
            mini_epoch = 10
        else:
            save_by_loss = 'g_loss'
            mini_epoch = 90
        ckpt = tf.keras.callbacks.ModelCheckpoint(
            weight_path,
            monitor=save_by_loss,
            save_best_only=True,
            save_weights_only=True,
            mode='min',
            save_freq='epoch'
        )
        cond_gan.compile(
            d_optimizer=tf.keras.optimizers.Adam(learning_rate=0.00000003),
            g_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
            loss_fn=tf.keras.losses.BinaryCrossentropy(from_logits=True)
        )
        cond_gan.fit(dataset, epochs=mini_epoch * epoch_modifier, callbacks=[ckpt])
        cond_gan.train_dis = not cond_gan.train_dis
