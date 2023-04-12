batch_size = 64
num_channels = 1
num_classes = 10
image_size = 28
latent_dim = 128
generator_in_channels = latent_dim + num_classes
discriminator_in_channels = num_channels + num_classes
