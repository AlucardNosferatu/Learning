from config import noise_dim, weight_path, num_classes
from model.CGAN import ConditionalGAN
from model.discriminator import spawn_d
from model.generator import spawn_g, spawn_g_conv1d
from utils import get_noise_with_condition, convert_array

cond_gan = ConditionalGAN(
    discriminator=spawn_d(),
    generator=spawn_g_conv1d(),
    latent_dim=noise_dim
)
random_vector_labels = get_noise_with_condition(list(range(num_classes)))
cond_gan.load_weights(weight_path)
generated_images = cond_gan.generator.predict(random_vector_labels)
res, w2v = convert_array(generated_images)
for line in res:
    print(''.join([word[0][0] for word in line]))
